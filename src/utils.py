import requests
import json
import gradio as gr
from settings import settings
from query_rewrite import query_rewrite_tmp
from query_routing_prompt import QUERY_ROUTING_CAN_NOT_PROCESS_TEMPLATE as query_routing_template
from safety_check import prompt as safety_check_prompt
from env import auth_key, chat_url, azure_url, azure_api_key

QPILOT_AVAILABLE = False

def request_api(messages):
    if QPILOT_AVAILABLE:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_key}"
        }
        data = {
            "model": "gpt-4",
            "stream": False,
            'messages': messages
        }
        res = requests.post(chat_url, headers=headers, data=json.dumps(data))
        return res
    else:
        headers = {
            'Content-Type': 'application/json', 
            'api-key': azure_api_key
        }
        data = {
            'max_tokens': 1024,
            "temperature": 0.2,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 0.95,
            'messages': messages
        }
        res = requests.post(
            azure_url,
            headers=headers,
            data=json.dumps(data)
        )
        return res    

def create_messages(system_prompt, input_content, history):
    res = [{"role": "system", "content": system_prompt}]
    for record in history:
        res.append({"role": "user", "content": record[0]})
        res.append({"role": "assistant", "content": record[1]})

    res.append({"role": "user", "content": input_content})
    print(f"messages: {res}")
    return res

def chat_completion(input_content, history, character):
    print(f"{character=}")
    print(f"{history=}")
    system_prompt = f"你将扮演{character}，你要根据以下设定回复用户（PC）：{settings[character]}"
    res = request_api(create_messages(system_prompt, input_content, history))
    try:
        evaluation = res.json()["choices"][0]["message"]["content"]
        return evaluation
    except:
        print(f"{input_content=}")
        print(f"res={res.json()}")
        gr.Warning("发生错误")
        return "<发生错误>"

def create_context(history, character):
    context = []
    for record in history:
        context.append(''.join(['玩家: ', record[0]]))
        context.append(''.join([f'{character}: ', record[1]]))
    return '\n'.join(context)

def rewrite_query(query, history, character):
    print(f"{query=}")
    # print(f"{history=}")
    # print(f"{character=}")
    context = create_context(history, character)
    print(f"{context=}")
    res = request_api([{"role": "user", "content": query_rewrite_tmp.format(context, query)}])
    try:
        evaluation = res.json()["choices"][0]["message"]["content"]
        return evaluation
    except:
        print(f"res={res.json()}")
        gr.Warning("发生错误")
        return None

def boundary_filter(query, history, character):
    context = create_context(history, character)
    res = request_api([{"role": "user", "content": query_routing_template.format(chat_history=context, query=query)}])
    try:
        evaluation = res.json()["choices"][0]["message"]["content"]
    except:
        print(f"res={res.json()}")
        gr.Warning("发生错误")
        return None

    print(f'query routing evaluation: {evaluation}')

    if evaluation not in ['是','否']:
        evaluation = '是'

    if evaluation == '是':
        gr.Info("可执行")
        return query
    else:
        gr.Warning("不可执行")
        return None

def check_for_safety(history):
    last_record = history[-1]
    query = last_record[0]
    response = last_record[1]
    res = request_api([{"role": "user", "content": safety_check_prompt.format(query=query, response=response)}])
    try:
        evaluation = res.json()["choices"][0]["message"]["content"]
        gr.Info(f"回复评估：{evaluation}")
    except:
        print(f"res={res.json()}")
        gr.Warning("发生错误")