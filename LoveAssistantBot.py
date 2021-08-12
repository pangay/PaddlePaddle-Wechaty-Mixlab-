import os
import cv2
import asyncio
import numpy as np
import paddlehub as hub
#from ppgan.apps import Photo2CartoonPredictor#人像动漫化
from PIL import Image
#from ppgan.apps import AnimeGANPredictor#场景动漫化
#from ppgan.apps import LapStylePredictor

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)
robot_state = 0 #机器人状态
style = ''#待模拟风格

# 藏头诗
def cts(data):

    long = len(data)

    if long <= 4:
        long = 4
    else:
        long = 8
    print(long)
    module = hub.Module(name="ernie_gen_acrostic_poetry", line=long, word=7)

    results = module.generate(texts=[data], use_gpu=True, beam_width=1)
    for result in results:
        print(results)
        return result[0]
#一键情话生成
def qh(data):
    module = module = hub.Module(name="ernie_gen_lover_words")
    results = module.generate(texts=[data], use_gpu=True, beam_width=1)
    for result in results:
        print(results)
        return result[0]
#一键对联生成
def dl(data):
    
    module = hub.Module(name="ernie_gen_couplet")
    results = module.generate(texts=[data], use_gpu=True, beam_width=1)
    for result in results:
        print(results)
        return result[0]
def img_transform(img_path, img_name, style):
    """
    将图片转换为新海诚《你的名字》、《天气之子》风格的图片
    img_path: 图片的路径
    img_name: 图片的文件名
    """
    # 图片转换后存放的路径
    img_new_path = './image-new/' + img_name

    model = hub.Module(name= style , use_gpu=True)
    # 模型预测
    result = model.style_transfer(images=[cv2.imread(img_path)])

    # 将图片保存到指定路径
    cv2.imwrite(img_new_path, result[0])


    # 返回新图片的路径
    return img_new_path
def envirstyle(img_path,style): #没办法使用 ppgan.apps
    img_new_path = './image-new/' + img_name
    predictor = LapStylePredictor(output=img_new_path,
                                style=style_chose,
                                weight_path=None,
                                style_image_path=None)
    return img_new_path
def stylepro(img_path_img1, img_name_img1,img_path_style,img_name_style):
    results = stylepro_artistic.style_transfer(images=[{
        'content': cv2.imread(img_path_img1),
        'styles': [cv2.imread(img_path_style)]}],
        alpha = 1.0,
        visualization = True)
    img_new_path = './image-new/' + img_name_img1
    cv2.imwrite(img_new_path, result)
    
    return img_new_path
        

