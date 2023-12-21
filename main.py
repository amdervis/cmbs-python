# Install and import request module 
import requests
import getpass

api_login = "https://pythontest2021.azurewebsites.net/api/Login"
api_mfa = "https://pythontest2021.azurewebsites.net/api/Get2FACode"

user = str(input("Enter your username: "))
pwd = getpass.getpass("Enter your password: ")
login_data = {"username": user, "password": pwd}

res_login = requests.post(api_login, json=login_data)
res_login_json = res_login.json()

if res_login.status_code == 404: 
    print("Entered user does not exist or the password is incorrect.")
    exit()

elif res_login.status_code == 200:
    if res_login_json["success"] and res_login_json["is2FAEnabled"] == False:
        print("2FA for this account is not enabled. \nToken: %s" % res_login_json["token"])
        exit()
    
    elif res_login_json["success"] and res_login_json["is2FAEnabled"]:
        res_mfa = requests.post(api_mfa, json=login_data)
        res_mfa_body = res_mfa.content
        print("2FA is enabled.\nReceived Token: %s" % res_mfa_body)
        token_input = str(input("Enter your token: "))

        token_auth = requests.post(api_login, json={"username": user, "password": pwd, "code": str(token_input)}).json()
        if token_auth["success"]:
            print("-" * 47)
            print("Token auth OK! \nYour token: %s" % token_auth["token"])
            print("-" * 47)