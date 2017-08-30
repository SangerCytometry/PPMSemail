#Copyright (c) 2017 Genome Research Ltd.

#PPMSemail
#v1.0 Sept 2017
#Python 2.7 (2016)
#Author : Christopher Hall, Wellcome Trust Sanger Institute, christopher.hall@sanger.ac.uk

#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

#This script emails the last user of each instrument using data obtained form the PPMS calendar

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
if weekday == '4':
    endtime = '16:30:00'
else:
    endtime = '17:00:00'

#Read the booking schedule, sort todays and just keep the last booking for each instrument
df = pd.read_csv(csvfile)
dp = df[df['Start date'] == date]
dk = dp[dp['End time'] > endtime]
dk = dk.sort_values(by='End time')
dk = dk.drop_duplicates(subset='System', keep='last', inplace=False)

#Import and merge the user list (this is from PPMS Users/Groups)
userlist=("tabulated-user-list.csv")
ul = pd.read_csv(userlist)
merged = dk.merge(ul, how='inner',left_on="User ID", right_on='id')

#Creates and sends an email using smtplib
analysers = ('Cytoflex','BD Fortessa 1','BD Fortessa 2','BDLSRII','CL2 Sony 1','CL2 Sony 2') #this line indicates which instruments to incluse in the email.
for index, row in merged.iterrows():
    username,instrument,emailadress = row['name'], row['System'], row['email']
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
