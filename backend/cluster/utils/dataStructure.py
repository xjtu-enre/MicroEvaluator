import collections
import numpy as np


class UnionFind(object):
    """并查集类"""

    def __init__(self, n):
        """长度为n的并查集"""
        self.uf = [-1 for i in range(n + 1)]  # 列表0位置空出
        self.sets_count = n  # 判断并查集里共有几个集合, 初始化默认互相独立

    def find(self, p):
        """尾递归"""
        if self.uf[p] < 0:
            return p
        self.uf[p] = self.find(self.uf[p])
        return self.uf[p]

    def union(self, p, q):
        """连通p,q 让q指向p"""
        proot = self.find(p)
        qroot = self.find(q)
        if proot == qroot:
            return
        elif self.uf[proot] > self.uf[qroot]:  # 负数比较, 左边规模更小
            self.uf[qroot] += self.uf[proot]
            self.uf[proot] = qroot
        else:
            self.uf[proot] += self.uf[qroot]  # 规模相加
            self.uf[qroot] = proot
        self.sets_count -= 1  # 连通后集合总数减一


class ProjectFilesTrieNode:
    def __init__(self, name):
        self.children = []
        self.count = 0
        self.indexMap = {}
        self.changeLoc = 0
        self.catelogueType = 1
        self.end = False
        self.id = id
        self.name = name
        self.parent_pk = 0
        self.qualifiedName = ''
        self.size = 0
        self.value = []

    def getId(self):
        return self.id

    def getItem(self):
        item = {'id': self.id, 'name': self.name, 'qualifiedName': self.qualifiedName, 'value': self.value,
                'parent_catelogue': self.parent_pk, 'catelogue_type': self.catelogueType, 'end': self.end}
        return item

    def setCatelogueType(self, catelogue_type):
        self.catelogueType = catelogue_type

    def setChangeLoc(self, changeLoc):
        self.changeLoc = changeLoc

    def setEnd(self, end):
        self.end = end

    def setId(self, id):
        self.id = id

    def setParentPk(self, id):
        self.parent_pk = id

    def setQualifiedName(self, name):
        self.qualifiedName = name

    def setSize(self, size):
        self.size = size

    def setValue(self, value):
        self.value = value


class ProjectFilesTrieTree:
    def __init__(self, max, parent_pk, version_project_id):
        self.version_project_id = version_project_id
        self.id = parent_pk - 1
        self._root = ProjectFilesTrieNode('root')
        self._nodeList = []
        self.baseValue = 20
        self.maxValue = 1000
        self.maxChangeLoc = max

    def get_size_by_changeLoc(self, number):
        return self.baseValue + number / self.maxChangeLoc * (self.maxValue - self.baseValue)

    def insert(self, words, changeLoc):
        node = self._root
        for word in enumerate(words):
            if node.indexMap.get(word[1]) is None:
                node.indexMap[word[1]] = node.count
                node.count += 1
                temp = ProjectFilesTrieNode(word[1])
                temp.setQualifiedName('/'.join(words[:word[0] + 1]))
                node.children.append(temp)
            node = node.children[node.indexMap[word[1]]]
        node.setChangeLoc(changeLoc)
        node.setEnd(True)
        node.setQualifiedName('/'.join(words))
        node.setSize(float('%.3f' % self.get_size_by_changeLoc(changeLoc)))

    # 返回父亲结点的id
    def search(self, words):
        node = self._root
        for word in words[:-1]:
            if node.indexMap[word] is None:
                return None
            node = node.children[node.indexMap[word]]
        return node.getId()

    def getRoot(self):
        self.DFS(self._root, self.id, 1)
        self.BFS()
        return self._nodeList

    # 深度遍历
    def DFS(self, node, parent_pk, catelogue_type):
        temp = []
        node.setCatelogueType(catelogue_type)
        if node.children is not None:
            for child in node.children:
                temp.append(self.DFS(child, node.id, node.catelogueType + 1))
        item = {}
        if temp:
            item['count'] = sum([selector['count'] for selector in temp])
            item['value'] = [sum([selector['value'][0] for selector in temp]),
                             sum([selector['value'][1] for selector in temp]),
                             item['count'], 1]
        else:
            item['count'] = 1
            item['value'] = [node.size, 35.0, node.changeLoc, 0]
        node.setValue(item['value'])
        return item

    # 广度遍历
    def BFS(self):
        queue = collections.deque()
        queue.append(self._root)
        while len(queue) != 0:
            self.id += 1
            node = queue.popleft()
            node.setId(self.id)
            if node.name != 'root':
                node.setParentPk(self.search(node.qualifiedName.split('/')))
            self._nodeList.append(node.getItem())
            if node.children is not None:
                for child in node.children:
                    queue.append(child)


