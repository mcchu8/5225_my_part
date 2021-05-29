import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Lambda function variables
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Photo')
    #print(event['photo_url'])
    
   
        
    try:
        # Get the old tag from table based on url
        # Oldtag_dict is a dict of dict {"Item": {"image_URL":"url", "tag":"oldtag"}}
        oldtag_dict = table.get_item(
            Key={
                'photo_url': event["photo_url"]
            }
            )
        # Get oldtag from oldtag_dict and append

        oldtag = oldtag_dict["Item"]["tags"]

        if type(event["tags"]) == list:
            oldtag.extend(event["tags"])
        else: 
            oldtag.append(event["tags"])
        
        # remove duplicate item
        oldtag = list( dict.fromkeys(oldtag) )
        print("oldtag: ", oldtag)
        
        # update the tag
        result = table.update_item(
            Key={
                'photo_url': event["photo_url"]
            },
            UpdateExpression= "SET tags=:t",
            ExpressionAttributeValues={
                ':t': oldtag
            },
            ReturnValues='UPDATED_NEW'
        )
        response =  {"statusCode": 200,
                        "body": json.dumps({
                            "message": "Successful response",
                        }),
                        "headers":{ 'Access-Control-Allow-Origin' : '*' }}
        
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])

        else:
            raise
    else:
        return response
