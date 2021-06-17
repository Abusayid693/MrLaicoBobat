
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


# ================SPELLING CHECK=======================
def check_spelling(message):
  message_splited = message.lower().split()
  blob = TextBlob(message)          #pass message to check spelling
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


spell_check=1
Sentiment_check=1



@client.event
async def on_message(message):
  text=message.content.lower().strip()
  
  # Making sure bot does not respond itself
  if message.author==client.user:
   return

  corrections=check_spelling(message.content) if not "laico" in text else []

  if spell_check  and len(corrections):
    for text in corrections:
      await message.channel.send(text)

  

  elif "laico" in text:
    response_message=random.choice(words_response)
    user_name=message.author.name
    # replacing "$" with author name
    response_message=response_message.replace("$", user_name)

    await message.channel.send(response_message)
    

  else  :


   
    
    text=message.content
    #Getting message sentiment
    result=check_sentiment(text) 
    print(message.author.name) 
   
    #If sad replying back 
    if result=="Sad":
      await message.channel.send("u seem "+result+" today")
    
    #If bored replying back
    if result=="Bored":
      await message.channel.send("u seem "+result)

    #If happy reacting
    if result=="Happy":
      await message.add_reaction(emoji.get("milk"))

    # If excited reacting
    if result=="Excited":
      await message.add_reaction(emoji.get("milk"))
    
    # If fear reacting
    if result=="Fear":
      await message.add_reaction(emoji.get("milk"))
    to_append=0













keep_alive()
client.run(os.environ['TOKEN'])
    

