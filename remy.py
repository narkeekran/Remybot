import os
from slack_bolt import App
import praw



#login to reddit
PRAW = praw.Reddit(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    password=os.environ.get("PASSWORD"),
    user_agent=os.environ.get("USER_AGENT"),
    username=os.environ.get("USERNAME"),
)


# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.message("surprise me")
def request(message, say):
    sub=PRAW.random_subreddit(nsfw=1)    
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "www.reddit.com/r/" + sub.display_name + ">" },
            }
        ],
        text=f""
    )


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
