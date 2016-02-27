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
        if key == 11:
            print("<int>")
            print(len(self.children) < maxChildren)
            print(len(self.values) < maxChildren - 1)
            print("<\int>")
        if len(self.children) < maxChildren and len(self.values) < maxChildren - 1:
            if len(self.children) == 0:  #it's a leaf
                self.insertIntoArbit(kvPair)
            else: #it's not a leaf, so give to kids
                index = len(self.values)
                for i,(k,v) in enumerate(self.values):
                    if key<k:
                        index = i
                        break
                self.children[index].insert((key,value))
        else:  #overflowing
            self.splitIfNecessary((key,value))


    def splitIfNecessary(self,kvPair):
        key = kvPair[0]
        value = kvPair[1]
        if self.isRoot == True:
            newParent = BTreeNode()
            self.isRoot = False
            self.parentNode = newParent
            newParent.isRoot = True
        index = len(self.values)
        for i,(k,v) in enumerate(self.values):
            if key < k:
                index = i
                break
        self.values.insert(index,(key,value))
        mid = int(len(self.values)/2) if len(self.values)%2==0 else int((len(self.values)+1)/2)
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
        self.parentNode.getMedianFromChild(median)

    def getMedianFromChild(self,median):
        key = median[0]
        value = median[1]
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
    for i,(k,v) in enumerate([(x,[x]) for x in range(1,11)]):
        print("inserting "+ str((k,v)))
        tree.insert((k,v))
    print(tree.root.values)
    for child in tree.root.children:
        print(child.values)


main()
