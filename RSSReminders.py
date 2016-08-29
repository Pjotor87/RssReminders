#!/usr/bin/env python
import datetime
try:
    # For Python 3.0 and later
    import urllib.request as urllib2
except ImportError:
    # Fall back to Python 2's urllib2
    import urllib2
from bs4 import BeautifulSoup
import os
import sys
import RoboMail
import ApplicationSettings

def main():
    # Create a list of error messages.
    errorMessages = []
    try:
        # Ensure DB folder exists
        if not os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/DB"):
            os.makedirs(os.path.dirname(os.path.realpath(sys.argv[0]))+"/DB")
        # Get rss feeds from file
        rssFeedUrls = []
        with open(os.path.dirname(os.path.realpath(sys.argv[0]))+"/RSSFeedUrls.txt") as rssFeedUrlsFile:
            rssFeedUrls = [line.strip() for line in rssFeedUrlsFile]
        # Create a hash of all the new episodes to broadcast to the subscribers. Key: tv show, values: episode titles
        broadcastHash = {}
        # Loop through rss urls.
        for rssFeedUrl in rssFeedUrls:
            try:
                rssFeedMarkup = BeautifulSoup((str(urllib2.urlopen(urllib2.Request(rssFeedUrl.split('=')[1], headers={'User-Agent':"Magic Browser"})).read())), 'html.parser')
                # Get the content of all nodes in rss markup
                titles = []
                for item in rssFeedMarkup.find_all('item'):
                    title = item.findChild('title').get_text()
                    titles.append(title.encode('utf-8'))
                showTitle = rssFeedUrl.split('=')[0]
                # Ensure DB File for show
                dbFilePath = os.path.dirname(os.path.realpath(sys.argv[0]))+"/DB/"+showTitle+".txt"
                # Create the file if it doesn't exist
                open(dbFilePath, 'a').close()
                # Get a list of all new items by checking if the retrieved ones already exist in the database or not
                newTitles = []
                with open(dbFilePath, 'r') as tvShowDbFile:
                    dbEntries = [line.strip() for line in tvShowDbFile]
                    for episodeTitle in titles:
                        if episodeTitle not in dbEntries:
                            newTitles.append(episodeTitle)
                # Truncate and write the DB File
                with open(dbFilePath, 'w') as tvShowDbFile:
                    for title in titles:
                        tvShowDbFile.write("%s\n" % title)
                # Add new titles to broadcast hash
                if newTitles:
                    broadcastHash[showTitle] = newTitles
            except:
                errorMessages.append("***Error when checking show: " + showTitle + "*** " + str(sys.exc_info()[0]))
        if broadcastHash:
            # Get subscribers.
            subscribers = []
            with open(os.path.dirname(os.path.realpath(sys.argv[0]))+"/Subscribers.txt") as subscribersFile:
                subscribers = [line.strip() for line in subscribersFile]
            if subscribers:
                # Compile email message
                emailMsg = 'There are new tv show episodes available!<br /><br />'
                for key in broadcastHash:
                    emailMsg += "<b>" + key + "</b><br />"
                    for newEpisodeTitle in broadcastHash[key]:
                        emailMsg += newEpisodeTitle + "<br />"
                # Send emails to subscribers.
                for subscriber in subscribers:
                    try:
                        RoboMail.send_gmail_message_from_robot(subscriber, "Rss feed update", emailMsg, False, None)
                    except:
                        errorMessages.append("***Error when sending mail to subscriber: " + subscriber + " *** " + str(sys.exc_info()[0]))
    except:
        errorMessages.append("***Error when running rss reminders: *** " + str(sys.exc_info()[0]))
    # Send error messages email.
    if errorMessages:
        # Compile email message
        errorEmailMsg = "<b>Exceptions caught when running RSS Reminders:</b><br /><br />"
        for errorMessage in errorMessages:
            errorEmailMsg += errorMessage + "<br />"
            # Send email to admin.
            RoboMail.send_gmail_message_from_robot(ApplicationSettings.settings.Get("AdminEmail"), "Error report - RSS Reminders", errorEmailMsg, False, None)

main()
