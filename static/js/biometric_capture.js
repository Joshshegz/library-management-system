(function () {
  const video = document.getElementById("nose-video");
  const canvas = document.getElementById("nose-canvas");
  const noseInput = document.getElementById("nose_image");
  const livenessInput = document.getElementById("nose_liveness_frames");
  const captureBtn = document.getElementById("capture-nose");
  const nextBtn = document.getElementById("liveness-next-btn");
  const preview = document.getElementById("nose-preview");
  const statusEl = document.getElementById("liveness-status");
  const progressEl = document.getElementById("liveness-progress");
  const hintEl = document.getElementById("liveness-hint");
  const promptOverlay = document.getElementById("liveness-prompt");
  const promptText = document.getElementById("liveness-prompt-text");
  const countdownEl = document.getElementById("liveness-countdown");
  const root = document.querySelector(".nose-capture-v2");

  if (!video || !canvas || !noseInput) return;

  const AUTO_START = !root || root.dataset.livenessAuto !== "false";
  const MANUAL_PACE = !root || root.dataset.livenessPace !== "auto";
  const MIRROR_CAMERA = !root || root.dataset.mirrorCamera !== "false";

  const STEPS = [
    {
      step: 1,
      prepare: "Look at the camera",
      detail: "Centre your face and keep your nose visible.",
      captureMsg: "Hold still…",
      captureBtn: "Capture step 1",
      nextBtn: "Continue to step 2",
    },
    {
      step: 2,
      prepare: "Open your mouth wide",
      detail: "Show your teeth or open wide — then tap capture while your mouth is open.",
      captureMsg: "Capture with mouth open…",
      captureBtn: "Capture step 2 (mouth open)",
      nextBtn: "Continue to step 3",
    },
    {
      step: 3,
      prepare: "Look at the camera again",
      detail: "Centre your face and hold still for the final capture.",
      captureMsg: "Hold still…",
      captureBtn: "Capture final frame",
      nextBtn: "Finish liveness check",
    },
  ];

  let capturing = false;
  let autoStarted = false;
  let completed = false;
  let cameraStream = null;
  let waitHintTimer = null;
  let userActionResolve = null;

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function setStatus(text, isError) {
    if (!statusEl) return;
    statusEl.textContent = text;
    statusEl.className = isError
      ? "liveness-status liveness-status--error"
      : "liveness-status liveness-status--ok";
  }

  function showPrompt(main, sub, countdown) {
    if (promptOverlay) promptOverlay.hidden = false;
    if (promptText) {
      promptText.innerHTML = sub
        ? "<strong>" + main + "</strong><span>" + sub + "</span>"
        : "<strong>" + main + "</strong>";
    }
    if (countdownEl) {
      countdownEl.textContent = countdown || "";
      countdownEl.hidden = !countdown;
    }
  }

  function hidePrompt() {
    if (promptOverlay) promptOverlay.hidden = true;
    if (countdownEl) countdownEl.hidden = true;
    hideNextButton();
  }

  function hideNextButton() {
    if (!nextBtn) return;
    nextBtn.hidden = true;
    nextBtn.disabled = false;
  }

  function showNextButton(label) {
    if (!nextBtn) return Promise.resolve();
    return new Promise((resolve) => {
      userActionResolve = resolve;
      nextBtn.textContent = label;
      nextBtn.hidden = false;
      nextBtn.disabled = false;
      nextBtn.focus();
    });
  }

  function waitForUserClick(label) {
    if (!nextBtn) return sleep(800);
    return showNextButton(label).then(() => {
      hideNextButton();
      if (userActionResolve) userActionResolve = null;
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      if (userActionResolve) {
        const done = userActionResolve;
        userActionResolve = null;
        nextBtn.disabled = true;
        done();
      }
    });
  }

  function showRetryButton(label) {
    if (!captureBtn) return;
    captureBtn.hidden = false;
    captureBtn.textContent = label || "↻ Try again";
  }

  function cameraErrorMessage(err) {
    const name = err && err.name ? err.name : "";
    if (name === "NotAllowedError" || name === "PermissionDeniedError") {
      return "Camera blocked. Allow webcam access in your browser, then click Try again.";
    }
    if (name === "NotFoundError" || name === "DevicesNotFoundError") {
      return "No camera found. Connect a webcam and try again.";
    }
    if (name === "NotReadableError" || name === "TrackStartError") {
      return "Camera is in use by another app. Close it and try again.";
    }
    return (err && err.message) || "Could not start the camera.";
  }

  function grabFrame() {
    const w = video.videoWidth;
    const h = video.videoHeight;
    if (!w || !h) {
      throw new Error("Camera is not ready yet.");
    }
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext("2d");
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    if (MIRROR_CAMERA) {
      ctx.translate(w, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, w, h);
    return canvas.toDataURL("image/jpeg", 0.92);
  }

  function markStep(stepNum, state) {
    if (!progressEl) return;
    const el = progressEl.querySelector('[data-step="' + stepNum + '"]');
    if (el) {
      el.classList.remove("is-active", "is-done");
      if (state) el.classList.add(state);
    }
  }

  function resetProgress() {
    if (!progressEl) return;
    progressEl.querySelectorAll(".liveness-step").forEach((el) => {
      el.classList.remove("is-active", "is-done");
    });
  }

  function isVideoReady() {
    return video.readyState >= 2 && video.videoWidth > 0 && video.videoHeight > 0;
  }

  function waitForVideoReady(timeoutMs) {
    return new Promise((resolve, reject) => {
      if (isVideoReady()) {
        resolve();
        return;
      }

      let settled = false;
      const finish = (fn) => {
        if (settled) return;
        settled = true;
        clearInterval(poll);
        clearTimeout(timer);
        video.removeEventListener("loadedmetadata", onMeta);
        video.removeEventListener("loadeddata", onMeta);
        video.removeEventListener("playing", onMeta);
        fn();
      };

      const tryResolve = () => {
        if (isVideoReady()) finish(resolve);
      };

      const onMeta = () => tryResolve();

      video.addEventListener("loadedmetadata", onMeta);
      video.addEventListener("loadeddata", onMeta);
      video.addEventListener("playing", onMeta);

      const poll = setInterval(tryResolve, 150);
      const timer = setTimeout(
        () => finish(() => reject(new Error("Camera feed did not start. Click Try again."))),
        timeoutMs || 12000
      );
    });
  }

  async function attachCameraStream(stream) {
    if (cameraStream) {
      cameraStream.getTracks().forEach((t) => t.stop());
    }
    cameraStream = stream;
    video.srcObject = stream;
    video.muted = true;
    video.playsInline = true;

    try {
      await video.play();
    } catch (playErr) {
      if (playErr && playErr.name !== "AbortError") {
        throw playErr;
      }
    }

    await waitForVideoReady(12000);
  }

  async function countdownPrepare(seconds) {
    for (let s = seconds; s >= 1; s--) {
      if (countdownEl) {
        countdownEl.textContent = String(s);
        countdownEl.hidden = false;
      }
      await sleep(1000);
    }
    if (countdownEl) countdownEl.hidden = true;
  }

  function finishLiveness(frames) {
    hidePrompt();
    noseInput.value = frames[frames.length - 1];
    if (livenessInput) {
      livenessInput.value = JSON.stringify(frames);
    }
    if (preview) {
      preview.src = frames[frames.length - 1];
      preview.style.display = "block";
    }

    completed = true;
    setStatus("Liveness complete. You can submit the form now.", false);
    if (hintEl) {
      hintEl.textContent = "All 3 steps recorded. Submit when you are ready.";
    }
    showRetryButton("↻ Repeat liveness check");
    document.dispatchEvent(new CustomEvent("liveness:complete"));
  }

  async function runLivenessCaptureManual() {
    const frames = [];

    showPrompt("Liveness check", "Go at your own pace — use the button for each step.", "");
    setStatus("Tap the button when you are ready for each capture.", false);
    await waitForUserClick("Begin step 1");

    for (let i = 0; i < STEPS.length; i++) {
      const cfg = STEPS[i];
      markStep(cfg.step, "is-active");
      showPrompt(cfg.prepare, cfg.detail, "");
      await waitForUserClick(cfg.captureBtn);

      showPrompt(cfg.captureMsg, "Capturing now…", "●");
      await sleep(300);
      frames.push(grabFrame());
      markStep(cfg.step, "is-done");

      if (i < STEPS.length - 1) {
        showPrompt("Step " + cfg.step + " saved", "Take your time before the next step.", "");
        await waitForUserClick(cfg.nextBtn);
      }
    }

    finishLiveness(frames);
  }

  async function runLivenessCaptureAuto() {
    const frames = [];

    showPrompt("Get ready", "Liveness check starting…", "");
    setStatus("Follow the instructions on the camera.", false);
    await sleep(800);

    for (const cfg of STEPS) {
      markStep(cfg.step, "is-active");
      showPrompt(cfg.prepare, cfg.detail, "");

      const countdownSec = cfg.step === 1 ? 3 : 2;
      await countdownPrepare(countdownSec);

      showPrompt(cfg.captureMsg, "Do not move", "●");
      await sleep(cfg.step === 2 ? 350 : 700);
      frames.push(grabFrame());
      markStep(cfg.step, "is-done");

      if (cfg.step < STEPS.length) {
        showPrompt("Good", "Next step in a moment…", "");
        await sleep(600);
      }
    }

    finishLiveness(frames);
  }

  async function runLivenessCapture() {
    if (capturing) return;
    if (!isVideoReady()) {
      setStatus("Camera not ready. Click Try again.", true);
      showRetryButton("↻ Try again");
      return;
    }

    capturing = true;
    completed = false;
    if (captureBtn) captureBtn.hidden = true;
    hideNextButton();
    noseInput.value = "";
    if (livenessInput) livenessInput.value = "";
    resetProgress();

    try {
      if (MANUAL_PACE) {
        await runLivenessCaptureManual();
      } else {
        await runLivenessCaptureAuto();
      }
    } catch (err) {
      hidePrompt();
      setStatus(err.message || String(err), true);
      resetProgress();
      showRetryButton("↻ Try again");
    } finally {
      capturing = false;
    }
  }

  async function startCameraAndLiveness() {
    clearTimeout(waitHintTimer);
    if (captureBtn) captureBtn.hidden = true;
    hideNextButton();

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      hidePrompt();
      setStatus(
        "Camera needs a secure page. Open http://localhost:8000 (not a file:// link).",
        true
      );
      showRetryButton("↻ Retry");
      return;
    }

    showPrompt("Starting camera", "Allow webcam access when your browser asks.", "");

    waitHintTimer = setTimeout(() => {
      showPrompt(
        "Waiting for camera",
        "Check the address bar for a camera icon and choose Allow.",
        ""
      );
    }, 2500);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } },
        audio: false,
      });

      clearTimeout(waitHintTimer);
      await attachCameraStream(stream);

      if (MANUAL_PACE) {
        showPrompt(
          "Camera ready",
          "Start when you are ready — you control each step with the button below.",
          ""
        );
        setStatus("Use the gold button to move through each capture step.", false);
        if (hintEl) {
          hintEl.textContent =
            "Manual mode: tap the button when ready for each step (no auto countdown).";
        }
        await waitForUserClick("Start liveness check");
        autoStarted = true;
        await runLivenessCapture();
      } else if (AUTO_START && !autoStarted && !completed) {
        showPrompt("Camera ready", "Liveness will begin automatically…", "3");
        await sleep(1200);
        autoStarted = true;
        await runLivenessCapture();
      } else {
        hidePrompt();
        showRetryButton("↻ Start liveness check");
      }
    } catch (err) {
      clearTimeout(waitHintTimer);
      hidePrompt();
      setStatus(cameraErrorMessage(err), true);
      showRetryButton("↻ Try again");
    }
  }

  const form = document.getElementById("biometric-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      const hasLiveness =
        livenessInput && livenessInput.value && livenessInput.value.length > 10;
      if (!hasLiveness) {
        e.preventDefault();
        alert("Complete all 3 liveness steps before submitting.");
      }
    });
  }

  if (captureBtn) {
    captureBtn.addEventListener("click", async () => {
      autoStarted = true;
      if (!isVideoReady()) {
        await startCameraAndLiveness();
        if (isVideoReady() && !completed) await runLivenessCapture();
      } else {
        await runLivenessCapture();
      }
    });
  }

  function boot() {
    if (!root || root.offsetParent !== null) {
      startCameraAndLiveness();
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          observer.disconnect();
          startCameraAndLiveness();
        }
      },
      { threshold: 0.05 }
    );
    observer.observe(root);
    setTimeout(() => {
      if (!cameraStream && !completed) {
        observer.disconnect();
        startCameraAndLiveness();
      }
    }, 500);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
