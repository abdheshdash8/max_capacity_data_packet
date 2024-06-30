class Empty(Exception):
    '''Error attempting to access an element from an empty container.'''
    pass

class PriorityQueueBase:
    '''Abstract base class for a priority queue.'''

    class _Item:
        '''Lightweight composite to store priority queue items'''
        __slots__ = '_key' , '_value'   # Its for  memory optimisation.
        def __init__(self, k, v): 
            self._key = k
            self._value = v

        def __gt__(self, other):
            return self._key > other._key # compare items based on their keys

    def is_empty(self): # concrete method assuming abstract len
        '''Return True if the priority queue is empty.'''
        return len(self) == 0

class MaxHeapPriorityQueue(PriorityQueueBase): # base class defines Item
    '''A min-oriented priority queue implemented with a binary heap.'''
    #------------------------------ nonpublic behaviors ------------------------------
    def _parent(self, j):
        return (j - 1) // 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)   # index beyond end of list?

    def _has_right(self, j):
        return self._right(j) < len(self._data)  # index beyond end of list?

    def _swap(self, i, j):
        '''Swap the elements at indices i and j of the array.'''
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] > self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)    # recur at position of parent

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            big_child = left   # although right may be smaller
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] > self._data[left]:
                    big_child = right
            if self._data[big_child] > self._data[j]:
                self._swap(j, big_child)
                self._downheap(big_child)

#------------------------------ public behaviors ------------------------------
    def __init__(self):
        '''Create a new empty Priority Queue.'''
        self._data = [ ]
    def __len__ (self):
        '''Return the number of items in the priority queue.'''
        return len(self._data)

    def add(self, key, value):
        '''Add a key-value pair to the priority queue.'''
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)   # upheap newly added position

    def max(self):
        '''Return but do not remove (k,v) tuple with minimum key.
        Raise Empty exception if empty.'''
        if self.is_empty( ):
            raise Empty( "Priority queue is empty." )
        item = self._data[0]
        return (item._key, item._value)

    def remove_max(self):
        '''Remove and return (k,v) tuple with minimum key.
        Raise Empty exception if empty.'''
        if self.is_empty( ):
            raise Empty( "Priority queue is empty." )
        self._swap(0, len(self._data) - 1) # put minimum item at the end
        item = self._data.pop( ) # and remove it from the list;
        self._downheap(0) # then fix new root
        return (item._key, item._value)

class Graph:
    def __init__(self, n):
        self.v = n  # n is the number of vertices in the graph.
        self.data = {}
    def addEdge(self, s, t, cap):
        if not s in self.data:
            if not t in self.data:
                self.data[s] = [[t, cap, 0]]
                self.data[t] = [[s, cap, 0]]
            else:
                self.data[s] = [[t, cap, 0]]
                self.data[t].append([s, cap, 0])
        else:
            if not t in self.data:
                self.data[s].append([t, cap, 0])
                self.data[t] = [[s, cap, 0]]
            else:
                self.data[s].append([t, cap, 0])
                self.data[t].append([s, cap, 0])
    def neighbours(self, s):
        l = []
        for i in range(len(self.data[s])):
            if self.data[s][i][2] == 0:
                #print('b')
                l.append((self.data[s][i][1], self.data[s][i][0])) 
                self.data[s][i][2] = 1
                j = findList(self.data[self.data[s][i][0]], s, 0, self.data[s][i][1]) 
                if j != None:
                    self.data[self.data[s][i][0]][j][2] = 1
        return l
def findList(l, item, index, cap):
    l1 = []
    n = len(l)
    for i in range(n):
        if l[i][index] == item:
            if l[i][1] == cap:
                return i

def reverseList(l):
    n = len(l)
    if n == 0 or n == 1:
        return l
    for i in range(n//2):
        l[i], l[n-1-i] = l[n-1-i], l[i]
    return l

def findMaxCapacity(n, links, s, t):
    graph = Graph(n)
    m = len(links)
    for i in range(m):
        graph.addEdge(links[i][0], links[i][1], links[i][2])
    #print(graph.data)
    if not t in graph.data:
        return (0, [])
    storage = {s:(0, "N.A.")}
    cap = 0
    heap = MaxHeapPriorityQueue()
    for i in range(len(graph.data[s])):
        graph.data[s][i][2] = 1
        j = findList(graph.data[graph.data[s][i][0]], s, 0, graph.data[s][i][1]) 
        if j != None:
            graph.data[graph.data[s][i][0]][j][2] = 1
            heap.add(graph.data[s][i][1], graph.data[s][i][0])
    #print(graph.data)
    if len(heap) != 0:
        (key1, value1) = heap.remove_max()
        storage[value1] = (key1, s)
        cap = key1
        #print(heap._data)
        #print(storage) 
    for i in range(len(links) - 1):
        l = graph.neighbours(value1)
        #print(l)
        for j in range(len(l)):
            heap.add(l[j][0], l[j][1])
        (key, value) = heap.remove_max()
        if cap > key:
            if not value in storage:
                storage[value] = (key, value1)
                cap = key
        else:
            if not value in storage:
                storage[value] = (cap, value1)
        value1, key1 = value, key
        #print(storage)
    route  = []
    #print(storage)
    if t in storage:
        route.append(t)
        i = storage[t][1]
        route.append(i)
        while i != s:
            i = storage[i][1] 
            route.append(i)
        return (storage[t][0], reverseList(route))
    else:
        return (0, [])    

print(findMaxCapacity(3,[(0,1,1),(1,2,1)],0,1))

print(findMaxCapacity(4,[(0,1,30),(0,3,10),(1,2,40),(2,3,50),(0,1,60),(1,3,50)],0,3))
print(findMaxCapacity(4,[(0,1,30),(1,2,40),(2,3,50),(0,3,10)],0,3))
print(findMaxCapacity(5,[(0,1,3),(1,2,5),(2,3,2),(3,4,3),(4,0,8),(0,3,7),(1,3,4)],0,2))
print(findMaxCapacity(7,[(0,1,2),(0,2,5),(1,3,4), (2,3,4),(3,4,6),(3,5,4),(2,6,1),(6,5,2)],0,5))
