# -*- coding:gbk -*-
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
import random,os,re


def ��JSON�ļ�(fileName=""):
    import json
    if fileName!='':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName,mode='r',encoding="utf-8") as file:
                return json.loads(file.read())

data = ��JSON�ļ�("./plugins/bullshit/data.json")
�������� = data["famous"] # a ����ǰ��滰��b�������滰
ǰ��滰 = data["before"] # ����������ǰ��Ū��ϻ�
����滰 = data['after']  # ���������Ժ���Ū��ϻ�
�ϻ� = data['bosh'] # ����������Ҫ�ϻ���Դ

xx = "ѧ�����˻�"

�ظ��� = 2

def ϴ�Ʊ���(�б�):
    global �ظ���
    �� = list(�б�) * �ظ���
    while True:
        random.shuffle(��)
        for Ԫ�� in ��:
            yield Ԫ��

��һ��ϻ� = ϴ�Ʊ���(�ϻ�)
��һ���������� = ϴ�Ʊ���(��������)

def ������������():
    global ��һ����������
    xx = next(��һ����������)
    xx = xx.replace(  "a",random.choice(ǰ��滰) )
    xx = xx.replace(  "b",random.choice(����滰) )
    return xx

def ����һ��():
    return'\n'

@on_command('bullshit', aliases=('д����'))
async def bullshit(session: CommandSession):
    xx = session.get('text')
    tmp = str()
    while ( len(tmp) < 2000 ) :
        ��֧ = random.randint(0,100)
        if ��֧ < 5:
            tmp += ����һ��()
        elif ��֧ < 20 :
            tmp += ������������()
        else:
            tmp += next(��һ��ϻ�)
    tmp = tmp.replace("x",xx)
    
    textarr = tmp.split('\n')
    textarrfi = []
    for i in textarr:
        for ch in i:
            if u'\u4e00' <= ch <= u'\u9fff':
                textarrfi.append(i)
                break
    for i in textarrfi:
            await session.send(i)
        
@bullshit.args_parser
async def _(session: CommandSession):
    # ȥ����Ϣ��β�Ŀհ׷�
    stripped_arg = session.current_arg_text.strip()
    session.state['text'] = stripped_arg
    session.state[session.current_key] = stripped_arg
    
@on_natural_language(keywords={'д����'})
async def _(session: NLPSession):
    # ������ͼ���ǰ������������ֱ��ʾ���ŶȺ���ͼ������
    return IntentCommand(90.0, 'bullshit')