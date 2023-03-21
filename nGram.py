from trie import Trie
from datetime import datetime

class NGram:
    def __init__(self, n=7):
        self.n = n
        self.trie = Trie()
        self.candidates = []

    # type: "n_gram": 原本算法, "one_time": 改进算法
    def train(self, sentences, type="one_time", save=True):
        print("training with {}".format(type))
        # 获取初次分割
        print("total sentences length:", len(sentences))
        for i, sentence in enumerate(sentences):
            if i % 10000 == 0:
                print("{}/{}".format(i, len(sentences)))
            # 若n大于句子长度时，窗口长度应当减小至句子长度
            windowSize = min(self.n, len(sentence))

            # 从句子的第一个字开始，每次向后移动一个字，直到窗口到达句子末尾
            for i in range(len(sentence) - windowSize + 1):
                # 将长度大于2的全部插入trie树
                for j in range(1, windowSize):
                    self.trie.insert(sentence[i:i+j+1])

        # 获取candidates
        self.trie.find(self.trie, "", self.candidates)
        # 按照长度从大到小排序，长度相同的按照出现次数从大到小排序
        self.candidates = sorted(self.candidates, key=lambda x: (len(x["str"]), x["count"]), reverse=True)
        print("candidates length:", len(self.candidates))

        if type == "n_gram":
            time = 0
            while self.check(sentences):
                time += 1
                for sentence in sentences:
                    curCandidates = [candidate for candidate in self.candidates if candidate["str"] in sentence]
                    self.prune(curCandidates)
                    sentences = self.split(sentences)
                print("n-gram times:", time)
            # print(self.candidates)
        
        elif type == "one_time":
            print('pruning candidates')
            self.prune(self.candidates)
            print('splitting {} sentences'.format(len(sentences)))
            sentences = self.split(sentences)
            print('done')

        if save:
            self.saveModel()
        
    def predict(self, sentence):
        return self.split(sentence)

    # 检查sentences中的每个sentence是否会出现两个及以上的n-gram
    def check(self, sentences):
        for sentence in sentences:
            one = False # 是否出现过一个n-gram
            for candidate in self.candidates:
                if candidate["str"] in sentence:
                    if one:
                        print("2 n-grams!", sentence)
                        return True
                    else:
                        one = True
        return False

    # 对candidates中的n-gram进行取舍，保留出现次数最多的n-gram
    # 先记录到删除列表，最后再删除，太慢，但直接删除我写不出来
    def prune(self, curCandidates):
        print("candidates length:", len(curCandidates))
        count = 0
        # del_list = []
        del_name = []
        # 从长到短遍历candidates
        for i in range(len(curCandidates)):
            count += 1
            if count % 10000 == 0:
                print("{}/{}".format(count, len(curCandidates)))
            # 从短到长遍历长度小于candidates[i]的candidates
            for j in range(len(curCandidates) - 1, i, -1):
                if curCandidates[j]["str"] in curCandidates[i]["str"]:
                    if curCandidates[j]["count"] > curCandidates[i]["count"]:
                        # del_list.append(i)
                        del_name.append(curCandidates[i])
                        break
                    else:
                        # del_list.append(j)
                        del_name.append(curCandidates[j])
        print("{} to delete".format(len(del_name)))
        count = 0
        for name in del_name:
            count += 1
            if count % 1000 == 0:
                print("{}/{}".format(count, len(del_name)))
            if name in self.candidates:
                self.candidates.remove(name)
        # self.candidates = [self.candidates[i] for i in range(len(self.candidates)) if i not in del_list]


    # 边遍历边删除，快，但我写不对
    '''
    def prune(self, curCandidates):
        print("candidates length:", len(curCandidates))
        count = 0
        # del_list = []
        # 从长到短遍历candidates
        for i in range(len(curCandidates)):
            count += 1
            if count % 10000 == 0:
                print("{}/{}".format(count, len(curCandidates)))
            # 从短到长遍历长度小于candidates[i]的candidates
            for j in range(len(curCandidates) - 1, i, -1):
                for k in range(j, i, -1):
                    if k == j:
                        continue
                    if curCandidates[j]["str"] in curCandidates[i]["str"] and curCandidates[k]["str"] in curCandidates[i]["str"]:
                        if curCandidates[j]["count"] > curCandidates[i]["count"] or curCandidates[k]["count"] > curCandidates[i]["count"]:
                            self.candidates.remove(curCandidates[i])
                            i -= 1
                            j -= 1
                            k -= 1
                            break
                        elif curCandidates[i]["count"] >= curCandidates[k]["count"] and curCandidates[i]["count"] >= curCandidates[j]["count"]:
                            self.candidates.remove(curCandidates[k])
                            k -= 1
                            j -= 1
                            self.candidates.remove(curCandidates[j])
                            j -= 1
    '''

    # 按照candidates中的n-gram对sentences进行分割
    def split(self, sentences):
        count = 0
        res = []
        for sentence in sentences:
            count += 1
            if count % 10000 == 0:
                print("{}/{}".format(count, len(sentences)))
            # 将sentence中的n-gram替换为" "
            for candidate in self.candidates:
                if candidate["str"] in sentence:
                    sentence = sentence.replace(candidate["str"], " " + candidate["str"] + " ")
            # 将sentence按照" "分割
            tmp = sentence.split()
            res.extend(tmp)
        return res
    
    def saveModel(self):
        with open('model/model-{}-{}.weights'.format(str(datetime.now()).replace(':', '-'), len(self.candidates)), 'w', encoding='utf-8') as f:
            for candidate in self.candidates:
                f.write(candidate['str'] + ' ' + str(candidate['count']) + '\n')
            f.close()
        
    def loadModel(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                self.candidates.append({'str': line.split()[0], 'count': int(line.split()[1])})
            f.close()