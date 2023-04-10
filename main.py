import discord
from config import *
from discord import app_commands
from discord import components
from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands import CommandNotFound
from discord.utils import get
import datetime
import asyncio
import time
import json
import random


#Define our bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = app_commands.CommandTree(client)

channel_ids = [channel_id_1, channel_id_2,channel_id_3,channel_id_4]
eggs_images = ["egg_red","egg_blue","egg_yellow","egg_grey","egg_purple","egg_green"]

@client.event
async def on_ready():
    await bot.sync(guild=discord.Object(id=discord_server_id))
    print(f"{client.user} has connected to Discord!")


@bot.command(name="egghunt",description="Notify people about an egg hunt.",guild=discord.Object(id=discord_server_id))
async def raid_start(ctx):
    if ctx.user.id != egg_hunt_admin:
        await ctx.response.send_message("You have no permission to start an egghunt.")
        return


    allowed_mentions = discord.AllowedMentions(roles=True,users=True, everyone=True)
    # Send the raid notification message
    embedVar = discord.Embed(title="Egg Hunt",description=f'A new Egg hunt is starting!',color=0xa84300)
    file = discord.File("assets/egghunt_announcement_image.png", filename="egghunt_announcement_image.png")
    embedVar.set_image(url="attachment://egghunt_announcement_image.png")
    embedVar.add_field(name=f'How to participate:',value='`React with `🥚 ',inline = False)
    embedVar.add_field(name=f'Total eggs:',value='`50`',inline = False)
    embedVar.add_field(name=f'Event starts in:',value='`10 minutes`',inline = False)

    participants = []
    dead_players = []

    round_num = 1
#, file=file
    await ctx.response.send_message(content="",embed = embedVar,file=file)
    raid_msg = await ctx.original_response()
    emoji = "🥚"
    await raid_msg.add_reaction(emoji)

    try:
        reaction, user = await client.wait_for("reaction_add", timeout=initial_timeout_announcement, check=lambda r,u: r.emoji == emoji)
        # Wait for up to 5 minutes or until 5 people have reacted
        while len(participants) < 500:
            reaction, user = await client.wait_for("reaction_add", timeout=timeout_after_someone_reacts, check=lambda r, u: r.emoji ==emoji and u.id != egg_hunt_admin)

    except asyncio.TimeoutError:
        pass

    channel = client.get_channel(announcement_channel)

    message = await channel.fetch_message(raid_msg.id)

    for reaction in message.reactions:
        async for userz in reaction.users():
            if userz.id not in participants and userz.id != egg_hunt_admin:
                participants.append(userz.id)
    if len(participants) < 1:
        await raid_msg.edit(content=f"Not enough people have joined the egg hunt. :(",embed = None)
        return

    eggs = {user_id: 0 for user_id in participants}
    no_eggs = []

    participants_mention = ", ".join([f"<@{user_id}>" for user_id in participants])
    embedraidVar = discord.Embed(title="Raid",description=f'A new egg hunt is starting!',color=0xa84300)
    file = discord.File("assets/egghunt_announcement_image.png", filename="egghunt_announcement_image.png")
    embedraidVar.set_image(url="attachment://egghunt_announcement_image.png")
    embedraidVar.add_field(name=f'Number of participants:',value=f'`{len(participants)}`',inline = False)
    embedraidVar.add_field(name=f'Conditions satisfied:',value='`True`',inline = False)
    embedraidVar.add_field(name=f'Rules:',value='You have to find the eggs messages from the `Egg Hunt Bot` that appear in different channels inside the Strange Clan discord (no private messages) and react to the 🥚 Egg emoji. Only the first reaction (after the bot) will counts as a point!',inline = False)
    await raid_msg.edit(content="",embed = embedraidVar)


    await asyncio.sleep(30)
    # Keep attacking the boss until everyone dies or the boss dies
    counter_rounds = 0
    while participants and round_num <= total_egg_hunt_rounds:
        channel = client.get_channel(random.choice(channel_ids))

        embedBossVar = discord.Embed(title="A shiny Egg",color=0xa84300)
        random_egg_img = random.choice(eggs_images)
        random_egg_img_link = "assets/" + str(random_egg_img) + ".png"
        random_egg_img_name = str(random_egg_img) + ".png"
        random_egg_img_attach = "attachment://" + str(random_egg_img) + ".png"
        file = discord.File(random_egg_img_link, filename=random_egg_img_name)
        embedBossVar.set_image(url=random_egg_img_attach)
        embedBossVar.add_field(name=f'Round:',value=f'`{round_num}`',inline = False)
        embedBossVar.add_field(name=f'Action:',value='Be the first one to react to `claim` the Egg',inline = False)
        attck_msg = await channel.send(content="",embed = embedBossVar, file=file)
        attack_emoji = emoji
        await attck_msg.add_reaction(attack_emoji)
        # Wait for participants to react with the attack emoji, or for 10 seconds to elapse
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=20, check=lambda r, u: r.emoji == attack_emoji and u.id in participants)
            eggs[user.id] += 1
            embedBossVaredit = discord.Embed(title="A shiny Egg",color=0xa84300)
            embedBossVaredit.set_image(url=random_egg_img_attach)
            embedBossVaredit.add_field(name=f'Round:',value=f'`{round_num}`',inline = False)
            embedBossVaredit.add_field(name=f'Result:',value=f'Egg claimed by <@{user.id}>',inline = False)
            await attck_msg.edit(content="",embed = embedBossVaredit)
        except asyncio.TimeoutError:
            pass

        # Increment the round number
        round_num += 1
        
        await asyncio.sleep(5)

        await attck_msg.delete()

    # The raid has ended
    if round_num >= total_egg_hunt_rounds:
        max_keys = [key for key, value in eggs.items() if value == max(eggs.values())]
        participants_with_eggs = ", ".join([f"<@{user_id}> : {eggs[user_id]}" for user_id in participants if eggs[user_id] > 0])
        #participants_no_eggs = ", ".join([f"<@{user_id}>" for user_id in participants if eggs[user_id] == 0])
        embedWinVar = discord.Embed(title="Egg hunt finished",color=0xa84300)
        file = discord.File("assets/egghunt_announcement_image.png", filename="egghunt_announcement_image.png")
        embedWinVar.set_image(url="attachment://egghunt_announcement_image.png")
        embedWinVar.add_field(name=f'Result:',value='The Egg Hunt has concluded!',inline = False)
        stringy_text    = ", ".join([f"<@{maxis}>" for maxis in max_keys])
        embedWinVar.add_field(name=f'__MVP:__',value=f'{stringy_text}',inline = False)
        embedWinVar.add_field(name=f'__Successful egg hunters:__',value=f'{participants_with_eggs}',inline = False)

        await ctx.followup.send(content="",file=file, embed = embedWinVar)


client.run(DISCORD_TOKEN)
