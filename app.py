# encoding='utf-8

# @Time: 2024-04-25
# @File: %
#!/usr/bin/env
from icecream import ic
from pydantic import BaseModel
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder  # 导入jsonable_encoder来处理MongoDB文档
from bson import ObjectId
from openai import OpenAI


app = FastAPI()


# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Translate(BaseModel):
    text: str
    model: str = 'gpt-3.5-turbo'
    source_lang: str
    target_langulage: str

# 定义一个可以用来切换的API密钥和base_url
api_keys = [
    ('sk-Nm7wjb4E0uHMCGuS0130357b6732458d92062c7eB5111c8f', 'https://run.v36.cm/v1'),
    ('sk-vxai76FlE154fhnx5963819d87164b15B87bFbD61fE70881', 'https://api.oaipro.com/v1')
]

@app.post("/translate")
async def get_translte(translate: Translate):
    # 初始使用第一个API密钥
    api_key, base_url = api_keys[0]
    
    # 提取请求中的参数
    text = translate.text.strip().replace(",", "").replace("，", "")
    model = translate.model
    source_lang = translate.source_lang
    target_language = translate.target_langulage
    
    # ic(text, model, source_lang, target_language)
    
    # 封装翻译请求
    def request_translation(api_key, base_url):
        ic(api_key, base_url)
        client = OpenAI(api_key=api_key, base_url=base_url)
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a professional, authentic translation engine. You translate the input text from {source_lang} to {target_language}, returning only the translated text without any explanations."},
                    {"role": "user", "content": text}
                ]
            )
            # 判断返回结果是否有效
            if completion.choices and completion.choices[0].message:
                return completion.choices[0].message.content
            else:
                return "No translation result."
        except Exception as e:
            ic(f"Error: {e}")
            return None

    # 首先尝试使用第一个API密钥
    translated_text = request_translation(api_key, base_url)
    # ic(translated_text)
    
    # 如果第一个API密钥失败，尝试使用第二个API密钥
    if not translated_text:
        api_key, base_url = api_keys[1]
        translated_text = request_translation(api_key, base_url)
    
    if translated_text:
        return translated_text
    else:
        return "Translation failed after retrying with a different API key."






class deepseekv2(BaseModel):
    source_lang: str
    target_lang: str
    text_list: list


@app.post("/deepseekv2")
async def deepseektranslate(deepseekv2: deepseekv2):
    client = OpenAI(api_key="sk-b9c5cedfa1ab418c8711df72e23a1f6e",
                    base_url="https://api.deepseek.com/")
    source_lang = deepseekv2.source_lang
    target_lang = deepseekv2.target_lang
    # text_list = deepseekv2.text_list
    full_text = "\n".join(deepseekv2.text_list)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"You are a professional, authentic translation engine. You only return the translated text, without any explanations."},
            {"role": "user",
                "content": f"Please translate into {target_lang} (avoid explaining the original text):{full_text}"}
        ]
    )
    try:
        # Accessing the response content safely
        translated_text = response.choices[0].message.content
    except IndexError:
        raise HTTPException(
            status_code=500, detail="Translation failed or no content returned")
    ic(translated_text)
    # datas = {
    #         "translations": translated_text.split("\n"),
    #         "detected_source_lang": full_text + " " + source_lang,
    #         "text": translated_text
    #
    #         }
    translated_texts = translated_text.split("\n")
    datas = {
        "translations": [{
            "detected_source_lang": source_lang,
            "text": item
        } for item in translated_texts],
        
    }
    ic(datas)

    return datas

    # return (response.choices[0].message.content)


if __name__ == "__main__":
    # exit()
    uvicorn.run("app:app", reload=True, port=5055, host="0.0.0.0")
