# Project documentation

## Django learning roadmap (1 hour / day)

**File:** [django-roadmap-1-hour-per-day.pdf](./django-roadmap-1-hour-per-day.pdf)

Study guide for learning Django from zero Python, paced at **~1 hour per day** (~6 months). Includes:

- 12 modules (Python → SQL → Django → DRF → deploy → capstone)
- Weekly projects (Module 12 capstone = this LAUTECH library system)
- Clickable links to courses, docs, and videos

### Regenerate the PDF

```powershell
.\venv\Scripts\pip.exe install fpdf2
.\venv\Scripts\python.exe scripts\generate_django_roadmap_pdf.py
```

Output is written to this folder.
