# -*- coding:gbk -*-
from nonebot import on_command, CommandSession

@on_command('addpeople', aliases=('加人'))
async def weather(session: CommandSession):
    people = session.get('people', prompt='你想加谁？')
    file = open('./peoplelist.txt','a')
    file.write(people+'\n')
    file.close()
    
    await session.send('加人成功！')
    
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['people'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要加的人不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg