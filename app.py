from flask import Flask, jsonify
import boto3
import os
import time
import threading
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Use the custom endpoint if needed (e.g., for non-AWS S3 services like iDrive e2)
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
GB_PLAN_CAP = int(os.getenv('S3_GB_PLAN_CAP'))
PORT = int(os.getenv('PORT', 80))

# Global cache variables
cached_value = None
last_update_time = 0
CACHE_DURATION = 12 * 60 * 60  # 12 hours in seconds

# Initialize Boto3 S3 client with custom endpoint
s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT_URL  # Set custom endpoint here
)


def update_cache():
    global cached_value, last_update_time
    # Update the cached value and the timestamp
    total_gb, total_bytes, perc = get_total_gb()
    cached_value = { "total_gb": total_gb, "total_bytes": total_bytes, "usage_percentage": perc }
    last_update_time = time.time()
    app.logger.info("Cache updated successfully")

def cache_updater():
    while True:
        time.sleep(CACHE_DURATION)  # Sleep for 12 hours
        update_cache()  # Update the cache every 12 hours

def get_total_gb():
    total_bytes = 0
    # List all buckets
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    # Iterate through each bucket
    for bucket in buckets:
        bucketObj = boto3.resource('s3', endpoint_url=S3_ENDPOINT_URL).Bucket(bucket)
        for object in bucketObj.objects.all():
            total_bytes += object.size

    # Convert total size from bytes to GB
    total_gb = total_bytes / (1024 ** 3)
    return round(total_gb, 2), total_bytes, round((total_gb * 100 / GB_PLAN_CAP), 2)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Pong"})

@app.route('/get-total-gb', methods=['GET'])
def total_gb():
    return jsonify(cached_value)

if __name__ == '__main__':
    # Initialize cache on startup
    update_cache()
    threading.Thread(target=cache_updater, daemon=True).start()
    app.run(host='0.0.0.0', port=PORT)
