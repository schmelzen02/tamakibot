import discord
import os
import re

import neko
import tl
import battle

# client
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

# 起動時に動作する処理
@client.event
async def on_ready():
    print('server started.')

# メッセージ駆動処理
@client.event
async def on_message(message):
    # botのメッセージは無視
    if message.author.bot:
        return

    # contentを空白、改行区切りでsplit
    content_lines = [ x.split(' ') for x in re.subn('( |　)+', ' ', message.content)[0].split('\n')]

    if content_lines[0][0] == '/neko':
        # /nekoコマンド
        await neko.exec(message)
    elif content_lines[0][0] == 'tl':
        # tlコマンド
        await tl.exec(message, content_lines)
    elif content_lines[0][0] == '/battle':
        await battle.exec(message, content_lines)

@client.event
async def on_raw_reaction_add(payload):
    # botのリアクションは無視
    if payload.member.bot:
        return

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # タマキbotが追加したメッセージの場合
    if message.author == client.user:
        if '#battle' in message.content:
            await battle.battle_reaction(payload, message)

# run nekobot
client.run(os.getenv('DISCORD_TOKEN'))
