import re
import pandas as pd
from datetime import date, timedelta

LOCAL_DIR = "/tmp/"


def main():
    tweets = pd.read_csv(LOCAL_DIR + "data_fetched.csv")

    # formating to the datetime
    tweets.rename(columns={
        'Tweet': 'tweet',
        'Time': 'dt',
        'Retweet from': 'retweet_from',
    },
                  inplace=True)

    tweets.drop(columns=['User'], inplace=True)
    tweets['before_clean_len'] = [len(t) for t in tweets.tweet]
    tweets['tweet'] = tweets['tweet'].apply(
        lambda t: re.sub(r'@[A-Za-z0-9]+', '', t))
    tweets['tweet'] = tweets['tweet'].apply(
        lambda t: re.sub(r'https?://[A-Za-z0-9./]+', '', t))
    tweets['tweet'] = tweets['tweet'].apply(
        lambda t: re.sub(r'[^A-Za-z]+', '', t))
    tweets['tweet'] = tweets['tweet'].str.lower()
    tweets['after_clean_len'] = [len(t) for t in tweets.tweet]

    yesterday = date.today() - timedelta(days=1)
    dt = yesterday.strftime("%Y-%m-%d")
    tweets['dt'] = dt

    tweets.to_csv(LOCAL_DIR + "data_cleaned.csv", index=False)


if __name__ == "__main__":
    main()
