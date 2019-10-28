# -*- coding:gbk -*-
from nonebot import on_command, CommandSession
import random

@on_command('rollson', aliases=('������'))
async def weather(session: CommandSession):
    file = open('./peoplelist.txt','r')
    lines = file.readlines()
    file.close()
    count = len(lines)
    father = random.randint(1,count)
    while True:
        son = random.randint(1,count)
        if not son == father:
            break
    father = lines[father-1]
    son = lines[son-1]
    file.close()
    
    await session.send(f'{son}��{father}�Ķ��ӣ�')