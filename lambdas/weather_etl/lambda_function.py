import json
import boto3
from datetime import datetime
import time # Added this library to safely handle timestamps

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'WeatherTable'

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        data = json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        print(f"Error downloading/parsing Weather JSON: {e}")
        return {'statusCode': 400, 'body': 'JSON Parsing Error'}
        
    table = dynamodb.Table(TABLE_NAME)
    
    current = data.get('current_weather', {})
    
    if not current.get('temperature') and not current.get('windspeed'):
        print("ETL AUDIT: Total:1 | Inserted:0 | Rejected:1 (Missing data)")
        return {'statusCode': 200, 'body': 'No valid weather metrics found.'}
        
    try:
        # BUG FIX: Open-Meteo returns time as a text string (e.g., "2026-07-01T12:00").
        # Instead of parsing their string, we will use Python's safe time.time() 
        # to generate a unique mathematical ID that DynamoDB will accept.
        reading_id = f"wx-{int(time.time())}"
        wind_speed = float(current.get('windspeed', 0))
        
        status = "ADVISORY" if wind_speed > 15.0 else "NORMAL"
        
        clean_item = {
            'reading_id': reading_id,
            'dataset_type': 'weather_metric',
            'temperature_celsius': str(current.get('temperature')),
            'windspeed_kmh': str(wind_speed),
            'weather_code': str(current.get('weathercode', 0)),
            'wind_status': status,
            'processed_at': datetime.utcnow().isoformat()
        }
        
        table.put_item(Item=clean_item)
        print("ETL AUDIT: Total:1 | Inserted:1 | Rejected:0")
        return {'statusCode': 200, 'body': 'Weather data successfully loaded.'}
        
    except Exception as e:
        print(f"Error inserting to DynamoDB: {e}")
        return {'statusCode': 500, 'body': 'Database Write Error'}