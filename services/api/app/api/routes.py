from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from uuid import uuid4
import boto3, os, json
from app.api.jobs import enqueue_job


router = APIRouter()


MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET = os.getenv("MINIO_BUCKET", "pdfs")


s3 = boto3.client(
's3',
endpoint_url=f"http://{MINIO_ENDPOINT}",
aws_access_key_id=MINIO_ACCESS_KEY,
aws_secret_access_key=MINIO_SECRET_KEY,
region_name="us-east-1",
)


@router.post('/uploads')
async def upload_file(file: UploadFile = File(...)):
# Persist to MinIO and create job record
ext = file.filename.split('.')[-1]
object_key = f"incoming/{uuid4()}.{ext}"
content = await file.read()
try:
s3.put_object(Bucket=BUCKET, Key=object_key, Body=content)
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))


job = enqueue_job({
'type': 'convert',
'input': object_key,
'options': {'target': 'pdf'}
})
return {"job_id": job}


@router.post('/jobs/merge')
def merge_docs(item: dict):
# item: {"inputs": [object_keys], "output_name": "merged.pdf"}
job = enqueue_job({
'type': 'merge',
'inputs': item.get('inputs', []),
'output': item.get('output_name', f"merged-{uuid4()}.pdf")
})
return {"job_id": job}
