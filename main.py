
# Mr laico bot

import discord
import os
import paralleldots
import random
from textblob import TextBlob
from keep_alive import keep_alive
from replit import db




Sentiment_API = os.environ['API_KEY']

client=discord.Client()                 #Setting Discord
paralleldots.set_api_key(Sentiment_API) #Setting API

# "$" special character is to replace with user name
words_response=[
  "Hi! $",
  "How are things with you $",
  "It’s good to see you $",
  "Howdy! $",
  "Hi, $. What’s new?",
  "Good to see you $",
  "Look who it is! $",
  "Oh, it’s you $! Hi there!",
  "Hi $, it’s me again!",
  "Hang in ther $ ,i am busy!"
  ]


emoji = {
  "milk": "🥛",
  "cow": "🐄",
  "shark": "🦈",
  "basketball": "🏀",
  "boba": "🧋",
  "wave": "👋",
  "s" : "🆂",
  "h": "🅷",
  "i": "🅸",
  "t": "🆃",
  "z": "🆉"
  }


Sad=["i am sad"]
Bored=["i am Bored"]

# ================SPELLING CHECK=======================
def check_spelling(message):
  message_splited = message.lower().split()
  blob = TextBlob(message.lower())          #pass message to check spelling
  ans=blob.correct()
  ans_splited=ans.split()           
 #  Loop through the messages to find if there was spelling mistake
  corrections=[]
  for i in range(len(message_splited)):
    if message_splited[i] in ans_splited:
      continue        
    else :  
      a="it's "+ans_splited[i]+" not "+message_splited[i]+"\n"
      corrections.append(a)

  return corrections               # Returns a array



#=============== EMOTIONS CHECK ========================
def check_sentiment(message):
  emotions= paralleldots.emotion( message ).get('emotion')
  Max_emotion=max(emotions, key=emotions.get)
  # print(emotions)
  return Max_emotion              # Returns emotion with max probability











# BOT FUNCTIONS
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


to_spell_check=1
Sentiment_check=1



@client.event
async def on_message(message):
  text=message.content.lower().strip()
  
  # Making sure bot does not respond itself
  if message.author==client.user:
   return
  # getting corrections
  corrections=check_spelling(message.content)

  if "laico" in text:
    response_message=random.choice(words_response)
    user_name=message.author.name
    # replacing "$" with author name
    response_message=response_message.replace("$", user_name)
    await message.channel.send(response_message)
  
  # correction execution
  elif to_spell_check and len(corrections):
    await auto_response(message,len(corrections),corrections,1,0,0)  

  else  :       
    text=message.content
    #Getting message sentiment
    result=check_sentiment(text)            
    await auto_response(message,result=="Sad",Sad,1,0,0)    
    await auto_response(message,result=="Bored",Bored,1,0,0)    
    await auto_response(message,result=="Happy",0,0,1,emoji.get("milk"))   
    await auto_response(message,result=="Excited",0,0,1,emoji.get("milk"))
    await auto_response(message,result=="Fear",0,0,1,emoji.get("milk"))  
    to_append=0


async def auto_response(message,condition,context_send,send,react,context_react):
  if condition and send:
    for i in context_send:
      await message.channel.send(i)
  if condition and react:
    for i in context_react:
      await message.add_reaction(i)

keep_alive()
client.run(os.environ['TOKEN'])
    

