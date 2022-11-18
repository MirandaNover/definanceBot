from importlib.metadata import metadata
from multiprocessing import AuthenticationError
from termHandler import Term
import config as cfg
from tweepyauth import authenticate
import sqlalchemy as db
from datetime import datetime
import pandas as pd


def main():
    engine = db.create_engine(f"mysql://{cfg.db['user']}:{cfg.db['pass']}@{cfg.db['host']}/{cfg.db['db']}")                        
    connection = engine.connect()
    metadata = db.MetaData()
    tweets_table = db.Table('tweets', metadata, autoload=True, autoload_with=engine)
    
    prev_ids = connection.execute(db.select(tweets_table.columns.id))
    df = pd.DataFrame(prev_ids)

    api = authenticate(cfg.tweepy['API_key'], cfg.tweepy['API_secret_key'], 
    cfg.tweepy['access_token'], cfg.tweepy['access_token_secret'])
    mentions = api.mentions_timeline()

    for mention in mentions:             
        tweet = mention.text
        id_str = mention.id_str
        current = connection.execute(db.select([tweets_table])).fetchall()
        df = pd.DataFrame(current)
        if id_str not in df['id'].values:
            query = db.insert(tweets_table).values(time=datetime.now(), id=id_str)
            ResultProxy = connection.execute(query)
            reply = Term(tweet).format_term()
            api.update_status(status=reply, in_reply_to_status_id=id_str)




if __name__== '__main__':
    main()


