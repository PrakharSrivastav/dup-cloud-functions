from google.cloud import pubsub_v1
from google.cloud import storage
import json
from google.auth.exceptions import DefaultCredentialsError
from google.api_core.exceptions import AlreadyExists
import time
import csv
from io import StringIO

# Setup configurations
try:
    with open("config.json") as f:
        configurations = f.read()
    config = json.loads(configurations, encoding="UTF-8")
except Exception as e:
    raise Exception("Invalid configuration setup. Please validate if config.json is setup properly")

# Setup storage and pubsub clients
try:
    storageClient = storage.Client()
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
except DefaultCredentialsError as e:
    raise Exception("Invalid login credentials. Please make sure GOOGLE_APPLICATION_CREDENTIALS is setup")
except Exception as e:
    raise e


def callback(message):
    try:
        print(message.data)
        read_file_contents(json.loads(message.data, encoding="UTF-8"))
        message.ack()
    except KeyError as e:
        raise Exception("Please check the data published to pub_sub. One of the keys referenced does not exist")
    except Exception as e:
        print("Some error", e)


def read_file_contents(bucket_info):
    try:
        print(bucket_info)
        bucket = storageClient.get_bucket(bucket_info.get("bucket"))
        blob = bucket.get_blob(bucket_info.get("name"))
        if blob.content_type == "text/csv":
            print(blob.download_as_string().splitlines())
            f = StringIO(blob.download_as_string().decode().splitlines())
            # reader = csv.reader(f)
            print((f.read()))
            # for row in reader:
            #     print('\t'.join(row))
            # if csv_file is not None:
            # f = blob.download_as_string()
            # print(f)
            # reader = csv.reader(f.split('\n'), csv.excel,delimiter=';')
            # for row in reader:
            #     print(row)
        else:
            raise Exception("Invalid file type. We only support csv files")
    except Exception as e:
        print("Error parsin the file", e)
        print(e.args)


# if blob.content_type() =


def subscribe_to_source_topic():
    # Create the subscription
    try:
        topic_path = subscriber.topic_path(
            config.get("PROJECT_ID"),
            config.get("SOURCE_TOPIC")
        )

        subscription_path = subscriber.subscription_path(
            config.get("PROJECT_ID"),
            config.get("SOURCE_TOPIC_SUBSCRIBER")
        )

        subscriber.create_subscription(subscription_path, topic_path)
    except KeyError as e:
        print("Invalid configuration keys")
        raise Exception("Trying to access wrong key from configuration. Please check your configuration access")
    except AlreadyExists as e:
        print("You are trying to create an existing subscription. Please change the name for your subscriber")
        # print('Subscription created: {}'.format(subscription))
    except KeyboardInterrupt as e:
        print("Manual Interruption")

    subscriber.subscribe(subscription_path, callback=callback)

    print('Listening for messages on {}'.format(subscription_path))
    while True:
        print("reading")
        time.sleep(10)


subscribe_to_source_topic()
