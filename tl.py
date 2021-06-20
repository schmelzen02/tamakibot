import datetime

# tl command
async def exec(message, content_lines):
    print(f'tl command.')

    try:
        target_time_str = content_lines[0][1]
        target_time = str2time(target_time_str)
        diff_time = base_time - target_time

        new_tl = []
        for x in content_lines[1:]:
            tmp = x.copy()
            old_time = str2time(tmp[0])
            new_time = old_time - diff_time
            if new_time > zero_time:
                tmp[0] = time2str(new_time)
                new_tl.append(tmp)

        new_tl_str = '\n'.join([' '.join(x) for x in new_tl])

        await message.channel.send(f'{target_time_str}でのTLにゃ\n```{new_tl_str}```')
    except Exception as e:
        print(e)
        await message.channel.send('間違ったTLにゃ')

# 文字列 -> datetime
def str2time(time_str):
    return datetime.datetime.strptime(time_str, '%M:%S')

# datetime -> 文字列
def time2str(time):
    return time.strftime('%#M:%S')

zero_time = str2time('0:00')
base_time = str2time('1:30')
