# cleanup-gmail
Python script to mark certain older messages as read in gmail

## Credit
This is modified from [Devansh07](https://auth.geeksforgeeks.org/user/devansh07)'s GeeksforGeeks article
[How to read Emails from Gmail using Gmail API in Python](https://www.geeksforgeeks.org/how-to-read-emails-from-gmail-using-gmail-api-in-python/).

## Preliminaries
 1. Create a Google Cloud account if you don't have one
 2. Create a project for (your version of) this app and generate credentials for it, following the instructions in [Devansh07's article](https://www.geeksforgeeks.org/how-to-read-emails-from-gmail-using-gmail-api-in-python/).  In addition to what's described there, you will need to allow write access with one of the OAuth scopes `https://mail.google.com/` or 
`https://www.googleapis.com/auth/gmail.modify`.
 3. Save the application secrets JSON file as `client_secret.json`

## Configuration
There are two important global variables defined near the top of the file:

```python
### USER CONFIGURATION ###
REALLY_DO_IT=False
SEARCH_STRING='older:1/7/2023 -label:IMPORTANT is:unread -is:starred'
```
`SEARCH_STRING` is a GMail search string (the `q` parameter for [`users.messages.list`](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list#query-parameters)) indicating the set of messages to mark as unread.

`REALLY_DO_IT` is a flag.  If set to `False`, the script will run its queries and enumerate the messages to mark, but not actually change them.  If set to `True`, the script will do its thing.

## Warning
This script is meant as a starting point for developers, and it does not have the niceties or quality assurance expected for end-user software.  You need to understand the code and modify it to suit your needs before granting it access to your mailbox and running it.

This script is not interactive, there are no command-line options, and there are minimal warnings.  If it is bug-free, it will do what the preceding configuration variables tell it to, as soon as you run it.  If there are errors, it will do whatever it feels like, and do so with full write access to your gmail account. **UNDERSTAND THE CODE** before giving it access to your account and running it.
