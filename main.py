import json
import os

from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()

project_id = os.environ['GCP_PROJECT']

configurations = None

with open('config.json') as f:
    configurations = f.read()

config = json.loads(configurations)


def file_upload_trigger(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.
    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    topic_name = config.get("RESULT_TOPIC")
    message_data = json.dumps(data).encode('utf-8')
    topic_path = publisher.topic_path(project_id, topic_name)
    future = publisher.publish(topic_path, data=message_data)
    future.result()

#
# {
#   "bucket" : "dup-tenant-a",
#   "contentLanguage" : "en",
#   "contentType" : "application/octet-stream",
#   "crc32c" : "GLsuKA==",
#   "etag" : "CJnT48+qjt4CEAE=",
#   "generation" : "1539808756820377",
#   "id" : "dup-tenant-a/Svarut.seq/1539808756820377",
#   "kind" : "storage#object",
#   "md5Hash" : "3NwFDV+flTXGvOIdPOwV/A==",
#   "mediaLink" : "https://www.googleapis.com/download/storage/v1/b/dup-tenant-a/o/Svarut.seq?generation=1539808756820377&alt=media",
#   "metageneration" : "1",
#   "name" : "Svarut.seq",
#   "selfLink" : "https://www.googleapis.com/storage/v1/b/dup-tenant-a/o/Svarut.seq",
#   "size" : "246",
#   "storageClass" : "REGIONAL",
#   "timeCreated" : "2018-10-17T20:39:16.819Z",
#   "timeStorageClassUpdated" : "2018-10-17T20:39:16.819Z",
#   "updated" : "2018-10-17T20:39:16.819"
#   }
