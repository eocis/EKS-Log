import gzip
import json
import logging
import base64
import os
   
from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Lambda 환경변수
SLACK_CHANNEL = os.environ['slackChannel']
HOOK_URL = os.environ['hookUrl']

# Log Setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)
   
def lambda_handler(event, context):
    
    # Cloudwatch 트리거시 전달되는 데이터 선택
    cw_data = event['awslogs']['data']
    
    # awslog data를 ByteCode로 변환
    compressed_payload = base64.b64decode(cw_data)
    
    # 변환된 코드를 압축
    uncompressed_payload = gzip.decompress(compressed_payload)
    
    # 압축된 데이터를 JSON으로 사용
    payload = json.loads(uncompressed_payload)  #dict > list
    reason = payload['owner']
    event_list = payload['logEvents']  #list < dict
    event = event_list[0] #dict > json
    message = json.loads(event['message'])
    
    # 가공된 데이터 사용
    log = message['log']
    container_name = message['kubernetes']['container_name']
    pod = message['kubernetes']['pod_id']
    
    # Slack Message Form
    slack_body = f'''
    Pod: {pod}
    Container_name: {container_name}
    Log: {log}
    '''
    
    # Slack Message Body
    slack_message = {
        "channel": SLACK_CHANNEL,
        "username": "EKS Alert",
        "text": slack_body
    }

    # POST Request
    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        # Send
        response.read()
        logger.info(f"message posted to {os.environ[slackChannel]}")
        
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
    except:
        logger.info(f"message post error")