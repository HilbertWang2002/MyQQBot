# -*- coding:gbk -*-
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
import requests,asyncio

@on_command('dbili', aliases=('下载b站'))
async def luxunt(session: CommandSession):
    text = session.state.get('text')
    data = text.split(' ')
    if data[1]:
        while True:
            r = requests.get('http://forestnothing.xyz:5000/downbilibili?av='+data[1])
            if r.text == 'downloading':
                await session.send('正在下载。。。')
            if r.text == 'downloaded':
                await session.send('下载完成，点击http://forestnothing.xyz/video/'+data[1]+'.mp4下载')
                return
            if r.text == 'failed':
                await session.send('啊下载出错了！你的av号是否正确呢？')
                return
            await asyncio.sleep(5)
            
                                        
@on_natural_language(keywords={'下载b站'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'dbili', args = {'text': session.msg_text})