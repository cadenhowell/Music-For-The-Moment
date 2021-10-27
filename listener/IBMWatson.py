import json
import os

from dotenv import load_dotenv
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ToneAnalyzerV3

load_dotenv()


# Authentication via IAM
authenticator = IAMAuthenticator(os.environ['WATSON_API_KEY'])
service = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator)
service.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com')

def SentimentAnalysis(transcript):
    try:

        response = service.tone(
            tone_input=transcript,
            content_type="text/plain").get_result()

        tones = json.loads(json.dumps(response))['document_tone']['tones']

        return tones
    except:
        print('Failed to communicate with Watson')