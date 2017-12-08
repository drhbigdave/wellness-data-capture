from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from datetime import datetime

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

table = dynamodb.Table('wellness')

#is the timestamp current or historical
currentOrNot = input('are you inputting historical or current data?\
 provide "c" for current, "h" for a noncurrent entry:  ')
if currentOrNot is 'c':
    timestamp = str(datetime.today())
else:
    timestamp = str(input('provide the time for the data input -\
     \'year-month-day hour:min:sec\' example: \'2017-05-27 13:06:01:    '))

realm = 'supplements'
adhoc_name_input = input('supply the name of the new supplement here..  ')
adhoc_ammount_input = int(input('supply the amount here..  '))

'''
area for unused variables until i find a better way:
        'beta-alanine': betaAlanine,
'''

response = table.put_item(
   Item={
        'realm': realm,
        'timestamp': timestamp,
        adhoc_name_input: adhoc_ammount_input
        }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))