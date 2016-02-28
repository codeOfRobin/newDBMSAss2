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
        if len(self.children) <= maxChildren and len(self.values) <= maxChildren - 1:
            if len(self.children) == 0:  #it's a leaf
                if len(self.values) == maxChildren - 1:
                    self.splitIfNecessary(kvPair)
                else:
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
        midChildren = int(len(self.children)/2) if len(self.children)%2==0 else int((len(self.children)+1)/2)
        median = self.values[mid]
        print("median"+ str(median))
        del self.values[mid]
        leftNode = BTreeNode()
        leftNode.values = self.values[:mid]
        leftNode.children = self.children[:midChildren]
        rightNode = BTreeNode()
        rightNode.values = self.values[mid:]
        rightNode.children = self.children[midChildren:]
        leftNode.parentNode = self.parentNode
        rightNode.parentNode = self.parentNode
        index = len(self.parentNode.values)
        if median[0] == 9:
            print(self.values)
            print(rightNode.values)
            print(leftNode.values)
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
            self.splitIfNecessary(median)

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
                return self.values[i]
            elif k>key:
                index = i
                break
        if len(self.children) == 0:
            return None
        else:
            return self.children[index].search(key)

    def remove(self,key):
        for i,(k,v) in enumerate(self.values):
            if k == key:
                if len(children) == 0:
                    self.values.pop(i)
                    return
                else:
                    (successorNode,successorIndex) = self.getSuccessor(key)
                    self.values[i] = self.successorNode.values[successorIndex]
                    if len(successorNode.values)>1:
                        successorNode.values.pop(successorIndex)
                    else:
                        leftSibling, rightSibling = self.getSibilings()
                        if leftSibling and len(self.leftSibling.values)>1:
                            successorNode.performLeftRotation(leftSibling,successorIndex)
                        elif rightSibling and len(self.rightSibling.values)>1:
                            successorNode.performRightRotation()
                        else:
                            successorNode.performFuses()
                    return
            elif k>key:
                return self.children[i].remove(key)
        return self.children[-1].remove(key)

    def performLeftRotation(self,leftSibling,successorIndex):
        index = 0
        for i,c in self.parentNode.children:
            if c == self:
                index = i
                break
        parentPair = self.parentNode.values[index - 1]
        self.parentNode.values[i] = leftSibling.values.pop()
        self.values[successorIndex] = parentPair

    def performRightRotation(self,rightSibling,successorIndex):
        index = 0
        for i,c in self.parentNode.children:
            if c == self:
                index = i
                break
        parentPair = self.parentNode.values[index - 1]
        self.parentNode.values[i] = leftSibling.values.pop()
        self.values[successorIndex] = parentPair

    def performFuses(self):
        return

    def getSibilings(self):
        for i,c in enumerate(self.parentNode.children):
            if c == self:
                if i == 0:
                    return (None,self.parentNode.children[i+1])
                elif i == len(self.parentNode.children) - 1:
                    return (self.parentNode.children[i-1],None)
                else:
                    return (self.parentNode.children[i-1],self.parentNode.children[i+1])
        return (None,None)

    def getSuccessor(self,key):
        for i,(k,v) in enumerate(self.values):
            if key < k:
                if len(self.children) == 0:
                    # self.values.pop(i)#diff
                    return(self,i)
                else:
                    return self.children[i].getSuccessor(key)
            elif key == k:
                return self.children[i+1].getSuccessor(key)
        return self.children[-1].getSuccessor(key)

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

    def remove(self,key):
        if self.root == None:
            return False
        self.root.remove(key)
        if not self.root.isRoot:
            self.root = self.root.children[0]

    def search(self,key):
        if self.root!=None:
            return self.root.search(key)
        else:
            return None
    def inOrderTraverse(self):
        self.root.inOrderTraverse()

def main():
    tree = BTree()
    for i,(k,v) in enumerate([(x,[x]) for x in range(1,17)]):
        print("inserting "+ str((k,v)))
        tree.insert((k,v))
    print(tree.root.values)
    tree.insert((16,1024))
    for child in tree.root.children:
        print("child")
        print(child.values)
        for grandChild in child.children:
            print("grandChildchild")
            print(grandChild.values)
main()
