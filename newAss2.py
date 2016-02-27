minChildren = 2
maxChildren = 4
class BTreeNode:
    def __init__(self, values = None):
        self.values = []
        self.children = []
        self.parentNode = None
        self.isRoot = None
        if values:
            self.values = values

    def insert(self,kvPair):
        key = kvPair[0]
        value = kvPair[1]
        index = len(self.values)
        for i,(k,v) in enumerate(self.values):
            if key < k:
                index = i
                break
        if len(self.values)==0:
            self.values.insert(index,(key,value))
            return
        if len(self.children)<maxChildren and len(self.values)<maxChildren - 1:
            if len(self.children) == 0:
                self.values.insert(index,(key,value))
            else:
                self.children[index].insert((key,value))
        else:
            self.splitIfNecessary((key,value))
            self.parentNode.getMedianFromChild(median)

            # print("<intermediates>")
            # print(newParent.values)
            # for child in newParent.children:
            #     print(child.values)
            # print("<\intermediates>")
            #
    def splitIfNecessary(self,kvPair):
        key = kvPair[0]
        value = kvPair[1]
        if self.isRoot == True:
            newParent = BTreeNode()
            self.isRoot = False
            self.parentNode = newParent
            newParent.isRoot = True

        self.values.insert(index,(key,value))
        mid = int(len(self.values)/2) if len(self.values)%2==0 else int(len(self.values)/2) + 1
        median = self.values[mid]
        print("median"+ str(median))
        del self.values[mid]
        leftNode = BTreeNode()
        leftNode.values = self.values[:mid]
        leftNode.children = self.children[:mid]
        rightNode = BTreeNode()
        rightNode.values = self.values[mid:]
        rightNode.children = self.children[mid:]
        leftNode.parentNode = self.parentNode
        rightNode.parentNode = self.parentNode
        # self.parentNode.children = [leftNode,rightNode]
        index = len(self.parentNode.values)
        for i,(k,v) in enumerate(self.parentNode.values):
            if self.values[0][0]<k:
                index = i
                break
        if len(self.parentNode.children)!=0:
            del self.parentNode.children[index]
        self.parentNode.children.insert(index,rightNode)
        self.parentNode.children.insert(index,leftNode)
        for child in leftNode.children:
            child.parentNode = leftNode
        for child in rightNode.children:
            child.parentNode = rightNode

    def getMedianFromChild(self,median):
        index = len(self.values)
        for i,(k,v) in enumerate(self.values):
            if key < k:
                index = i
                break
        if len(self.values) < maxChildren -1:
            self.values.insert(index,median)
        else:
            splitIfNecessary(median)

    def insertIntoArbit(self,kvPair):
        key = kvPair[0]
        value = kvPair[1]
        index = len(self.values)
        for i,(k,v) in enumerate(self.values):
            if key < k:
                index = i
                break
        self.values.insert(index,(key,value))

    def search(self,key):
        index = len(self.values)
        for i,(k,v) in enumerate(self.values):
            if k==key:
                return self.values
            elif k>key:
                index = i
                break
        if len(self.children) == 0:
            return None
        else:
            return self.children[index].search(key)
    # def inOrderTraverse(self):
    #     for i,(k,v) in enumerate(self.values):
    #         print(self.children[i].inOrderTraverse())
    #         print(self.values[i])


class BTree:
    def __init__(self):
        self.root = None
    def insert(self, kvPair):
        key = kvPair[0]
        value = kvPair[1]
        preSearchNode = self.search(key)
        if self.root == None:
            node = BTreeNode()
            node.isRoot = True
            self.root = node
            node.values = [kvPair]
            return
        if preSearchNode != None:
            preSearchNode[1].append(value)
        else:
            self.root.insert((key, value))
            if not self.root.isRoot:
                print("resetting root from "+ str(self.root.values) + "to " + str(self.root.parentNode.values))
                x = self.root
                self.root = self.root.parentNode
                del x

    def search(self,key):
        if self.root!=None:
            return self.root.search(key)
        else:
            return None
    def inOrderTraverse(self):
        self.root.inOrderTraverse()

def main():
    tree = BTree()
    for i,(k,v) in enumerate([(x,[x]) for x in range(1,8)]):
        print("inserting "+ str((k,v)))
        tree.insert((k,v))
    print("results:")
    print(tree.root.values)
    for child in tree.root.children:
        print(child.values)
    # root = BTreeNode()
    # tree.root = root
    # root.values = [(10,[10])]
    # root.isRoot = True
    #
    # child1 = BTreeNode()
    # child1.values = [(4,[4]),(6,[6]),(8,[8])]
    # child1.parentNode = root
    # root.children = [child1]
    #
    # grand1 = BTreeNode()
    # grand1.values = [(1,[1])]
    # grand1.parentNode = child1
    #
    # grand2 = BTreeNode()
    # grand2.values = [(5,[5])]
    # grand2.parentNode = child1
    #
    # grand3 = BTreeNode()
    # grand3.values = [(7,[7])]
    # grand3.parentNode = child1
    #
    # grand4 = BTreeNode()
    # grand4.values = [(9,[9])]
    # grand4.parentNode = child1
    # child1.children = [grand1,grand2,grand3,grand4]
    #
    # x = tree.search(7)
    # print(tree.root.isRoot)

main()
