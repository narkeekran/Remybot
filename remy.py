import os
import time
from slackclient import SlackClient
import praw
import re
import random

#set remy's bot id and API id as a variable

SLACK_BOT_TOKEN = "tokenhoooo"
BOT_ID = "U22EWBJA0"
PRAW = praw.Reddit(user_agent='Remy by /u/narkeekran')

#string match for @'ing remy
AT_BOT = "<@" + BOT_ID + ">"

#inststantiate slack token 
slack_client = SlackClient(SLACK_BOT_TOKEN) 


READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading


if __name__ == "__main__":
	if slack_client.rtm_connect():
		slack_client.api_call("chat.postMessage", channel="#nsfwtest", text="TITTIES TIME", as_user=True )
		print("Remy is connected and running!")
		while True:
		#get read from slack	
			output = slack_client.rtm_read()
			print(output)
			for evt in output:
				if "type" in evt:
					if evt["type"] == "message" and "text" in evt:
					#if type == message save the actual message and the channel as variables
						message=evt["text"]
						if message.find(AT_BOT) != -1:
							#print(message)
							channel=evt["channel"]
							user_id=evt['user']
							lower_message=message.lower()
							if (lower_message.find("hello") != -1) or (lower_message.find("hi") != -1):
								slack_client.rtm_send_message(channel, "Hello <@{}> ;)".format(user_id))
							if lower_message.find("/r/") != -1:
								subreddit = re.findall('\/r\/\w+',lower_message)
								sub = re.findall('\w+',subreddit[0])
								#print(subreddit)
								#print(sub[1])
								#print(lower_message)
								top=random.randint(1,25)
								submissions = PRAW.get_subreddit(sub[1]).get_top(limit=top)
								for item in submissions:
									#print(item.url)
									link=item.url
								slack_client.rtm_send_message(channel, "<@{}>".format(user_id))
								slack_client.api_call("chat.postMessage", channel=channel, text=link, as_user=True, unfurl_media=True) 
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed, invalid token?")



	
