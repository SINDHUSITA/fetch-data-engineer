import json
import logging
import os
import boto3
from dotenv import load_dotenv
from configparser import ConfigParser
from datetime import datetime
import psycopg2
import base64
load_dotenv()

# environment setup
AWS_REGION = os.environ.get("AWS_REGION")
AWS_KEY_ID = os.environ.get("AWS_KEY_ID")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_ENDPOINT_URL = os.environ.get("AWS_ENDPOINT_URL")
AWS_SESSION = os.environ.get("AWS_SESSION")
PYTHON_HASH_SEED = os.environ.get("PYTHON_HASH_SEED")

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

# AWS SQS client config
sqs_client = boto3.client("sqs", endpoint_url = AWS_ENDPOINT_URL, region_name=AWS_REGION, aws_access_key_id= AWS_KEY_ID,
                   aws_secret_access_key=AWS_ACCESS_KEY, aws_session_token = AWS_SESSION)

def receive_queue_message(queue_url):
    """
    Retrieves one or more messages from the specified queue.
    """
    try:
        response = sqs_client.receive_message(QueueUrl=queue_url)
    except ClientError:
        logger.exception(
            f'Could not receive the message from the - {queue_url}.')
        raise
    else:
        logger.info(f'Received message(s) from {QUEUE_URL}.')
        return response

def db_config(filename='database.ini', section='postgresql'):
    """
        Establishes connection with PostGres server with given specifications.
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def mask_pii(raw_str):
    b64_mask_str = base64.b64encode(raw_str.encode("utf-8"))
    return b64_mask_str.decode()

def unmask_pii(encoded_str):
    byte_str = bytes(encoded_str, 'utf-8')
    raw_str = base64.b64decode(byte_str)
    return raw_str.decode()

if __name__ == '__main__':
    # CONSTANTS
    QUEUE_URL = 'http://localhost:4566/000000000000/login-queue'
    messages = receive_queue_message(QUEUE_URL) #read messages from SQS queue

    if not PYTHON_HASH_SEED:
        os.environ["PYTHON_HASH_SEED"] = "0" #add hash seed if not present already in env

    params = db_config()
    logger.info('Connecting to the PostgreSQL database...')
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    except:
        logger.error('Error in establishing connection to Postgres.')

    for msg in messages['Messages']:
        logger.info('Inserting message to PostGres...')
        msg_body = json.loads(msg['Body'])

        # masking PII
        msg_body['masked_device_id'] = mask_pii(msg_body['device_id'])
        msg_body['masked_ip'] = mask_pii(msg_body['ip'])
        msg_body['app_version'] = int(''.join(x for x in msg_body['app_version'].split('.'))) #converting version strings like 5.6.3 to 563 integers
        del(msg_body['ip'])
        del(msg_body['device_id'])

        # adding timestamp
        msg_body['create_date'] = datetime.now().date()
        receipt_handle = msg['ReceiptHandle']

        # Inserting in database
        placeholders = ', '.join(['%s'] * len(msg_body))
        columns = ', '.join(msg_body.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('user_logins', columns, placeholders)
        cur.execute(sql, list(msg_body.values()))
        conn.commit()
        logger.info("Posted messages to Postgres server")
    cur.close()