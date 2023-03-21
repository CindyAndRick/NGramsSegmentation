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
    oneText = splitText('秦睿洋是朱瑞麒的儿子')
    # nGram.train(text, "n_gram")
    modelPath = 'model\model-1000lines-18443can-2304s.weights'
    nGram.loadModel(modelPath)
    print(nGram.predict(oneText))
    endTime = time.perf_counter()
    RunTime = endTime - startTime
    print('Running time: %s Seconds'%(RunTime))

if __name__ == '__main__':
    path = 'dataset/newsdata.txt'
    # testTrie()
    # print(splitText('你好，我是Rick，我来自623424中。过'))
    # print(splitText(readText(path)[0]))
    testNGram(path)