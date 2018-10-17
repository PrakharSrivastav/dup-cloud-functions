def hello_gcs_generic(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.
    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    print(data)
    # print('Event ID: {}'.format(context.event_id))
    # print('Event type: {}'.format(context.event_type))
    print('Bucket Name os: {}'.format(data['bucket']))
    # print('File: {}'.format(data['name']))
    # print('Metageneration: {}'.format(data['metageneration']))
    # print('Created: {}'.format(data['timeCreated']))
    # print('Updated: {}'.format(data['updated']))
