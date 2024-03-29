#ref:  http://cis.stvincent.edu/html/tutorials/swd/btree/btree.html
#ref: https://github.com/alansammarone/BTree/blob/master/btree.py

import sys
import json
import re
from prettytable import PrettyTable
import pickle

schemas = {}
records = {}
relations = []
BTrees = {}
StringHashes = {}
types = {}
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
                return (self,i)
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
                if len(self.children) == 0 and len(self.values)>1:
                    self.values.pop(i)
                    return
                else:
                    if len(self.values) == 1: ##underflowing leaf
                        successorNode = self
                        successorIndex = 0
                    else:
                        (successorNode,successorIndex) = self.getSuccessor(key)
                    self.values[i] = successorNode.values[successorIndex]
                    if len(successorNode.values)>1:
                        successorNode.values.pop(successorIndex)
                    else:
                        leftSibling, rightSibling = self.getSibilings()
                        if leftSibling and len(leftSibling.values)>1:
                            successorNode.performLeftRotation(leftSibling,successorIndex)
                        elif rightSibling and len(rightSibling.values)>1:
                            successorNode.performRightRotation(rightSibling,successorIndex)
                        else:
                            successorNode.performFuses()
                    return
            elif k>key:
                return self.children[i].remove(key)
        return self.children[-1].remove(key)

    def performLeftRotation(self,leftSibling,successorIndex):
        index = 0
        for i,c in enumerate(self.parentNode.children):
            if c == self:
                index = i
                break
        parentPair = self.parentNode.values[index - 1]
        self.parentNode.values[i - 1] = leftSibling.values.pop()
        if self.children != []:
            self.children.insert(0,leftSibling.children.pop())
        if len(self.values)!=0:
            self.values[successorIndex] = parentPair
        else:
            self.values.insert(0,parentPair)

    def performRightRotation(self,rightSibling,successorIndex):
        index = 0
        for i,c in enumerate(self.parentNode.children):
            if c == self:
                index = i
                break
        parentPair = self.parentNode.values[index - 1]
        self.parentNode.values[i] = rightSibling.values.pop(0)
        if self.children != []:
            self.children.push(leftSibling.children.pop(0))
        if len(self.values)!=0:
            self.values[successorIndex] = parentPair
        else:
            self.values.insert(0,parentPair)

    def performFuses(self):
        leftSibling, rightSibling = self.getSibilings()
        index = 0
        for i,c in enumerate(self.parentNode.children):
            if c == self:
                index = i
                break
        parentPair = self.parentNode.values[index - 1]
        if leftSibling:
            self.parentNode.children.pop(index)
            leftSibling.values.append(parentPair)
            if self.children:
                leftSibling.children += self.children

        elif rightSibling:
            self.parentNode.children.pop(index)
            rightSibling.values.insert(0,parentPair)
            if self.children:
                rightSibling.children += self.children

        self.parentNode.values.pop(index - 1)
        if len(self.parentNode.values) == 0:
            parent = self.parentNode
            if not self.parentNode.isRoot:
                leftSibling, rightSibling = self.parentNode.getSibilings()
                if leftSibling and len(leftSibling.values)>1:
                    self.parentNode.performLeftRotation(leftSibling,0)
                elif rightSibling and len(rightSibling.values)>1:
                    self.parentNode.performRightRotation(rightSibling,0)
                else:
                    self.parentNode.performFuses()
                # if self.parentNode.parentNode:
                #     print(self.parentNode.parentNode.children)
                #     for i,c in enumerate(self.parentNode.parentNode.children):
                #         if c==self.parentNode:
                #             c.values = self.values

            else:
                self.isRoot = True
                self.parentNode.isRoot = False
                self.parent = None


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
    def inOrderTraverse(self):
        i=0
        for value in self.values:
            if len(self.children) != 0:
                self.children[i].inOrderTraverse()
            print(value)
            i+=1
        if len(self.children) != 0:
            self.children[-1].inOrderTraverse()