class SectionFilesTrieNode:
    def __init__(self, name):
        self.children = []
        self.count = 0
        self.end = False
        self.id = id
        self.indexMap = {}
        self.name = name
        self.parent_pk = 0
        self.qualifiedName = ''
        self.sectionType = 1
        self.subEnd = False

    def getId(self):
        return self.id

    def getItem(self):
        item = {'id': self.id, 'name': self.name, 'parent_file': self.parent_pk, 'qualifiedName': self.qualifiedName,
                'section_type': self.sectionType, 'end': self.end, 'subEnd': self.subEnd}
        return item

    def setEnd(self, end):
        self.end = end

    def setId(self, id):
        self.id = id

    def setParentPk(self, id):
        self.parent_pk = id

    def setQualifiedName(self, name):
        self.qualifiedName = name

    def setSectionType(self, section_type):
        self.sectionType = section_type

    def setSubEnd(self, sub_end):
        self.subEnd = sub_end


class SectionFilesTrieTree:
    def __init__(self, parent_pk):
        self.id = parent_pk - 1
        self._root = SectionFilesTrieNode('root')
        self._nodeList = []

    def insert(self, words):
        node = self._root
        for word in enumerate(words):
            if node.indexMap.get(word[1]) is None:
                if word[0] == len(words) - 1:
                    node.setSubEnd(True)
                node.indexMap[word[1]] = node.count
                node.count += 1
                temp = SectionFilesTrieNode(word[1])
                temp.setQualifiedName('/'.join(words[:word[0] + 1]))
                node.children.append(temp)
            node = node.children[node.indexMap[word[1]]]
        node.setSubEnd(True)
        node.setEnd(True)
        node.setQualifiedName('/'.join(words))

    # 返回父亲结点的id
    def search(self, words):
        node = self._root
        for word in words[:-1]:
            if node.indexMap[word] is None:
                return None
            node = node.children[node.indexMap[word]]
        return node.getId()

    def getRoot(self):
        self.DFS(self._root, 1)
        self.BFS()
        return self._nodeList

    # 深度遍历
    def DFS(self, node, catelogue_type):
        temp = []
        node.setSectionType(catelogue_type)
        if node.children is not None:
            for child in node.children:
                temp.append(self.DFS(child, node.sectionType + 1))

    # 广度遍历
    def BFS(self):
        queue = collections.deque()
        queue.append(self._root)
        while len(queue) != 0:
            self.id += 1
            node = queue.popleft()
            node.setId(self.id)
            if node.name != 'root':
                node.setParentPk(self.search(node.qualifiedName.split('/')))
            self._nodeList.append(node.getItem())
            if node.children is not None:
                for child in node.children:
                    queue.append(child)


class ProjectFilesGraph:
    def __init__(self, nodes, edges):
        self.length = len(nodes)
        self.edges = edges
        self.matrix = self.get_adjacency_matrix()
        self.inDegrees = np.sum(self.matrix, axis=0)
        self.adjacency_table = [np.nonzero(self.matrix[i]) for i in range(self.length)]

    def get_adjacency_matrix(self):
        matrix = np.zeros((self.length, self.length), dtype=int)
        for edge in self.edges:
            items = list(edge.values())
            matrix[items[0]][items[1]] = 1
        return matrix

    def is_circle_exist(self):
        cnt = 0
        queue = collections.deque()
        for i in range(self.length):
            if self.inDegrees[i] == 0:
                queue.append(i)
        while len(queue) > 0:
            cnt += 1
            temp = self.adjacency_table[queue.popleft()][0]
            if len(temp) != 0:
                for i in temp:
                    self.inDegrees[i] -= 1
                    if self.inDegrees[i] == 0:
                        queue.append(i)
        return cnt != self.length
