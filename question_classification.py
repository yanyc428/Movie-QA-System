# -*- coding: UTF-8 -*-
# 对问题进行分类

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
from sklearn.linear_model import LogisticRegression
from nodes import GraphNodes
from functools import partial


class LRClassifier(object):

    def read_train_data(self):
        train_x = []
        train_y = []
        # 读取文件内容
        with(open("./questions/label.txt", "r", encoding="utf-8")) as fr:
            lines = fr.readlines()
            for one_line in lines:
                temp = one_line.split('	')
                # print(temp)
                word_list = list(jieba.cut(str(temp[1]).strip()))
                # 将这一行加入结果集
                train_x.append(" ".join(word_list))
                train_y.append(temp[0])

        self.train_x, self.train_y = train_x, train_y

    def __init__(self):
        # 读取训练数据
        self.read_train_data()
        # 训练模型
        self.tv = TfidfVectorizer()
        self.model = self.train_model_lr()
        self._nodes = GraphNodes()
        self._actors = self._nodes.get_actors()
        self._movies = self._nodes.get_movies()
        self._type = self._nodes.get_type()

        for word in self._actors:
            jieba.add_word(word)
        for word in self._movies:
            jieba.add_word(word)
        for word in self._type:
            jieba.add_word(word)

    def train_model_lr(self):
        x_train, y_train = self.train_x, self.train_y
        train_data = self.tv.fit_transform(x_train).toarray()
        clf = LogisticRegression(solver='liblinear', max_iter=5000, multi_class='ovr')
        clf.fit(train_data, y_train)
        return clf

    def transform_question(self, question):

        raw_words = list(jieba.cut(question))
        words = list(jieba.cut(question))

        def transform_movies(x):
            return "nm" if x in self._movies else x

        def transform_actors(x):
            return "nnt" if x in self._actors else x

        def transform_type(x):
            return "ng" if x in self._type else x

        def transform_numbers(x):
            try:
                float(x)
                return "x"
            except ValueError:
                return x

        methods = [transform_movies, transform_actors, transform_type, transform_numbers]

        for method in methods:
            words = map(method, words)

        return " ".join(raw_words), " ".join(words)


    def predict(self, question):
        question = [self.transform_question(question)[1]]
        test_data = self.tv.transform(question).toarray()
        y_predict = self.model.predict(test_data)[0]
        return int(y_predict)


if __name__ == '__main__':
    qc = LRClassifier()
    print(qc.predict("章子怡出生在哪里"))
    print(qc.transform_question("章子怡出生在哪里"))
