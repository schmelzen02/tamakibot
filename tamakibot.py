import discord
import os

import neko
import neko_help
import tl
import tl_help

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

    # /nekoコマンド
    if message.content == '/neko':
        await neko.do(message)

    # tlコマンド
    elif message.content.startswith('tl '):
        await tl.do(message)

# run nekobot
client.run(os.getenv('DISCORD_TOKEN'))
