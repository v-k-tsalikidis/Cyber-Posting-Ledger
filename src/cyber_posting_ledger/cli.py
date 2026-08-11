"""
Command Line Interface (CLI) & Web Server for Cyber Posting Ledger.
"""

import http.server
import json
import socketserver
import sys
from pathlib import Path

import click

from cyber_posting_ledger import __version__
from cyber_posting_ledger.analyzer import analyze_cv_coverage
from cyber_posting_ledger.exporter import generate_html_report
from cyber_posting_ledger.generator import (
    format_brief_markdown,
    generate_application_brief,
)
from cyber_posting_ledger.models import (
    CandidateProfile,
    VacancyRecord,
)
from cyber_posting_ledger.scoring import evaluate_vacancy
from cyber_posting_ledger.storage import VacancyStorage


@click.group()
@click.version_option(version=__version__, prog_name="cyber-posting-ledger")
def cli():
    """Cyber Posting Ledger CLI - Academic & Recruiter-Grounded Cybersecurity Career Intelligence Engine."""


@cli.command("list")
def list_vacancies():
    """List all tracked vacancies and their multi-dimensional fit scores."""
    storage = VacancyStorage()
    records = storage.load_all()

    if not records:
        click.echo("No vacancies currently tracked.")
        return

    click.echo("\nCyber Posting Ledger Tracked Vacancies:")
    click.echo("=" * 95)
    click.echo(
        f"{'ID':<10} {'ORGANIZATION':<15} {'TITLE':<30} {'STATUS':<14} {'ELIG':<6} {'FIT':<6} {'STRAT':<6} {'PRACT':<6}"
    )
    click.echo("-" * 95)

    profile = storage.load_profile()
    for r in records:
        res = r.fit_result or evaluate_vacancy(r, profile)
        click.echo(
            f"{r.id:<10} {r.organization[:14]:<15} {r.title[:29]:<30} {res.overall_status:<14} "
            f"{res.formal_eligibility_score:<6} {res.substantive_fit_score:<6} {res.strategic_value_score:<6} {res.practical_value_score:<6}"
        )
    click.echo("=" * 95 + "\n")


@cli.command("score")
@click.option("--id", "record_id", required=True, help="Vacancy Record ID (e.g., VAC-001)")
def score_vacancy(record_id: str):
    """Evaluate multi-dimensional fit scores and detailed observations for a vacancy."""
    storage = VacancyStorage()
    record = storage.get_by_id(record_id)
    profile = storage.load_profile()

    if not record:
        click.echo(f"Error: Vacancy with ID '{record_id}' not found.", err=True)
        sys.exit(1)

    res = evaluate_vacancy(record, profile)

    click.echo("\n========================================================")
    click.echo(f" Cyber Posting Ledger FIT ASSESSMENT: {record.id} - {record.title}")
    click.echo(f" Candidate: {profile.candidate_name} ({', '.join(profile.nationalities)})")
    click.echo(f" Organization: {record.organization} ({record.grade_or_level})")
    click.echo("========================================================")
    click.echo(f" Formal Eligibility Score:   {res.formal_eligibility_score} / 100")
    click.echo(f" Substantive Role Fit Score: {res.substantive_fit_score} / 100")
    click.echo(f" Strategic Value Score:      {res.strategic_value_score} / 100")
    click.echo(f" Practical Value Score:      {res.practical_value_score} / 100")
    click.echo(f" Overall Status:             {res.overall_status.upper()}")
    if res.cybok_mapping:
        click.echo(f" CyBOK Category:             {res.cybok_mapping.primary_category.value}")
        click.echo(f" NICE Role Alignment:        {res.cybok_mapping.nice_framework_role}")
    click.echo("--------------------------------------------------------")

    if res.disqualification_reasons:
        click.echo("\nDisqualification / Alert Reasons:")
        for reason in res.disqualification_reasons:
            click.echo(f"  [!] {reason}")

    click.echo("\nEvaluation Observations & Evidence:")
    for obs in res.observations:
        click.echo(f"  * {obs}")
    click.echo("========================================================\n")


@cli.command("generate-brief")
@click.option("--id", "record_id", required=True, help="Vacancy Record ID (e.g., VAC-001)")
@click.option("--out", "out_file", type=click.Path(), help="Output markdown file path")
def generate_brief_cmd(record_id: str, out_file: str | None):
    """Generate a tailored Application Alignment Brief for a vacancy."""
    storage = VacancyStorage()
    record = storage.get_by_id(record_id)
    profile = storage.load_profile()

    if not record:
        click.echo(f"Error: Vacancy with ID '{record_id}' not found.", err=True)
        sys.exit(1)

    brief = generate_application_brief(record, profile)
    md_content = format_brief_markdown(brief)

    if out_file:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        click.echo(f"Application Brief exported to '{out_file}'.")
    else:
        click.echo(md_content)


