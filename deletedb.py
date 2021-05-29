import json
from decimal import Decimal
from pprint import pprint
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Photo')
    #print("Hihi" + event['image_URL'])
    # return {"statusCode": 200,
    #         "body": json.dumps({
    #             "message": event,
    #         }),
    #         "headers":{ 'Access-Control-Allow-Origin' : '*' }}
    try:
        response = table.delete_item(
            Key={
                'photo_url': event["photo_url"]
            },
            ReturnValues='ALL_OLD'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])

        else:
            raise
    else:
        return response


