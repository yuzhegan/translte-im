# encoding='utf-8

# @Time: 2024-04-25
# @File: %
#!/usr/bin/env
from icecream import ic
import os

from openai import OpenAI
import json

from openai import OpenAI
client = OpenAI(api_key='sk-s5FeMy0tzTcwa2uyDcBf3c6606C140038a7f904888309aE7',
                base_url='https://cf.luouse.site/v1')
# client = OpenAI()


def translate_text(text, target_language, model):
    completion = client.chat.completions.create(
        model = model,
        messages=[
            {"role": "system", "content": f"You are a professional, authentic translation engine. You translate the input text to {target_language}, returning only the translated text without any explanations."},
            {"role": "user", "content": text}
        ]
    )
    # message = completion.choices[0].message
    if completion.choices and completion.choices[0].message:
        # 直接打印消息内容
        print(completion.choices[0].message.content)
    else:
        print("No translation result.")

    # print(message['content'])
    return


translate_text("Запчасти Сальник коленвала Victor Reinz(FPM(Fluor-Kautschuk)) для Audi A6 II(C5) 1997-2005. Артикул 81-24292-10 - 550 р", "Chinese", "gpt-3.5-turbo")
translate_text("Запчасти Сальник коленвала Victor Reinz(FPM(Fluor-Kautschuk)) для Audi A6 II(C5) 1997-2005. Артикул 81-24292-10 - 550 р", "English", "gpt-3.5-turbo")
