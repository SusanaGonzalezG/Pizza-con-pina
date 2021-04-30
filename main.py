#from botometer import Botometer
import tweepy
from textblob import TextBlob
import json
import unicodedata
from deep_translator import GoogleTranslator

from textblob.exceptions import NotTranslated

tweetPrueba = "Gracias a Nico por su entrevista y a su gran perro Mica por su compañia. Hablamos de la inclusión y la " \
              "importancia de los perros de seguridad #Diosesamor @CamachoEsGei google.com 22.13"

#nChecar imagenes/video
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

def main():

    #---------------- Cuenta entre comillas dobles, sin @
    cuentaDeDiputado = "JTrianaT"
    #-------------------- ^^^^

    consumer_key = "VPegZu8V1iD7HSZ4rvyLfCtmd"
    consumer_secret = "0BJ0HUCC4NAEcQghwwtqrKXHFFRQZ52WRicG8Xb8tQ0rGsAC5K"

    access_token = "1383461526200209412-HXTe94Jo7PphohvME7CkmBfQm4yg9u"
    access_token_secret = "I9nQothxyDWdkji08wZZEjIoUOZuk9v6PMbP4vMcwzxEE"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    translator = GoogleTranslator(source="es", target="en")
    count = 0
    polarityAvg = 0
    MAX = 1000
    for tweet in tweepy.Cursor(api.user_timeline, id=cuentaDeDiputado, tweet_mode="extended").items():
        tweetJSON = tweet._json
        fullText = tweetJSON["full_text"]
        if "RT @" not in fullText and fullText[0] != '@':
            cleanText = cleanTweet(fullText)
            try:
                sentiment = TextBlob(str(translator.translate(cleanText))).sentiment
                polarityAvg += sentiment.polarity
                count += 1
                print(count)
            except Exception as e:
                print(e)
                continue
            if count == MAX:
                break
    print("PolarityAvg = " + str(polarityAvg/count))

main()
