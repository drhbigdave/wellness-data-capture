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
fishoilDha = 3468
fishoilEpa = 660
hmb = 1500
panthothenicAcid = 500
pqq = 10
rezV = 400
ubiquinol = 100
greenTeaExtractECGC = 200
greenTeaExtractCatechins = 320
koreanGinseng = 600
tribulus = 2250
bcaa = 1650
tyrosine = 500
eliteprominerals = 3
creatine = 5000
garlic = 1000
vitaminD = 400
msm = 2000

'''
area for unused variables until i find a better way:
        'beta-alanine': betaAlanine,
        'greenTeaECGC': greenTeaExtractECGC,
        'greenTeaCatequins': greenTeaExtractCatechins,
        'tribulus': tribulus,
        'bcaa': bcaa,
        'korean-ginseng': koreanGinseng,
        'pqq': pqq,
        'ubiquinol': ubiquinol,
        'tyrosine': tyrosine,
        'acetyl-carnitine': acetylCarnitine,
        'vitaminD' : vitaminD
                'rez-v': rezV,
                'hmb': hmb,
                'msm': msm,    
'''

response = table.put_item(
   Item={
        'realm': realm,
        'timestamp': timestamp,
        'aspirin': aspirin,
        'fishoil(dha)': fishoilDha,
        'fishoil(epa)': fishoilEpa,
        'panthothenic-acid': panthothenicAcid,
        'beta-alanine': betaAlanine,
        'eliteprominerals': eliteprominerals,
        'creatine' : creatine,
        'garlic' : garlic,
        'pqq': pqq,
        'ubiquinol': ubiquinol,
        'vitaminD': vitaminD,
        'msm' : msm
        }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))