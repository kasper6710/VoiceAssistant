import os
import speech_recognition as sr
import pyttsx3
import datetime
import random
import webbrowser
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from requests import Session

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
            'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


def speak(audio):
    print("[]log " + audio)
    engine.say(audio)
    engine.runAndWait()


def UsdRate():
    nowConvert = str(datetime.date.today())
    nowTime = str(datetime.datetime.now())

    if nowTime[11] == '0':
        change = int(nowConvert[-2:]) - 1
        nowConvert = nowConvert[:-2] + str(change)

    nowConvert = nowConvert[-2:] + "." + nowConvert[5:-3] + "." + nowConvert[0:4]

    url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date=' + nowConvert

    session = Session()

    try:
        response = session.get(url)
        data = json.loads(response.text)
        for temp in data['exchangeRate']:
            for i in temp.keys():
                if i == 'currency' and temp[i] == 'USD':
                    return temp['saleRateNB']

    except (ConnectionError, Timeout, TooManyRedirects):
        return -1


def crypto():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '15',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '95ffabb3-e004-4cb7-825c-7587ebcf7905',
    }

    session = Session()
    session.headers.update(headers)

    if UsdRate() != -1:
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            bitcoinRate = data['data'][0]['quote']['USD']['price']
            dogecoinRate = 0
            for temp in data['data']:
                if temp['name'] == 'Dogecoin':
                    dogecoinRate = temp['quote']['USD']['price']

            usd = UsdRate()

            print('Bitcoin rate -> ' + str(bitcoinRate))
            print('Dogecoin rate -> ' + str(dogecoinRate))
            # btc = 1<- Write number of BTC which you have
            # doge = 1<- Write number of DOGE which you have
            # print('___________')
            # print('USD bitcoin you have -> ' + str(bitcoinRate * btc))
            # print('USD dogecoin you have -> ' + str(dogecoinRate * doge))
            # print('___________')
            # print('UAH bitcoin you have -> ' + str(bitcoinRate * btc * usd))
            # print('UAH dogecoin you have -> ' + str(dogecoinRate * doge * usd))
            # print('___________')
            # print('Summary USD -> ' + str(bitcoinRate * btc + dogecoinRate * doge))
            # print('Summary UAH -> ' + str(usd * (bitcoinRate * btc + dogecoinRate * doge)))
            # print('___________')


        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
    else:
        print('Error in UsdRate def :D (be happy)')


def encrypting(str1):
    n1 = random.randint(1, 25)
    str1 = str1.lower()
    newStr = ""
    for i in str1:
        if i in alphabet:
            newStr += alphabet[(alphabet.index(i) + n1) % 26]
        else:
            newStr += i

    file = open("crypting.txt", 'w+')

    file.write(str(n1))
    file.write("\n")
    file.write(newStr)

    file.close()
    return newStr


def decrypting():
    file = open("crypting.txt", 'r')
    list1 = file.readlines()

    n1 = int(list1[0])
    str1 = list1[1]

    file.close()
    str1 = str1.lower()

    newStr = ""
    for i in str1:
        if i in alphabet:
            newStr += alphabet[alphabet.index(i) - n1]
        else:
            newStr += i
    return newStr


def greet():
    current = int(datetime.datetime.now().hour)

    if (current >= 0) and (current < 12):
        speak('Good Morning!')

    if (current >= 12) and (current < 18):
        speak('Good Afternoon!')

    if (current >= 18) and (current != 0):
        speak('Good Evening!')


greet()

speak('Hello Sir, I am your digital assistant Emily\n How may I help you?')


def myCommand():
    r = sr.Recognizer()

    with sr.Microphone(device_index=1) as source:

        print("Listening...")

        r.pause_threshold = 0.5

        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en')

        print('User: ' + query + '\n')

    except sr.UnknownValueError:

        speak('Sorry sir! I didn\'t get that! Try to repeat your command.')

        return myCommand()

    return query


def myCommandUn():
    r = sr.Recognizer()

    with sr.Microphone(device_index=1) as source:

        print("Listening...")

        r.pause_threshold = 0.5

        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en')

        print('User: ' + query + '\n')

    except sr.UnknownValueError:

        return myCommandUn()

    return query


if __name__ == '__main__':
    isOffline = False
    isFirst = True
    wakeUp = ""

    while True:
        if not isFirst:
            wakeUp = myCommandUn()
            wakeUp = wakeUp.lower()

        if ('emily' in wakeUp) or ('wake' in wakeUp) or isFirst:
            if not isFirst:
                speak("Yes, Sir")

            while True:
                cmd = myCommand()
                cmd = cmd.lower()

                if 'open youtube' in cmd:
                    speak("Opening Youtube...")
                    webbrowser.open('https://www.youtube.com/')

                elif 'current time' in cmd:
                    now = datetime.datetime.now()
                    speak("Now is " + str(now.hour) + " hours " + str(now.minute) + " minutes " + str(
                        now.second) + " seconds ")

                elif 'spider' in cmd:
                    players = ["Sergey", "Andriy", "Ivan", "Nika", "Sasaha", "Bodyan", "Tanya"]
                    speak("Pidor is " + random.choice(players))

                elif 'music' in cmd:
                    speak("Switching on music...")
                    numMus = random.randint(1, 1)
                    numMus = str(numMus)
                    link1 = "C:\\Users\\Admin\\Desktop\\Projects\\Python\\JARVISE\\music\\" + numMus + ".mp3"
                    os.system(link1)
                    isFirst = False
                    break

                elif 'joke' in cmd:
                    speak("I will try to do it...")
                    webbrowser.open("https://www.youtube.com/watch?v=t2gCkEr3In8")

                elif 'encrypt' in cmd:
                    speak("Which message you want to encrypt")
                    message = myCommand()
                    speak("is encrypted like:")
                    speak(encrypting(message))

                elif 'decrypt' in cmd:
                    speak("Decryption is:")
                    speak(decrypting())

                elif 'crypto' in cmd:
                    speak('Ok, wait a minute')
                    crypto()
                    speak('Сryptocurrency report executed')

                elif 'you are jarvise' in cmd:
                    speak('Yes I know that the programme name is Jarvise, but my name is Emily')

                elif 'sleep' in cmd:
                    speak("Good bye")
                    isFirst = False
                    break

                elif 'off' in cmd:
                    speak("Switching off system")
                    isOffline = True
                    break
        if 'off' in wakeUp:
            isOffline = True
        if isOffline:
            break
