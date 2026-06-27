# Hydrology Job AI Pro

Production-ready daily job-search automation for UK hydrology, water resources, flood risk, catchment management, climate resilience, and environmental research roles.

## What it does

- Searches 50+ UK water-sector and academic job sources.
- Uses compliant RSS feeds, public pages, APIs, and Apify connectors where appropriate.
- Stores jobs in SQLite locally or PostgreSQL in production.
- Detects duplicates by normalized title, employer, location, and URL.
- Filters and scores jobs using hydrology keywords and weighted relevance rules.
- Updates a Google Sheets dashboard.
- Sends Gmail alerts for high-priority jobs.
- Generates draft CV bullet points and cover-letter paragraphs for human review.
- Runs automatically every day through GitHub Actions.

## Quick start

### 1. Upload to GitHub

Upload the extracted repository contents, not the ZIP file.

Required structure:

```text
.github/workflows/daily-job-search.yml
main.py
requirements.txt
src/
config/
templates/
```

### 2. Add GitHub Secrets

Go to:

`Repository → Settings → Secrets and variables → Actions → New repository secret`

Add these secrets:

```text
EMAIL_USER              Your Gmail address
EMAIL_APP_PASSWORD      Gmail app password, not normal Gmail password
EMAIL_TO                Your receiving email
GOOGLE_SHEET_ID         Google Sheet ID
GOOGLE_SERVICE_ACCOUNT_JSON  Full Google service account JSON as one line
OPENAI_API_KEY          Optional, for AI tailoring
APIFY_TOKEN             Optional, for LinkedIn/Indeed actors
DATABASE_URL            Optional PostgreSQL URL. If missing, SQLite is used.
```

### 3. Run manually

Go to:

`Actions → Daily Hydrology Job Search → Run workflow`

### 4. Daily automatic run

The workflow runs daily at 07:00 UTC by default. Edit `.github/workflows/daily-job-search.yml` to change time.

## Important compliance note

LinkedIn, Indeed, Reed, Totaljobs, Monster and CV-Library may restrict direct scraping. This repository is designed to use compliant methods:

- RSS feeds where available.
- Official APIs if available.
- Apify actors or approved connectors.
- Public pages only when allowed by robots.txt and terms.

Human review is required before submitting applications. The system does not auto-apply.

## Google Sheet tabs

Create a Google Sheet with these tabs:

1. `Jobs`
2. `Applications`
3. `Summary`
4. `AI Drafts`
5. `Config`

The system will create headers automatically.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Windows local run

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Folder structure

```text
src/sources/        Job source connectors
src/storage/        SQLite/PostgreSQL database and Google Sheets
src/alerts/         Gmail alerts
src/ai/             AI CV and cover letter drafting
src/utils/          Keywords, scoring, deduplication
config/             Sources and keywords
.github/workflows/  Daily GitHub Action
```
