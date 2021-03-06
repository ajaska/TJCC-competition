#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import sqlite3 as sql
import sys, os
from Cookie import SimpleCookie

print "Content-Type: text/html\n"
print "<html><body>"

form = cgi.FieldStorage()

id = int(form.getvalue('id'))
status = ''

cookie = SimpleCookie(os.environ['HTTP_COOKIE'])
if 'KOOKIE' in cookie:
    username = cookie['KOOKIE'].value.split('_')[0]
    with sql.connect('./database') as connection:
        d = connection.cursor()
    
        d.execute('SELECT votedFor FROM users WHERE username="%s"' % (username,))
        votedFor = eval(d.fetchone()[0])
        d.execute('SELECT stories FROM users WHERE username="%s"' % (username,))
        stories = eval(d.fetchone()[0])
        if id in votedFor:
            status = 'voted'
        elif id in stories:
            status = 'author'
        else:
            votedFor.append(id)
            d.execute('UPDATE users SET votedFor="%s" WHERE username="%s"' % (votedFor, username))
            d.execute('SELECT votes FROM stories WHERE id=%d' % (id,))
            votes = d.fetchone()[0]
            d.execute('UPDATE stories SET votes=%d WHERE id=%d' % (votes+1, id))
            status = 'success'
    
        connection.commit()
        d.close()
else:
    status='guest'

print '<meta http-equiv="REFRESH" content="0;browse.py?id=%d&status=%s">' % (id,status)
print "</body></html>"
