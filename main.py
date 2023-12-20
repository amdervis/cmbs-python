# Install and import request module 
import requests
import getpass

api_login = "https://pythontest2021.azurewebsites.net/api/Login"
api_mfa = "https://pythontest2021.azurewebsites.net/api/Get2FACode"


user = str(input("Enter your username: "))
pwd = getpass.getpass("Enter your password: ")
data = {"username": user, "password": pwd, "code": "string"}

res = requests.post(api_login, json=data)
#print(res.json())

# Check if the request was successful (status code 200)
if res.status_code == 200:
    # Parse the JSON content of the response
    data = res.json()
    print(data)

    if data["success"] and data["is2FAEnabled"] == False:
        print("Token: %s" % data["token"])

elif res.status_code == 404:
    print("Username or password is incorrect. Exiting.")
    exit()