class BTree:
    def __init__(self):
        self.root = None

    def insert(self, kvPair):
        key = kvPair[0]
        value = kvPair[1]
        (preSearchNode,index) = (None,None)
        if self.search(key):
            searched = self.search(key)
            preSearchNode = searched[0]
            index = searched[1]
        if self.root == None:
            node = BTreeNode()
            node.isRoot = True
            self.root = node
            node.values = [kvPair]
            return
        if preSearchNode != None:
            if isinstance(preSearchNode.values[index][1], list):
                preSearchNode.values[index][1].append(value)
            else:
                intVal = preSearchNode.values[index][1]
                preSearchNode.values[index] = (key,[intVal,value])
        else:
            self.root.insert((key, value))
            if not self.root.isRoot:
                # print("resetting root from "+ str(self.root.values) + "to " + str(self.root.parentNode.values))
                x = self.root
                self.root = self.root.parentNode
                del x

    def remove(self,key):
        if self.root == None:
            return False
        self.root.remove(key)
        if not self.root.isRoot:
            self.root = self.root.children[0]
            self.root.isRoot = True

    def search(self,key):
        if self.root!=None:
            return self.root.search(key)
        else:
            return None
    def inOrderTraverse(self):
        self.root.inOrderTraverse()


def removeFirst(arr):
	return arr[1:]


def main():
    if len(sys.argv) != 2:
        raise ValueError('You done screwed up')

    with open(sys.argv[1]) as f:
        content = [x[:-1] for x in f.readlines()]
        numberOfTables = int(content[0][1:])
        content = removeFirst(content)
        for i in range(0,numberOfTables):
            nameOfTable = content[0]
            schemas[nameOfTable] = {}
            records[nameOfTable] = {}
            types[nameOfTable] = {}
            content = removeFirst(content)
            numberOfAttrs = int(content[0][1:])
            content = removeFirst(content)
            attrNames = content[0].split(',')
            content = removeFirst(content)

            BTrees[nameOfTable] = {}
            StringHashes[nameOfTable] = {}

            for attr in attrNames:
                BTrees[nameOfTable][attr] = BTree()
                StringHashes[nameOfTable][attr] = {}
            numberOfRecords = int(content[0][1:])
            content = removeFirst(content)
            for j in range(0, numberOfRecords):
            	dic = {}
            	tup = content[j].split(',')
            	for k,attr in enumerate(attrNames):
                    try:
                        BTrees[nameOfTable][attr].insert((int(tup[k]),int(tup[0])))
                        schemas[nameOfTable][k] = {}
                        schemas[nameOfTable][k]["type"] = "int"
                        schemas[nameOfTable][k]["attr"] = attr
                        types[nameOfTable][attr] = "int"
                        dic[attr] = int(tup[k])
                    except ValueError:
                        if tup[k] in StringHashes[nameOfTable][attr]:
                            StringHashes[nameOfTable][attr][tup[k]].append(int(tup[0]))
                        else:
                            StringHashes[nameOfTable][attr][tup[k]] = [int(tup[0])]
                        schemas[nameOfTable][k] = {}
                        schemas[nameOfTable][k]["type"] = "string"
                        types[nameOfTable][attr] = "string"
                        schemas[nameOfTable][k]["attr"] = attr
                        dic[attr] = tup[k]
            	records[nameOfTable][tup[0]] = dic
            content = content[numberOfRecords:]
            content = removeFirst(content)
        content = removeFirst(content)

        filehandler = open("BTrees.obj","wb")
        pickle.dump(BTrees,filehandler)
        filehandler.close()
        filehandler = open("schemas.obj","wb")
        pickle.dump(schemas,filehandler)
        filehandler.close()
        filehandler = open("StringHashes.obj","wb")
        pickle.dump(StringHashes,filehandler)
        filehandler.close()
        filehandler = open("records.obj","wb")
        pickle.dump(records,filehandler)
        filehandler.close()
        filehandler = open("types.obj","wb")
        pickle.dump(types,filehandler)
        filehandler.close()
        # print(BTrees["Product"]["Id"].root.values)
        # for child in BTrees["Product"]["Id"].root.children:
        #     print(child.values)
        # print("records")
        # print(json.dumps(records,sort_keys=True, indent=4))
        # print("schemas")
        # print(json.dumps(schemas,sort_keys=True, indent=4))
        # print("StringHashes")
        # print(json.dumps(StringHashes,sort_keys=True, indent=4))
        #
    # tree = BTree()
    # for i,(k,v) in enumerate([(x,[x]) for x in range(1,17)]):
    #     print("inserting "+ str((k,v)))
    #     tree.insert((k,v))
    # tree.insert((16,1024))
    # tree.inOrderTraverse()
    # for child in tree.root.children:
    #     print("child")
    #     print(child.values)
    #     for grandChild in child.children:
    #         print("grandChildchild")
    #         print(grandChild.values)
    #
    # print("AFTER REMOVAL\n\n\n")
    # print(tree.root.values)
    # for child in tree.root.children:
    #     print("child")
    #     print(child.values)
    #     for grandChild in child.children:
    #         print("grandChildchild")
    #         print(grandChild.values)
main()
