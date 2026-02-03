import json
import boto3
import uuid
from datetime import datetime
from urllib.parse import urlparse

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("links")

def generate_code():
    return uuid.uuid4().hex[:6]

def extract_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }

def lambda_handler(event, context):

    # ✅ Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": ""
        }

    try:
        body = json.loads(event.get("body") or "{}")
        target_url = body.get("target_url")

        if not target_url:
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps({"error": "target_url is required"})
            }

        domain = extract_domain(target_url)

        # 🔍 Scan with pagination (safe for growth)
        scan_kwargs = {
            "ProjectionExpression": "code, target_url, click_count"
        }

        while True:
            response = table.scan(**scan_kwargs)

            for item in response.get("Items", []):
                existing_domain = extract_domain(item["target_url"])
                if existing_domain == domain:
                    # ♻️ Existing domain → increment counter
                    table.update_item(
                        Key={"code": item["code"]},
                        UpdateExpression="SET click_count = if_not_exists(click_count, :z) + :o",
                        ExpressionAttributeValues={
                            ":o": 1,
                            ":z": 0
                        }
                    )

                    return {
                        "statusCode": 200,
                        "headers": cors_headers(),
                        "body": json.dumps({
                            "code": item["code"],
                            "short_url": f"https://vinnuverse.site/{item['code']}",
                            "domain": domain,
                            "message": "Existing domain reused"
                        })
                    }

            if "LastEvaluatedKey" not in response:
                break

            scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]

        # 🆕 Create new short URL
        code = generate_code()
        now = datetime.utcnow().isoformat()

        table.put_item(
            Item={
                "code": code,
                "target_url": target_url,   # ✅ FULL LONG URL (any length)
                "created_at": now,
                "click_count": 1
            }
        )

        return {
            "statusCode": 201,
            "headers": cors_headers(),
            "body": json.dumps({
                "code": code,
                "short_url": f"https://vinnuverse.site/{code}",
                "domain": domain,
                "message": "Short URL created"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers(),
            "body": json.dumps({"error": str(e)})
        }
