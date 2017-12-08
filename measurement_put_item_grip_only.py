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
currentOrNot = input('are you inputting historical or\
 current data? provide "c" for current, "h" for a noncurrent entry:  ')
if currentOrNot is 'c':
    timestamp = str(datetime.today())
else:
    timestamp = str(input('provide the time for the data\
     input - \'year-month-day hour:min:sec\' example: \'2017-05-27 13:06:01:    '))

#choose the realm for the put
chooseRealm = input('Will you be capturing - measurements - \
    supplements - pain - or 5:2fast? provide "m" , "s" "p" or "f" or leave \
    this blank to create a new realm:   ')
if chooseRealm is 'm':
    realm = 'measurements'
elif chooseRealm is 's':
    realm = 'supplements'
elif chooseRealm is 'p':
    realm = 'pain'
else:
    realm = str(input('if you want to create a new realm type it here\
    in lowercase letters:   '))

rtgrip = input('in lbs, what was your right grip strength \
    measurment (taken to 1 decimal place)? ')
ltgrip = input('in lbs, what was your left grip strength \
    measurment (taken to 1 decimal place)? ')


response = table.put_item(
   Item={
        'realm': realm,
        'timestamp': timestamp,
        'fat': decimal.Decimal(fat),
        'hydration': decimal.Decimal(hydration),
        'notes': notes,
        'waist': decimal.Decimal(waist),
        'weight': decimal.Decimal(weight),
        'right-grip': decimal.Decimal(rtgrip),
        'left-grip': decimal.Decimal(ltgrip)
        }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))