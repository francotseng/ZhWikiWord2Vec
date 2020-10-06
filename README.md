# ZhWikiWord2Vec
ZhWikiWord2Vec 项目实现了中英文维基百科语料上的 Word2Vec 实验。

将下载的语料数据归档文件 zhwiki-latest-pages-articles.xml.bz2 放到项目的 data/ 目录下，然后执行 main.py 文件，可以进行语料处理和词向量训练，并用输入的词语测试生成的模型。

## Examples
```bash
# python main.py 自然语言 人工智能 AI
2020-10-06 18:54:47,646 - zhwiki_word2vec [INFO]: Text file already exists, skip prepare_corpus().
2020-10-06 18:54:47,647 - zhwiki_word2vec [INFO]: Model file already exists, skip train_model().
2020-10-06 18:54:47,649 - zhwiki_word2vec [INFO]: Testing model with words ['自然语言', '人工智能', 'AI']
2020-10-06 18:54:47,649 - gensim.utils [INFO]: loading Word2Vec object from output/zhwiki-latest-pages-articles.mdl
2020-10-06 18:54:51,159 - gensim.utils [INFO]: loading wv recursively from output/zhwiki-latest-pages-articles.mdl.wv.* with mmap=None
2020-10-06 18:54:51,160 - gensim.utils [INFO]: loading vectors from output/zhwiki-latest-pages-articles.mdl.wv.vectors.npy with mmap=None
2020-10-06 18:54:55,935 - gensim.utils [INFO]: setting ignored attribute vectors_norm to None
2020-10-06 18:54:55,936 - gensim.utils [INFO]: loading vocabulary recursively from output/zhwiki-latest-pages-articles.mdl.vocabulary.* with mmap=None
2020-10-06 18:54:55,936 - gensim.utils [INFO]: loading trainables recursively from output/zhwiki-latest-pages-articles.mdl.trainables.* with mmap=None
2020-10-06 18:54:55,936 - gensim.utils [INFO]: loading syn1neg from output/zhwiki-latest-pages-articles.mdl.trainables.syn1neg.npy with mmap=None
2020-10-06 18:54:59,215 - gensim.utils [INFO]: setting ignored attribute cum_table to None
2020-10-06 18:54:59,215 - gensim.utils [INFO]: loaded output/zhwiki-latest-pages-articles.mdl
2020-10-06 18:55:00,405 - gensim.models.keyedvectors [INFO]: precomputing L2-norms of word weight vectors

Words most related to "自然语言":
[
    ('数据挖掘', 0.7077358961105347),
    ('语义学', 0.6923495531082153),
    ('词法', 0.6769447922706604),
    ('机器翻译', 0.6719241142272949),
    ('人工神经网络', 0.671123206615448),
    ('数据结构', 0.6686602830886841),
    ('可视化', 0.6656603813171387),
    ('正则表达式', 0.6653014421463013),
    ('语义', 0.6650019288063049),
    ('用例', 0.662421703338623)
]

Words most related to "人工智能":
[
    ('虚拟现实', 0.6142095327377319),
    ('计算机', 0.6076732873916626),
    ('电脑', 0.5972285270690918),
    ('机器人学', 0.5887557864189148),
    ('数据挖掘', 0.5884934663772583),
    ('超级计算机', 0.5790497064590454),
    ('电脑系统', 0.5771250128746033),
    ('软件工程', 0.5738922953605652),
    ('智能', 0.5677090883255005),
    ('软件开发', 0.5626024007797241)
]

Error: KeyError("word 'AI' not in vocabulary")
```

## Notes
语料文件下载链接：https://dumps.wikimedia.org/zhwiki/latest/

## References
[中英文维基百科语料上的Word2Vec实验](https://www.52nlp.cn/%E4%B8%AD%E8%8B%B1%E6%96%87%E7%BB%B4%E5%9F%BA%E7%99%BE%E7%A7%91%E8%AF%AD%E6%96%99%E4%B8%8A%E7%9A%84word2vec%E5%AE%9E%E9%AA%8C/comment-page-1)
