import pandas as pd

LOCAL_DIR = "/tmp/"


def main():
    tweets = pd.read_csv("/usr/local/airflow/dags/data/data.csv",
                         encoding='latin1')

    # formating to the datetime
    tweets = tweets.assign(Time=pd.to_datetime(tweets.Time))\
                   .drop('row ID', axis='columns')

    tweets.to_csv(LOCAL_DIR + "data_fetched.csv", index=False)


if __name__ == "__main__":
    main()
