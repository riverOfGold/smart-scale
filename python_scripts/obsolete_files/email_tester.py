#!/usr/bin/env/python3

# Two parts to this script:
     # FIRST: get the ip address of the pi
     # SECOND: send an email to kirk.mcmillan@griegseafood.com containing that ip address

# PART 1
import subprocess
try:
    host_ip = subprocess.getoutput("hostname -I")
except:
    host_ip = "problem connecting, no IP available."

# PART 2
import smtplib
#start talking to the SMTP server for GMAIL
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.ehlo()

#now login as my gmail user
username='pihatchery19@gmail.com'
password='23rdbday'
s.login(username, password)

# the email objects
replyto='pihatchery19@gmail.com'
sendto='kirk.mcmillan@griegseafood.com'
sendtoshow='kirk.mcmillan@griegseafood.com'
subject=host_ip #subject line
content='The IP address is '+host_ip #content
#compose the email. should probably use the email python module
mailtext='From: '+replyto+'\nTo: '+sendtoshow+'\nSubject: '+subject+'\n'+content
#send the email
s.sendmail(replyto, sendto, mailtext)
#we're done
rslt=s.quit()
#print the result
