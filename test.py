import boto3

ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='/TEST/CICD/OPEN_API_KEY', WithDecryption=True)
print(parameter['Parameter']['Value'])