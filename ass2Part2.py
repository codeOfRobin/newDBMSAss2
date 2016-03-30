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

def idsForNonJoinCondition(condition,nameOfTable):
    regexPattern = '|'.join(map(re.escape, ['<','>','=']))
    parts = [x for x in re.split(regexPattern,condition) if x!='']
    attr = parts[0]
    if types[nameOfTable][attr] == "int":
        if condition[len(attr)] == "=":
            tup = BTrees[nameOfTable][attr].search(int(parts[1]))
            return tup[0].values[tup[1]][1]
    else:
        return StringHashes[nameOfTable][attr][parts[1]]


def main():
    global types,BTrees,records,schemas,StringHashes
    file = open("BTrees.obj",'rb')
    BTrees = pickle.load(file)
    file.close()
    file = open("records.obj",'rb')
    records = pickle.load(file)
    file.close()
    file = open("schemas.obj",'rb')
    schemas = pickle.load(file)
    file.close()
    file = open("StringHashes.obj",'rb')
    StringHashes = pickle.load(file)
    file.close()
    file = open("types.obj",'rb')
    types = pickle.load(file)
    file.close()
    with open(sys.argv[1]) as f:
        content = [x[:-1] for x in f.readlines()]
        for query in content:
            tup = query.split(" ")
            if tup[0] == "insert":
                nameOfTable = tup[1]
                values = tup[2].split(",")
                dic = {}
                attrNames = [schemas[nameOfTable][k]["attr"] for k in sorted(schemas[nameOfTable].keys())]
                for i,value in enumerate(values):
                    attr = attrNames[i]
                    dic[attr] = value
                    if schemas[nameOfTable][i]["type"] == "string":
                        if value in StringHashes[nameOfTable][attr]:
                            StringHashes[nameOfTable][attr][value].append(int(values[0]))
                        else:
                            StringHashes[nameOfTable][attr][value] = [int(values[0])]
                    else:
                        BTrees[nameOfTable][attr].insert((int(value),int(values[0])))
                records[nameOfTable][values[0]] = dic
            elif tup[0] == "update":
                pass
            elif tup[0] == "delete":
                pass
            elif tup[0] == "select":
                columns = tup[1].split(",")
                table = tup[3]
                ids = idsForNonJoinCondition(tup[5],table)
                results = []
                for ide in ids:
                    dic = {}
                    i=0
                    for col in columns:
                        dic[col] = records[table][str(ide)][col]
                    results.append(dic)
                t = PrettyTable([x for x in columns])
                for row in results:
                    t.add_row([row[key] for key in columns])
                print(t)

main()
