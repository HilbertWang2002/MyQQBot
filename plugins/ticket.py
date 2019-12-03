# -*- coding:gbk -*-
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
from plugins.ticket_base import *

@on_command('ticket', aliases=('查询车票：'))
async def ticket(session: CommandSession):
    text = session.state.get('text')[5:]
    a = text.split(' ')
    for i in a:
        await session.send(i)
    msgs = fun(a[0],a[1],a[2],a[3],a[4])
    msgs_2 = []
    for i in msgs:
        msgs_2.append(' '.join(i))
    await session.send('\n'.join(msgs_2))

@on_natural_language(keywords={'查询车票：'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'ticket', args = {'text': session.msg_text})
