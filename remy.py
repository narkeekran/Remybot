import os
import time
from slackclient import SlackClient
import praw
import re
import random


#version number
remy_version = "1.0"

#set remy's bot id and API id as a variable

SLACK_BOT_TOKEN = "TOKEN-HOOOO"
BOT_ID = "ID"
PRAW = praw.Reddit(user_agent='Remy by /u/narkeekran')

#string match for @'ing remy
AT_BOT = "<@" + BOT_ID + ">"

#inststantiate slack token
slack_client = SlackClient(SLACK_BOT_TOKEN)

#help messege
help_message =  ">>>I get images (mostly porn) from reddit! Try the following: \n */r/$subreddit* _for a random post from the top 50_ \n  *surprise me* _for a random image from a random NSFW subreddit_ \n"

#Setting read delay
READ_WEBSOCKET_DELAY = 1



def help(channel, user_id):
	slack_client.api_call("chat.postMessage", channel=channel, text=help_message.format(user_id), as_user=True, unfurl_media=True)

def version(channel, user_id):
	slack_client.api_call("chat.postMessage", channel=channel, text="Hi I'm currently running version: " + remy_version.format(user_id), as_user=True, unfurl_media=True)

def surprise_me(channel, user_id):
	top=random.randint(1,100)
	submissions = PRAW.get_subreddit("randnsfw").get_top(limit=top)
	for item in submissions:
		link=item.url
		title=item.title
		subname=item.subreddit
	slack_client.rtm_send_message(channel, "<@{}>".format(user_id))
	slack_client.api_call("chat.postMessage", channel=channel, text='<https://www.reddit.com/r/' + str(subname) + '| /r/' + str(subname) + '>', as_user=True)
	slack_client.api_call("chat.postMessage", channel=channel, text='<' + link + '|' + title +'>', as_user=True, unfurl_media=True)

def nsfwsuboftheday():
	subname =""
	subname = PRAW.get_subreddit('randnsfw')
	print(subname)

def top_post(channel, user_id, lower_message):
	subreddit = re.findall('\/r\/\w+',lower_message)
	sub = re.findall('\w+',subreddit[0])
	link="" # set the link variable to nothing, this is so Remy can error out when a subreddit exists but doesn't give back links
	try:
		top=random.randint(1,100)
		submissions = PRAW.get_subreddit(sub[1]).get_top(limit=top)
		for item in submissions:
			link=item.url
			title=item.title
		if link:
			slack_client.rtm_send_message(channel, "<@{}>".format(user_id))
			slack_client.api_call("chat.postMessage", channel=channel, text='<' + link + '|' + title +'>', as_user=True, unfurl_media=True)
		else:
			print("nothing here")
			slack_client.api_call("chat.postMessage", channel=channel, text="There's nothing there", as_user=True, unfurl_media=True)

	except (praw.errors.InvalidSubreddit, praw.errors.Forbidden, praw.errors.NotFound):
		slack_client.api_call("chat.postMessage", channel=channel, text="WTF subreddit is that?", as_user=True, unfurl_media=True)


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
							channel=evt["channel"]
							user_id=evt['user']
							lower_message=message.lower()
							if (lower_message.find("hello") != -1) or (lower_message.find("hi") != -1):
								slack_client.rtm_send_message(channel, "Hello <@{}> ;)".format(user_id))
							if lower_message.find("/r/") != -1:
								top_post(channel, user_id, lower_message)
							if lower_message.find("surprise me") != -1:
								surprise_me(channel, user_id)
							if (lower_message.find("help") != -1) or (lower_message.find("halp") != -1) or (lower_message.find("i'm dumb") != -1):
								help(channel, user_id)
							if lower_message.find("version") != -1:
								version(channel, user_id)

			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed, invalid token?")
