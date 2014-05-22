#!/usr/bin/python
"""An alternative method is to get the token with this and set it with the web form."""

import getpass
import urllib
import urllib2

print('Enter the username of the reddit account.')
username = raw_input('--> ')

print('Enter the password of the reddit account.')
password = getpass.getpass('--> ')

payload = urllib.urlencode({
    'api_type': 'json',
    'user': username,
    'passwd': password,
})
req = urllib2.Request('https://ssl.reddit.com/api/login', payload)
req.add_header('User-Agent', 'reddit-grammar-bot login script')
response = urllib2.urlopen(req)
print(response.read())
