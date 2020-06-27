class Node():
    def __init__(self, state, parent, action):
        self.state = state # Person
        self.parent = parent # previous state
        self.action = action # Movie
    def getState(self):
        return self.state #person

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action # movie


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def search_state(self, state):
        for node in self.frontier:
            if node.state == state:
                return node
        return None
        
    def empty(self):
        return len(self.frontier) == 0

    def printFrontier(self):
        for i in self.frontier:
            print(getattr(i, 'state'))

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
