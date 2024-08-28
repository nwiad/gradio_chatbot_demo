import json
import requests
import time
import time
import pandas as pd
import random
import json
import query_routing_prompt
import logging
from env import discriminator_url

class QueryCanNotProcessRoutingDiscriminator:
    
    def __init__(self,url=None):

        self.url = discriminator_url
        self.QUERY_ROUTING_TEMPLATE = query_routing_prompt.QUERY_ROUTING_CAN_NOT_PROCESS_TEMPLATE
        self.npc_name = '智能NPC'
        self.logger = logging.getLogger('logger')

    def query_routing(self,input_):

        url = self.url

        messages = [
                    {
                        "role": "user",
                        "content": input_
                    }
                ]

        body = {
                "model": "qwen1.5-7b_query_cls",        # 模型名，与服务端对齐
                "stop": "<|im_end|>",       # 生成终止符
                "temperature": 0,
                # "top_p": 0.8,
                # "repetition_penalty": 1.1,
                "max_tokens": 64,
                "seed": int(time.time()),    # 随机数种子
                "messages": messages
            }


        try:
            print(requests.post(url, json=body))
            r = requests.post(url, json=body).json()
            reply = r["choices"][0]["message"]["content"]
        except:
            reply = 'None'
        return reply



    def _parse_chat_history(self,chat_history):
        context_query = sum(chat_history, [])
        roles = ['玩家', self.npc_name]
        for i, c in enumerate(context_query):
            if c is None:
                continue
            c = f'{roles[i % 2]}：{c}'
            context_query[i] = c
        context_query = list(filter(None, context_query))
        return context_query[:-1], context_query[-1]

    def get_query_routing(self,chat_history):
        context, query = self._parse_chat_history(chat_history)
        if len(context)!= 0 and "玩家：" in context[0]:
            context = '\n'.join(context[:])
        elif len(context) == 0 :
            context = ""
        else:
            context = '\n'.join(context[:])


        if context == '':
            chat_history = '玩家：'+query
        else:
            chat_history = context+'\n玩家：'+query

        chat_history = chat_history.replace('GG',self.npc_name)
        print(chat_history,query)
        input_ = self.QUERY_ROUTING_TEMPLATE.format(chat_history=chat_history, query=query)

        output = self.query_routing(input_)
        self.logger.info(f'【query路由模型判断是否可执行query】{output}')

        if output not in ['是','否']:
            output = '是'
        
        return True if output == '是' else False 

    def get_query_routing_for_demo(self, query, context):
        input_ = self.QUERY_ROUTING_TEMPLATE.format(chat_history=context, query=query)

        output = self.query_routing(input_)
        self.logger.info(f'【query路由模型判断是否可执行query】{output}')

        if output not in ['是','否']:
            output = '是'
        
        return True if output == '是' else False 

