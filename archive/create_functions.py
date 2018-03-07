from __future__ import print_function # Python 2/3 compatibility
import boto3
import decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

table = dynamodb.Table('wellness')

required_hash_data = {}
required_hash_data['realm'] = realm_input
required_hash_data['timestamp'] = timestamp_input
required_hash_data['weight'] = decimal.Decimal(weight_input)

#write to wellness table
with table.batch_writer() as batch:
    batch.put_item(final_input_data)

print("PutItem succeeded:")