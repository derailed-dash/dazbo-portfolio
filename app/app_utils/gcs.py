"""
Description: Google Cloud Storage utility.
Why: Handles uploading images and generating public URLs for portfolio assets.
How: Uses google-cloud-storage library.
"""

from google.cloud import storage


class GCSClient:
    def __init__(self, project_id: str, bucket_name: str):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.client = storage.Client(project=project_id)
        self.bucket = self.client.bucket(bucket_name)

    def upload_image(self, file_content: bytes, filename: str, content_type: str) -> str:
        """
        Uploads an image to GCS and returns its public URL.
        """
        blob = self.bucket.blob(filename)
        blob.upload_from_string(file_content, content_type=content_type)
        return self.get_public_url(filename)

    def get_public_url(self, filename: str) -> str:
        """
        Constructs the public URL for a given filename.
        Assumption: The bucket is configured for public access.
        """
        # Using the standard GCS public URL format
        return f"https://storage.googleapis.com/{self.bucket_name}/{filename}"
