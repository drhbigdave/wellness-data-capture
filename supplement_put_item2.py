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
acetylCarnitine = 500
aspirin = 81
betaAlanine = 2250
fishoilDha = 1460
fishoilEpa = 660
hmb = 1000
panthothenicAcid = 500
pqq = 10
rezV = 400
tyrosine = 500
ubiquinol = 100
vitex = 450
tribulus = 2250
vitamind = 400
creatine = 5000
rhodiolaRosea = 500

response = table.put_item(
   Item={
        'realm': realm,
        'timestamp': timestamp,
        'hmb': hmb,
        'aspirin': aspirin,
        'beta-alanine': betaAlanine,
        'fishoil(dha)': fishoilDha,
        'fishoil(epa)': fishoilEpa,
        'panthothenic-acid': panthothenicAcid,
        'pqq': pqq,
        'rez-v': rezV,
        'tyrosine': tyrosine,
        'ubiquinol': ubiquinol,
        'acetyl-carnitine': acetylCarnitine,
        'vitex': vitex,
        'tribulus': tribulus,
        'creatine': creatine,
        'vitaminD': vitamind,
        'rhodiola-rosea': rhodiolaRosea
        }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))