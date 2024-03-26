import discord
import os
from discord import channel
import requests
import json
import random
import time
os.system("pip install -qU replit")
from replit import db
db["special_encouragements"] = ["You were safe this time", "Your lucky I'm not in the mood right now", "I'll insult you later", "I'm feeling nice right now"]
intents = discord.Intents.default()
intents.message_content = True

special_servers = [1207263711597699072, 1213349839782289518]

admin_channel = 1216574994767806494

client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "love", "left me", "cry", "cries"]

starter_encouragements = [
  "bob"
]



if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  channel_id = message.channel.id
  guild_id = message.guild.id
  guild_name = message.guild.name
  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.author.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
        # Convert the "ObservedList" to a regular list
        encouragements_list = []
        encouragements_list = list(db["encouragements"])
        options += encouragements_list  # Concatenate lists
    if any(word in msg for word in sad_words):
      if guild_id in special_servers:
        encouragements_list = list(db["encouragements"])
        special_encouragment_list = list(db["special_encouragements"])
        options += encouragements_list
        options += special_encouragment_list
        await message.channel.send(random.choice(options))
      else:
        encouragements_list = list(db["encouragements"])
        await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    if channel_id == admin_channel:

      encouraging_message = msg.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message added.")
    elif channel_id != admin_channel:
      await message.channel.send("You are not authorized to use this command.")

  if msg.startswith("$del"):
    if channel_id == admin_channel:

      encouragements = []
      if "encouragements" in db.keys():
          index_str = msg.split("$del", 1)[1].strip()  # Remove leading/trailing whitespace
          try:
              index = int(index_str)
              delete_encouragment(index)
              encouragements = db["encouragements"]
          except ValueError:
              await message.channel.send("Invalid index provided. Please provide a valid integer index.")
      await message.channel.send(encouragements)
    elif channel_id != admin_channel:
      await message.channel.send("You are not authorized to use this command.")

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = str(db["encouragements"])
      clean_encouragements = encouragements.replace('ObservedList(value=', '')
      await message.channel.send(clean_encouragements)
      await message.channel.send(db["encouragements"])

  if msg.startswith("$responding"):
    if channel_id == admin_channel:
      value = msg.split("$responding ",1)[1]

      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")
    elif channel_id != admin_channel:
      await message.channel.send("You are not authorized to use this command.")

  if msg.startswith("$delete all"):
    if channel_id == admin_channel:
      encouragements = []
      encouragements_list = []
      db["encouragements"] = []
      await message.channel.send("All encouragements have been deleted.")
    elif channel_id != admin_channel:
      await message.channel.send("You do not have permission to use this command.")

client.run(os.environ['TOKEN'])

