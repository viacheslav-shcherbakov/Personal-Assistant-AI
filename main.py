"""
Personal Assistant v0.2
Created by: Josh Vitvitsky
10/20/2021 11:00 AM
"""
import os 
import time
import json
import random
from datetime import datetime
import speech_recognition as sr
listener = sr.Recognizer()
from gtts import gTTS
from playsound import playsound
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

import custom_commands_handler
#custom_commands_handler.boot()

#SETUP
AI_NAME='Jarvis'
# Create a new instance of a ChatBot
bot = ChatBot(
    AI_NAME,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.db'
)
trainer = ChatterBotCorpusTrainer(bot)
custom_trainer=ListTrainer(bot)

trainer.train(
    #"chatterbot.corpus.english"
    "chatterbot.corpus.english.greetings",
    #"chatterbot.corpus.english.conversations"
)

formal_trainer=json.loads(open('custom_trainers/formal_train.json','r').read())
formal_trainer_list=[]
for branch in formal_trainer:
    for line in formal_trainer[branch]:
        formal_trainer_list.append(line.replace('*N', AI_NAME))
        formal_trainer_list.append(formal_trainer[branch][line].replace('*N', AI_NAME))

print(formal_trainer_list)
custom_trainer.train(formal_trainer_list)

def main():
    in_convo=False
    in_convo_time=datetime.now()
    print('{} is online.'.format(AI_NAME))
    # The following loop will execute each time the user enters input
    while True:
        try:
            with sr.Microphone() as source:
                print('Listening...')
                voice = listener.listen(source)
                try:
                    voice_input = listener.recognize_google(voice)
                except:
                    voice_input=None

            convo_time_difference=datetime.now()-in_convo_time
            print('Since last replied message: ', convo_time_difference.total_seconds()/60)
            if(in_convo==True and (convo_time_difference.total_seconds()/60)>0.3):
                in_convo=False
                print('No longer in conversation')

            if voice_input!=None:
                print(str(voice_input))
                if str(voice_input).lower().find(AI_NAME.lower())!=-1 or in_convo==True:
                    if command_handler(str(voice_input)):
                        in_convo=True
                        in_convo_time=datetime.now()
                        print('In conversation with the bot')
                    else:
                        in_convo=True
                        in_convo_time=datetime.now()
                        print('In conversation with the bot')
                        #Just convo with bot
                        user_input = voice_input
                        bot_response = bot.get_response(user_input)
                        print(str(bot_response))
                        
                        #Puts sir in resonable locations to make it sound more proper
                        n=random.randint(0,1)
                        if n==1:
                            bot_response=str(bot_response).replace(',', ' sir,')

                        tts = gTTS(text=str(bot_response), lang='en', tld='co.uk', slow=False)
                        date_string = datetime.now().strftime("%d%m%Y%H%M%S")
                        filename='{}.mp3'.format(date_string)
                        print(filename)
                        tts.save(filename)
                        playsound(filename)
                        #time.sleep(0.3)
                        os.remove(filename)
                else:
                    pass

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

def command_handler(user_input):
    pass

main()