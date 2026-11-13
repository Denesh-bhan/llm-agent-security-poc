"""Generate a concise PDF report from the latest CSV results."""
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

root = Path(__file__).parent
csv_path = root / "results" / "results.csv"
if not csv_path.exists():
    raise SystemExit("Run the test suite first; results/results.csv was not found.")
df = pd.read_csv(csv_path)
out = root / "reports" / "security_report.pdf"
styles = getSampleStyleSheet()
story = [Paragraph("LLM & Agentic AI Security POC Report", styles["Title"]),
         Paragraph("YGF NGO AI Security Internship — Round 2", styles["Heading2"]),
         Paragraph("Scope: local application, fictional markers, mock tools, and controlled tests only.", styles["BodyText"]),
         Spacer(1, 12),
         Paragraph("Methodology", styles["Heading1"]),
         Paragraph("The project runs 30 prompt-based test cases against configured Claude and Gemini models. Each selected model is tested in baseline and hardened modes. The application records responses and heuristic classifications. Tool controls are enforced by the application rather than relying on model compliance.", styles["BodyText"]),
         Spacer(1, 10),
         Paragraph("Results summary", styles["Heading1"])]
summary = df.groupby(["Phase","Model","Result"]).size().reset_index(name="Count")
data = [list(summary.columns)] + summary.astype(str).values.tolist()
tbl = Table(data, repeatRows=1)
tbl.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#24364b")),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("GRID",(0,0),(-1,-1),0.4,colors.grey),
    ("PADDING",(0,0),(-1,-1),6)
]))
story += [tbl, Spacer(1, 12),
          Paragraph("Model comparison", styles["Heading1"]),
          Paragraph("Compare the Blocked / Partial / Succeeded counts for Claude and Gemini in the results table. Differences can reflect model version, provider safety behavior, prompt handling, and stochastic output. This POC's labels are heuristic and should be manually reviewed before making security claims.", styles["BodyText"]),
          Spacer(1, 10),
          Paragraph("Limitations and ethical controls", styles["Heading1"]),
          Paragraph("All data is fictional. The email tool creates drafts only; HTTP is restricted to mock endpoints; file access uses an in-memory fake filesystem; and calculator input is parsed through a strict arithmetic AST allowlist. The model-output evaluator is a simple heuristic, not a complete security oracle. API model names and test timestamps are recorded in the environment/configuration and should be included in the final README.", styles["BodyText"])]
SimpleDocTemplate(str(out), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42).build(story)
print(f"Created {out}")
