import requests
import stdiomask
import datetime
import json
import pprint
from tabulate import tabulate
import creds
import colorama
from colorama import Fore,Style,Back

colorama.init(autoreset=False)
# Variables
session_token = ''
apiURL = creds.apiURL # API URL here
mods = {
    "auth":"sessions/",
    "proj":"projects/",
    "aUsers":"app-users/",
    "user":"users/",
    "assign":"assignments/"
}


# Authentication Function
def authenticate():
    subData = json.dumps({"email": creds.logEmail, "password": creds.logPass})
    headers = {'Content-Type': 'application/json'}
    req = requests.post(apiURL+mods['auth'], data=subData, headers=headers)
    if req.ok == True:
        print(Fore.YELLOW + "Authentication complete" + Style.RESET_ALL)
        return req.json()['token']
    else:
        req.json()

# List Users Function
def list_users(token):
    token_text = f"Bearer {token}"
    headers = {'Authorization': token_text}
    req = requests.get(apiURL+mods['user'], headers=headers)
    if req.ok == True:
        usr_list = []
        usrCounter = 0
        for user in req.json():
            a_user = {}
            a_user['count'] = usrCounter
            a_user['ActorID'] = user['id']
            a_user['name'] = user['displayName']
            a_user['email'] = user['email']
            a_user['type'] = user['type']
            a_user['createdAt'] = user['createdAt']
            usr_list.append(a_user)
            usrCounter+=1
        print(Fore.BLUE)
        print(tabulate(usr_list, headers="keys"))
        print(Style.RESET_ALL)

# Get email of selected actorID
def get_user_email(token,actorID):
    token_text = f"Bearer {token}"
    headers = {'Authorization': token_text}
    req = requests.get(apiURL+mods['user'], headers=headers)
    if req.ok == True:
        usr_list = []
        for user in req.json():
            if user['id'] == actorID:
                a_user = {}
                a_user['ActorID'] = user['id']
                a_user['name'] = user['displayName']
                a_user['email'] = user['email']
                a_user['type'] = user['type']
                a_user['createdAt'] = user['createdAt']
                usr_list.append(a_user)
                print(Fore.BLUE)
                print(tabulate(usr_list, headers="keys"))
                print(Style.RESET_ALL)
                return usr_list[0]['email']
    else:
        print(req.json())


def list_projects(token):
    token_text = f"Bearer {token}"
    headers = {'Authorization': token_text, 'X-Extended-Metadata': 'True'}
    req = requests.get(apiURL+mods['proj'], headers=headers)
    if req.ok == True:
        proj_list = []
        prjCount = 0
        for proj in req.json():
            a_proj = {}
            a_proj['id'] = proj['id']
            a_proj['name'] = proj['name']
            a_proj['archived'] = proj['archived']
            a_proj['forms'] = proj['forms']
            a_proj['appUsers'] = proj['appUsers']
            a_proj['lastSubmission'] = proj['lastSubmission']
            proj_list.append(a_proj)
            prjCount += 1
        print(Fore.BLUE)
        print(tabulate(proj_list, headers="keys"))
        print(Style.RESET_ALL)
    else:
        print(req.json())

# List all forms for specific project
def list_forms(token,projectID):
    token_text = f"Bearer {token}"
    headers = {'Authorization': token_text, 'X-Extended-Metadata': 'True'}
    req = requests.get(apiURL+mods['proj']+projectID+"/forms/", headers=headers)
    if req.ok == True:
        form_list = []
        frmCount = 0
        for form in req.json():
            a_form = {}
            a_form['id'] = form['xmlFormId']
            a_form['enketoId'] = form['enketoId']
            a_form['name'] = form['name']
            a_form['state'] = form['state']
            a_form['submissions'] = form['submissions']
            a_form['createdAt'] = form['createdAt']
            a_form['lastSubmission'] = form['lastSubmission']
            form_list.append(a_form)
            frmCount += 1
        print(Fore.BLUE)
        print(tabulate(form_list, headers="keys"))
        print(Style.RESET_ALL)
    else:
        print(req.url)
        print(req.json())

