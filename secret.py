import boto3
from boto3.dynamodb.conditions import Key
import time
import hashlib
import json
from cryptothis import encrypt, decrypt

class secret():
 
 def __init__(self):
  self.dynamodb = boto3.resource('dynamodb')
  self.table = self.dynamodb.Table('SecretAPP')
  
 def get_hashid(self,event):
  return str(hashlib.sha256(str(event['pathParameters']['environment']+event['pathParameters']['application']+event['pathParameters']['type']+event['pathParameters']['data']).encode('utf-8')).hexdigest())
  
  
 def create(self,event):
   
   result = {}
   data = json.loads(event['body'])
   timestamp = int(time.time() * 1000)


   value = json.loads(event['body'])


   item = {
       'hashID': self.get_hashid(event),
       'environment':event['pathParameters']['environment'],
       'application': event['pathParameters']['application'],
       'type':event['pathParameters']['type'],
       'data':event['pathParameters']['data'],
       'value': encrypt(value['value']),
       'createdAt': timestamp,
       'updatedAt': timestamp
   }

   try:
       self.table.put_item(Item=item)
       result['status'] = 200
       result['message'] = "Criado com Sucesso"

   except Exception as e:
       result['status'] = 400
       result['message'] = "Erro ao criar: %s" % e
       pass


   return result
   
 def get(self,event):
  
  result = {}
  print(event)

  key = {
      'hashID': self.get_hashid(event)
      }
        
  try:
      item = self.table.get_item(Key=key)
      result['status'] = 200
      result['message'] = decrypt(item['Item']['value'].value)


  except Exception as e:
      result['status'] = 400
      result['message'] = "Erro ao obter: %s" % e
      pass


  return result
  
  
 def get_data_by_type(self,event):

  result = {}
  items=[]
  

        
  try:
      item = self.table.query(IndexName='application-index',KeyConditionExpression=Key('application').eq(event['pathParameters']['application']))
      result['status'] = 200

      for it in item['Items']:
       if event['pathParameters']['environment'] == it['environment']:
        items.append({'environment':it['environment'],'application':it['application'],'type':it['type'],'data':it['data']})
      result['message'] = {'items': items}
      


  except Exception as e:
      result['status'] = 400
      result['message'] = "Erro ao obter: %s" % e
      pass


  return result