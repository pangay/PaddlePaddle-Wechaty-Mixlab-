import cv2
import os
os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'puppet_padlocal_1320c819baf548c4a20f394443422b70'
os.environ['WECHATY_PUPPET']='wechaty-puppet-service'
os.environ['WECHATY_PUPPET_HOSTIE_TOKEN'] = 'puppet_padlocal_1320c819baf548c4a20f394443422b70'
import asyncio
import logging
import paddlehub as hub
from typing import Optional, Union
from wechaty_puppet import FileBox, ScanStatus  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# 定义paddlehub模型
model_animegan_v1_hayao_60 = hub.Module(name='animegan_v1_hayao_60', use_gpu=False)
model_animegan_v2_shinkai_33 = hub.Module(name='animegan_v2_shinkai_33', use_gpu=False)
module_ernie_gen_lover_words = hub.Module(name="ernie_gen_lover_words")
model_animegan_v2_paprika_74=hub.Module(name='animegan_v2_paprika_74',use_gpu=False)
model_stylepro_artistic=hub.Module(name='stylepro_artistic')
# 将图片转换为动漫风格
# 一键情话生成
def qh(data):
    results = module_ernie_gen_lover_words.generate(texts=[data], use_gpu=False, beam_width=1)
    for result in results:
        print(results)
        return result[0]
#新海诚风格
def img_to_anime_animegan_v2_shinkai_33(img_name, img_path):
    # 图片名保持不变
    img_new_name = img_name

    # 图片路径改变
    img_new_path = './images-new/' + img_new_name

    # 模型预测
    result = model_animegan_v2_shinkai_33.style_transfer(images=[cv2.imread(img_path)])

    # 将新图片存储到新路径
    cv2.imwrite(img_new_path, result[0])

    return img_new_path

#宫崎骏风格
def img_to_anime_animegan_v1_hayao_60(img_name, img_path):
    # 图片名保持不变
    img_new_name = img_name

    # 图片路径改变
    img_new_path = './images-new/' + img_new_name

    # 模型预测
    result = model_animegan_v1_hayao_60.style_transfer(images=[cv2.imread(img_path)])

    # 将新图片存储到新路径
    cv2.imwrite(img_new_path, result[0])

    return img_new_path

# 将第一张图片转换为第二张图片的风格
def img_to_art(img_name, img_path, img_art_path):
    # 图片名保持不变
    img_new_name = img_name

    # 图片路径改变
    img_new_path = './images-new/' + img_new_name

    # 模型预测
    result = model_stylepro_artistic.style_transfer(images=[{'content': cv2.imread(img_path),'styles': [cv2.imread(img_art_path)]}],)

    # 将新图片存储到新路径
    cv2.imwrite(img_new_path, result[0]['data'])

    return img_new_path

