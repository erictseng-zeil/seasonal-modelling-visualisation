import os
import io
import json
from google.cloud import storage
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import google.auth

# --- Read configuration from environment variables ---
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'mbie-jobs-online')
DRIVE_FOLDERS_JSON = os.environ.get(
    'DRIVE_FOLDERS_TO_SYNC', 
    '{"monthly-data/archive": "1j4rFz3gw3KtjPvmLQPRxL5XuR7HJA74k", "monthly-data/latest": "1eNRWxjTziXr3k5qP_tjPbJkJ1MuDvA2Y"}'
)
DRIVE_FOLDERS_TO_SYNC = json.loads(DRIVE_FOLDERS_JSON)

# --- Initialise Google service clients ---
try:
    credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/drive.readonly'])
    drive_service = build('drive', 'v3', credentials=credentials)
    storage_client = storage.Client()
except Exception as e:
    print(f"Failed to initialise Google API Client: {e}")
    drive_service = None
    storage_client = None

def sync_drive_folder_to_gcs(drive_folder_id, gcs_destination_prefix, bucket):
    """ Recursively sync all CSV files from a Google Drive folder to GCS """
    query = f"'{drive_folder_id}' in parents and trashed = false"
    try:
        results = drive_service.files().list(
            q=query,
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        items = results.get('files', [])

        for item in items:
            item_name = item['name']
            item_id = item['id']
            gcs_object_path = os.path.join(gcs_destination_prefix, item_name)

            # If it's a folder, recurse into it
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                sync_drive_folder_to_gcs(item_id, gcs_object_path, bucket)
            # If it's a file, check if it's a CSV
            elif item_name.lower().endswith('.csv'):
                print(f"Found CSV file, processing: {item_name} -> gs://{GCS_BUCKET_NAME}/{gcs_object_path}")

                # This is the download & upload logic
                request = drive_service.files().get_media(fileId=item_id)

                # 1) Create an in-memory binary stream
                file_in_memory = io.BytesIO()

                # 2) Create a downloader to write the file content to the memory stream
                downloader = MediaIoBaseDownload(file_in_memory, request)

                # 3) Execute the download
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    # You can uncomment the next line to see detailed progress
                    # print(f"  -> Download progress: {int(status.progress() * 100)}%")

                # 4) Move the stream pointer to the beginning, preparing for upload
                file_in_memory.seek(0)
                
                # 5) Upload to GCS
                blob = bucket.blob(gcs_object_path)
                blob.upload_from_file(file_in_memory, content_type='text/csv')
                print(f"  -> ✔️ Upload successful: gs://{GCS_BUCKET_NAME}/{gcs_object_path}")
            else:
                # If it's neither a folder nor a CSV, ignore it
                print(f"Ignored non-folder/non-CSV file: {item_name}")

    except Exception as e:
        print(f"Failed to access Drive Folder ID '{drive_folder_id}': {e}")
        print("  -> ❗️ Please ensure this folder is shared with your service account.")

def main(request):
    """Entry point for Cloud Function"""
    if not all([drive_service, storage_client, GCS_BUCKET_NAME, DRIVE_FOLDERS_TO_SYNC]):
        print("Error: Function initialization is incomplete or environment variables are not set.")
        return 'Configuration Error', 500

    print("--- Start syncing CSV files ---")
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    for gcs_path, drive_id in DRIVE_FOLDERS_TO_SYNC.items():
        print(f"\n syncing CSVs from Google Drive ID '{drive_id}' to GCS path '{gcs_path}'")
        sync_drive_folder_to_gcs(drive_id, gcs_path, bucket)

    print("\n--- All sync tasks completed ---")
    return "Sync process completed successfully.", 200