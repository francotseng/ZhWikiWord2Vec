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


import re
import jieba
import zhconv

from opencc import OpenCC

cc = OpenCC('t2s')


def cht_to_chs_opencc(line):
    """
    将繁体转换成简体，使用 opencc 库
    :param line: 原始语句
    :return: 转化为简体的语句
    """
    line = cc.convert(line)
    return line


def cht_to_chs_zhconv(line):
    """
    将繁体转换成简体，使用 zhconv 库
    :param line: 原始语句
    :return: 转化为简体的语句
    """
    line = zhconv.convert(line, 'zh-cn')
    return line


def remove_non_chinese(tokens):
    """
    移除列表中的非中文元素
    :param tokens: 词语列表
    :return: 移除了非中文元素的列表
    """
    rst = []
    cn_reg = '^[\u4e00-\u9fa5]+$'

    for token in tokens:
        if re.search(cn_reg, token):
            rst.append(token)

    return rst


def cut_sentence(line):
    """
    将一行句子分解成词语列表
    :param line: 原始语句
    :return: 分词后的词语列表
    """
    return jieba.cut(line.replace(' ', ''))


def cut_and_remove_non_chinese(line):
    """
    将句子分词，然后移除其中的非中文词语
    :param line: 原始语句
    :return: 分词并移除了非中文词语的语句
    """
    tokens = jieba.cut(line.replace(' ', ''))
    tokens = remove_non_chinese(tokens)
    line_cut = ' '.join(tokens)
    return line_cut


def file_diff(path1, path2):
    """
    比较两个文本文件内容的差异
    :param path1: 第一个文本文件
    :param path2: 第二个文本文件
    :return:
    """
    i = 0
    count = 0

    print('Compare difference between [%s] and [%s] ...' % (path1, path2))

    with open(path1, 'r', encoding='utf-8') as f1, \
            open(path2, 'r', encoding='utf-8') as f2:
        for line1, line2 in zip(f1.readlines(), f2.readlines()):
            i += 1
            n = min(len(line1), len(line2))
            if line1 != line2:
                print("line %d:" % i, end='')
                for j in range(n):
                    if line1[j] != line2[j]:
                        count += 1
                        print(" [%s - %s]," % (line1[j], line2[j]), end='')
                print('')

    print('Total different words in two file: %d' % count)
