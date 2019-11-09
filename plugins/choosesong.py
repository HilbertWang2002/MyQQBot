# -*- coding:gbk -*-
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
from nonebot.message import unescape
import random,requests,json

@on_command('choosesong', aliases = ('点歌'))
async def say(session: CommandSession):
    id = json.loads(requests.get('https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?g_tk=5381&uin=0&format=json&inCharset=utf-8&outCharset=utf-8%C2%ACice=0&platform=h5&needNewCode=1&tpl=3&page=detail&type=top&topid=27&_=1519963122923').text)['songlist'][random.randint(0,99)]['data']['songid']
    await session.send(unescape(f'[CQ:music,type=qq,id={id}]'))

@on_natural_language(keywords={'点歌'})
async def _(session: NLPSession):
    # 返回意图命令,前两个参数必填,分别表示置信度和意图命令名
    return IntentCommand(90.0, 'choosesong')