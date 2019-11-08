# -*- coding:gbk -*-
import json
from typing import Optional

import aiohttp
from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression

# �����޷���ȡͼ��ظ�ʱ�ġ���Expression����
EXPR_DONT_UNDERSTAND = (
    '�����ڻ���̫��������˵ʲô�أ���û��ϵ���Ժ���һ��ø�ǿ�أ�',
    '���е㿴���������˼ѽ�����Ը�����Щ�򵥵Ļ�����',
    '��ʵ�Ҳ�̫���������˼����',
    '��ǸŶ�������ڵ����������ܹ���������˵ʲô�����һ���͵ġ�'
)


# ע��һ�����ڲ�ʹ�õ��������Ҫ aliases
@on_command('tuling')
async def tuling(session: CommandSession):
    # ��ȡ��ѡ�������������û�� message ����������ᱻ�жϣ�message �������� None
    message = session.state.get('message')

    # ͨ����װ�ĺ�����ȡͼ������˵Ļظ�
    reply = await call_tuling_api(session, message)
    if reply:
        # �������ͼ������˳ɹ����õ��˻ظ�����ת��֮���͸��û�
        # ת������Ϣ�е�ĳЩ�����ַ���ת�����Ա��� ��Q ���������Ϊ CQ ��
        await session.send(escape(reply))
    else:
        # �������ʧ�ܣ����������ص���������Ŀǰ�����ˣ������޷���ȡͼ��ظ�ʱ�ġ���
        # ����� render_expression() �����Ὣһ��������Ⱦ��һ���ַ�����Ϣ
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))


@on_natural_language
async def _(session: NLPSession):
    # �����Ŷ� 60.0 ���� tuling ����
    # ȷ���κ���Ϣ�����ҽ���������Ȼ���Դ������޷�����ʱ��ʹ�� tuling ����
    return IntentCommand(60.0, 'tuling', args={'message': session.msg_text})


async def call_tuling_api(session: CommandSession, text: str) -> Optional[str]:
    # ����ͼ������˵� API ��ȡ�ظ�

    if not text:
        return None

    url = 'http://openapi.tuling123.com/openapi/api/v2'

    # ������������
    payload = {
        'reqType': 0,
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': session.bot.config.TULING_API_KEY,
            'userId': context_id(session.ctx, use_hash=True)
        }
    }

    group_unique_id = context_id(session.ctx, mode='group', use_hash=True)
    if group_unique_id:
        payload['userInfo']['groupId'] = group_unique_id

    try:
        # ʹ�� aiohttp �ⷢ�����յ�����
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload) as response:
                if response.status != 200:
                    # ��� HTTP ��Ӧ״̬�벻�� 200��˵������ʧ��
                    return None

                resp_payload = json.loads(await response.text())
                if resp_payload['results']:
                    for result in resp_payload['results']:
                        if result['resultType'] == 'text':
                            # �����ı����͵Ļظ�
                            return result['values']['text']
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # �׳������κ��쳣��˵������ʧ��
        return None