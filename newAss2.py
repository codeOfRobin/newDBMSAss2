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
        index = len(self.children)
        for i,(k,v) in enumerate(self.values):
            if key < k:
                index = i
                break
        if len(self.children)<maxChildren:
            if len(self.children) == 0:
                self.values.insert(index,(key,value))
            else:
                self.children[index].insert((key,value))
        else:
            newParent = BTreeNode()
            self.values.insert(index,(key,value))
            median = self.values[len(self.values)/2]
            newParent.values = [median]
            del self.values[index]

            leftNode = BTreeNode()
            leftNode.values = self.values[:len(self.values)/2]
            leftNode.children = self.children[:len(self.values)/2]
            rightNode = BTreeNode()
            rightNode.values = self.values[len(self.values)/2:]
            rightNode.children = self.children[len(self.values)/2:]
            leftNode.parentNode = newParent
            rightNode.parentNode = newParent
            newParent.children = [leftNode,rightNode]
            if self.isRoot == True:
                self.isRoot = False
                newParent.isRoot = True
    def search(self,key):
        for i,(k,v) in enumerate(self.values):
            if k==key:
                return self.values
            elif k>key:
                return self.children[i].search(key)
        return self.children[-1].search(key)
    def inOrderTraverse(self):
        for i,(k,v) in self.values:
            print(self.children[i].inOrderTraverse())
            print(self.values[i])


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
            node.values = kvPair
            return
        if preSearchNode != None:
            preSearchNode[1].append(value)
        else:
            self.root.insert((key, value))
    def search(self,key):
        if self.root!=None:
            return self.root.search(key)
        else:
            return None
    def inOrderTraverse(self):
        self.root.inOrderTraverse()

def main():
    tree = BTree()
    tree.insert((10,[10]))
    tree.insert((3,[3]))
    tree.insert((4,[4]))
    tree.insert((5,[5]))
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
    print(tree.root.isRoot)

main()
