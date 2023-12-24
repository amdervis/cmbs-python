import requests
import getpass

API_LOGIN = "https://pythontest2021.azurewebsites.net/api/Login"
API_MFA = "https://pythontest2021.azurewebsites.net/api/Get2FACode"

def user_input(prompt):
    return input(prompt).strip()

def login(username, password):
    login_data = {"username": username, "password": password}
    response = requests.post(API_LOGIN, json=login_data)

    if response.status_code == 404:
        print("Entered user does not exist or the password is incorrect.")
        exit()
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"Error during login: {response.status_code}")
        exit()

def handle_2fa(username, password):
    mfa_data = {"username": username, "password": password}
    response = requests.post(API_MFA, json=mfa_data)
    
    if response.status_code != 200:
        print(f"Error during 2FA request: {response.status_code}")
        exit()

    print("2FA is enabled.\nReceived Token:", response.text)
    token_input = user_input("Enter your token: ")

    token_auth_data = {"username": username, "password": password, "code": token_input}
    response = requests.post(API_LOGIN, json=token_auth_data)

    if response.status_code != 200:
        print("-" * 47)
        print("Token auth FAILED!")
        print("-" * 47)
    else:
        print("-" * 47)
        print("Token auth OK! \nYour token:", response.json()["token"])
        print("-" * 47)

if __name__ == "__main__":
    username = user_input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    login_result = login(username, password)

    if login_result["success"] and not login_result["is2FAEnabled"]:
        print("2FA for this account is not enabled.\nToken:", login_result["token"])
    elif login_result["success"] and login_result["is2FAEnabled"]:
        handle_2fa(username, password)
