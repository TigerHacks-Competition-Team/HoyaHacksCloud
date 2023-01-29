import functions_framework

# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def trans_event(cloud_event):
    # Your code here
    # Access the CloudEvent data payload via cloud_event.data
    return "Hello World"