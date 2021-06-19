import re
import datetime

# tlコマンド
async def do(message):
    try:
        print('tlコマンド')
        command_str = message.content
        command_str = re.subn('( |　)+', ' ', command_str)[0]

        if not re.match(r'^tl [01]:[0-5][0-9]\n([01]:[0-5][0-9] .+\n?)+$', command_str):
            raise Exception

        result = ''

        zero_time = str2time('0:00')
        base_time = str2time('1:30')

        target_time_str = re.search(r'^tl ([01]:[0-9][0-9])', command_str).groups()[0]
        target_time = str2time(target_time_str)

        diff_time = base_time - target_time
        
        result += target_time_str + 'でのTLにゃ\n```'

        for tl_line in re.findall(r'([01]:[0-9][0-9]) (.+)', command_str):
            tl_time = str2time(tl_line[0])

            new_tl_time = tl_time - diff_time

            if (zero_time < new_tl_time):
                result += time2str(new_tl_time) + ' ' + tl_line[1] + '\n'

        result += '```'

        await message.channel.send(result)
    except:
        await message.channel.send('間違ったTLにゃ')

# 文字列 -> datetime
def str2time(time_str):
    return datetime.datetime.strptime(time_str, '%M:%S')

# datetime -> 文字列
def time2str(time):
    return time.strftime('%#M:%S')
