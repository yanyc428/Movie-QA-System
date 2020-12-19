# -*- coding: UTF-8 -*-
'''
接收原始问题
对原始问题进行分词、词性标注等处理
对问题进行抽象
'''

import os
import re
import sys

import jieba.posseg

from question_classification import  LRClassifier
from question_template import QuestionTemplate


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


# blockPrint()
# enablePrint()

class Question():
    def __init__(self):
        # 初始化相关设置：读取词汇表，训练分类器，连接数据库
        # 训练分类器
        self.classify_model = LRClassifier()
        # 读取问题模板
        with(open("./questions/question_classification.txt", "r", encoding="utf-8")) as f:
            question_mode_list = f.readlines()
        self.question_mode_dict = {}
        for one_mode in question_mode_list:
            # 读取一行
            mode_id, mode_str = str(one_mode).strip().split(":")
            # 处理一行，并存入
            self.question_mode_dict[int(mode_id)] = str(mode_str).strip()
        # 创建问题模板对象
        self.questiontemplate = QuestionTemplate()

    def question_process(self, question):
        # 接收问题
        self.raw_question, self.pos_question = self.classify_model.transform_question(question)
        # 得到问题的模板
        self.question_template_id_str = self.get_question_template()
        # 查询图数据库,得到答案
        self.answer = self.query_template()
        return self.answer


    def get_question_template(self):
        # # 通过分类器获取问题模板编号
        question_template_num = self.classify_model.predict(self.raw_question)
        # print("使用模板编号：", question_template_num)
        question_template = self.question_mode_dict[question_template_num]
        # print("问题模板：", question_template)
        question_template_id_str = str(question_template_num) + "\t" + question_template
        return question_template_id_str

    # 根据问题模板的具体类容，构造cql语句，并查询
    def query_template(self):
        # 调用问题模板类中的获取答案的方法
        try:
            answer = self.questiontemplate.get_question_answer(self.raw_question, self.pos_question, self.question_template_id_str)
            if answer == '':
                answer = "数据库作者太懒啦，这里什么都没有！！！"
        except Exception as e :
            print(e)
            answer = "我也不知道啊！"
        return answer
