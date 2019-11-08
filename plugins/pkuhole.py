# -*- coding: UTF-8 -*-
import nonebot,pytz,requests,os,time
from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError

@nonebot.scheduler.scheduled_job('interval', minutes=30)
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    url = f'https://github.com/martinwu42/pkuholebackup/raw/master/archive/{now.year}'+'%02d' % now.month +f'/pkuhole{now.year}'+'%02d' % now.month + '%02d' % now.day +'.txt'
    r = requests.get(url)
    count = 0
    msgs = u''
    
    with open('./temp/__date','r') as code:
        redate = code.read()
    
    nowdate = f'{now.year}{now.month}{now.day}'
    
    if not redate == nowdate:
        with open("./temp/__0", "w",encoding='utf-8') as code:
            code.write(r.content.decode('utf-8'))
        with open("./temp/__0", "r",encoding='utf-8') as code:
            for i in code.readlines():
                    msgs = msgs + i.encode('utf-8').decode('utf-8')
    else:
        fore = open('./temp/__0','r',encoding='utf-8')
        forefile = fore.readlines()
        
        for i in forefile:
            count+=1
        fore.close()
        
        with open("./temp/__1", "w",encoding='utf-8') as code:
            code.write(r.content.decode('utf-8'))
        with open("./temp/__1", "r",encoding='utf-8') as code:    
            for i in code.readlines()[:-count]:
                msgs = msgs + i.encode('utf-8').decode('utf-8')
        os.remove('./temp/__0')
        os.rename('./temp/__1','./temp/__0')
    with open('./temp/__date','w') as code:
        code.write(nowdate)
        
    if msgs == '':
        pass
    else:    
        msgblocks = msgs.split('#')[1:]
    
        msgs_to_send = []
    
        for i in msgblocks:
            if i[0] == 'p':
                msgs_to_send.append(i[:-2])
            if i[0] == 'c':
                msgs_to_send[-1] = msgs_to_send[-1] + '\n' + '\n'.join(i.split('\n')[1::-2])
        with open('./temp/test.txt','w',encoding = 'utf-8') as code:
            code.write('\n\n'.join(msgs_to_send))
        
        time_to_sleep = 1800//len(msgs_to_send)      
        for i in msgs_to_send[::-1]:
            await send_by_block(i,bot)
            time.sleep(time_to_sleep)        
            
async def send_by_block(msgs,bot):
    try:
        msgsraws = msgs.split('\n')
        rownum = len(msgsraws)
        for i in range(0,(rownum-1)//10+1):     
            await bot.send_group_msg(group_id=750501153,
                                 message = '\n'.join(msgsraws[i*10:(i+1)*10]))
    except CQHttpError:
        pass