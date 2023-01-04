# -*- coding: utf-8 -*-
"""
@Project    : Movie-QA-System-1.0
@File       : main
@Email      : yanyuchen@zju.edu.cn
@Author     : Yan Yuchen
@Time       : 2023/1/4 22:54
"""
import json

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from process_question import Question

app = fastapi.FastAPI()

# 使用中间件以拓展跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建问题处理对象，这样模型就可以常驻内存
que = Question()


@app.get('/neo4j/search')
async def search(q: str):
    answer = que.question_process(q)
    print(que.raw_question)
    res_dict = {
        "raw_question": que.raw_question,
        "pos_question": que.pos_question,
        "template": que.question_template_id_str,
        "cql": que.questiontemplate.cql,
        "answer": answer}
    return res_dict
