import praw
import pdb
import re
import os


# Reddit instance
reddit = praw.Reddit('bot')

# Create a list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# Or load the list of posts we have replied to
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

subreddit = reddit.subreddit('testingground4bots')
for submission in subreddit.hot(limit=100):

    # Make sure you didn't already reply to this post
    if submission.id not in posts_replied_to:

        # Not case sensitive
        if re.search("comeback", submission.title, re.IGNORECASE):
            # Reply
            submission.reply("brrrrrr")
            print("Bot replying to : ", submission.title)

            # Store id in list
            posts_replied_to.append(submission.id)

# Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

        