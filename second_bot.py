import praw
import pdb
import re
import os

import pandas as pd

# Reddit instance
reddit = praw.Reddit('bot')

if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []

# Or load the list of posts we have replied to
else:
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))


tickers = set()
df=pd.read_csv('companylist.csv')
for index,rows in df.iterrows():
    tickers.add(rows.Symbol.lower())

subreddit = reddit.subreddit('testingground4bots')
for comment in subreddit.stream.comments():
    body = comment.body.lower()

    if body == 'what are you into' and comment.id not in comments_replied_to:
        parent_comment = comment.parent()
        parent_comment.refresh()

        parent_author = parent_comment.author

        ticker_freq = {}
        for c in parent_author.comments.new(limit=None):
            for word in c.body.split():
                if word in tickers:
                    ticker_freq.setdefault(word, 0)
                    count = ticker_freq[word]
                    ticker_freq[word] = count + 1

        sorted_d = sorted(ticker_freq.items(), key=lambda x: x[1], reverse=True)
        reply_text = "##{} ticker mentions\n".format(parent_author.name)
        reply_text += "|Symbol|Frequency|\n"
        reply_text += "|------|---------|\n"
        for (key,value) in sorted_d:
            reply_text += "|{}    |{}     |\n".format(key,value)

        print(reply_text)
        comment.reply(reply_text)

        comments_replied_to.append(comment.id)
        # Write updated list to file
        with open("comments_replied_to.txt", "w") as f:
            for comment_id in comments_replied_to:
                f.write(comment_id + "\n")
    




