#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Tseng. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import os
import logging
import multiprocessing

from prettyprinter import cpprint
from gensim.models import word2vec
from gensim.corpora import WikiCorpus

from utils import cht_to_chs_zhconv, cut_sentence, remove_non_chinese

LOG = logging.getLogger(__name__)


class ZhWikiWord2Vec(object):
    """专用于处理 zhwiki 语料的词向量模型"""

    def __init__(self, corpus_path):
        _output_dir = 'output'
        _text_ext = 'txt'
        _model_ext = 'mdl'
        _vector_ext = 'vec'

        data_dir, corpus_file = os.path.split(corpus_path)
        name = corpus_file.split('.', 1)[0]

        # 生成输出目录路径
        if data_dir.endswith('data'):
            _output_dir = 'output'.join(data_dir.rsplit('data', 1))
        else:
            _output_dir = os.path.join(data_dir, 'output')

        # 创建输出目录
        if not os.path.exists(_output_dir):
            os.makedirs(_output_dir)

        # 生成结果文件路径
        self.corpus_path = os.path.join(data_dir, corpus_file)
        self.text_path = os.path.join(
            _output_dir, '%s.%s' % (name, _text_ext))
        self.model_path = os.path.join(
            _output_dir, '%s.%s' % (name, _model_ext))
        self.vector_path = os.path.join(
            _output_dir, '%s.%s' % (name, _vector_ext))

    def prepare_corpus(self):
        """
        将原始 Wiki 语料文件转化为文本文件，同时进行简体化和分词处理，保存为 UTF-8 编码
        :param:
        :return:
        """
        if os.path.exists(self.text_path):
            LOG.info('Text file already exists, skip prepare_corpus().')
            return
        if not os.path.exists(self.corpus_path):
            LOG.error('Corpus file [%s] not exists, please put it under '
                      'data directory' % self.corpus_path)
            exit(1)

        i = 0
        space = ' '

        LOG.info('Start processing wiki corpus into texts ...')

        # 读入指定的 wiki 归档文件，生成语料
        corpus_file = WikiCorpus(self.corpus_path,
                                 lemmatize=False, dictionary={})

        with open(self.text_path, 'wb') as text_file:
            for tokens in corpus_file.get_texts():
                # 将 tokens 列表拼接成一个字符串
                line = space.join(tokens)
                # 将 line 简体化、分词并去除非中文词语
                line = cht_to_chs_zhconv(line)
                tokens = cut_sentence(line)
                tokens = remove_non_chinese(tokens)
                line = ' '.join(tokens) + '\n'
                # 结果写入语料文本文件
                text_file.write(bytes(line, encoding='utf-8'))
                i = i + 1
                if i % 10000 == 0:
                    LOG.info('Saved articles: %d ...' % i)

        LOG.info('End processing corpus. Saved %d articles' % i)

    def train_model(self):
        """
        训练词向量模型，要求先将原始语料转化为分词后的文本语料
        :param:
        :return:
        """
        if os.path.exists(self.model_path):
            LOG.info('Model file already exists, skip train_model().')
            return

        LOG.info('Start training word2vec model ...')

        # 词向量训练
        ls = word2vec.LineSentence(self.text_path)
        mdl = word2vec.Word2Vec(ls, size=350, window=5, min_count=10,
                                workers=multiprocessing.cpu_count())

        # trim unneeded model memory = use(much) less RAM
        mdl.wv.init_sims(replace=True)

        # 保存模型
        mdl.save(self.model_path)
        mdl.wv.save_word2vec_format(self.vector_path, binary=False)

        LOG.info('End training word2vec model. Output files: %s, %s'
                 % (self.model_path, self.vector_path))

    def test_model(self, words):
        """
        测试词向量模型，查找每个词语最相近的 10个词
        :param words: 待测试的词语列表
        :return:
        """
        if not os.path.exists(self.model_path):
            LOG.error('Model file not exists, please train the model first')
            exit(1)

        if not isinstance(words, list):
            words = [words]

        LOG.info('Testing model with words %s' % str(words))

        # 加载词向量模型
        mdl = word2vec.Word2Vec.load(self.model_path)

        for word in words:
            try:
                # 查找与 word 最相近的 10个词
                tops = mdl.wv.most_similar(word, topn=10)
                print('\nWords most related to "%s":' % word)
                cpprint(tops)
            # 捕获异常并跳过，比如 word 不在词汇表中会抛出 KeyError
            except Exception as e:
                print('\nError:', repr(e))
