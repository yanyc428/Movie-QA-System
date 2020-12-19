# -*- coding: utf-8 -*-

from process_question import Question
# 创建问题处理对象，这样模型就可以常驻内存
print("start")
que=Question()
print("end")
result=que.question_process("李连杰生日是哪天？")
print(result)
