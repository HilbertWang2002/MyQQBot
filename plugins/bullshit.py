# -*- coding:gbk -*-
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
import random,os,re


def 读JSON文件(fileName=""):
    import json
    if fileName!='':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName,mode='r',encoding="utf-8") as file:
                return json.loads(file.read())

data = 读JSON文件("./plugins/bullshit/data.json")
名人名言 = data["famous"] # a 代表前面垫话，b代表后面垫话
前面垫话 = data["before"] # 在名人名言前面弄点废话
后面垫话 = data['after']  # 在名人名言后面弄点废话
废话 = data['bosh'] # 代表文章主要废话来源

xx = "学生会退会"

重复度 = 2

def 洗牌遍历(列表):
    global 重复度
    池 = list(列表) * 重复度
    while True:
        random.shuffle(池)
        for 元素 in 池:
            yield 元素

下一句废话 = 洗牌遍历(废话)
下一句名人名言 = 洗牌遍历(名人名言)

def 来点名人名言():
    global 下一句名人名言
    xx = next(下一句名人名言)
    xx = xx.replace(  "a",random.choice(前面垫话) )
    xx = xx.replace(  "b",random.choice(后面垫话) )
    return xx

def 另起一段():
    return'\n'

@on_command('bullshit', aliases=('写文章'))
async def bullshit(session: CommandSession):
    xx = session.get('text')
    tmp = str()
    while ( len(tmp) < 2000 ) :
        分支 = random.randint(0,100)
        if 分支 < 5:
            tmp += 另起一段()
        elif 分支 < 20 :
            tmp += 来点名人名言()
        else:
            tmp += next(下一句废话)
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
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.state['text'] = stripped_arg
    session.state[session.current_key] = stripped_arg
    
@on_natural_language(keywords={'写文章'})
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'bullshit')