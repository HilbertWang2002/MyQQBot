# -*- coding:gbk -*-
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
import requests,json,time

@on_command('cov', aliases=('疫情数据'))
async def luxunt(session: CommandSession):
    text = session.state.get('text')
    data = text.split(' ')
    if len(data) == 1:
        r = requests.get('https://lab.isaaclin.cn/nCoV/api/overall')
        if r.status_code != 200:
            await session.send(f'出现错误了！返回码为{r.status_code}')
            return
        data = json.loads(r.text)
        if data['success'] == True:
            temp = data['results'][0]
            eng = ['currentConfirmedCount','confirmedCount','suspectedCount','curedCount','deadCount','seriousCount','currentConfirmedIncr','confirmedIncr','suspectedIncr','curedIncr','deadIncr','seriousIncr']
            chs = ['现存确诊','累计确诊','疑似确诊','治愈数','死亡数','重症数','当前确诊感染者较前日增量','确诊较前日增量','疑似较前日增量','治愈数较前日增量','死亡人数增量','重症增量']
            text_to_send = ''
            error_msg = ''
            for i in range(len(eng)):
                try:
                    text_to_send =  text_to_send + '\n' + chs[i] + '：' + str(temp[eng[i]])
                except Exception:
                    error_msg = error_msg+chs[i]+'、'
            await session.send('已更新：'+ text_to_send)
            await session.send('未更新：'+ error_msg[:-1])
            await session.send('更新时间：'+time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}' ,time.localtime(float(temp['updateTime'])/1000)).format(y='年', m='月', d='日', h='时', f='分', s='秒'))
            return
    if len(data) > 1:
        if data[1] == '提示':
            r = requests.get('https://lab.isaaclin.cn/nCoV/api/overall')
            if r.status_code != 200:
                await session.send(f'出现错误了！返回码为{r.status_code}')
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
                await session.send('更新时间：'+time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}' ,time.localtime(float(temp['updateTime'])/1000)).format(y='年', m='月', d='日', h='时', f='分', s='秒'))
                return
        else:
            r = requests.get('https://lab.isaaclin.cn/nCoV/api/area?province='+data[1])
            if r.status_code != 200:
                await session.send(f'出现错误了！返回码为{r.status_code}')
                return
            data = json.loads(r.text)
            if data['success'] == True:
                if len(data['results']) == 0:
                    await session.send('你输入的名字有问题！')
                else:
                    temp = data['results'][0]
                    await session.send(f"地区名称：{temp['provinceName']},英文名：{temp['provinceEnglishName']},现存确诊{temp['currentConfirmedCount']}例，累计确诊{temp['confirmedCount']}例，疑似{temp['suspectedCount']}例，治愈{temp['curedCount']}例，死亡{temp['deadCount']}例。")
                    await session.send('更新时间：'+time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}' ,time.localtime(float(temp['updateTime'])/1000)).format(y='年', m='月', d='日', h='时', f='分', s='秒'))
                    return
                              
@on_natural_language(keywords={'疫情数据'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'cov', args = {'text': session.msg_text})