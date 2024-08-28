import requests
import time
import pandas as pd
from env import rewrite_url

query_rewrite_tmp="""请你帮助我完成以下玩家提问改写任务。目的是根据上下文，改写和完善玩家当前提问。

请使用以下方式进行改写： 
1.输出标准化，你的输出必须满足：符号是中文半角；数字统一用中文的形式（11——>十一） 
2.指代消解：从历史对话中推理出代词所指，并替换之（稷下通：你知道学士鹅吗？玩家：他好棒（替换成学士鹅好棒）） 
3.信息补全：根据历史对话完整玩家提问（稷下通：你知道学士鹅吗？玩家：没听过（我没听过学士鹅）） 

请尽可能满足改写结果标准： 
1.正确：改写前后意思不变 
2.明晰：改写之后的当前玩家提问应该独立于对话，即便单独看也能明确看懂，无歧义 
3.信息丰富：尽可能从历史对话中整合更多的信息，便于检索器检索更多相关的有用信息 
4.表达简洁：不添加额外无关信息，不添加无意义的修辞 

现在开始你的任务： 
【历史对话】
{} 
【玩家当前提问】
{}
【玩家当前提问改写】
"""  

class QueryRewrite:
    
    def __init__(self): 
        pass
        
    def get_query_rewrite(self,chat_his_str, query):
        
        url = rewrite_url

        body = {
            "model": "qwen4b_query_rewrite",        # 模型名，与服务端对齐
            "stop": "<|im_end|>",       # 生成终止符
            "temperature": 0.8,
            "top_p": 0.8,
            "repetition_penalty": 1.1,
            "max_tokens": 64,
            "seed": int(time.time()),    # 随机数种子
            "messages": [
                {
                    "role": "user",
                    "content": query_rewrite_tmp.format(chat_his_str, query)
                }
            ]
        }

        r = requests.post(url, json=body).json()
        
        try:
            response = r["choices"][0]["message"]["content"]
        except:
            response = 'None'
        return response



if __name__ == '__main__':
    query_rewrite = QueryRewrite()
    print(query_rewrite.get_query_rewrite('','你是谁')) # chat history, query