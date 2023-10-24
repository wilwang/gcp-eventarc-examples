# Disable a bucket on custom log metric alert
This is an example of using [EventArc](https://cloud.google.com/eventarc/docs#docs) to trigger a [Cloud Function v2](https://cloud.google.com/functions?hl=en) from a [metrics alert](https://cloud.google.com/monitoring/alerts) based on a [custom log metric](https://cloud.google.com/logging/docs/logs-based-metrics).

In this particular example, when a process is over executing a bucket operation (e.g., list), we want to remove the service account from the bucket to remove its access and stop the operations. This example is specific for a single bucket, so it's not scalable, but you could create the log filter to be broader and transform your data to group by bucket name for a more generic solution.

## Create the custom metric
1. [Turn on data access](https://cloud.google.com/logging/docs/audit/configure-data-access) (user-read) audit log for the bucket
2. Create log filter to test you are capturing the correct logs
```
resource.type="gcs_bucket"
resource.labels.project_id="<PROJECT_ID>"
protoPayload.methodName="storage.objects.list"
protoPayload.authenticationInfo.principalEmail:"<ACCOUNT_EMAIL>"
```
3. Create a log metric using the filter above
4. View the custom metric in metrics explorer through the Log-based Metrics interface on Cloud Logging
5. Test your log metric by running:
```
for i in {1..10}; do gsutil ls gs://<BUCKET_NAME>; done;
```

## Create a metric alert
1. Create a [metric-threshold alert policy](https://cloud.google.com/monitoring/alerts/using-alerting-ui) for the custom log metric you created
2. Use the `sum` function for the rolling window function
3. Set a threshold and configure the alert trigger and threshold position
4. Create a notification to use a PubSub topic

## Create a Cloud Function that will be driven by EventArc 
1. Cloud Functions v2 can be deployed via [CLI](https://cloud.google.com/functions/docs/create-deploy-gcloud) or [console](https://cloud.google.com/functions/docs/console-quickstart)
2. Deploy the code in [gcs_bucket_disable_on_high_activity.py](./gcs_bucket_disable_on_high_activity.py)
3. Give the Monitoring Service Account (service-<project_number>@gcp-sa-monitoring-notification.iam.gserviceaccount.com) Pub/Sub Publisher role
4. Give the service account that the Cloud Function will run under Cloud Run Invoker role
