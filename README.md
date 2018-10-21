### Create project

### Create Bucket
```commandline
gsutil mb -c regional -l europe-north1 gs://your_bucket_name -p your_project_id
```

### Update the python functions

### Deployment
```commandline
gcloud functions deploy file_upload_trigger \
    --runtime python37 \
    --trigger-resource dup-tenant-a \
    --trigger-event google.storage.object.finalize
``` 




### Delete a function
```commandline
gcloud functions delete hello_gcs_generic 
```

#### Object Finalize trigger
- On new object creation.
- On overwriting existing object.
- Ignores Archive and metadata

Decides when the event would be triggered.
```commandline
trigger-event google.storage.object.finalize
```
#### Object Delete trigger
- Useful for non-versioning buckets.
- Triggered when old version of an object is overwritten.
```commandline
trigger-event google.storage.object.delete
```

#### Object Archive trigger
- only used with versioning buckets.
- triggered when an object is overwritten or deleted.
```commandline
trigger-event google.storage.object.archive 
```

#### Object Archive trigger
- when metadata update happens on an object
```commandline
trigger-event google.storage.object.metadataUpdate 
```


```json
{
  "bucket" : "dup-tenant-a", 
  "contentLanguage" : "en", 
  "contentType" : "application/octet-stream", 
  "crc32c" : "GLsuKA==", 
  "etag" : "CJnT48+qjt4CEAE=", 
  "generation" : "1539808756820377", 
  "id" : "dup-tenant-a/Svarut.seq/1539808756820377", 
  "kind" : "storage#object", 
  "md5Hash" : "3NwFDV+flTXGvOIdPOwV/A==", 
  "mediaLink" : "https://www.googleapis.com/download/storage/v1/b/dup-tenant-a/o/Svarut.seq?generation=1539808756820377&alt=media", 
  "metageneration" : "1", 
  "name" : "Svarut.seq", 
  "selfLink" : "https://www.googleapis.com/storage/v1/b/dup-tenant-a/o/Svarut.seq", 
  "size" : "246", 
  "storageClass" : "REGIONAL", 
  "timeCreated" : "2018-10-17T20:39:16.819Z", 
  "timeStorageClassUpdated" : "2018-10-17T20:39:16.819Z", 
  "updated" : "2018-10-17T20:39:16.819"
  }
```


Create pubsub topic and subscriptions
 gcloud pubsub topics create fileUplodTopic

 gcloud pubsub subscriptions create processFileUpload --topic fileUplodTopic
 
 gcloud pubsub subscriptions pull processFileUpload
