import json
import boto3
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'ProductTable'

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        data = json.loads(response['Body'].read().decode('utf-8'))
        product_list = data.get('products', [])
    except Exception as e:
        print(f"Error downloading/parsing Products JSON: {e}")
        return {'statusCode': 400, 'body': 'JSON Parsing Error'}
        
    table = dynamodb.Table(TABLE_NAME)
    total_input = 0
    inserted = 0
    rejected = 0
    
    for prod in product_list:
        total_input += 1
        try:
            if not prod.get('id') or not prod.get('price'):
                rejected += 1
                continue
                
            price = float(prod['price'])
            discount_pct = float(prod.get('discountPercentage', 0))
            
            # Transformation: Calculate the exact final sale price
            discount_amount = price * (discount_pct / 100.0)
            final_price = round(price - discount_amount, 2)
            
            clean_item = {
                'product_id': str(prod['id']),
                'dataset_type': 'catalog_item',
                'title': prod.get('title', 'Unknown Product'),
                'category': prod.get('category', 'General'),
                'original_price': str(price),
                'sale_price': str(final_price),
                'stock_level': str(prod.get('stock', 0)),
                'processed_at': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=clean_item)
            inserted += 1
            
        except Exception as e:
            print(f"Error scaling product catalog row: {e}")
            rejected += 1
            
    print(f"ETL AUDIT: Total:{total_input} | Inserted:{inserted} | Rejected:{rejected}")
    return {'statusCode': 200, 'body': f"Catalog synced. Loaded {inserted} items."}