import os
import discord
import pymupdf
import io
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
    if message.content.startswith('-pdf-to-image'):
        parts = message.content.split()  
        if message.attachments and message.attachments[0].filename.endswith('.pdf') and len(parts) > 1 and parts[1].isdigit():
            page = int(parts[1])
            pdf_attachment = message.attachments[0]
            pdf_filename = "temp.pdf"
            await pdf_attachment.save(pdf_filename)

            try:            
                doc = pymupdf.open(pdf_filename)
            
                if 1 <= page <= len(doc):
                    page_obj = doc[page - 1]
                    pix = page_obj.get_pixmap(dpi=300)
                    image_bytes = pix.tobytes("png")
                    image_file = discord.File(io.BytesIO(image_bytes), filename=f"output_page_{page}.png")
                    await message.channel.send(file=image_file)
                else:
                    await message.channel.send(f"This file have {len(doc)} pages. Please provide a correct number!")
            finally:
                if os.path.exists(pdf_filename):
                    os.remove(pdf_filename)           
        else:
            await message.channel.send("Please provided correct code: -pdf-to-image <number_page>")
        return
server_on()

client.run(os.getenv('TOKEN'))