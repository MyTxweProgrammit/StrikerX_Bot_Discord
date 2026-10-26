import os
import discord
from datetime import date
from server import server_on

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
            return
    if message.content.startswith('-bye'):
        await message.channel.send("Goodbye! I will see you later!")
        return
    if message.content.startswith("-hello"): 
        await message.channel.send("Hey, There!")
        return
    if message.content.startswith('-help'):
        await message.channel.send("What can I help you? Please tell me.")
        return
    if message.content.startswith('-today'):
        await message.channel.send(f"Date: {date.today()}")
        return
    if message.content.startswith('-clear'):
        if message.author.guild_permissions.manage_messages:
              delete = await message.channel.purge(limit=100)
              await message.channel.send(f"Cleared {len(delete)} messages.")
        else:
            await message.channel.send("You don't have permission to do this.")
        return
    
server_on()

client.run(os.getenv('TOKEN'))