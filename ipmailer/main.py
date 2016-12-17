#!/usr/bin/env python3

__author__ = "Dominik Rimpf"
__credits__ = "Cody Giles"
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "1.1"
__maintainer__ = "Dominik Rimpf"
__email__ = "dev@d-rimpf.de"
__status__ = "Production"

import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime
import socket

def connect_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type

# Change to your own account information
# Account Information
to = 'raspi@d-rimpf.de' # Email to send to.
sender = 'raspi2@d-rimpf.de' # Email to send from.
mail_user = 'raspi@d-rimpf.de' # Email to send from.
mail_password = 'z4zp6Q6_EzwjjoH_NHzU' # mail password.
smtpserver = smtplib.SMTP('sslout.df.eu', 25) # Server to use.

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(mail_user, mail_password)  # Log in to server
today = datetime.date.today()  # Get current time/date

arg='ip route list'  # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE,universal_newlines=True)
data = p.communicate()  # Get data from 'p terminal'.

# Split IP text block into three, and divide the two containing IPs into words.
ip_lines = data[0].splitlines()
split_line = ip_lines[1].split()

# con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
ip_type = connect_type(split_line)

"""Because the text 'src' is always followed by an ip address,
we can use the 'index' function to find 'src' and add one to
get the index position of our ip.
"""
ipaddr = split_line[split_line.index('src')+1]

# Creates a sentence for each ip address.
my_ip = 'Your %s ip is %s' % (ip_type, ipaddr)
hostname = socket.gethostname()

# Creates the text, subject, 'from', and 'to' of the message.
msg = MIMEText(my_ip)
msg['Subject'] = 'IP for %s on %s' % (hostname, today.strftime('%d %b %Y'))
msg['From'] = sender
msg['To'] = to
# Sends the message
smtpserver.sendmail(mail_user, [to], msg.as_string())
# Closes the smtp server.
smtpserver.quit()
