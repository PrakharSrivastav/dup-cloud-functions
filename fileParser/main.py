from google.cloud import pubsub_v1
from google.cloud import storage
from google.cloud import bigquery

from google.auth.exceptions import DefaultCredentialsError
from google.api_core.exceptions import AlreadyExists
import time, csv, json

# Setup configurations
try:
    with open("config.json") as f:
        config = json.loads(f.read(), encoding="UTF-8")
except Exception as e:
    raise Exception("Invalid configuration setup. Please validate if config.json is setup properly")

# Setup storage and pubsub clients
try:
    storage_client = storage.Client()
    subscriber = pubsub_v1.SubscriberClient()
    bq_client = bigquery.Client()
except DefaultCredentialsError as e:
    raise Exception("Invalid login credentials. Please make sure GOOGLE_APPLICATION_CREDENTIALS is setup")
except Exception as e:
    raise e


def callback(message):
    try:
        message.ack()
        bucket_info = json.loads(message.data, encoding="UTF-8")
        keys = read_file_contents(json.loads(message.data, encoding="UTF-8"))
        load_dataset_bq(bucket_info, keys)

    except KeyError as e:
        raise Exception("Please check the data published to pub_sub. One of the keys referenced does not exist")
    except Exception as e:
        print("Some error", type(e) ,e )


def load_dataset_bq(bucket_info, keys):
    try:
        print(bucket_info)
        print(keys)
        uri = 'gs://{}/{}'.format(bucket_info.get("bucket"), bucket_info.get("name"))

        dataset_id = bucket_info.get("name").replace(".", "_")
        dataset = bigquery.Dataset(bq_client.dataset(dataset_id))
        bq_client.create_dataset(dataset)
        print("dataset_id {}".format(dataset_id))
        dataset_ref = bq_client.dataset(dataset_id)

        print("uri is {}".format(uri))
        job_config = bigquery.LoadJobConfig()
        job_config.schema = [bigquery.SchemaField(items, "STRING") for items in keys]

        job_config.skip_leading_rows = 1
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.field_delimiter = ";"


        load_job = bq_client.load_table_from_uri(
            uri,
            dataset_ref.table(dataset_id),
            job_config=job_config
        )
        print('Starting job {}'.format(load_job.job_id))
        load_job.result()  # Waits for table load to complete.
        print('Job finished.')
        destination_table = bq_client.get_table(dataset_id)
        print('Loaded {} rows.'.format(destination_table.num_rows))
    except KeyError as ex:
        print("BQ : ", ex)


# Stream the contents of the csv file to pubsub for example
def read_file_contents(bucket_info):
    try:
        print(bucket_info)
        bucket = storage_client.get_bucket(bucket_info.get("bucket"))
        blob = bucket.get_blob(bucket_info.get("name"))
        if blob is not None and blob.content_type == "text/csv":
            lines = blob.download_as_string().decode().split("\n")
            reader = csv.DictReader(lines, delimiter=";")
            for row in reader:
                if row and row is not None:
                    # print(row['meterpoint_id'])
                    print()
                    return row.keys()
        else:
            raise Exception("Invalid file type. We only support csv files")
    except Exception as e:
        print("Error parsing the file", e)
        print(e.args)


def subscribe_to_source_topic():
    # Create the subscription
    try:
        project_id = config.get("PROJECT_ID")
        source_topic = config.get("SOURCE_TOPIC")
        topic_subscriber = config.get("SOURCE_TOPIC_SUBSCRIBER")
        if project_id and source_topic and topic_subscriber:
            topic = subscriber.topic_path(project_id, source_topic)
            path = subscriber.subscription_path(project_id, topic_subscriber)
            subscriber.create_subscription(path, topic)
        else:
            raise Exception("Configuration properties not set")

    except KeyError:
        print("Invalid configuration keys")
        raise Exception("Trying to access wrong key from configuration. Please check your configuration access")

    except KeyboardInterrupt as e:
        print("Manual Interruption")

    except AlreadyExists as e:
        print("You are trying to create an existing subscription. Please change the name for your subscriber")

    subscriber.subscribe(path, callback=callback)
    print('Listening for messages on {}'.format(path))

    while True:
        time.sleep(10)


subscribe_to_source_topic()
