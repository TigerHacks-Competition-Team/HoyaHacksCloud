import functions_framework
from urllib.request import urlopen
import json
import requests
import os


# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def trans_end(cloud_event):
    # Your code here
    # Access the CloudEvent data payload via cloud_event.data
    #print(f"Cloud_Event Data: {str(cloud_event.data)}")
    print(cloud_event)
    url = cloud_event.data["mediaLink"]
    id = cloud_event.data["name"].split(".")[0]
    
    # store the response of URL
    response = urlopen(url)
    
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())

    transcription = ""
    for result in data_json["results"]:
        transcription = transcription + " " + result["alternatives"][0]["transcript"]

    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {os.environ.get('SUPABASE_KEY')}"
    }
    data = {
        "id": id,
        "transcription": transcription
    }
    print(f"Callback with key {os.environ.get('SUPABASE_KEY')}")
    callback = "https://hkwrlworzfpsgkaxcobm.functions.supabase.co/transcription_callback"
    response = requests.post(callback, headers=headers, json=data)
    print(f"Callback request sent: {transcription}")
    return "Hello World"