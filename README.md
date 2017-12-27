# app_vault
Store Secrets on a Security Way.

 - The secrets are stored on the AWS Dynamodb encrypted. 
 - It's used the AWS KMS solution to manage the encryption key and the encryption algoritm.
 - The user is authenticated using AWS IAM solution and the API Gateway Token.
