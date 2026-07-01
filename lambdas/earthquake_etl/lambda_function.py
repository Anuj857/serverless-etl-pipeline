import json
import boto3
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'EarthquakeTable'

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    try:
        # Download and parse the JSON from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        data = json.loads(response['Body'].read().decode('utf-8'))
        
        # USGS GeoJSON stores the actual events in the 'features' list
        features = data.get('features', [])
    except Exception as e:
        print(f"Error downloading/parsing Earthquake JSON: {e}")
        return {'statusCode': 400, 'body': 'JSON Parsing Error'}
        
    table = dynamodb.Table(TABLE_NAME)
    total_input = 0
    inserted = 0
    rejected = 0
    
    for feature in features:
        total_input += 1
        props = feature.get('properties', {})
        event_id = feature.get('id')
        
        try:
            # Transform Rule 1: Reject records missing an ID or a valid magnitude
            # (This will intentionally catch and reject that "unknown123" mock record!)
            if not event_id or props.get('mag') is None:
                rejected += 1
                continue
                
            mag = float(props['mag'])
            
            # Transform Rule 2: Create derived field based on severity
            alert_level = "CRITICAL" if mag >= 5.0 else "NORMAL"
            
            # Load: Build the clean item matching our DynamoDB Partition Key (event_id)
            clean_item = {
                'event_id': str(event_id),
                'dataset_type': 'earthquake_event',
                'magnitude': str(mag),
                'location': props.get('place', 'Unknown'),
                'alert_level': alert_level,
                'event_time_ms': str(props.get('time', 0)),
                'processed_at': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=clean_item)
            inserted += 1
            
        except Exception as e:
            print(f"Error processing earthquake event: {e}")
            rejected += 1
            
    # Audit Logs for CloudWatch
    print(f"ETL AUDIT: Total:{total_input} | Inserted:{inserted} | Rejected:{rejected}")
    return {'statusCode': 200, 'body': f"Earthquake data processed. Loaded {inserted} items."}