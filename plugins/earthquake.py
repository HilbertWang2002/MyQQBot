# -*- coding: gbk -*-
import nonebot,pytz,requests,asyncio,json,time
@nonebot.scheduler.scheduled_job(
    'interval',
    # weeks=0,
    # days=0,
    # hours=0,
    minutes=5,
    # seconds=0,
    # start_date=time.now(),
    # end_date=None,
)
async def _():
    bot = nonebot.get_bot()
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_hour.geojson'
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.text)['features']
        for i in data:
            x = i['properties']
            with open('earthquake.data','r') as code:
                happened = code.readlines()
            if (str(x['time'])+'\n') in happened:
                continue
            with open('earthquake.data','a') as code:
                code.write(str(x['time'])+'\n')
            x['time'] = time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}' ,time.localtime(float(x['time'])/1000)).format(y='年', m='月', d='日', h='时', f='分', s='秒')
            x['updated'] = time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}' ,time.localtime(float(x['updated'])/1000)).format(y='年', m='月', d='日', h='时', f='分', s='秒')
            eng = ['mag','place','time','updated','url',]
            chs = ['震级:','位置:','地震发生时间:','信息更新时间:','详细信息请点击：']
            text_to_send = '地震信息：'
            for j in range(len(eng)):
                try:
                    text_to_send = text_to_send + '\n' + chs[j] + ' ' + str(x[eng[j]])
                except Exception:
                    pass
            x = i['geometry']['coordinates']
            eng = ['longitude','latitude','depth']
            x[2] = str(x[2])+'km'
            chs = ['经度:','纬度:','深度:']
            text_to_send2 = '震源信息：'
            for j in range(len(eng)):
                try:
                    text_to_send2 = text_to_send2 + '\n' + chs[j] + ' ' + str(x[j])
                except Exception as e:
                    pass
            await bot.send_group_msg(group_id=750501153,
                                 message = text_to_send)
            await bot.send_group_msg(group_id=750501153,
                                 message = text_to_send2)
            await bot.send_group_msg(group_id=750501153,
                                 message = '已成功处理一个来自usgs的地震消息！')
            
	