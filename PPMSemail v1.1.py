#PPMSemail
#v1.1 Sept 2017
#Python 2.7 (2016)
#Author : Christopher Hall, Wellcome Trust Sanger Institute, christopher.hall@sanger.ac.uk
#License : GPLv3 https://www.gnu.org/licenses/gpl-3.0.html

#This script emails the last user of each instrument using data obtained form the PPMS calendar

#Version 1.1 changes:
#  does not merge with the tabulated user list as Stratocore have included user email addresses in our custom report
#  corrected error in weekday line.  '4' changed to 4   

#import dependencies
import pandas as pd
import datetime as dt
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import os

#set 'working directory' to help windows task scheduler.  This is where the script is saved
os.chdir('C:/Users/Operator/Desktop')

#Prepare file, asertain todays date and choose out of office time.  (We close at 30 mins earlier on Friday(4))
csvfile=("outputfile.csv")
date=dt.datetime.today().strftime("%Y-%m-%d")
weekday = dt.datetime.today().weekday()
if weekday == 4:
    endtime = '16:30:00'
else:
    endtime = '17:00:00'

#Read the booking schedule, sort todays and just keep the last booking for each instrument
df = pd.read_csv(csvfile)
dp = df[df['Start date'] == date]
dk = dp[dp['End time'] > endtime]
dk = dk.sort_values(by='End time')
dk = dk.drop_duplicates(subset='System', keep='last', inplace=False)

#Creates and sends an email using smtplib
analysers = ('Cytoflex','BD Fortessa 1','BD Fortessa 2','BDLSRII','CL2 Sony 1','CL2 Sony 2') #this line indicates which instruments to incluse in the email.
for index, row in dk.iterrows():
    username,instrument,emailadress = row['User name'], row['System'], row['User Email']
    if any(s in instrument for s in analysers): 
        username = username.split()[-1]
        message = "Dear "+username+"\n\nOur records show that you are the last user of "+instrument+" today.  Please remember to turn it off after use.\n\nKind regards\n\nThe Cytometry Core Facility\n\n\n\nDO NOT REPLY:This email address is not monitored."
        
        fromaddr = "" #put your sending email here
        toaddr = emailadress
        cc= "" #put your cc email here 
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Cc'] = cc
        msg['Subject'] = "Automated last user reminder"
         
        body = message
        msg.attach(MIMEText(body, 'plain'))
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "") #put your email password here
        text = msg.as_string()
        server.sendmail(fromaddr, [toaddr,cc], text)
        server.quit()
