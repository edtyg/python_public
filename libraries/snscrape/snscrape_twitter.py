"""
pip install snscrape
"""
import snscrape.modules.twitter as sntwitter
import pandas as pd
from typing import Optional


def get_tweets(user: str, limit: int, since: Optional[str] = None):
    if since is None:
        query = f"from:{user}"
    else:
        query = f"from:{user} since:{since}"

    tweets = []
    limit = limit

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            tweets.append(
                [
                    tweet.date,
                    tweet.user.username,
                    tweet.content,
                    tweet.url,
                    tweet.likeCount,
                ]
            )

    columns = ["date", "username", "content", "url", "like_count"]
    df = pd.DataFrame(tweets, columns=columns)

    return df


if __name__ == "__main__":
    username = "elonmusk"
    limit = 10000
    since = "2022-10-01"

    df = get_tweets(username, limit, since)
