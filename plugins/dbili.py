# -*- coding:gbk -*-
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
import requests,asyncio

@on_command('dbili', aliases=('����bվ'))
async def luxunt(session: CommandSession):
    text = session.state.get('text')
    data = text.split(' ')
    if data[1]:
        while True:
            r = requests.get('http://forestnothing.xyz:5000/downbilibili?av='+data[1])
            if r.text == 'downloading':
                await session.send('�������ء�����')
            if r.text == 'downloaded':
                await session.send('������ɣ����http://forestnothing.xyz/video/'+data[1]+'.mp4����')
                return
            if r.text == 'failed':
                await session.send('�����س����ˣ����av���Ƿ���ȷ�أ�')
                return
            await asyncio.sleep(5)
            
                                        
@on_natural_language(keywords={'����bվ'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'dbili', args = {'text': session.msg_text})