@cli.command("analyze-cv")
@click.option("--id", "record_id", required=True, help="Vacancy Record ID (e.g., VAC-001)")
@click.option(
    "--cv-file",
    type=click.Path(exists=True),
    required=True,
    help="Path to raw CV markdown/text file",
)
def analyze_cv_cmd(record_id: str, cv_file: str):
    """Analyze CV text coverage against target vacancy requirements."""
    storage = VacancyStorage()
    record = storage.get_by_id(record_id)
    if not record:
        click.echo(f"Error: Vacancy with ID '{record_id}' not found.", err=True)
        sys.exit(1)

    with open(cv_file, encoding="utf-8") as f:
        cv_text = f.read()

    res = analyze_cv_coverage(cv_text, record)
    click.echo(f"\n--- CV COVERAGE ANALYSIS FOR {record.id} ---")
    click.echo(
        f"Coverage Score: {res.coverage_percentage}% ({len(res.matched_keywords)}/{res.total_required_keywords} keywords)"
    )
    click.echo(f"Matched Keywords: {', '.join(res.matched_keywords)}")
    click.echo(f"Missing Keywords: {', '.join(res.missing_keywords)}")
    click.echo("\nRecommendations:")
    for rec in res.recommendations:
        click.echo(f"  * {rec}")
    click.echo("-------------------------------------------\n")


@cli.command("export-html")
@click.option("--id", "record_id", required=True, help="Vacancy Record ID (e.g., VAC-001)")
@click.option("--out", "out_file", type=click.Path(), required=True, help="Output HTML file path")
def export_html_cmd(record_id: str, out_file: str):
    """Export standalone, publication-quality HTML report for a vacancy."""
    storage = VacancyStorage()
    record = storage.get_by_id(record_id)
    profile = storage.load_profile()

    if not record:
        click.echo(f"Error: Vacancy with ID '{record_id}' not found.", err=True)
        sys.exit(1)

    html = generate_html_report(record, profile)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    click.echo(f"HTML Report exported to '{out_file}'.")


@cli.command("serve")
@click.option("--port", default=8000, help="Port to run local web server on")
def serve_dashboard(port: int):
    """Serve Cyber Posting Ledger Dashboard UI."""
    # The dashboard assets ship inside the package, so this works from an
    # installed copy and not only from a source checkout.
    frontend_dir = Path(__file__).parent / "frontend"
    if not frontend_dir.exists():
        click.echo(
            "Error: dashboard files are missing from the installation. "
            "Reinstall with 'pip install --force-reinstall cyber-posting-ledger'.",
            err=True,
        )
        sys.exit(1)

    class DashboardHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(frontend_dir), **kwargs)

        def do_GET(self):
            storage = VacancyStorage()
            if self.path == "/api/vacancies":
                records = storage.load_all()
                data = [r.model_dump() for r in records]
                self._send_json(data)
            elif self.path == "/api/profile":
                profile = storage.load_profile()
                self._send_json(profile.model_dump())
            elif self.path.startswith("/api/vacancies/") and self.path.endswith("/brief"):
                rec_id = self.path.replace("/api/vacancies/", "").replace("/brief", "").strip()
                record = storage.get_by_id(rec_id)
                profile = storage.load_profile()
                if record:
                    brief = generate_application_brief(record, profile)
                    md_text = format_brief_markdown(brief)
                    self._send_json({"brief": brief.model_dump(), "markdown": md_text})
                else:
                    self.send_error(404, "Vacancy not found")
            elif self.path.startswith("/api/vacancies/") and self.path.endswith("/export-html"):
                rec_id = (
                    self.path.replace("/api/vacancies/", "").replace("/export-html", "").strip()
                )
                record = storage.get_by_id(rec_id)
                profile = storage.load_profile()
                if record:
                    html_content = generate_html_report(record, profile)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(html_content.encode("utf-8"))
                else:
                    self.send_error(404, "Vacancy not found")
            else:
                super().do_GET()

        def do_POST(self):
            storage = VacancyStorage()
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body.decode("utf-8")) if body else {}

            if self.path == "/api/profile":
                try:
                    profile = CandidateProfile.model_validate(payload)
                    storage.save_profile(profile)
                    self._send_json({"status": "success", "profile": profile.model_dump()})
                except (ValueError, KeyError, TypeError) as e:
                    self._send_json({"status": "error", "message": str(e)}, status=400)

            elif self.path == "/api/vacancies":
                try:
                    record = VacancyRecord.model_validate(payload)
                    storage.save(record)
                    updated = storage.get_by_id(record.id)
                    self._send_json(
                        {
                            "status": "success",
                            "vacancy": updated.model_dump() if updated else {},
                        }
                    )
                except (ValueError, KeyError, TypeError) as e:
                    self._send_json({"status": "error", "message": str(e)}, status=400)

            elif self.path.startswith("/api/vacancies/") and self.path.endswith("/analyze-cv"):
                rec_id = self.path.replace("/api/vacancies/", "").replace("/analyze-cv", "").strip()
                record = storage.get_by_id(rec_id)
                cv_text = payload.get("cv_text", "")
                if record:
                    res = analyze_cv_coverage(cv_text, record)
                    self._send_json({"coverage": res.model_dump()})
                else:
                    self.send_error(404, "Vacancy not found")

            else:
                self.send_error(404, "Endpoint not found")

        def do_DELETE(self):
            storage = VacancyStorage()
            if self.path.startswith("/api/vacancies/"):
                rec_id = self.path.replace("/api/vacancies/", "").strip()
                success = storage.delete(rec_id)
                self._send_json({"status": "deleted" if success else "not_found", "id": rec_id})
            else:
                self.send_error(404)

        def _send_json(self, data: dict, status: int = 200):
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, default=str).encode("utf-8"))

    click.echo(f"Serving Cyber Posting Ledger Dashboard at http://localhost:{port} ...")
    try:
        with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")


if __name__ == "__main__":
    cli()
