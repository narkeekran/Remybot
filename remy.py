import os
import time
from slackclient import SlackClient
import praw


#set remy's bot id and API id as a variable

SLACK_BOT_TOKEN = "TOKEN-HOOO"
BOT_ID = "U22EWBJA0"
PRAW = praw.Reddit(user_agent='Remybot by /u/narkeekran')

#string match for @'ing remy
AT_BOT = "<@" + BOT_ID + ">"

#inststantiate slack token 
slack_client = SlackClient(SLACK_BOT_TOKEN) 







if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading
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
							print(message)
							channel=evt["channel"]
							user_id=evt['user']
							lower_message=message.lower()
							if (lower_message.find("hello") != -1) or (lower_message.find("hi") != -1):
								slack_client.rtm_send_message(channel, "Hello <@{}> ;)".format(user_id))
							if lower_message.find("boobs") != -1:

#								submissions = PRAW.get_subreddit('boobs').get_top(limit=25)
#								for item in submissions:
									
								slack_client.rtm_send_message(channel, "<@{}>".format(user_id))
								slack_client.api_call("chat.postMessage", channel=channel, text="http://i.imgur.com/JTOqbvG.jpg", as_user=True, unfurl_media=True) 
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed, invalid token?")



	
