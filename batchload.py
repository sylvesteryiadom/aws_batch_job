import boto3
session = boto3.session.Session(region_name='us-east-1')
dynamodb = session.resource('dynamodb')

table = dynamodb.Table("batch_table")

content = "x" * 100

for i in range(10):
    for j in range(10):
        print(i, j)
        table.put_item(Item={'primk': i, 'seck': j, 'Content': {"S": content}})

print("Upload complete..")