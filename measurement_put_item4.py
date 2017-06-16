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
timestamp = str('2017-05-27 08:00:00')
realm = 'measurements'
notes = 'none'

#is the timestamp current or historical
#currentOrNot = input('are you inputting historical or current data? provide "c" for current, "h" for a noncurrent entry:  ')
#if currentOrNot is 'c':
#    timestamp = str(datetime.today())
#else:
#    timestamp = str(input('provide the time for the data input - \'year-month-day hour:min:sec\' example: \'2017-05-27 13:06:01:    '))

'''
realm = input('Will you be capturing - measurements - supplements - pain - or 5:2fast?  ')
fat = input('what fat % did the tanita scale indicate (taken to 1 decimal place)? ')
hydration = float(input('what hydration value did the tanita scale indicate (taken to 1 decimal place)? '))
notes = input('are there any notes you\'d like to capture? ')
waist = input('in inches, what was your waist measurement (taken to 1 decimal place)? ')
weight = input('in lbs, what weight did the tanita scale indicate (taken to 1 decimal place)? ')
rtgrip = input('in lbs, what was your right grip strength measurment (taken to 1 decimal place)? ')
ltgrip = input('in lbs, what was your left grip strength measurment (taken to 1 decimal place)? ')
'''

response = table.put_item(
   Item={
        'realm': realm,
        'timestamp': timestamp,
        'fat': decimal.Decimal(15.3),
        'hydration': decimal.Decimal(55.1),
        'notes': notes,
        'waist': decimal.Decimal(36.5),
        'weight': decimal.Decimal(196.0),
        'right-grip': decimal.Decimal(113.8),
        'left-grip': decimal.Decimal(127.8)
        }
)

print(type(hydration))
print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))