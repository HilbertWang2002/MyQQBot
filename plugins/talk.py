# -*- coding:gbk -*-
from nonebot import on_command, CommandSession
import requests,json
@on_command('talk', aliases=(''))
async def talk(session: CommandSession):
    sentence = session.get('sentence', prompt='你想和我说什么？')
    payload = {'showapi_appid':'107968','info':sentence,'userid':'userid','showapi_sign':'f8f1ea25878742e69dfc5a5ef6eff9b7'}
    r = requests.get("http://route.showapi.com/60-27", params=payload)
    text = json.loads(r.text)
    await session.send(text['showapi_res_body']['text'])
    
@talk.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['sentence'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要说的话不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg