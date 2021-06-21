import discord

import re
import io

async def exec(message, content_lines):
    print('battle command.')

    try:
        day = content_lines[0][1]
        if not day in ['1', '2', '3', '4', '5']:
            raise Exception

        await message.channel.send(f'クラバト{day}日目頑張るにゃ\n凸が終わったらスタンプをつけるにゃ')

        agg_target_messages = [
            await message.channel.send('```1凸目にゃ```'),
            await message.channel.send('```1凸目の持ち越しにゃ```'),
            await message.channel.send('```2凸目にゃ```'),
            await message.channel.send('```2凸目の持ち越しにゃ```'),
            await message.channel.send('```3凸目にゃ```'),
            await message.channel.send('```3凸目の持ち越しにゃ```')
        ]

        for target_message in agg_target_messages:
            await add_cat_reaction(target_message)

        agg_id_list = ','.join([str(x.id) for x in agg_target_messages])

        aggregate_message = await message.channel.send(f'集計する時はこのメッセージにスタンプをつけてにゃ #agg\n```[{day}日目,{agg_id_list}]```')
        await add_cat_reaction(aggregate_message)
    except Exception as e:
        print(e)
        await message.channel.send('コマンドが間違ってるにゃ')

async def aggregate(message):
    print('battle aggregate.')

    try:
        target = re.search(r'\[(.+)\]', message.content).group(1).split(',')

        members = filter(lambda x: not x.bot,  message.guild.members)
        members = {x.discriminator: [ x.name, '未', '未', '未', '未', '未', '未' ] for x in members }

        day = target[0]

        await message.channel.send(f'{day}を集計するにゃ')

        for i in range(1, 7):
            await aggregate_sub(message.channel, members, target, i)
    
        csv = 'プレイヤー名,1凸目,1凸目持ち越し,2凸目,2凸目持ち越し,3凸目,3凸目持ち越し\n' + '\n'.join([ ','.join(member) for member in members.values()])
        
        with io.StringIO(csv) as bs:
            await message.channel.send(f'{day}を集計したにゃ', file=discord.File(bs, f'{day}.csv'))
    except Exception as e:
        print(e)
        message.channel.send('集計に失敗したにゃ...')

async def aggregate_sub(channel, members, target, i):
    message = await channel.fetch_message(target[i])

    for reaction in message.reactions:
        async for user in reaction.users():
            if user.discriminator in members:
                members[user.discriminator][i] = '済'


async def add_cat_reaction(message):
    try:
        await message.add_reaction('<:tamaki:787338723188277258>')
    except:
        try:
            await message.add_reaction('<:tamaki:856169668507467788>')
        except:
            await message.add_reaction('\N{Cat Face with Wry Smile}')