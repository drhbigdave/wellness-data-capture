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

realm = 'supplements'
#currentTime = datetime.today()
#timestamp = str(currentTime)
timestamp = '2017-05-26 17:34:55.647274'
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
        'vitex': vitex
        }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))