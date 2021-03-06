from __future__ import print_function # Python 2/3 compatibility
import boto3
import decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

table = dynamodb.Table('wellness')

#is the timestamp current or historical
currentOrNot = input('are you inputting historical or\
 current data? provide "c" for current, "h" for a noncurrent entry:  ')
if currentOrNot is 'c':
    timestampInput = str(datetime.today())
else:
    timestampInput = str(input('provide the time for the data\
     input - \'year-month-day hour:min:sec\' example: \'2017-05-27 13:06:01:    '))

#choose the realm for the put
chooseRealm = input('Will you be capturing - measurements - \
    supplements - pain - or 5:2fast? provide "m" , "s" "p" or "f" or leave \
    this blank to create a new realm:   ')
if chooseRealm is 'm':
    realmInput = 'measurements'
elif chooseRealm is 's':
    realmInput = 'supplements'
elif chooseRealm is 'p':
    realmInput = 'pain'
else:
    realmInput = str(input('if you want to create a new realm type it here\
    in lowercase letters:   '))

#put required hash data from input into dict
required_hash_data = {
    'realm': realmInput,
    'timestamp': timestampInput
}

#capture key value data and put in dict, flow tbd
measurement_capture = {}
fat_input = (input('what fat % did the tanita scale indicate\
 (taken to 1 decimal place)? '))
measurement_capture['fat'] = decimal.Decimal(fat_input)

hydration_input = (input('what hydration value did the tanita scale \
    indicate (taken to 1 decimal place)? '))
measurement_capture['hydration'] = decimal.Decimal(hydration_input)

notes_input = input('are there any notes you\'d like to capture? ')
measurement_capture['notes'] = notes_input

waist_input = input('in inches, what was your waist measurement \
    (taken to 1 decimal place)? ')
measurement_capture['waist'] = decimal.Decimal(waist_input)

weight_input = input('in lbs, what weight did the tanita scale \
    indicate (taken to 1 decimal place)? ')
measurement_capture['weight'] = decimal.Decimal(weight_input)

rtgrip_input = input('in lbs, what was your right grip strength \
    measurment (taken to 1 decimal place)? ')
measurement_capture['right-grip'] = decimal.Decimal(rtgrip_input)

ltgrip_input = input('in lbs, what was your left grip strength \
    measurment (taken to 1 decimal place)? ')
measurement_capture['left-grip'] = decimal.Decimal(ltgrip_input)

ltcalf_input = input('in inches measure the left calf at its largest \
    point, to 1 decimal place   ')
measurement_capture['left-calf'] = decimal.Decimal(ltcalf_input)

rtcalf_input = input('in inches measure the right calf at its \
    largest point   ')
measurement_capture['right-calf'] = decimal.Decimal(rtcalf_input)

ltleg_input = input('in inches measure the left leg at its largest \
    point   ')
measurement_capture['left-leg'] = decimal.Decimal(ltleg_input)

rtleg_input = input('in inches measure the right leg at its \
    largest point   ')
measurement_capture['right-leg'] = decimal.Decimal(ltleg_input)

#combine dicts
final_input_data = measurement_capture.copy()
final_input_data.update(required_hash_data)


#write to wellness table
with table.batch_writer() as batch:
    batch.put_item(final_input_data)

print("PutItem succeeded:")