async def on_message(msg: Message):
    talker = msg.talker()
    global robot_state
    global style
    # robot_state = 0
    if msg.text() == '哈喽！':
        await msg.say('你需要什么服务呢?本机器人提供\n 情话生成器 \n 代你来表白 \n 专属情头生成 服务')
    if msg.text() == 'hi' or msg.text() == '你好':
        await talker.say('你好这里是 脱单一键帮忙机器人 非常开心能为您服务\n 本机器人现在可提供\n 情话生成器 \n 代你来表白 \n 专属情头生成 服务')
    if msg.text() == '你是谁':
        await talker.say('我是您的专属脱单机器人呀')
    if msg.text() == '再见':
        await talker.say('很高兴为您服务，祝您表白成功哦')
    if msg.text() == '情话生成器':
        # 选择生成情话的种类
        await talker.say('请选择您想要的种类\n藏头诗\n一键情话\n对联')
    if msg.text() == '专属情头生成':
        await talker.say('现在有七种风格可以选取\n 梵高星空风格\n海洋风格 \n 电子线路风格 \n 星云风格 \n 宫崎骏《起风了》 \n 新海诚《你的名字》\n 今敏《红辣椒》\n 您也可以选择输入:风格融合   融合生成您自己的专属头像  ')
    if msg.text() == '藏头诗':
        robot_state = 1
    if robot_state==1:  
        await talker.say('已收到制作藏头诗请求 请发送您的想要藏匿的内容1~8字')
        await talker.say('')
        print(msg.text()[0:])
        await talker.say(cts(msg.text()[0:]))
        robot_state=0

    if msg.text() == '一键情话':
        robot_state = 2
        await talker.say('已收到制作情话的请求 请发送您的关键词')
    if  robot_state == 2:
        await talker.say('已经收到你的心意' + msg.text() + '，请您稍等哦')
        print(msg.text())
        await talker.say(qh(msg.text()))
        robot_state=0
    if msg.text() == '对联':
        robot_state = 3
    if  robot_state==3:
        await talker.say('已收到制作对联的请求 请发送您的上联')
        await talker.say('')
        print(msg.text()[0:])
        await talker.say(dl(msg.text()[0:]))
        robot_state=0
    if msg.text() == '风格融合':
        
        robot_state=11
        await talker.say('已收到制作情侣头像的请求')
        await talker.say('请发送您的风格图片')

    if msg.text() == '梵高星空风格':
        robot_state = 4
        await talker.say('已收到制作 梵高星空风格情侣头像 请求 请发送您的头像')
    if msg.text() == '海洋风格':
        robot_state = 5
        await talker.say('已收到制作 海洋风格情侣头像 请求 请发送您的头像')
    if msg.text() == '电子线路风格':
        robot_state = 6
        await talker.say('已收到制作电子线路风格情侣头像请求 请发送您的头像')
    if msg.text()=='星云风格':
        robot_state=7
        await talker.say('已收到制作星云风格情侣头像请求 请发送您的头像')
    if msg.text()=='宫崎骏《起风了》':
        robot_state=8
        await talker.say('已收到制作宫崎骏《起风了》风格情侣头像请求 请发送您的头像')
        
    if msg.text()=='新海诚《你的名字》':
        robot_state=9
        await talker.say('已收到制作新海诚《你的名字》风格情侣头像请求 请发送您的头像')
        
    if msg.text()=='今敏《红辣椒》':
        robot_state=10
        await talker.say('已收到制作今敏《红辣椒》风格情侣头像请求 请发送您的头像') 
        
        
    if robot_state == 8 and msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
        
         #  宫崎骏《起风了》
        await talker.say('已收到图像，开始模拟中')    
        
        file_box_2 = await msg.to_file_box()

        # 获取图片名
        img_name = file_box_2.name

        # 图片保存的路径
        img_path = './image/' + img_name

        # 将图片保存为本地文件
        await file_box_2.to_file(file_path=img_path)
        
        style='animegan_v1_hayao_60'

        # 调用图片风格转换的函数
        img_new_path = img_transform(img_path, img_name,style)

        # 从新的路径获取图片
        file_box_3 = FileBox.from_file(img_new_path)

        await msg.say(file_box_3)

    if robot_state == 9 and msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
        
         #  新海诚《你的名字》
        await talker.say('已收到图像，开始模拟中')    
        
        file_box_2 = await msg.to_file_box()

        # 获取图片名
        img_name = file_box_2.name

        # 图片保存的路径
        img_path = './image/' + img_name

        # 将图片保存为本地文件
        await file_box_2.to_file(file_path=img_path)
        
        style='animegan_v2_shinkai_33'

        # 调用图片风格转换的函数
        img_new_path = img_transform(img_path, img_name,style)

        # 从新的路径获取图片
        file_box_3 = FileBox.from_file(img_new_path)

        await msg.say(file_box_3)        

    if robot_state == 10 and msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
        
        await talker.say('已收到图像，开始模拟中')    
        
        file_box_2 = await msg.to_file_box()

        # 获取图片名
        img_name = file_box_2.name

        # 图片保存的路径
        img_path = './image/' + img_name

        # 将图片保存为本地文件
        await file_box_2.to_file(file_path=img_path)
        
        style='animegan_v2_paprika_74'

        # 调用图片风格转换的函数
        img_new_path = img_transform(img_path, img_name,style)

        # 从新的路径获取图片
        file_box_3 = FileBox.from_file(img_new_path)
        
        await msg.say(file_box_3)          

    if robot_state == 11 and msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
        
        await talker.say('已收到风格图片')    
        
        file_box_style = await msg.to_file_box()

        # 获取图片名
        img_name_style = file_box_style.name

        # 图片保存的路径
        img_path_style = './image/' + img_name_style

        # 将图片保存为本地文件
        await file_box__style.to_file(file_path=img_path_style)
        
        await talker.say('请输入一张头像')
        
        file_box_img1 = await msg.to_file_box()

        # 获取图片名
        img_name_img1 = file_box_img1.name

        # 图片保存的路径
        img_path_img1 = './image/' + img_name_img1

        # 将图片保存为本地文件
        await file_box__img1.to_file(file_path=img_path_img1)        


        # 调用图片风格转换的函数
        img_new_path = stylepro(img_path_img1, img_name_img1,img_path_style,img_name_style)

        # 从新的路径获取图片
        file_box_3 = FileBox.from_file(img_new_path)
        
        await msg.say(file_box_3)    

async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)


async def on_login(user: Contact):
    print(user)


async def main():
    # 确保我们在环境变量中设置了WECHATY_PUPPET_SERVICE_TOKEN
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())
