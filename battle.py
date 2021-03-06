import discord

import re
import io

REACTION_ONE_HALF = '<:zero_half:856912616613085215>'
REACTION_ONE = '1️⃣'
REACTION_TWO_HALF = '<:one_half:856912617074065408>'
REACTION_TWO = '2️⃣'
REACTION_THREE_HALF = '<:two_half:856912616995946516>'
REACTION_THREE = '3️⃣'
REACTION_AGGREGATE = '⚙️'

async def exec(message, content_lines):
    print('battle command.')

    try:
        day = content_lines[0][1]
        if not day in ['1', '2', '3', '4', '5']:
            raise Exception

        description = f'クラバト{day}日目頑張るにゃ\n凸が終わったらスタンプをつけて欲しいにゃ　#battle\n'
        description += '> ' + REACTION_ONE_HALF + '　1凸目持ち越しあり\n'
        description += '> ' + REACTION_ONE + '　1凸目完了\n'
        description += '> ' + REACTION_TWO_HALF + '　2凸目持ち越しあり\n'
        description += '> ' + REACTION_TWO + '　2凸目完了\n'
        description += '> ' + REACTION_THREE_HALF + '　3凸目持ち越しあり\n'
        description += '> ' + REACTION_THREE + '　3凸目完了\n'
        description += '> ' + REACTION_AGGREGATE + '　集計'

        send_message = await message.channel.send(description)
        await send_message.add_reaction(REACTION_ONE_HALF)
        await send_message.add_reaction(REACTION_ONE)
        await send_message.add_reaction(REACTION_TWO_HALF)
        await send_message.add_reaction(REACTION_TWO)
        await send_message.add_reaction(REACTION_THREE_HALF)
        await send_message.add_reaction(REACTION_THREE)
        await send_message.add_reaction(REACTION_AGGREGATE)
    except Exception as e:
        print(e)
        await message.channel.send('コマンドが間違ってるにゃ')

async def battle_reaction(payload, message):
    print('battle reaction.')

    if payload.emoji.name == REACTION_AGGREGATE:
        await aggregate(message)
    else:
        await unify(payload, message)

async def unify(payload, message):
    print('unify.')

    member = payload.member
    emoji = str(payload.emoji)

    if emoji == REACTION_ONE:
        await message.remove_reaction(REACTION_ONE_HALF, member)
    if emoji == REACTION_ONE_HALF:
        await message.remove_reaction(REACTION_ONE, member)
    elif emoji == REACTION_TWO:
        await message.remove_reaction(REACTION_TWO_HALF, member)
    elif emoji == REACTION_TWO_HALF:
        await message.remove_reaction(REACTION_TWO, member)
    elif emoji == REACTION_THREE:
        await message.remove_reaction(REACTION_THREE_HALF, member)
    elif emoji == REACTION_THREE_HALF:
        await message.remove_reaction(REACTION_THREE, member)

async def aggregate(message):
    print('aggregate.')

    all_members = get_all_members(message)

    members = { member.discriminator: [ member.name, '-', '-', '-' ] for member in all_members }

    for reaction in message.reactions:
        if reaction.emoji == REACTION_AGGREGATE:
            continue

        emoji = str(reaction.emoji)

        async for user in reaction.users():
            if not user.discriminator in members:
                continue

            state = members[user.discriminator]
            if emoji == REACTION_ONE_HALF and state[1] == '-':
                state[1] = '持ち越し'
            elif emoji == REACTION_ONE:
                state[1] = '済'
            elif emoji == REACTION_TWO_HALF and state[2] == '-':
                state[2] = '持ち越し'
            elif emoji == REACTION_TWO:
                state[2] = '済'
            elif emoji == REACTION_THREE_HALF and state[3] == '-':
                state[3] = '持ち越し'
            elif emoji == REACTION_THREE:
                state[3] = '済'

    target = re.search(r'クラバト(.)日目', message.content).group(1)

    csv = 'プレイヤー名,1凸目,2凸目,3凸目\n' + '\n'.join([ ','.join(member) for member in members.values()])

    with io.StringIO(csv) as bs:
        send_message = await message.channel.send(f'クラバト{target}日目を集計したにゃ', file=discord.File(bs, f'clan_battle_{target}.csv'))
        await send_message.delete(delay=60)

def get_all_members(message):
    return list(filter(lambda x: not x.bot,  message.guild.members))
