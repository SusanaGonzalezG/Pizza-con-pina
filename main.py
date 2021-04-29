#from botometer import Botometer
import tweepy as tw
from textblob import TextBlob

tweetPrueba = "Gracias a Nico por su entrevista y a su gran perro Mica por su compañia. Hablamos de la inclusión y la " \
              "importancia de los perros de seguridad #Diosesamor @CamachoEsGei google.com 22.13"

#nChecar imagenes/video
# Hashtags, menciones, emojis, url
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
        if word[0] != '#' and '@' not in word and not isURL(word):
            cleanWords += word + " "
    return cleanWords


print(tweetPrueba)
cleanTweet(tweetPrueba)

