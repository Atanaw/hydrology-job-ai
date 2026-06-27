"""Optional local helper to create headers in a connected Google Sheet."""
from src.storage.sheets import GoogleSheetsClient, JOB_HEADERS, DRAFT_HEADERS, SUMMARY_HEADERS

client = GoogleSheetsClient()
if not client.enabled:
    raise SystemExit("Google Sheets is not configured. Set GOOGLE_SHEET_ID and GOOGLE_SERVICE_ACCOUNT_JSON.")
client._worksheet("Jobs", JOB_HEADERS)
client._worksheet("AI Drafts", DRAFT_HEADERS)
client._worksheet("Summary", SUMMARY_HEADERS)
client._worksheet("Applications", ["job_id", "title", "employer", "status", "deadline", "applied_date", "interview_date", "notes"])
client._worksheet("Config", ["setting", "value"])
print("Google Sheet tabs created/verified.")
