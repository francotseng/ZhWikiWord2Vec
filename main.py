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


import sys
import logging

from zhwiki_word2vec import ZhWikiWord2Vec

logging.basicConfig(format='%(asctime)s - %(name)s '
                           '[%(levelname)s]: %(message)s', level=logging.INFO)
LOG = logging.getLogger(__name__)


def main():
    """
    Simple stdin/stdout interface.
    """
    words = ['自然语言', '国庆']
    corpus_path = 'data/zhwiki-latest-pages-articles.xml.bz2'

    if len(sys.argv) > 1:
        words = sys.argv[1:]

    # 初始化 Word2Vec 对象
    word2vec = ZhWikiWord2Vec(corpus_path)

    # Step 1：数据预处理，得到简体化、分词后的文本数据
    word2vec.prepare_corpus()
    # Step 2：Word2Vec 模型训练
    word2vec.train_model()
    # Step 3：模型测试
    word2vec.test_model(words)


if __name__ == '__main__':
    sys.exit(main())
