# PPMSemail
Python script to email the last user of the day if they are operating outside office hours using data from PPMS (www.stratocore.com)

## Instructions
1: Download the user list from 'Grous/Users' in PPMS

2: Create a batch file that downloads the booking data

3: Change:
        line 23, the directory of the .py
        
        line 26, the name of the booking file
        
        line 29-32, choose your 'out of office' times
        
        line 47, list the instruments that you want to set up the email for
        
        line 52, adjust the message to suit
        
        line 54 & 56, your email address(es)
        
        line 66, your email provider and their port number
        
        line 68, your email password
        
4: Use task scheduler, or equivalent, to automate 2 and 3

## Notes
We use cURL to download the booking information from a custom PPMS report (contact Startocore for information).
  curl -k -d "action=Report19&startDate=2017-08-01&endDate=2018-08-01&dateformat=print&outformat=csv&apikey=xxx&coreid=1" "https://ppms.eu/yoursite/API2/" > C:\Users\Operator\Desktop\outputfile.csv

I'll probably include this step in the python script in the future and just download todays bookings (similar to PPMS2CSV).

To run the file in Windows through task scheduler; create a batch file containing something along the lines of:
  c:\Python27\python.exe C:\Users\Operator\Desktop\PPMSemail.py
