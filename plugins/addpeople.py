# -*- coding:gbk -*-
from nonebot import on_command, CommandSession

@on_command('addpeople', aliases=('����'))
async def weather(session: CommandSession):
    people = session.get('people', prompt='�����˭��')
    file = open('./peoplelist.txt','a')
    file.write(people+'\n')
    file.close()
    
    await session.send('���˳ɹ���')
    
@weather.args_parser
async def _(session: CommandSession):
    # ȥ����Ϣ��β�Ŀհ׷�
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # �������һ�����У���һ�ν�������Ự��
        if stripped_arg:
            session.state['people'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('Ҫ�ӵ��˲���Ϊ���أ�����������')
    session.state[session.current_key] = stripped_arg