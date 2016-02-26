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
    def insert():
        print("inserting")

    def search(self,key):
        for i,(k,v) in enumerate(self.values):
            if k==key:
                return self.values
            elif k>key:
                return self.children[i].search(key)
        return self.children[-1].search(key)



class BTree:
    def __init__(self):
        self.root = None
    def insert(self,key):
        self.root.insert()
    def search(self,key):
        return self.root.search(key)

def main():
    tree = BTree()
    root = BTreeNode()
    tree.root = root
    root.values = [(10,10)]
    root.isRoot = True

    child1 = BTreeNode()
    child1.values = [(4,4),(6,6),(8,8)]
    child1.parentNode = root
    root.children = [child1]

    grand1 = BTreeNode()
    grand1.values = [(1,1)]
    grand1.parentNode = child1

    grand2 = BTreeNode()
    grand2.values = [(5,5)]
    grand2.parentNode = child1

    grand3 = BTreeNode()
    grand3.values = [(7,7)]
    grand3.parentNode = child1

    grand4 = BTreeNode()
    grand4.values = [(9,9)]
    grand4.parentNode = child1
    child1.children = [grand1,grand2,grand3,grand4]

    x = tree.search(7)
    print(x)

main()
