# Google Sheets Setup

1. Create a Google Sheet.
2. Copy the Sheet ID from the URL.
3. Create a Google Cloud service account.
4. Enable Google Sheets API and Google Drive API.
5. Download the service account JSON.
6. Share your Google Sheet with the service account email as Editor.
7. In GitHub Secrets add:
   - GOOGLE_SHEET_ID
   - GOOGLE_SERVICE_ACCOUNT_JSON

Paste GOOGLE_SERVICE_ACCOUNT_JSON as one-line JSON.
