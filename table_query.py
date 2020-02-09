from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
#import decimal
#from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
#class DecimalEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, decimal.Decimal):
#            if o % 1 > 0:
#                return float(o)
#            else:
#                return int(o)
#        return super(DecimalEncoder, self).default(o)

session = boto3.setup_default_session(profile_name='dynamo')

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

table = dynamodb.Table('wellness')

response2 = table.query(
        KeyConditionExpression=Key('realm').eq('measurements'))

#print(response)
all_supps = set()

for i in response2['Items']:
    for x in i:
        all_supps.add(x)
        
print(all_supps)

supp = 'waist'
timestamp = '2019'

#for i in response2['Items']:
#    if timestamp in i['timestamp']:
#        print(i['timestamp'], i[supp])
        

for i in response2['Items']:
    if supp in i:
        print(i['timestamp'], i[supp])
    




#measurement_capture = {}
#
#realm = 'measurements'
#timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S"))
#required_hash_data = {
#    'realm': realm,
#    'timestamp': timestamp
#}



#[d['value'] for d in l if 'value' in d]

#for i in response['Items']:
#    print(i['rez-v'])


