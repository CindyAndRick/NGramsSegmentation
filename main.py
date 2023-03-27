from nGram import NGram, Trie
from utils import splitText, readText
import time

def testTrie():
    trie = Trie()
    trie.insert('hello')
    trie.insert('world')
    trie.insert('hi')
    trie.insert('hi')
    trie.print()
    print(trie.search('hi'))
    print(trie.search('hello'))
    print(trie.search('world'))
    print(trie.search('h'))
    trie.drop('hi')
    print(trie.search('hi'))
    trie.print()

def testNGram(path):
    startTime = time.perf_counter()
    nGram = NGram()
    # text = splitText(readText(path, 1000))
    oneText = splitText('在这一年中，中国的改革开放和现代化建设继续向前迈进。国民经济保持了“高增长、低通胀”的良好发展态势。农业生产再次获得好的收成，企业改革继续深化，人民生活进一步改善。对外经济技术合作与交流不断扩大。民主法制建设、精神文明建设和其他各项事业都有新的进展。我们十分关注最近一个时期一些国家和地区发生的金融风波，我们相信通过这些国家和地区的努力以及有关的国际合作，情况会逐步得到缓解。总的来说，中国改革和发展的全局继续保持了稳定。')
    # nGram.train(text, "one_time")
    modelPath = 'model\model-2023-03-25 18-59-18.912687-41484.weights'
    idiomPath = 'dataset/myIdioms.txt'
    nGram.loadModel(modelPath)
    # nGram.loadIdioms(idiomPath)
    print(nGram.predict(oneText))
    endTime = time.perf_counter()
    RunTime = endTime - startTime
    print('Running time: %s Seconds'%(RunTime))

def shell():
    nGram = NGram()
    modelPath = 'model\model-2023-03-25 18-59-18.912687-41484.weights'
    idiomPath = 'dataset/myIdioms.txt'
    nGram.loadModel(modelPath)
    nGram.loadIdioms(idiomPath)
    while True:
        sentence = input('请输入一句话：')
        if sentence == 'exit':
            break
        # nGram.train(splitText(sentence), "one_time", save=False)
        print(nGram.predict(splitText(sentence)))

if __name__ == '__main__':
    path = 'dataset/newsdata.txt'
    # testTrie()
    # print(splitText('你好，我是Rick，我来自623424中。过'))
    # print(splitText(readText(path)[0]))
    # testNGram(path)
    shell()