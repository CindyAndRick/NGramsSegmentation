class Trie:
    def __init__(self):
        self.cur = ''
        self.children = {}
        self.count = 0 # 当且仅当某单词以此节点结尾时，此节点count++

    def insert(self, word):
        node = self
        for c in word:
            if c not in node.children:
                node.children[c] = Trie()
            node = node.children[c]
            node.cur = c
        node.count += 1
    
    def search(self, word):
        node = self
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.count
    
    # 实际上并没有删除路径，只是将count置为0
    def drop(self, word):
        node = self
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        node.count = 0

    # 遍历并找到count>2的结点
    # str在传入时需要传入空值，被用作静态局部变量（python中没有静态局部变量）
    # res在传入时需要传入空列表，为结果
    def find(self, node, str, res):
        str += node.cur
        if node.count >= 2:
            res.append({"str": str, "count": node.count})
        for child in node.children.values():
            self.find(child, str, res)
        str = str[:-1]

    def print(self):
        print('count:', self.count, 'cur:', self.cur, self.children.keys(), 'children num:', len(self.children))
        for child in self.children.values():
                child.print()
    
    