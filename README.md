# RssReminders
This python application uses a gmail robot to send an email reminder whenever a new tv episode appears on rss-feeds from https://showrss.info/

The target environment when I made this was my Raspberry pi 2 model B running raspbian 8.

How to
------
Step 1. Create a gmail account and add the account info to the file "Settings.txt" (RobotGmailUsername and RobotGmailPassword). This account will send out email notifications.

Step 2. Add your own email in the file "Settings.txt" (AdminEmail)
    This email adress will receive potential error messages and such.
    
Step 3. Add some tv shows to the file "RSSFeedUrls.txt" where each line in the file is a tv show. The left value is the tv show title and the right value is the public rss feed to the show from https://showrss.info/
    The left value can be whatever you'd like it to be, but beware of illegal characters since it will be used as the name of the txt database file that stores all of the rss links you've already been reminded of once before.
    
Step 4. Add one or more subscriber email adresses in the "Subscribers.txt" file.

Step 5. Set up a cronjob or scheduled task that runs "RSSReminders.py".

___

Please send me a message if you have any questions/feedback or would like to contribute :)
