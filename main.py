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
async def on_member_join(member):
    role_id = 1564494948919803954
    role = member.guild.get_role(role_id)
            
    if role is None:
        print("Can't found a role on this server.")
        return
    try:
        await member.add_roles(role)
        print("Already set the first role for user in server!")
    except discord.Forbidden:
        print("Bot don't have a high role to change it.")
    return

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
    # if message.content.startswith('-role') and message.author.guild_permissions.manage_messages:
    #     target_member = message.mentions[0] if message.mentions else message.author
        
    #     role_id = 1564492134952738866
    #     role = message.guild.get_role(role_id)
        
    #     if role is None:
    #         await message.channel.send("ไม่พบ Role นี้ในเซิร์ฟเวอร์")
    #         return

    #     try:
    #         await target_member.add_roles(role)
    #         await message.channel.send(f"เพิ่มยศ {role.name} ให้กับ {target_member.mention} เรียบร้อยแล้ว!")
    #     except discord.Forbidden:
    #         await message.channel.send("บอทไม่มีสิทธิ์สูงพอที่จะจัดการยศนี้ (ตำแหน่ง Role ของบอทต้องอยู่สูงกว่า Role ที่จะแจก)")
    #     return
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