class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    step = 0
    def __init__(self):
        super().__init__()

        # 图像信息
        # [flag, img, img_name, img_path, img_new_name, img_new_path]
        self.img = [True, None, None, None, None, None]
    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        global state
        from_contact = msg.talker()
        text = msg.text()
        type = msg.type()
        room = msg.room()
        # 不处理群消息
        if room is None:
            if text == 'hi' or text == '你好':
                conversation = from_contact
                await conversation.ready()
                await conversation.say(
                    '这是自动回复：机器人目前的功能有：\n1 回复"一键情话"，LoveAssestentBot教你说情话\n2 收到"情头"，自动回复一组情头\n3发送“情头生成器”，带你体验不同风格的情侣头像\n 4.发送“风格转换”带你体验制作自己喜欢的风格情头')
            if text=='情头生成器':
                conversation=from_contact
                await  conversation.ready()
                await  conversation.say('这里是情头生成器，请选择您想要的风格现在有\n1.宫崎骏风格\n2.新海诚风格\n3.金敏风格')

            if text == 'ding':
                conversation = from_contact
                await conversation.ready()
                await conversation.say('这是自动回复：dong dong dong')

            if text == '情头':
                conversation = from_contact

                # 从网络上加载图片到file_box
                img_url = 'https://t7.baidu.com/it/u=2926722410,2866117818&fm=193'
                file_box = FileBox.from_url(img_url, name='xx.jpg')
                img_url_2 = 'https://t9.baidu.com/it/u=899028494,1464612359&fm=193'
                file_box_2 = FileBox.from_url(img_url_2, name='xx.jpg')
                await conversation.ready()
                await conversation.say('这是自动回复：')
                await conversation.say(file_box)
                await conversation.say(file_box_2)
            if text == '风格转换':
                self.img[1] = 0
                state=3
                conversation = from_contact
                await conversation.ready()
                await conversation.say('这是自动回复：请输入您想转化的图片')
            if text == '一键情话':
                conversation = from_contact
                await conversation.say('已收到制作情话的请求 请发送1+您的关键词')
            if text[0] == '1':
                conversation = from_contact
                await conversation.say('已经收到你的心意' + text[1:] + '，请您稍等哦')
                print(text[1:])
                await conversation.say(qh(text[1:]))
            if text == '宫崎骏风格':
                conversation = from_contact
                state = 1
                await conversation.say('这是自动回复：请发送一张图片 会按输出宫崎骏风格')
            if text == '新海诚风格':
                conversation = from_contact
                state = 2
                await conversation.say('这是自动回复：请发送一张图片 会按输出新海诚风格')
            # 如果消息类型是图片
            if state == 1 and type == Message.Type.MESSAGE_TYPE_IMAGE:
                conversation = from_contact
                await conversation.ready()
                await conversation.say('这是自动回复：正在飞速处理中...')

                # 将msg转换为file_box
                file_box = await msg.to_file_box()

                # 获取图片名
                img_name = file_box.name

                # 图片保存的路径
                img_path = './images/' + img_name

                # 将图片保存到文件中
                await file_box.to_file(file_path=img_path, overwrite=True)

                # 调用函数，获取图片新路径
                img_new_path = img_to_anime_animegan_v1_hayao_60(img_name, img_path)

                # 从文件中加载图片到file_box
                file_box_new = FileBox.from_file(img_new_path)

                await conversation.say(file_box_new)
            if state == 2 and type == Message.Type.MESSAGE_TYPE_IMAGE:
                step=0
                conversation = from_contact
                await conversation.ready()
                await conversation.say('这是自动回复：正在飞速处理中...')

                # 将msg转换为file_box
                file_box = await msg.to_file_box()

                # 获取图片名
                img_name = file_box.name

                # 图片保存的路径
                img_path = './images/' + img_name

                # 将图片保存到文件中
                await file_box.to_file(file_path=img_path, overwrite=True)

                # 调用函数，获取图片新路径
                img_new_path = img_to_anime_animegan_v2_shinkai_33(img_name, img_path)

                # 从文件中加载图片到file_box
                file_box_new = FileBox.from_file(img_new_path)

                await conversation.say(file_box_new)
                # 如果消息类型是图片
            if state == 3 and type == Message.Type.MESSAGE_TYPE_IMAGE:
                self.img[0] = not self.img[0]
                if self.img[1] == 0:
                    self.img[1] = 1
                        # 将msg转换为file_box
                    file_box = await msg.to_file_box()

                        # 获取图片名
                    self.img[2] = file_box.name
                    # 图片保存的路径
                    self.img[3] = './images/' + self.img[2]

                    # 将图片保存到文件中
                    await file_box.to_file(file_path=self.img[3], overwrite=True)

                    conversation = from_contact
                    await conversation.ready()
                    await conversation.say('这是自动回复：请输入风格图片')



                if self.img[1] == 1 and self.img[0]:
                    self.img[1] = None
                    conversation = from_contact
                    await conversation.ready()
                    await conversation.say('这是自动回复：正在飞速处理中...')

                # 将msg转换为file_box
                    file_box_art = await msg.to_file_box()

                # 获取图片名
                    self.img[4] = file_box_art.name

                # 图片保存的路径
                    self.img[5] = './images/' + self.img[4]

                # 将图片保存到文件中
                    await file_box_art.to_file(file_path=self.img[5], overwrite=True)

                # 调用函数，获取图片新路径
                    img_new_path = img_to_art(self.img[2], self.img[3], self.img[5])

                # 从文件中加载图片到file_box
                    file_box_new = FileBox.from_file(img_new_path)

                    await conversation.say(file_box_new)
    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


bot: Optional[MyBot] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = MyBot()
    await bot.start()


asyncio.run(main())