# -*- coding:gbk -*-
from nonebot import on_command, CommandSession
import requests
import json
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    # 获取城市的天气预报
    weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    await session.send(weather_report)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def get_weather_of_city(city: str) -> str:
    payload = {'location': city, 'key': '86cf5098168b4ed9ba3f46b01027f5de'}
    r = requests.get("https://free-api.heweather.net/s6/weather/forecast", params=payload)
    text = json.loads(r.text)
    return f'{text["HeWeather6"][0]["daily_forecast"][0]["date"]}{city}的温度是{text["HeWeather6"][0]["daily_forecast"][0]["tmp_min"]}度到{text["HeWeather6"][0]["daily_forecast"][0]["tmp_max"]}度，{text["HeWeather6"][0]["daily_forecast"][0]["wind_dir"]}{text["HeWeather6"][0]["daily_forecast"][0]["wind_sc"]}级，{text["HeWeather6"][0]["daily_forecast"][0]["mr"]}太阳起床{text["HeWeather6"][0]["daily_forecast"][0]["ms"]}太阳睡觉.                    {text["HeWeather6"][0]["daily_forecast"][1]["date"]}{city}的温度是{text["HeWeather6"][0]["daily_forecast"][1]["tmp_min"]}度到{text["HeWeather6"][0]["daily_forecast"][1]["tmp_max"]}度，{text["HeWeather6"][0]["daily_forecast"][1]["wind_dir"]}{text["HeWeather6"][0]["daily_forecast"][1]["wind_sc"]}级，{text["HeWeather6"][0]["daily_forecast"][1]["mr"]}太阳起床{text["HeWeather6"][0]["daily_forecast"][1]["ms"]}太阳睡觉'