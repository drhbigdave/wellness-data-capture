#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 15:09:47 2018

@author: davidhagan
"""

import json, boto3, time, requests

def lambda_handler(event, context):
  if event['offerCode'] == 'AmazonEC2':
    offer = download_offer(event)
    prices = extract_prices(offer)
    upload_prices(prices)

def download_offer(event):
  response = requests.get(event['url']['json'])
  return json.loads(response.text)

def filter_products(products):
  filtered = []

  # Only interested in shared tenancy, linux instances
  for sku, product in products:
    a = product['attributes']
    if not ('locationType' in a and
            'location' in a and
            'tenancy' in a and
            a['tenancy'] == "Shared" and
            a['locationType'] == 'AWS Region' and
            a['operatingSystem'] == 'Linux'):
      continue

    a['sku'] = sku
    filtered.append(a)

  return filtered

def extract_prices(offer):
  terms = offer['terms']
  products = offer['products'].items()

  instances = {}
  for a in filter_products(products):
    term = terms['OnDemand'][a['sku']].items()[0][1]
    cost = [float(term['priceDimensions'].items()[0][1]['pricePerUnit']['USD'])]

    info = {"type" : a['instanceType'], "vcpu" : a['vcpu'], 
            "memory" : a['memory'].split(" ")[0], "cost" : cost}

    if not a['location'] in instances:
      instances[a['location']] = []

    instances[a['location']].append(info)

  return {'created': time.strftime("%c"), 'published': offer['publicationDate'], 
          'instances': instances}

def upload_prices(prices):
  s3 = boto3.client('s3')
  s3.put_object(ACL='public-read', Body=json.dumps(prices), ContentType='application/json', 
                Bucket='<bucket-name>', Key='prices.json')