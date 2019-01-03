from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from datetime import datetime

# Helper class to convert a DynamoDB item to JSON.
#class DecimalEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, decimal.Decimal):
#            if o % 1 > 0:
#                return float(o)
#            else:
#                return int(o)
#        return super(DecimalEncoder, self).default(o)

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
fishoilDha = 1100
fishoilEpa = 220
hmb = 3000
panthothenicAcid = 500
pqq = 10
rezV = 200
ubiquinol = 100
greenTeaExtractECGC = 200
greenTeaExtractCatechins = 320
koreanGinseng = 600
tribulus = 1500
bcaa = 1650
tyrosine = 500
eliteprominerals = 3
creatine = 5000
garlic = 1500
vitaminD = 1600
msm = 2000
potassium = 200
huperzineA = 100
theanine = 100
vitaminE = 400
Bcomplex = 1400
tongkatali = 80
niacin = 100
curcumin = 500
liver = 4500

'''
area for unused variables until i find a better way:
        'potassium': potassium,
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
        'eliteprominerals': eliteprominerals,
        'panthothenic-acid': panthothenicAcid,
        'garlic' : garlic,
        'huperzineA': huperzineA
        'rez-v': rezV,
        'hmb': hmb,
        'msm': msm,   
        'creatine' : creatine,
        'aspirin': aspirin,
        'beta-alanine': betaAlanine,    
        'pqq': pqq,
        'ubiquinol': ubiquinol,
        'curcumin': curcumin,
        'tongkat-ali': tongkatali,
        'fishoil(dha)': fishoilDha,
        'fishoil(epa)': fishoilEpa,
                'garlic' : garlic,
                        'curcumin': curcumin,
'''

response = table.put_item(
   Item={
        'realm': realm,
        'timestamp': timestamp,
        'vitaminD' : vitaminD,
        'msm': msm,   
        'creatine' : creatine,
        'aspirin': aspirin,
        'beta-alanine': betaAlanine,    
        'pqq': pqq,
        'ubiquinol': ubiquinol,
        'panthothenic-acid': panthothenicAcid,
        'niacin': niacin,
        'tyrosine': tyrosine,
        'acetyl-carnitine': acetylCarnitine,
        'fishoil(dha)': fishoilDha,
        'fishoil(epa)': fishoilEpa,
        'liver': liver,
        'curcumin': curcumin
        }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))