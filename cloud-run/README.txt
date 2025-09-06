# MBIE Jobs Online Monthly Data Sync

This repository contains a Python script designed to sync CSV files from specific Google Drive folders to a Google Cloud Storage (GCS) bucket. The script is intended for use as a Google Cloud Function.

## Features
- Recursively sync CSV files from Google Drive folders.
- Upload files to a specified GCS bucket.
- Handles both archive and latest data folders.

## Requirements
- Python 3.7+
- Google Cloud SDK installed and authenticated.
- Environment variables configured for:
  - `GCS_BUCKET_NAME`: Name of the GCS bucket.
  - `DRIVE_FOLDERS_TO_SYNC`: JSON mapping of GCS paths to Google Drive folder IDs.

## Usage
The script automatically syncs CSV files from the specified Google Drive folders to the GCS bucket. It can be triggered via HTTP requests.

## File Structure
- `mbie_jobs_online_monthly_download.py`: Main script for syncing data.
- `requirements`: Environment variables configuration file.

## Troubleshooting
- Ensure the Google Drive folders are shared with the service account used for authentication.
- Verify that the GCS bucket exists and the service account has write permissions.