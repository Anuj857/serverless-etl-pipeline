import json
import boto3
from datetime import datetime

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
    
    # Open-Meteo places real-time metrics inside 'current_weather'
    current = data.get('current_weather', {})
    
    if not current.get('temperature') and not current.get('windspeed'):
        print("ETL AUDIT: Total:1 | Inserted:0 | Rejected:1 (Missing data)")
        return {'statusCode': 200, 'body': 'No valid weather metrics found.'}
        
    try:
        # Create a unique reading ID using the timestamp
        reading_id = f"wx-{int(current.get('time', datetime.utcnow().timestamp()))}"
        wind_speed = float(current.get('windspeed', 0))
        
        # Business logic: flag high-wind safety alerts
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