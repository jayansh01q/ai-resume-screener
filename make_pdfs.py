"""
make_pdfs.py
------------
Generates two mock PDF resumes using the fpdf2 library:
  - sample_resume.pdf : Software Engineer (Python & SQL skills) — good match
  - bad_resume.pdf    : Head Chef (culinary field)              — bad match
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos


# ---------------------------------------------------------------------------
# Helper: draw a styled section header
# ---------------------------------------------------------------------------
def _section_header(pdf: FPDF, title: str) -> None:
    """Render a bold section header with an underline rule."""
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, title.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    # thin horizontal rule
    pdf.set_draw_color(100, 100, 100)
    pdf.set_line_width(0.4)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 180, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)


# ---------------------------------------------------------------------------
# Helper: write a block of body text
# ---------------------------------------------------------------------------
def _body(pdf: FPDF, text: str) -> None:
    pdf.multi_cell(0, 6, text)
    pdf.ln(1)


# ---------------------------------------------------------------------------
# Helper: write a two-column skill / info row
# ---------------------------------------------------------------------------
def _skill_row(pdf: FPDF, label: str, value: str, label_width: int = 40) -> None:
    """Print a label in bold then the value, wrapping if needed."""
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(label_width, 6, f"{label}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    # Remaining width = page width - left margin - right margin - label_width
    remaining = pdf.w - pdf.l_margin - pdf.r_margin - label_width
    pdf.multi_cell(remaining, 6, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# ---------------------------------------------------------------------------
# Helper: write an experience / education entry
# ---------------------------------------------------------------------------
def _entry(pdf: FPDF, role: str, org: str, period: str, bullets: list) -> None:
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 6, role, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"  |  {org}  |  {period}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    for bullet in bullets:
        pdf.cell(6, 6, "", new_x=XPos.RIGHT, new_y=YPos.TOP)   # indent spacer
        pdf.multi_cell(0, 6, f"*  {bullet}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


# ===========================================================================
# 1.  sample_resume.pdf  —  Software Engineer
# ===========================================================================
def generate_sample_resume(output_path: str = "sample_resume.pdf") -> None:
    pdf = FPDF(format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    # ── Name ────────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, "Alex Johnson", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # ── Contact ─────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(
        0, 6,
        "alex.johnson@email.com  |  (555) 123-4567  |  linkedin.com/in/alexjohnson  |  github.com/alexj",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C",
    )
    pdf.ln(3)

    # ── Summary ─────────────────────────────────────────────────────────────
    _section_header(pdf, "Professional Summary")
    _body(
        pdf,
        "Results-driven Software Engineer with 5+ years of experience designing, building, and "
        "maintaining scalable backend systems. Proficient in Python and SQL, with hands-on expertise "
        "in REST API development, data engineering pipelines, and cloud infrastructure. Passionate "
        "about clean code, automated testing, and continuous delivery.",
    )

    # ── Skills ──────────────────────────────────────────────────────────────
    _section_header(pdf, "Technical Skills")
    skills = [
        ("Languages",    "Python, SQL, Bash, JavaScript"),
        ("Databases",    "PostgreSQL, MySQL, SQLite, Redis"),
        ("Frameworks",   "Django, FastAPI, Flask"),
        ("DevOps/Cloud", "Docker, AWS (EC2, S3, Lambda), GitHub Actions, Linux"),
        ("Tools",        "Git, Pytest, Pandas, SQLAlchemy, Jupyter"),
    ]
    for label, value in skills:
        _skill_row(pdf, label, value)
    pdf.ln(1)

    # ── Experience ──────────────────────────────────────────────────────────
    _section_header(pdf, "Work Experience")

    _entry(
        pdf,
        "Software Engineer",
        "DataSpark Inc.",
        "June 2021 - Present",
        [
            "Developed and maintained Python-based ETL pipelines processing 10M+ records daily using "
            "Pandas, SQLAlchemy, and PostgreSQL.",
            "Designed RESTful APIs with FastAPI serving 50k+ daily requests, backed by SQL query "
            "optimisation that reduced average latency by 35%.",
            "Automated deployment workflows via GitHub Actions and Docker, cutting release cycles "
            "from bi-weekly to on-demand.",
            "Mentored 2 junior engineers on Python best practices, code review, and testing standards.",
        ],
    )

    _entry(
        pdf,
        "Junior Software Developer",
        "CodeBase Ltd.",
        "Aug 2019 - May 2021",
        [
            "Built internal reporting dashboards using Python (Flask) and SQL stored procedures.",
            "Migrated legacy MySQL scripts to PostgreSQL, improving query performance by 20%.",
            "Wrote unit and integration tests using Pytest, achieving 85%+ code coverage.",
        ],
    )

    # ── Education ───────────────────────────────────────────────────────────
    _section_header(pdf, "Education")
    _entry(
        pdf,
        "B.Sc. Computer Science",
        "State University",
        "2015 - 2019",
        [
            "Graduated with Honours (GPA 3.8/4.0).",
            "Relevant coursework: Data Structures & Algorithms, Databases (SQL), Operating Systems, "
            "Software Engineering.",
        ],
    )

    # ── Projects ────────────────────────────────────────────────────────────
    _section_header(pdf, "Projects")
    _entry(
        pdf,
        "Open-Source Python SQL Query Analyser",
        "github.com/alexj/sql-analyser",
        "2023",
        [
            "Built a CLI tool in Python that parses SQL queries, detects missing indexes, and "
            "suggests optimisations.",
            "350+ GitHub stars; published as a PyPI package.",
        ],
    )
    _entry(
        pdf,
        "Real-Time Data Pipeline",
        "Personal Project",
        "2022",
        [
            "End-to-end pipeline using Python, Kafka, and PostgreSQL to stream and store live "
            "stock-market data.",
        ],
    )

    pdf.output(output_path)
    print(f"[OK] Written: {output_path}")


# ===========================================================================
# 2.  bad_resume.pdf  —  Head Chef
# ===========================================================================
def generate_bad_resume(output_path: str = "bad_resume.pdf") -> None:
    pdf = FPDF(format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    # ── Name ────────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, "Marco Rossi", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # ── Contact ─────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(
        0, 6,
        "marco.rossi@cuisine.com  |  (555) 987-6543  |  Milan, Italy",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C",
    )
    pdf.ln(3)

    # ── Summary ─────────────────────────────────────────────────────────────
    _section_header(pdf, "Professional Summary")
    _body(
        pdf,
        "Award-winning Head Chef with 12 years of experience leading high-volume kitchens specialising "
        "in contemporary Italian and classic French cuisine. Recognised for creative menu development, "
        "rigorous food safety standards, and the ability to inspire and manage large culinary teams. "
        "Winner of the 2022 Regional Culinary Excellence Award.",
    )

    # ── Skills ──────────────────────────────────────────────────────────────
    _section_header(pdf, "Culinary Skills")
    culinary_skills = [
        ("Cuisine Styles",  "Italian, French, Mediterranean, Fusion"),
        ("Techniques",      "Sous Vide, Confit, Emulsification, Charcuterie, Pastry & Patisserie"),
        ("Kitchen Mgmt",    "Menu Planning, Food Costing, Inventory Control, Staff Training"),
        ("Certifications",  "ServSafe Food Manager, HACCP Level 3, Wine & Sommelier Foundation"),
        ("Languages",       "Italian (Native), French (Fluent), English (Professional)"),
    ]
    for label, value in culinary_skills:
        _skill_row(pdf, label, value)
    pdf.ln(1)

    # ── Experience ──────────────────────────────────────────────────────────
    _section_header(pdf, "Work Experience")

    _entry(
        pdf,
        "Head Chef",
        "La Bella Cucina, Rome",
        "March 2018 - Present",
        [
            "Oversee all kitchen operations for a 120-cover fine-dining restaurant, managing a team "
            "of 14 culinary staff.",
            "Designed seasonal tasting menus using locally sourced, organic ingredients, increasing "
            "average cover spend by 22%.",
            "Reduced food waste by 18% through disciplined inventory management and creative "
            "repurposing of trim.",
            "Maintained a 4.9/5 Michelin Guide inspector average across three consecutive visits.",
        ],
    )

    _entry(
        pdf,
        "Sous Chef",
        "Le Bistro Parisien, Paris",
        "Jan 2014 - Feb 2018",
        [
            "Assisted the Executive Chef in daily operations of a Michelin-starred establishment.",
            "Specialised in classical French sauces, charcuterie production, and pastry preparation.",
            "Trained and onboarded 8 junior chefs in knife skills, station management, and plating "
            "presentation.",
        ],
    )

    _entry(
        pdf,
        "Chef de Partie",
        "Ristorante Bellagio, Milan",
        "Sep 2011 - Dec 2013",
        [
            "Managed the pasta and antipasto station in a fast-paced, high-volume kitchen.",
            "Developed three signature pasta dishes now permanent fixtures on the restaurant menu.",
        ],
    )

    # ── Education ───────────────────────────────────────────────────────────
    _section_header(pdf, "Education")
    _entry(
        pdf,
        "Diploma in Culinary Arts",
        "Culinary Institute of Excellence, Florence",
        "2008 - 2011",
        [
            "Graduated with Distinction.",
            "Specialised in Classic French Technique and Italian Regional Cuisine.",
            "Stage (internship) at a two-Michelin-star restaurant in Lyon, France.",
        ],
    )

    # ── Awards ──────────────────────────────────────────────────────────────
    _section_header(pdf, "Awards & Recognition")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    awards = [
        "2022 Regional Culinary Excellence Award - Best Fine Dining Chef, Central Italy",
        "2020 Roma Food & Wine Festival - Gold Medal, Modern Italian Category",
        "2017 Young Chef of the Year - Ile-de-France Culinary Association",
    ]
    for award in awards:
        pdf.cell(6, 6, "", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.multi_cell(0, 6, f"*  {award}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    pdf.output(output_path)
    print(f"[OK] Written: {output_path}")


# ===========================================================================
# Entry point
# ===========================================================================
if __name__ == "__main__":
    generate_sample_resume("sample_resume.pdf")
    generate_bad_resume("bad_resume.pdf")
    print("\nDone! Both PDF resumes have been generated in the current directory.")
