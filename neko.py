import random

# /nekoコマンド
async def exec(message):

    dice = random.randint(1, 100)

    if dice > 95:
        await message.channel.send('に゛ゃ゛ーーーっ゛！？')
    elif dice > 70:
        await message.channel.send('にゃっ！にゃっ、にゃっ！')
    else:
        await message.channel.send('にゃっ')

