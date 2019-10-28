# -*- coding:gbk -*-
from nonebot import on_command, CommandSession
import requests
import json
# on_command װ��������������Ϊһ���������
# ���� weather Ϊ��������֣�ͬʱ����ʹ�ñ�����������������Ԥ��������������
@on_command('weather', aliases=('����', '����Ԥ��', '������'))
async def weather(session: CommandSession):
    # �ӻỰ״̬��session.state���л�ȡ�������ƣ�city���������ǰ�����ڣ���ѯ���û�
    city = session.get('city', prompt='�����ѯ�ĸ����е������أ�')
    # ��ȡ���е�����Ԥ��
    weather_report = await get_weather_of_city(city)
    # ���û���������Ԥ��
    await session.send(weather_report)


# weather.args_parser װ��������������Ϊ weather ����Ĳ���������
# ������������ڽ��û�����Ĳ�������������������Ҫ������
@weather.args_parser
async def _(session: CommandSession):
    # ȥ����Ϣ��β�Ŀհ׷�
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # �������һ�����У���һ�ν�������Ự��
        if stripped_arg:
            # ��һ�����в�����Ϊ�գ���ζ���û�ֱ�ӽ��������������������棬��Ϊ��������
            # �����û����ܷ����ˣ����� �Ͼ�
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # �û�û�з�����Ч�ĳ������ƣ����Ƿ����˿հ��ַ���������ʾ��������
        # ���� session.pause() ���ᷢ����Ϣ����ͣ��ǰ�Ự�����к���Ĵ��벻�ᱻ���У�
        session.pause('Ҫ��ѯ�ĳ������Ʋ���Ϊ���أ�����������')

    # �����ǰ�������û�ѯ�ʸ�����Ϣ�����籾���е�Ҫ��ѯ�ĳ��У������û�������Ч�������Ự״̬
    session.state[session.current_key] = stripped_arg


async def get_weather_of_city(city: str) -> str:
    payload = {'location': city, 'key': '86cf5098168b4ed9ba3f46b01027f5de'}
    r = requests.get("https://free-api.heweather.net/s6/weather/forecast", params=payload)
    text = json.loads(r.text)
    return f'{text["HeWeather6"][0]["daily_forecast"][0]["date"]}{city}���¶���{text["HeWeather6"][0]["daily_forecast"][0]["tmp_min"]}�ȵ�{text["HeWeather6"][0]["daily_forecast"][0]["tmp_max"]}�ȣ�{text["HeWeather6"][0]["daily_forecast"][0]["wind_dir"]}{text["HeWeather6"][0]["daily_forecast"][0]["wind_sc"]}����{text["HeWeather6"][0]["daily_forecast"][0]["mr"]}̫����{text["HeWeather6"][0]["daily_forecast"][0]["ms"]}̫��˯��.                    {text["HeWeather6"][0]["daily_forecast"][1]["date"]}{city}���¶���{text["HeWeather6"][0]["daily_forecast"][1]["tmp_min"]}�ȵ�{text["HeWeather6"][0]["daily_forecast"][1]["tmp_max"]}�ȣ�{text["HeWeather6"][0]["daily_forecast"][1]["wind_dir"]}{text["HeWeather6"][0]["daily_forecast"][1]["wind_sc"]}����{text["HeWeather6"][0]["daily_forecast"][1]["mr"]}̫����{text["HeWeather6"][0]["daily_forecast"][1]["ms"]}̫��˯��'