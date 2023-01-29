import functions_framework
from google.cloud import speech_v1 as speech

@functions_framework.http
def speech2text(request):
    print("Creating Speech Client")
    client = speech.SpeechClient()
    config = dict(language_code="en-US", enable_automatic_punctuation=True)
    audio = dict(uri="gs://cloud-samples-data/speech/brooklyn_bridge.flac")
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=10000)

    full_transcript = ""
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        full_transcript = full_transcript + " " + transcript

    return full_transcript