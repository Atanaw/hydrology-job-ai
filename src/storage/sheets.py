import json
import gspread
from google.oauth2.service_account import Credentials
from src.utils.config_loader import env

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

JOB_HEADERS = ["id", "title", "employer", "location", "salary", "score", "priority", "matched_keywords", "source", "url", "status", "deadline", "scraped_at"]
DRAFT_HEADERS = ["job_id", "title", "employer", "cv_bullets", "cover_letter_paragraph", "review_status"]
SUMMARY_HEADERS = ["metric", "value"]

class GoogleSheetsClient:
    def __init__(self):
        sheet_id = env("GOOGLE_SHEET_ID")
        service_json = env("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not sheet_id or not service_json:
            self.enabled = False
            return
        info = json.loads(service_json)
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        self.gc = gspread.authorize(creds)
        self.sheet = self.gc.open_by_key(sheet_id)
        self.enabled = True

    def _worksheet(self, name, headers):
        try:
            ws = self.sheet.worksheet(name)
        except gspread.WorksheetNotFound:
            ws = self.sheet.add_worksheet(title=name, rows=1000, cols=max(20, len(headers)))
        values = ws.get_all_values()
        if not values:
            ws.append_row(headers)
        return ws

    def append_jobs(self, jobs):
        if not self.enabled or not jobs:
            return
        ws = self._worksheet("Jobs", JOB_HEADERS)
        existing_ids = set(row[0] for row in ws.get_all_values()[1:] if row)
        rows = []
        for j in jobs:
            if j.id in existing_ids:
                continue
            rows.append([j.id, j.title, j.employer, j.location, j.salary, j.score, j.priority, ", ".join(j.matched_keywords), j.source, j.url, "new", j.deadline or "", j.scraped_at])
        if rows:
            ws.append_rows(rows, value_input_option="USER_ENTERED")

    def append_drafts(self, drafts):
        if not self.enabled or not drafts:
            return
        ws = self._worksheet("AI Drafts", DRAFT_HEADERS)
        rows = [[d["job_id"], d["title"], d["employer"], d["cv_bullets"], d["cover_letter_paragraph"], "needs human review"] for d in drafts]
        ws.append_rows(rows, value_input_option="USER_ENTERED")

    def update_summary(self, counts):
        if not self.enabled:
            return
        ws = self._worksheet("Summary", SUMMARY_HEADERS)
        ws.clear()
        ws.append_row(SUMMARY_HEADERS)
        ws.append_rows([[k, v] for k, v in counts.items()])
