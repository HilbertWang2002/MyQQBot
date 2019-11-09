# -*- coding: UTF-8 -*-
import nonebot,pytz,requests,asyncio,time,re
from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError
from config import KEYWORDS as keywords

@nonebot.scheduler.scheduled_job('cron', hour='*', minute = '9')
async def _():
    #获取机器人
    bot = nonebot.get_bot()
    #获取当前时间
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    #定义backup的地址，并获取
    url = f'https://github.com/martinwu42/pkuholebackup/raw/master/archive/{now.year}'+'%02d' % now.month +f'/pkuhole{now.year}'+'%02d' % now.month + '%02d' % now.day +'.txt'
    r = requests.get(url)
    #获得上次最后发送的一个的序号
    with open('./temp/__1','r',encoding = 'utf-8') as code:
        index = int(code.read())
    #获得所有的消息
    all_msgs = r.content.decode('utf-8')
    #整理消息
    sorted_msgs = []
    for i in re.split(r'\s+(?=#c|#p)',all_msgs):
        if i[1] == 'p':
            sorted_msgs.append(i)
        if i[1] == 'c':
            sorted_msgs[-1] = sorted_msgs[-1] + '\n' + '\n'.join(i.split('\n')[1::-2])
    #将整理后的消息和序号、时间一一对应
    sorted_msgs_dic = {}#格式是：{编号:[时间（秒）,内容]
    for i in sorted_msgs:
        sorted_msgs_dic[int(i.split(' ')[1])] = [time.mktime(time.strptime(i.split(' ')[2]+' '+i.split(' ')[3], "%Y-%m-%d %H:%M:%S")),i]
    #或得一个小时之前的消息的序号
    for i in sorted_msgs_dic.keys():
        if sorted_msgs_dic[i][0]<=time.time()-3600:
            maxindex = i
            break
    #获取要发送的消息内容
    msgs_to_send = []
    for i in sorted_msgs_dic.keys():
        if i > index and i <= maxindex:
            msgs_to_send.append(sorted_msgs_dic[i][1])
    #更新已发送的消息序号
    with open('./temp/__1','w',encoding = 'utf-8') as code:
        code.write(str(maxindex))
    #指定消息与消息之间的时间间隔
    time_to_sleep = 3590//len(msgs_to_send)
    #发送消息      
    for i in msgs_to_send[::-1]:
        await send_by_block(i,bot,keywords=keywords)
        await asyncio.sleep(time_to_sleep)        
#格式化发送消息
async def send_by_block(msgs,bot,keywords):
    try:
        msgsraws = msgs.split('\n')
        rownum = len(msgsraws)
        for i in range(0,(rownum-1)//10+1):     
            await bot.send_group_msg(group_id=938511236,
                                 message = '\n'.join(msgsraws[i*10:(i+1)*10]))
            for j in keywords:
                if j in msgs:
                    await bot.send_group_msg(group_id=750501153,
                                 message = '\n'.join(msgsraws[i*10:(i+1)*10]))
    except CQHttpError:
        pass
