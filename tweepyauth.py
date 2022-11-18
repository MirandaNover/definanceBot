import config as cfg
import tweepy

##Make class anf add authenticate as a method
## Then add get tweets method, get id method etc

def authenticate(API_key, API_secret_key, access_token, access_token_secret): # Authenticate to Twitter
    auth = tweepy.OAuthHandler(API_key, API_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication Successful")

    except Exception:
        print("Authentication Error")

    return api