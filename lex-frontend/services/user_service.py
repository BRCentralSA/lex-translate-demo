import boto3
import os

class UserService(object):
    def __init__(self):
        super().__init__()
        self.user_pool_id = os.getenv("USER_POOL_ID", "us-east-1_J4lq2g8gV")
        self.app_client_id = os.getenv("APP_CLIENT_ID", "7vjqg3lj1f5q3p6bk9c24jb5e1")

    def create_user(self, username, password, email):
        client = boto3.client("cognito-idp")

        try:
            # initial sign up
            resp = client.sign_up(
                ClientId=self.app_client_id,
                Username=username,
                Password=password,
                UserAttributes=[
                    {"Name": "email", "Value": email}
                ],
            )

            # then confirm signup
            confirm_resp = client.admin_confirm_sign_up(
                UserPoolId=self.user_pool_id, Username=username
            )
            print(f"[INFO] {resp}")
            password = None
            response = {"cognito_reponse": confirm_resp}
            return response
        except Exception as e:
            raise e
    
    def login(self, username, password):
        client = boto3.client("cognito-idp")
        try:
            resp = client.admin_initiate_auth(
                UserPoolId=self.user_pool_id,
                ClientId=self.app_client_id,
                AuthFlow="ADMIN_NO_SRP_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password
                },
            )
            print(f"INFO: {resp['AuthenticationResult']}")

            return resp["AuthenticationResult"]
        except Exception as e:
            raise e
    