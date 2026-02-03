import boto3
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("links")

def lambda_handler(event, context):

    # ✅ Handle OPTIONS (browser preflight)
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }

    code = event.get("pathParameters", {}).get("code")

    if not code or code == "favicon.ico":
        return {
            "statusCode": 404,
            "body": "Not found"
        }

    try:
        response = table.update_item(
            Key={"code": code},
            UpdateExpression="""
                SET click_count = if_not_exists(click_count, :zero) + :inc,
                    last_accessed = :now
            """,
            ConditionExpression="attribute_exists(code)",
            ExpressionAttributeValues={
                ":inc": 1,
                ":zero": 0,
                ":now": datetime.utcnow().isoformat()
            },
            ReturnValues="ALL_NEW"
        )

        target_url = response["Attributes"]["target_url"]

        # ✅ PURE REDIRECT (no CORS needed)
        return {
            "statusCode": 302,
            "headers": {
                "Location": target_url
            },
            "body": ""
        }

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {
                "statusCode": 404,
                "body": "Short URL not found"
            }

        return {
            "statusCode": 500,
            "body": "Internal server error"
        }
