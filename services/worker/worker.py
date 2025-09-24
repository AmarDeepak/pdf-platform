import pika, os, json, subprocess, boto3, tempfile
aws_secret_access_key=MINIO_SECRET_KEY,
)




def handle_convert(job):
# download, run libreoffice --headless --convert-to pdf, upload
input_key = job['input']
_, in_tmp = tempfile.mkstemp()
_, out_tmp = tempfile.mkstemp(suffix='.pdf')


s3.download_file(BUCKET, input_key, in_tmp)
# libreoffice conversion
proc = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', '/tmp', in_tmp], capture_output=True)
# assume output saved in /tmp with same basename
# find converted file
# upload result
# For reliability, do sanity checks and qpdf linearize
s3.upload_file(out_tmp, BUCKET, f"converted/{os.path.basename(out_tmp)}")




def callback(ch, method, properties, body):
job = json.loads(body)
try:
if job.get('type') == 'convert':
handle_convert(job)
elif job.get('type') == 'merge':
# implement merge using pypdf
from pypdf import PdfMerger
merger = PdfMerger()
tmp_files = []
for key in job.get('inputs', []):
_, tpath = tempfile.mkstemp(suffix='.' + key.split('.')[-1])
s3.download_file(BUCKET, key, tpath)
tmp_files.append(tpath)
merger.append(tpath)
out_path = tempfile.mktemp(suffix='.pdf')
merger.write(out_path)
merger.close()
s3.upload_file(out_path, BUCKET, f"merged/{os.path.basename(out_path)}")
# ack the message
ch.basic_ack(delivery_tag=method.delivery_tag)
except Exception as e:
print('job failed', e)
# optionally send to a dead letter queue
ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)




def main():
conn = pika.BlockingConnection(pika.URLParameters(RABBIT))
ch = conn.channel()
ch.queue_declare(queue='jobs', durable=True)
ch.basic_qos(prefetch_count=1)
ch.basic_consume(queue='jobs', on_message_callback=callback)
print('Worker started, waiting for jobs...')
ch.start_consuming()


if __name__ == '__main__':
main()
