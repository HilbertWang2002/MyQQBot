# -*- coding:gbk -*-
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
import requests,json,time

@on_command('cov', aliases=('��������'))
async def luxunt(session: CommandSession):
    text = session.state.get('text')
    data = text.split(' ')
    if len(data) == 1:
        r = requests.get('https://lab.isaaclin.cn/nCoV/api/overall')
        if r.status_code != 200:
            await session.send(f'���ִ����ˣ�������Ϊ{r.status_code}')
            return
        data = json.loads(r.text)
        if data['success'] == True:
            temp = data['results'][0]
            eng = ['currentConfirmedCount','confirmedCount','suspectedCount','curedCount','deadCount','seriousCount','currentConfirmedIncr','confirmedIncr','suspectedIncr','curedIncr','deadIncr','seriousIncr']
            chs = ['�ִ�ȷ��','�ۼ�ȷ��','����ȷ��','������','������','��֢��','��ǰȷ���Ⱦ�߽�ǰ������','ȷ���ǰ������','���ƽ�ǰ������','��������ǰ������','������������','��֢����']
            text_to_send = ''
            error_msg = ''
            for i in range(len(eng)):
                try:
                    text_to_send =  text_to_send + '\n' + chs[i] + '��' + str(temp[eng[i]])
                except Exception:
                    error_msg = error_msg+chs[i]+'��'
            await session.send('�Ѹ��£�'+ text_to_send)
            await session.send('δ���£�'+ error_msg[:-1])
            await session.send('����ʱ�䣺'+time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}' ,time.localtime(float(temp['updateTime'])/1000)).format(y='��', m='��', d='��', h='ʱ', f='��', s='��'))
            return
    if len(data) > 1:
        if data[1] == '��ʾ':
            r = requests.get('https://lab.isaaclin.cn/nCoV/api/overall')
            if r.status_code != 200:
                await session.send(f'���ִ����ˣ�������Ϊ{r.status_code}')
                return
            data = json.loads(r.text)
            if data['success'] == True:
                temp = data['results'][0]
                await session.send(temp['remark1'])
                await session.send(temp['remark2'])
                await session.send(temp['remark3'])
                await session.send(temp['note1'])
                await session.send(temp['note2'])
                await session.send(temp['note3'])
                await session.send('����ʱ�䣺'+time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}' ,time.localtime(float(temp['updateTime'])/1000)).format(y='��', m='��', d='��', h='ʱ', f='��', s='��'))
                return
        else:
            r = requests.get('https://lab.isaaclin.cn/nCoV/api/area?province='+data[1])
            if r.status_code != 200:
                await session.send(f'���ִ����ˣ�������Ϊ{r.status_code}')
                return
            data = json.loads(r.text)
            if data['success'] == True:
                if len(data['results']) == 0:
                    await session.send('����������������⣡')
                else:
                    temp = data['results'][0]
                    await session.send(f"�������ƣ�{temp['provinceName']},Ӣ������{temp['provinceEnglishName']},�ִ�ȷ��{temp['currentConfirmedCount']}�����ۼ�ȷ��{temp['confirmedCount']}��������{temp['suspectedCount']}��������{temp['curedCount']}��������{temp['deadCount']}����")
                    await session.send('����ʱ�䣺'+time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}' ,time.localtime(float(temp['updateTime'])/1000)).format(y='��', m='��', d='��', h='ʱ', f='��', s='��'))
                    return
                              
@on_natural_language(keywords={'��������'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'cov', args = {'text': session.msg_text})