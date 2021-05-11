import botometer
import tweepy
from textblob import TextBlob
import unicodedata
from deep_translator import GoogleTranslator

# Checar imagenes/video
# Hashtags, menciones, emojis, url


def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(string)
        return True
    except (TypeError, ValueError):
        pass
    return False


def isURL(word):
    try:
        dotIndex = word.index('.')
        if word[dotIndex+1].isalnum():
            return True
        return False
    except (ValueError, IndexError):
        return False


def cleanTweet(tweet):
    words = tweet.split(sep=' ')
    cleanWords = ""
    for word in words:
        try:
            if word[0] != '#' and '@' not in word and not isURL(word) and not isNumber(word):
                cleanWords += word + " "
        except IndexError:
            continue
    return cleanWords


def getTweets(api, cuentaDeDiputado):

    translator = GoogleTranslator(source="es", target="en")
    count = 0
    botPercentageAvg = 0
    MAX = 1000
    for tweet in tweepy.Cursor(api.user_timeline, id=cuentaDeDiputado, tweet_mode="extended").items():
        tweetJSON = tweet._json
        fullText = tweetJSON["full_text"]
        if "RT @" not in fullText and fullText[0] != '@':
            cleanText = cleanTweet(fullText)
            try:
                sentiment = TextBlob(str(translator.translate(cleanText))).sentiment
                botPercentageAvg += sentiment.polarity
                count += 1
                print(count)
            except Exception as e:
                print(e)
                continue
            if count == MAX:
                break
    print("PolarityAvg = " + str(botPercentageAvg / count))


def calculateMaxMinEngagement(api, cuentaDeDiputado):

    max = 0
    count = 0
    avgEngagement = 0
    MAX_TWEETS = 1000
    for tweet in tweepy.Cursor(api.user_timeline, id=cuentaDeDiputado, tweet_mode="extended").items():
        tweetJSON = tweet._json
        fullText = tweetJSON["full_text"]
        if "RT @" not in fullText and fullText[0] != '@':
            engagement = int(tweetJSON["retweet_count"]) + int(tweetJSON["favorite_count"])
            avgEngagement += engagement
            count += 1
            print(str(count)+"/"+str(MAX_TWEETS))
            if count == 1 or max < engagement:
                max = engagement
                print("Max changed, nuevo max = " + str(max))
            if count == 559:
                print("Engagement del tweet "+ str(count)+" = " + str(engagement))
            if count == MAX_TWEETS:
                break
    print("Cuenta analizada = " + cuentaDeDiputado)
    print("Tweets analizados = " + str(count))
    print("Max Engagement = " + str(max))
    print("Avg Engagement = " + str(avgEngagement/count))
    
def calculateBotPercentageAvg(api, cuentaDeDiputado, botometer):

    MAX_FOLLOWERS = 1000
    listAccounts = []
    for follower in tweepy.Cursor(api.followers, id=cuentaDeDiputado,).items(10):
        followerID = follower._json['screen_name']
        listAccounts.append(str('@' + followerID))
        if len(listAccounts) == MAX_FOLLOWERS:
            break

    print(listAccounts)
    avgBot = 0
    for _, result in botometer.check_accounts_in(listAccounts):
        avgBot += int(result['raw_scores']['universal']['fake_follower'])

    count = len(listAccounts)
    print("Cuenta analizada = " + cuentaDeDiputado)
    print("Followers analizados = " + str(count))
    print("Avg Engagement = " + str(avgBot / count))


def main():

    # - - - Solo cambien el nombre de las cuentas aquí
    # ---------------- Cuenta entre comillas dobles, sin @
    cuentaDeDiputado = "Marianavalto"
    # -------------------- ^^^^

    consumer_key = "VPegZu8V1iD7HSZ4rvyLfCtmd"
    consumer_secret = "0BJ0HUCC4NAEcQghwwtqrKXHFFRQZ52WRicG8Xb8tQ0rGsAC5K"

    access_token = "1383461526200209412-HXTe94Jo7PphohvME7CkmBfQm4yg9u"
    access_token_secret = "I9nQothxyDWdkji08wZZEjIoUOZuk9v6PMbP4vMcwzxEE"

    # --------- RapidAPI

    rapidapi_key = "398be2ebeemsh6a1555df87ce3e1p16985djsnf04e4880bd62"
    twitter_app_auth = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'access_token': access_token,
        'access_token_secret': access_token_secret,
    }

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    bom = botometer.Botometer(wait_on_ratelimit=True,
                              rapidapi_key=rapidapi_key,
                              **twitter_app_auth)

    # getTweets(api, cuentaDeDiputado)
    # calculateMaxMinEngagement(api, cuentaDeDiputado)

    # La nueva función vvvvvvvv
    calculateBotPercentageAvg(api, cuentaDeDiputado, bom)

main()
