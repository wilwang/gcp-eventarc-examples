import base64
import json
import functions_framework
from google.cloud import storage

@functions_framework.cloud_event
def handle_pubsub_event(cloud_event):
    data_str = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    #print (data_str)
    
    data = json.loads(data_str)
    bucket_name = data['incident']['resource']['labels']['bucket_name']
    print (f'{bucket_name} being over-accessed')

    storage_client = storage.Client()

    print ('bucket retrieved')
    bucket = storage_client.get_bucket(bucket_name)

    print ('get iam policy')
    policy = bucket.get_iam_policy(requested_policy_version=3)

    print ('list bindings')
    for binding in policy.bindings:
        print(binding)
        members = binding['members']

        for member in members:
            if member == 'serviceAccount:<SVC_ACCT>@<PROJECT_ID>.iam.gserviceaccount.com':
                print (f'remove {member}')
                binding['members'].discard(member)

    bucket.set_iam_policy(policy)







    
    