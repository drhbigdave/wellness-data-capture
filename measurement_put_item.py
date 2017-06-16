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

realm = input('Will you be capturing - measurements - supplements - pain - or 5:2fast?  ')
currentTime = datetime.today()
timestamp = str(currentTime)
fat = input('what fat % did the tanita scale indicate (taken to 1 decimal place)? ')
hydration = input('what hydration value did the tanita scale indicate (taken to 1 decimal place)? ')
notes = input('are there any notes you\'d like to capture? ')
waist = input('in inches, what was your waist measurement (taken to 1 decimal place)? ')
weight = input('in lbs, what weight did the tanita scale indicate (taken to 1 decimal place)?')
rtgrip = input('in lbs, what was your right grip strength measurment (taken to 1 decimal place)? ')
ltgrip = input('in lbs, what was your left grip strength measurment (taken to 1 decimal place)? ')


response = table.put_item(
   Item={
        'realm': realm,
        'timestamp': timestamp,
        'fat': fat,
        'hydration': hydration,
        'notes': notes,
        'waist': waist,
        'weight': weight,
        'right-grip': rtgrip,
        'left-grip': ltgrip
        }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))