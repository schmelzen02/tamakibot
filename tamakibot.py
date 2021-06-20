import discord
import os
import re

import neko
import tl

# client
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    print('server started.')

# メッセージ駆動処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # contentを空白、改行区切りでsplit
    content_lines = [ x.split(' ') for x in re.subn('( |　)+', ' ', message.content)[0].split('\n')]

    # /nekoコマンド
    if content_lines[0][0] == '/neko':
        await neko.exec(message)

    # tlコマンド
    elif content_lines[0][0] == 'tl':
        await tl.exec(message, content_lines)

# run nekobot
client.run(os.getenv('DISCORD_TOKEN'))