# Create New Project
def create_project(token,projName):
    if not projName:
        print(Fore.RED + "Error!\nYou have not supplied a name for this project" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    subData = json.dumps({"name": projName})
    req = requests.post(apiURL+mods['proj'], data=subData, headers=headers)
    if req.ok == True:
        print(req.json())
    else:
        print(req.json())

# Delete Project
def delete_project(token,projID):
    if not projID:
        print(Fore.RED + "Error!\nYou have not supplied a project to delete" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    req = requests.delete(apiURL+mods['proj']+projID, headers=headers)
    if req.ok == True:
        print(Fore.YELLOW +"Project successfully removed\n" + Style.RESET_ALL)
    else:
        print(req.json())

# Create a new User
def create_user(token,email,password,displayName="New User"):
    if not email:
        print(Fore.RED + "Error!\nYou did not supply an email for the user" + Style.RESET_ALL)
    if not password:
        print(Fore.RED + "Error!\nYou did not supply a password for the user" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    subData = json.dumps({"email": email, "password": password, "displayName": displayName})
    req = requests.post(apiURL+mods['user'], data=subData, headers=headers)
    if req.ok == False:
        print(req.url)
    pprint.pprint(req.json())


# Change user password
def change_password(token, actorID, oldPass, newPass):
    if not actorID:
        print(Fore.RED + "Error!\nYou have not supplied a user to update" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    subData = json.dumps({"old": oldPass, "new":newPass})
    req = requests.put(apiURL+mods['user']+str(actorID)+"/password", data=subData, headers=headers)
    print(req.url)
    if req.ok == True:
        print("Password changed\n")
    else:
        print(req.json())

# Initiate Password reset email
def send_password_reset_email(token,actorEmail,expireCurrent = False):
    if not actorEmail:
        print(Fore.RED + "Error!\nYou have not supplied an email address" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    subData = json.dumps({"email": actorEmail})
    req = requests.post(apiURL+mods['user']+"reset/initiate?invalidate={}".format(expireCurrent), data=subData, headers=headers)
    if req.ok == True:
        print("Password reset email sent\n")
    else:
        print(req.url)
        print(req.json())

def get_form_submissions(token,projectID,formID):
    if not projectID:
        print(Fore.RED + "Error!\nYou have not supplied a project ID" + Style.RESET_ALL)
    if not formID:
        print(Fore.RED + "Error!\nYou have not supplied a form ID" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'X-Extended-Metadata': 'true','Authorization': token_text}
    req = requests.get(apiURL+mods['proj']+projectID+"/forms/"+formID+"/submissions", headers=headers)
    if req.ok == False:
        print(Fore.YELLOW)
        print(req.url)
        print(req.json())
        print(Style.RESET_ALL)
    else:
        all_resp = []
        rspCount = 0
        for resp in req.json():
            a_resp = {}
            rspCount += 1
            a_resp['count'] = rspCount
            a_resp['deviceID'] = resp['deviceId']
            a_resp['instanceID'] = resp['instanceId']
            a_resp['submittedBy'] = resp['submitter']['displayName']
            a_resp['createdAt'] = resp['createdAt']
            all_resp.append(a_resp)
        print(Fore.BLUE)
        print(tabulate(all_resp, headers="keys"))
        print(Style.RESET_ALL)

# Export form submissions to excel
def get_form_submissions_excel(token,projectID,formID):
    if not projectID:
        print(Fore.RED + "Error!\nYou have not supplied a project ID" + Style.RESET_ALL)
    if not formID:
        print(Fore.RED + "Error!\nYou have not supplied a form ID" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'X-Extended-Metadata': 'true','Authorization': token_text}
    req = requests.get(apiURL+mods['proj']+projectID+"/forms/"+formID+"/submissions.csv.zip", headers=headers)
    if req.ok == True:
        currTime = datetime.datetime.now()
        file_name = f"{projectID}_{formID}-{currTime.strftime('%Y-%m-%d %H-%M-%S')}.csv.zip"
        with open(file_name, 'wb') as local_file:
            for chunk in req.iter_content(chunk_size=128):
                local_file.write(chunk)
        print(f"{file_name} saved successfully")
    else:
        print(req.json())

# Assign a site-wide role to existing user
def assign_role(token,actorID,roleID):
    if not actorID:
        print(Fore.RED + "Error!\nYou have not supplied a user ID" + Style.RESET_ALL)
    if not roleID:
        print(Fore.RED + "Error!\nYou have not supplied a role ID" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    req = requests.post(apiURL+mods['assign']+f"{roleID}/{actorID}", headers=headers)
    if req.ok == False:
        print(req.url)
    print(Fore.YELLOW)
    pprint.pprint(req.json())
    print(Style.RESET_ALL)

def list_roles(token):
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    req = requests.get(apiURL+"roles", headers=headers)
    if req.ok == True:
        all_roles = []
        roleCount = 0
        for roles in req.json():
            a_role = {}
            roleCount += 1
            a_role['count'] = roleCount
            a_role['id'] = roles['id']
            a_role['name'] = roles['name']
            a_role['system'] = roles['system']
            a_role['createdAt'] = roles['createdAt']
            all_roles.append(a_role)
        print(Fore.BLUE)
        print(tabulate(all_roles, headers="keys"))
        print(Style.RESET_ALL)

# Delete existing user
def delete_user(token,actorID):
    if not actorID:
        print(Fore.RED + "Error!\nYou have not supplied a user ID" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    req = requests.delete(apiURL+mods['user']+str(actorID), headers=headers)
    if req.ok == True:
        print(Fore.YELLOW + "User removed\n" + Style.RESET_ALL)
    else:
        print(req.url)
        print(req.json())

# Get form schema
def get_form_schema(token,projectID,formID):
    if not projectID:
        print(Fore.RED + "Error!\nYou have not supplied a project ID" + Style.RESET_ALL)
    if not formID:
        print(Fore.RED + "Error!\nYou have not supplied a form ID" + Style.RESET_ALL)
    token_text = f"Bearer {token}"
    headers = {'Content-Type': 'application/json','Authorization': token_text}
    req = requests.get(f"{apiURL}{mods['proj']}{projectID}/forms/{formID}/fields?odata=false", headers=headers)
    if req.ok == True:
        print(Fore.YELLOW)
        pprint.pprint(req.json())
        print(Style.RESET_ALL)
    else:
        print(Fore.RED)
        print(req.json())
        print(Style.RESET_ALL)


# Menu options 
def menu_op():
    menu = """
    option          Purpose
    ------          -----------------------------
      1             Authenticate with server
      2             List Users
      3             List Projects
      4             List Project Forms
      5             Create New User
      6             Create New Project
      7             Delete Existing User
      8             Delete Existing Project
      9             Change User Password
      10            Trigger User Password Reset
      11            Get Form Submissions
      12            Get Form Submissions (Excel)
      13            Assign User Role
      14            Get Form Schema

  * => Under development
"""
    # Present options to user
    print(Fore.GREEN + menu + Style.RESET_ALL)
    choice = input("Select an option:\t")
    if not choice:
        print(Fore.RED + "Error!\nYou did not select an option or your option is invalid" + Style.RESET_ALL)
        menu_op()
    else:
        choice = int(choice)

    global session_token
    # Check user selection and execute function calls
    if choice == 1:
        # Authenticate user credentials with server
        session_token = authenticate()
    elif choice == 2:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_users(session_token)
    elif choice == 3:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_projects(session_token)
    elif choice == 4:
        # list project forms
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_projects(session_token)
            print("o-"*50)
            pID = input("Provide project ID:\t")
            list_forms(session_token, pID)
    elif choice == 5:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            email = input("Provide user email:\t")
            pwd = input("Provide user password:\t")
            dispName = input("Provide user display name (Optional, Press enter to skip):\t")
            if not dispName:
                create_user(session_token, email, pwd)
            else:
                create_user(session_token, email, pwd, dispName)
            print("o-"*50)
            list_users(session_token)
    elif choice == 6:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            pname = input("Provide project Name:\t")
            create_project(session_token, pname)
    elif choice == 7:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_users(session_token)
            print("o-"*50)
            uID = int(input("Provide ActorID:\t"))
            delete_user(session_token,uID)
    elif choice == 8:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_projects(session_token)
            print("o-"*50)
            pID = input("Provide project ID:\t")
            delete_project(session_token, pID)
            print("o-"*50)
            list_projects(session_token)
    elif choice ==9:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            uID = int(input("Provide ActorID:\t"))
            oldPass = stdiomask.getpass(prompt="Users's current password:\t", mask="*")           
            newPass = stdiomask.getpass(prompt="New Password:\t", mask="*")
            print(f"Old: {type(oldPass)}")
            print(f"New: {type(newPass)}")
            change_password(session_token, uID, oldPass, newPass)
    elif choice==10:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_users(session_token)
            print("o-"*50)
            uID = int(input("Provide ActorID:\t"))
            selActorEmail = get_user_email(session_token,uID)
            print("o-"*50)
            if not selActorEmail:
                print(f"User with ActorID {uID} not found")
            else:
                send_password_reset_email(session_token, selActorEmail)
    elif choice == 11:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_projects(session_token)
            print("o-"*50)
            pID = input("Provide project ID:\t")
            list_forms(session_token,pID)
            print("o-"*50)
            fID = input("Provide form ID:\t")
            get_form_submissions(session_token,pID,fID)
    elif choice == 12:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_projects(session_token)
            print("o-"*50)
            pID = input("Provide project ID:\t")
            list_forms(session_token,pID)
            print("o-"*50)
            fID = input("Provide form ID:\t")
            get_form_submissions_excel(session_token,pID,fID)
    elif choice == 13:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_users(session_token)
            print("o-"*50)
            uID = input("Provide user ID:\t")
            list_roles(session_token)
            print("o-"*50)
            roleID = input("Provide role ID:\t")
            assign_role(session_token,uID,roleID)
    elif choice == 14:
        if not session_token:
            print(Fore.RED + "Error!\nYou will need to authenticate with server first." + Style.RESET_ALL)
        else:
            list_projects(session_token)
            print("o-"*50)
            pID = input("Provide project ID:\t")
            list_forms(session_token,pID)
            print("o-"*50)
            fID = input("Provide form ID:\t")
            get_form_schema(session_token,pID,fID)
    else:
        print(Fore.RED + "Error!\nYou did not select an option or your option is invalid" + Style.RESET_ALL)
    
    print("o-"*50)
    menu_op()

# main section of program
print("o-"*50)
menu_op()