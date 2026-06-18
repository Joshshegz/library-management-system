import time

from django.core.management.base import BaseCommand

from biometrics.models import BiometricTemplate
from biometrics.services.matcher import fused_distance, verify_templates


class Command(BaseCommand):
    help = (
        "Evaluate multimodal biometric performance (accuracy, FPR, sensitivity, "
        "specificity, average match time) using enrolled templates."
    )

    def handle(self, *args, **options):
        templates = list(BiometricTemplate.objects.select_related("user"))
        if len(templates) < 2:
            self.stdout.write(
                self.style.WARNING(
                    "Need at least 2 enrolled users for evaluation. "
                    "Enroll more subjects first."
                )
            )
            return

        tp = tn = fp = fn = 0
        times_ms = []

        for probe in templates:
            for gallery in templates:
                start = time.perf_counter()
                result = verify_templates(
                    probe.nose_features,
                    probe.thumb_features,
                    gallery.nose_features,
                    gallery.thumb_features,
                )
                elapsed = (time.perf_counter() - start) * 1000
                times_ms.append(elapsed)

                genuine = probe.user_id == gallery.user_id
                if genuine and result.accepted:
                    tp += 1
                elif genuine and not result.accepted:
                    fn += 1
                elif not genuine and result.accepted:
                    fp += 1
                else:
                    tn += 1

        total = tp + tn + fp + fn
        accuracy = (tp + tn) / total * 100 if total else 0
        sensitivity = tp / (tp + fn) * 100 if (tp + fn) else 0
        specificity = tn / (tn + fp) * 100 if (tn + fp) else 0
        fpr = fp / (fp + tn) * 100 if (fp + tn) else 0
        avg_ms = sum(times_ms) / len(times_ms) if times_ms else 0

        self.stdout.write(self.style.SUCCESS("\n=== Biometric evaluation report ===\n"))
        self.stdout.write(f"Enrolled subjects:     {len(templates)}")
        self.stdout.write(f"Comparison pairs:      {total}")
        self.stdout.write(f"True positives (TP):   {tp}")
        self.stdout.write(f"True negatives (TN):   {tn}")
        self.stdout.write(f"False positives (FP):  {fp}")
        self.stdout.write(f"False negatives (FN):  {fn}")
        self.stdout.write(f"Overall accuracy:      {accuracy:.2f}%")
        self.stdout.write(f"Sensitivity (TPR):     {sensitivity:.2f}%")
        self.stdout.write(f"Specificity (TNR):     {specificity:.2f}%")
        self.stdout.write(f"False positive rate:   {fpr:.2f}%")
        self.stdout.write(f"Avg match time:        {avg_ms:.2f} ms")
        self.stdout.write(
            "\nNote: For thesis data collection, enroll 50 LAUTECH subjects and "
            "re-run after live captures. Tune thresholds in settings.py if needed.\n"
        )
