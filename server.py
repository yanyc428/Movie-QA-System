# -*- coding: utf-8 -*-
import json
from flask import Flask, request
import sys
from process_question import Question
from flask_cors import cross_origin


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


app = Flask(__name__, static_url_path="")
app.after_request(after_request)

# 创建问题处理对象，这样模型就可以常驻内存
que = Question()


@cross_origin
@app.route('/neo4j/search')
def search():
    text = request.args.get('q')
    answer = que.question_process(text)
    print(que.raw_question)
    res_dict = {
        "raw_question": que.raw_question,
        "pos_question": que.pos_question,
        "template": que.question_template_id_str,
        "cql": que.questiontemplate.cql,
        "answer": answer}
    res = json.dumps(res_dict, ensure_ascii=False)
    print(res)
    return res


if __name__ == '__main__':
    # 部署到服务器时host要改成'0.0.0.0'
    app.run(debug=False, host='0.0.0.0', port=5001)
