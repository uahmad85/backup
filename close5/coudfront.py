import boto3
import json
import pprint


pp = pprint.PrettyPrinter(indent=2)

client = boto3.client('cloudfront')
#print client.list_distributions()
response = client.get_distribution(
        Id='E1E88YPNWHECOA'
)
pp.pprint(response)