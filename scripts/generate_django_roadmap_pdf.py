"""
Generate Django 3-month learning roadmap PDF (paced for ~1 hour/day).
Run: python scripts/generate_django_roadmap_pdf.py
"""
from pathlib import Path

from fpdf import FPDF

OUTPUT = Path(__file__).resolve().parent.parent / "docs" / "django-roadmap-1-hour-per-day.pdf"


class RoadmapPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

    def section_title(self, title: str):
        self.ln(4)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(74, 21, 21)
        self.multi_cell(0, 8, title)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        self.ln(2)

    def subsection(self, title: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11)
        self.multi_cell(0, 6, title)
        self.set_x(self.l_margin)
        self.ln(1)

    def body(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, text)
        self.set_x(self.l_margin)
        self.ln(2)

    def bullet(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, f"  - {text}")
        self.set_x(self.l_margin)

    def link_line(self, label: str, url: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 120)
        w = self.w - self.l_margin - self.r_margin
        self.cell(w, 5, label, link=url)
        self.ln(5)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 4, url)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        self.ln(2)


def build_pdf() -> None:
    pdf = RoadmapPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # Cover
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(74, 21, 21)
    pdf.cell(0, 12, "Django Developer Roadmap", ln=True)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(160, 127, 100)
    pdf.cell(0, 10, "From zero Python to deployable apps", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        0,
        6,
        "Pace: 1 hour per day (~7 hours/week)\n"
        "12 learning modules = about 26 calendar weeks (~6 months)\n\n"
        "Companion repo: library-management-system-1 (this FYP)\n"
        "Capstone module = build and explain this project\n\n"
        "Adesanwo Joshua Olusegun (2021000382)\n"
        "Abubakar Abdullah Ishaq (2021002417)",
    )
    pdf.ln(8)

    pdf.section_title("How to use this PDF")
    pdf.body(
        "Do ONE primary resource per module. Finish the weekly project before moving on. "
        "Extras are only when you are stuck. At 1 hour/day, each 'week' below is roughly "
        "2 calendar weeks - that is normal."
    )
    pdf.subsection("Daily rhythm (60 minutes)")
    for line in [
        "Minutes 1-10: Review yesterday's notes",
        "Minutes 11-35: Course/video or official docs (primary link)",
        "Minutes 36-50: Type code on your machine (no copy-paste only)",
        "Minutes 51-60: Write 3 bullets - what broke, what I learned, tomorrow's step",
    ]:
        pdf.bullet(line)
    pdf.ln(4)

    pdf.subsection("Where to spend the most time (ranked)")
    for line in [
        "1. Python basics + reading errors (Month 1)",
        "2. SQL + table relationships (before heavy ORM)",
        "3. Django models, migrations, queries",
        "4. Auth, permissions, forms",
        "5. Testing + service layer (not fat views)",
        "6. DRF + deployment (Month 3)",
    ]:
        pdf.bullet(line)
    pdf.ln(4)

    modules = [
        {
            "title": "Module 1 (Weeks 1-2) - Python from absolute zero",
            "focus": "Variables, loops, functions, files, venv, pip. Reading tracebacks.",
            "skip": "Async, metaclasses, deep OOP patterns.",
            "project": "CLI expense tracker or contact book (save JSON or SQLite).",
            "primary": [
                ("CS50 Introduction to Python (Harvard)", "https://cs50.harvard.edu/python/"),
                ("Automate the Boring Stuff (free book)", "https://automatetheboringstuff.com/"),
            ],
            "secondary": [
                ("Python for Everybody - Dr. Chuck (YouTube playlist)", "https://www.youtube.com/playlist?list=PL4E127D1650B18376"),
                ("freeCodeCamp - Python for Beginners (4hr video)", "https://www.youtube.com/watch?v=rfscVS0vtbw"),
                ("Programming with Mosh - Python for Beginners", "https://www.youtube.com/watch?v=_uQrJ0TkZlc"),
                ("Corey Schafer - Python basics playlist", "https://www.youtube.com/playlist?list=PL-osiE80TeTuHmtmKQXm85sQYxSbYiZfx"),
            ],
            "docs": [
                ("Official Python tutorial", "https://docs.python.org/3/tutorial/"),
                ("Virtual environments (venv)", "https://docs.python.org/3/tutorial/venv.html"),
                ("Real Python - Python 3 introduction path", "https://realpython.com/learning-paths/python3-introduction/"),
                ("MDN - What is HTTP?", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview"),
            ],
        },
        {
            "title": "Module 2 (Weeks 3-4) - SQL and relational thinking",
            "focus": "Tables, keys, JOINs, ER diagrams. Write SQL by hand before ORM.",
            "skip": "Sharding, NoSQL, advanced tuning.",
            "project": "Mini blog database: users, posts, comments + 10 queries you run yourself.",
            "primary": [
                ("SQLBolt (interactive - start here)", "https://sqlbolt.com/"),
                ("Mode Analytics SQL Tutorial", "https://mode.com/sql-tutorial/"),
            ],
            "secondary": [
                ("freeCodeCamp - SQL for Beginners", "https://www.youtube.com/watch?v=HXV3zeQKqGY"),
                ("DB Browser for SQLite (tool)", "https://sqlitebrowser.org/"),
            ],
            "docs": [
                ("SQLBolt - JOINs lesson", "https://www.sqlbolt.com/lesson/select_queries_with_joins"),
            ],
        },
        {
            "title": "Module 3 (Weeks 5-6) - First Django app",
            "focus": "URL -> view -> template. Models + migrations + admin.",
            "skip": "DRF, Celery, Docker, microservices.",
            "project": "Task board or club membership app (2-3 models, admin + custom pages).",
            "primary": [
                ("Official Django Tutorial (Polls) - all parts", "https://docs.djangoproject.com/en/stable/intro/tutorial01/"),
                ("Django for Everybody - Dr. Chuck (YouTube)", "https://www.youtube.com/playlist?list=PLU2v4jqYL9ECvGTfVu23feI0V4J99wJ3-"),
            ],
            "secondary": [
                ("Corey Schafer - Django playlist", "https://www.youtube.com/playlist?list=PL-osiE80TeTqZt9m_xXC5pSsNABfTkb4Z"),
                ("Django Girls tutorial", "https://tutorial.djangogirls.org/en/"),
                ("Traversy - Django crash course", "https://www.youtube.com/watch?v=e1IyzVyrFS4"),
            ],
            "docs": [
                ("Django installation", "https://docs.djangoproject.com/en/stable/topics/install/"),
                ("Models", "https://docs.djangoproject.com/en/stable/topics/db/models/"),
                ("Migrations", "https://docs.djangoproject.com/en/stable/topics/migrations/"),
                ("Templates", "https://docs.djangoproject.com/en/stable/topics/templates/"),
            ],
        },
        {
            "title": "Module 4 (Weeks 7-8) - Auth, users, templates",
            "focus": "Login/logout, custom User model early, CSRF, roles, ModelForms.",
            "skip": "Social auth OAuth until basics work.",
            "project": "Library lite v0: register/login, books, member vs librarian roles.",
            "primary": [
                ("Django - User authentication", "https://docs.djangoproject.com/en/stable/topics/auth/"),
                ("Django - Customizing authentication (custom User)", "https://docs.djangoproject.com/en/stable/topics/auth/customizing/"),
            ],
            "secondary": [
                ("Real Python - Django user management", "https://realpython.com/django-user-management/"),
                ("MDN - CSRF explained", "https://developer.mozilla.org/en-US/docs/Glossary/CSRF"),
            ],
            "docs": [
                ("Django forms", "https://docs.djangoproject.com/en/stable/topics/forms/"),
                ("ModelForms", "https://docs.djangoproject.com/en/stable/topics/forms/modelforms/"),
            ],
        },
        {
            "title": "Module 5 (Weeks 9-10) - ORM and queries",
            "focus": "filter, Q, annotate, select_related, prefetch_related, N+1 fixes.",
            "skip": "Premature caching.",
            "project": "Catalogue with search/filters and available copy counts.",
            "primary": [
                ("Django - Making queries", "https://docs.djangoproject.com/en/stable/topics/db/queries/"),
                ("select_related and prefetch_related", "https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-related"),
            ],
            "secondary": [
                ("Real Python - select_related / prefetch_related", "https://realpython.com/effective-django-queries-select-related-prefetch-related/"),
                ("Django Debug Toolbar", "https://django-debug-toolbar.readthedocs.io/en/latest/"),
            ],
            "docs": [
                ("Aggregation", "https://docs.djangoproject.com/en/stable/topics/db/aggregation/"),
            ],
        },
        {
            "title": "Module 6 (Weeks 11-12) - Class-based views and CRUD",
            "focus": "ListView, CreateView, UpdateView, DeleteView, permissions on writes.",
            "skip": "Mixing 5 different patterns in one app.",
            "project": "Librarian-only book CRUD; members read-only catalogue.",
            "primary": [
                ("Django - Class-based views intro", "https://docs.djangoproject.com/en/stable/topics/class-based-views/"),
                ("Generic display views", "https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-display/"),
                ("Generic editing views", "https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/"),
            ],
            "secondary": [],
            "docs": [
                ("CBV reference", "https://docs.djangoproject.com/en/stable/ref/class-based-views/"),
            ],
        },
        {
            "title": "Module 7 (Weeks 13-14) - Django REST Framework",
            "focus": "Serializers, ViewSets, API permissions, Postman testing.",
            "skip": "GraphQL, gRPC.",
            "project": "JSON API for books and loans (borrow/return rules in services).",
            "primary": [
                ("DRF - Quickstart", "https://www.django-rest-framework.org/tutorial/quickstart/"),
                ("DRF - Full tutorial", "https://www.django-rest-framework.org/tutorial/1-serialization/"),
            ],
            "secondary": [
                ("TestDriven.io - DRF getting started", "https://testdriven.io/blog/drf-getting-started/"),
                ("Postman downloads", "https://www.postman.com/downloads/"),
            ],
            "docs": [
                ("DRF installation", "https://www.django-rest-framework.org/#installation"),
            ],
        },
        {
            "title": "Module 8 (Weeks 15-16) - Testing and project structure",
            "focus": "pytest-django or TestCase, test borrow rules, services.py for business logic.",
            "skip": "100% coverage obsession.",
            "project": "Circulation module with 10-15 meaningful tests.",
            "primary": [
                ("Django - Testing overview", "https://docs.djangoproject.com/en/stable/topics/testing/"),
                ("pytest-django", "https://pytest-django.readthedocs.io/en/latest/"),
            ],
            "secondary": [
                ("Real Python - pytest intro", "https://realpython.com/pytest-python-testing/"),
                ("Real Python - Django testing", "https://realpython.com/testing-in-django-part-1-best-practices-and-examples/"),
            ],
            "docs": [
                ("django-environ", "https://django-environ.readthedocs.io/en/latest/"),
                ("Deployment checklist (preview)", "https://docs.djangoproject.com/en/stable/howto/deployment/checklist/"),
            ],
        },
        {
            "title": "Module 9 (Weeks 17-18) - Security and deployment",
            "focus": "DEBUG=False, SECRET_KEY, Postgres, deploy once, static files.",
            "skip": "Kubernetes.",
            "project": "Deploy library lite online (Render, Railway, or Fly.io).",
            "primary": [
                ("Django deployment checklist", "https://docs.djangoproject.com/en/stable/howto/deployment/checklist/"),
                ("Django - Security", "https://docs.djangoproject.com/en/stable/topics/security/"),
            ],
            "secondary": [
                ("Render - Deploy Django", "https://render.com/docs/deploy-django"),
                ("Railway - Django guide", "https://docs.railway.com/guides/django"),
                ("WhiteNoise static files", "https://whitenoise.readthedocs.io/en/stable/django.html"),
            ],
            "docs": [
                ("PostgreSQL notes", "https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes"),
            ],
        },
        {
            "title": "Module 10 (Weeks 19-20) - Performance and background tasks",
            "focus": "Measure slow queries first; one cache; one async job (email/reminder).",
            "skip": "Micro-optimizing before profiling.",
            "project": "Cache book list; overdue or due-soon background task.",
            "primary": [
                ("Django - DB optimization", "https://docs.djangoproject.com/en/stable/topics/db/optimization/"),
                ("Django - Caching", "https://docs.djangoproject.com/en/stable/topics/cache/"),
            ],
            "secondary": [
                ("Celery + Django first steps", "https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html"),
                ("Django-Q2 (simpler alternative)", "https://django-q2.readthedocs.io/en/master/"),
            ],
            "docs": [],
        },
        {
            "title": "Module 11 (Weeks 21-22) - Integration track (pick ONE)",
            "focus": "HTMX + Django OR DRF+React OR webcam stub for thesis.",
            "skip": "Doing all three half-finished.",
            "project": "HTMX catalogue search OR simple React page OR webcam POST endpoint.",
            "primary": [
                ("HTMX documentation", "https://htmx.org/docs/"),
                ("django-htmx", "https://github.com/adamchainz/django-htmx"),
            ],
            "secondary": [
                ("React - Learn", "https://react.dev/learn"),
                ("MediaPipe Face Landmarker (Python)", "https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/python"),
                ("MDN - Web Authentication API", "https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API"),
            ],
            "docs": [],
        },
        {
            "title": "Module 12 (Weeks 23-26) - Capstone portfolio project",
            "focus": "README, demo script, clean nav, tests, explain architecture in interview.",
            "skip": "New frameworks.",
            "project": "Full library system: accounts, catalogue, circulation, biometrics stub, deploy.",
            "primary": [
                ("GitHub - Basic writing and formatting (README)", "https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax"),
            ],
            "secondary": [
                ("Real Python - Getting started with Django", "https://realpython.com/getting-started-with-django/"),
                ("System design primer (optional)", "https://github.com/donnemartin/system-design-primer"),
            ],
            "docs": [],
        },
    ]

    for mod in modules:
        pdf.add_page()
        pdf.section_title(mod["title"])
        pdf.subsection("Focus")
        pdf.body(mod["focus"])
        pdf.subsection("Skip for now")
        pdf.body(mod["skip"])
        pdf.subsection("Project (build this before moving on)")
        pdf.body(mod["project"])
        pdf.subsection("Primary resources (finish one)")
        for label, url in mod["primary"]:
            pdf.link_line(label, url)
        if mod["secondary"]:
            pdf.subsection("Secondary (when stuck)")
            for label, url in mod["secondary"]:
                pdf.link_line(label, url)
        if mod["docs"]:
            pdf.subsection("Documentation bookmarks")
            for label, url in mod["docs"]:
                pdf.link_line(label, url)

    pdf.add_page()
    pdf.section_title("Minimum path if overwhelmed")
    pdf.body("Before Module 3, complete ONLY these three:")
    for label, url in [
        ("CS50 Python (first half of course)", "https://cs50.harvard.edu/python/"),
        ("SQLBolt lessons 1-12", "https://sqlbolt.com/"),
        ("Official Django Polls tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/"),
    ]:
        pdf.link_line(label, url)

    pdf.section_title("YouTube channels to subscribe")
    channels = [
        ("Corey Schafer", "https://www.youtube.com/@coreyms"),
        ("Programming with Mosh", "https://www.youtube.com/@programmingwithmosh"),
        ("freeCodeCamp", "https://www.youtube.com/@freecodecamp"),
        ("Arjan Codes", "https://www.youtube.com/@ArjanCodes"),
        ("TestDriven.io", "https://www.youtube.com/@testdrivenio"),
    ]
    for label, url in channels:
        pdf.link_line(label, url)

    pdf.section_title("Practice sites (max 30 min/day)")
    for label, url in [
        ("Exercism Python track", "https://exercism.org/tracks/python"),
        ("HackerRank Python", "https://www.hackerrank.com/domains/python"),
    ]:
        pdf.link_line(label, url)

    pdf.section_title("Calendar at 1 hour per day")
    pdf.body(
        "Module 1-2:  ~4 weeks (Python)\n"
        "Module 3-4:  ~4 weeks (SQL)\n"
        "Module 5-8:  ~8 weeks (Django core + auth)\n"
        "Module 9-12: ~10 weeks (ORM, CBV, DRF, tests)\n"
        "Module 13-16: ~8 weeks (deploy, perf, capstone)\n\n"
        "Total: about 6 months to job-ready junior Django level.\n"
        "Your LAUTECH library FYP is an excellent Module 12 capstone."
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
