# simple-mail-heartbeat.py - v1
#
# This will send a simple email and text message if a server cannot be pinged
# You will have to update the database yourself, as well as antyhing in this script
# to get it to work correctly in your environment
#
# The purpose of this script was to make a heartbeat, so you would know if a server
# went down over the weekend; can also be used to determine if you have lost internet
# access at all
#
# You will have to create your own Task Scheduler (or cronjob) to start the script
import json, subprocess, time, os;
from datetime import datetime;
import smtplib, ssl;
from email.message import EmailMessage;
import os;

#-------------------------------------------------------------------------------

class email(object):

    def __init__(self, sender, receiver, password, text_message):
        self.sender = sender;
        self.receiver = receiver;
        self.password = password;
        self.port = 465; # Change this
        self.text = False;
        self.text_message = text_message;

    def build(self, message, setting):
        msg = EmailMessage();
        msg.set_content(message);
        if setting:
            msg['Subject'] = "[HEARTBEAT - GOOD] - Servers alive!";
        else:
            self.text = True;
            msg['Subject'] = "[HEARTBEAT - BAD] - Servers down!";
        msg['From'] = self.sender;
        msg['To'] = self.receiver;
        return msg;

    def send(self, message, setting):
        smtpServer = "smtp.gmail.com"; # Change this to your SMTP server
        with smtplib.SMTP_SSL(smtpServer, self.port, context=ssl.create_default_context()) as server:
            server.login(self.sender, self.password);
            msg = self.build(message, setting);
            if (self.text and self.text_message) or (self.text_message == False):
                server.sendmail(self.sender, self.receiver, msg.as_string());

#-------------------------------------------------------------------------------

def main(e_list, sender, password, database, message=[], text_message=False):
    setting = True;

    with open(database, "r") as db:
        db = json.load(db)
        for e in db:
            ip = db[e]["ip"];
            name = db[e]["name"];
            # Checks on Windows; has to be updated for Linux
            output = subprocess.Popen(["ping.exe", ip, "-n", "1"], stdout = subprocess.PIPE).communicate()[0]
            if b"unreachable" in output or b"timed out" in output or b"could not find host" in output:
               message.append("{0} is NOT reachable, {1} is down as of {2}!".format(ip, name, datetime.now()))
               setting = False;
    # If the message variable still does not exist
    if not message:
        message.append("Heartbeat true - all devices responding to heartbeats.")
    # If the message variable exists
    if message:
        msg = "\n".join(message)
        for person in e_list:
            email(sender, person, password, text_message).send(msg, setting)

#-------------------------------------------------------------------------------
mailing_list = ["administrator@example.com"]; # Put in email targets here
text_list    = ["1234567890@phone.handler"]; # If you know the SMS targets, you can put them in here
sender_email = "service.account@example.com"; # The Service account that will be used to activate the script
sender_pass  = "password";
database     = r"C:\path\to\database.js";
current_time = datetime.now();
if 4 < current_time.weekday(): # Monday is 0, Sunday is 6
    main(e_list=mailing_list, sender=sender_email, password=sender_pass, database=database, text_message=False); # Sends email
    main(e_list=text_list, sender=sender_email, password=sender_pass, database=database, text_message=True); # Sends texts
elif not 8 < current_time.hour < 16: # Will not during work hours - 8AM - 4PM
    main(e_list=mailing_list, sender=sender_email, password=sender_pass, database=database, text_message=False); # Sends email
    main(e_list=text_list, sender=sender_email, password=sender_pass, database=database, text_message=True); # Sends texts
