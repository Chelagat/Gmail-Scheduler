Gmail Script 
By Norah Borus and Nick Negrete


Overview:
Our program automates sending email for Gmail users. This script will 
log into your email and send a message at a specified time. This is a console based program that 
takes in the recipient's email, the message body, the title, and the time the email should be 
sent. The message body can be entered through the console or can be loaded from a text file. 
The sending time must be entered in military time, e.g., 15:20 for 3:20 p.m. Currently, the 
program cannot be run as a background process. 


Motivation:
The motivation for this program was to save the embarrassment of sending an email at 3 a.m. 
Specifically, Nick needed to send an important email, but he didn't want to wake up early or 
send it really late at night, since it would look weird that he was up so late. So, he wondered 
how Python could help make his life easier. (Ultimately he just send the email at 3 a.m.) So, he and 
Norah decided to create a script that would log into someone's personal email and send a message at 
a specific time for their final project. 

Implementation:
The Gmail APIs allowed us to grant this program access to my email using 
get_credential. Then, we could send an email via a background process and using a method from https://developers.google.com/gmail/api/guides/sending. 
After implementing the basic sending mechanism, we loop until the time the user entered (proper credit to Artsiom 
Rudzenka of Stack Overflow), at which point we trigger the sending mechanism. 

Instructions:
You need to set up a project on the Google Developers Console and store the client secret of the project on your local machine, so as to give the program access to your Gmail account. See https://developers.google.com/gmail/api/quickstart/python for details.


Future Improvements:

In the future, we hope to implement scheduling for the following day. Will also allow a user to send multiple distint emails during the execution of the program.
