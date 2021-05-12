# An unOfficial CLI Client for ODK Central

### Table of Contents
* [What is this?](#what-is-this?)
* [What does it do?](#what-does-it-do?)
* [How does it work?](#how-does-it-work?)
* [How can I use it?](#how-can-i-use-it?)
* [Can I contribute?](#can-i-contribute?)
* [Who can I contact?](#who-can-i-contact?)

### What is this?
*unOffCentralMan* is a basic CLI tool to help perform some basic ODK Central tasks.

### What does it do?
Common tasks supported by *unOffCentralMan* are:
* Listing Users
* Listing Projects
* Listing Project Forms
* Creating Users
* Assigning User Roles
* Creating Projects
* Deleting Users
* Deleting Projects
* Changing User Password
* Triggering User Password Reset Email
* Getting Schema for Forms
* Getting Form Submissions
* Exporting Form Submissions to Excel(.csv)

### How does it work?
*unOffCentralMan* was written with python and as such will require a working instance of a Python 3 environment to function.
It mainly uses the [Requests](https://requests.readthedocs.io/en/master/) library and relies heavily on the API documentation for [ODK Central](https://odkcentral.docs.apiary.io/#reference)

## How can I use it?
To use the CLI Client, you can use the checklist below.
1. Ensure you have a working instance of Python 3. 
    - (**For Windows Users**) You can check this by launching Command prompt (**Windows Key + R**, type *cmd* and hit ENTER) then type `python -V` or `python --version`
    - (**For Linux Users**) Launch terminal (**Ctrl + Alt + T**, type *terminal* and hit ENTER) then type `python -V` or `python --version`
    - (**For Mac Users**) Launch terminal (**Cmd + Spacebar**, type *terminal* and hit RETURN) then type `python -V` or `python --version`
    - If you saw anything other than `Python 3.x.x` displayed after following the most relevant instruction above, then goto the [Python Website](https://www.python.org/downloads/) and get it installed.
2. Install the required packages
    - Launch Command Prompt or Terminal (*see point 1*)
    - Type `python -m pip install -r requirements.txt`
    - If you have multiple instances of python installed on your device:
        * Replace `python` in the command above with your preferred python3 instance. **eg** `python3.8 -m pip install -r requirements.txt`
3. Edit the **creds.py** file with the required details. An example is shown below:
```
logEmail = "sample@email.com"
logPass = "sampleSuperStrongPassword"
apiURL = "https://sampleDomain.com/v1/" # API URL here
```
4. Run the **odkCentralAPI_client.py** file in Command prompt or Terminal.


### Can I contribute?
If you're asking this, then you probably know more about this kinda thing than I do😁. I'd like to have a chat☺. Read on!👇👇

### Who can I contact?
You can reach out to 
* [@AnthonyAnkrah](https://github.com/AnthonyAnkrah) on Github
* or shoot me an email via ankrahtony@outlook.com