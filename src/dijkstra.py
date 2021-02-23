import sys, math
from graphviz import Digraph

class HeapNode:
    def __init__(self, vertex, distance):
        self.vertex = vertex
        self.distance = distance
        
class BinaryHeap:
    def __init__(self):
        self.a = []
        self.vertex_dist = {}
        
    def get(self, i):
        if  i >= len(self.a):
            return
        return self.a[i].distance
  
    def swap(self, i, j):
        self.a[i], self.a[j] = self.a[j], self.a[i]        
        
    def add(self, node):
        index_ = self.count()
        self.a.append(node)
        self.vertex_dist[node.vertex] = node.distance
        
        while index_ != 0:
            p = self.parent(index_)
            if self.get(p) > self.get(index_):
                self.swap(p, index_)
            index_ = p
            
    def count(self):
        return len(self.a)
    
    def is_empty(self):
        return len(self.a) == 0
    
    def down_heap(self, i):
        a = self.a 
        while True:
            m = a[i].distance
            if self.left(i) < len(a):
                m = min(m, a[self.left(i)].distance)
            if self.right(i) < len(a):
                m = min(m, a[self.right(i)].distance)
            if m == a[i].distance:
                break 
            if m == a[self.left(i)].distance:
                self.swap(i, self.left(i))
                i = self.left(i)
            else:   
                self.swap(i, self.right(i))            
                i = self.right(i)

    def remove_minimum(self): 
        if len(self.a) == 0:
            return
        elif len(self.a) == 1:
            x = self.a.pop()
            return x
        x = self.a[0]
        self.a[0] = self.a.pop()
        self.down_heap(0)
        return x
    
    def left(self, i):
        return (2 * i + 1)

    def right(self, i):
        return (2 * i + 2)

    def parent(self, i):
        return ((i - 1) // 2)
    
class Graph:
    def __init__(self):
        self.graph = {}
        self.vertices = set()
        self.shortest_distance = {}
        self.start_end_path = []
        self.predecessor = {}
        self.source_vertex = None
        self.target_vertex = None

    def read_graph(self):
        for line in sys.stdin:
            each_line = line.split()
            
            assert len(each_line) >= 2
                            
            if len(each_line) == 3:
                self.vertices.add(each_line[0])
                self.vertices.add(each_line[1])
        
                edges = {each_line[1]:float(each_line[2])}
        
                if each_line[0] in self.graph:
                    self.graph[each_line[0]].update(edges)
                else:
                    self.graph[each_line[0]] = edges
            else:
                self.source_vertex, self.target_vertex = each_line[0], each_line[1]
                break
                    
    def form_path(self, predecessor, target):
        if predecessor[target] == self.source_vertex:
            return self.start_end_path
        
        assert target in predecessor, "Target vertex is missing!"
        self.start_end_path.append(predecessor[target])
        target = predecessor[target]
        
        return self.form_path(predecessor, target)

    def find_shortest_path(self):
        my_queue = BinaryHeap()
        
        if self.source_vertex not in self.graph:
            print('Source vertex is not in the Graph!')
            sys.exit(0)
        elif self.source_vertex == self.target_vertex:
            print('Source and Target vertices are the same!')
            sys.exit(0)

        self.shortest_distance[self.source_vertex] = 0
        self.start_end_path.append(self.target_vertex)
        
        for vertex in self.vertices:
            
            if vertex != self.source_vertex:
                self.shortest_distance[vertex] = math.inf
                self.predecessor[vertex] = None
        
        for vertex, edges in self.graph.items():
                
            node = HeapNode(vertex, self.shortest_distance[vertex])
            
            my_queue.add(node)
        
        while my_queue.count() > 0:
            min_vertex_dist = my_queue.remove_minimum()
            
            if min_vertex_dist.vertex in self.graph:
                
                for neighbor, distance in self.graph[min_vertex_dist.vertex].items():
                    new_distance = self.shortest_distance[min_vertex_dist.vertex] + distance
                     
                    if self.target_vertex not in self.shortest_distance:
                        print('Target vertex is not in the Graph!')
                        sys.exit(0)
                    
                    if new_distance < self.shortest_distance[neighbor]:
                        self.shortest_distance[neighbor] = new_distance
                        self.predecessor[neighbor] = min_vertex_dist.vertex
                        
                        node = HeapNode(neighbor, new_distance)
                        my_queue.add(node)
                           
        print(f'Shortest distance from {self.source_vertex}',
              f'to {self.target_vertex} is {self.shortest_distance[self.target_vertex]}')
        
        if self.shortest_distance[self.target_vertex] == math.inf:
            print('Target vertex is not reachable from the Source vertex!')
            sys.exit(0)
 
        self.form_path(self.predecessor, self.target_vertex)
        
        self.start_end_path.append(self.source_vertex)
        
        self.start_end_path = self.start_end_path[::-1]
        
        print(f'The Path from the source to target vertices: {self.start_end_path}')
        
        return self.shortest_distance

    def visualize(self):      
        
        dot = Digraph(comment='Graph')
        
        def vertices(vertex):
            if vertex == self.start_end_path[0]:
                dot.node(vertex, vertex, color='blue', fontcolor='blue', fontsize='20.0')
            elif vertex == self.start_end_path[-1]:
                dot.node(vertex, vertex, color='red', fontcolor='red', fontsize='20.0')
            elif vertex in self.start_end_path[1:-1]:
                dot.node(vertex, vertex, color='orange', fontcolor='orange')            
            else:
                dot.node(vertex, vertex)
                
        def edges(vertex, neighbor, dist):
            if vertex in self.start_end_path and neighbor in self.start_end_path:
                dot.edge(vertex, neighbor, fillcolor='green', color='green', label=str(dist), fontcolor='red')
            else:
                dot.edge(vertex, neighbor, label=str(dist))           

        for vertex, neighbor in self.graph.items():
            vertices(vertex)
            
            for v, dist in neighbor.items():
                vertices(v)
                edges(vertex, v, dist)
        
        dot.render('graph.dot', view=True)

g = Graph()        

g.read_graph()

g.find_shortest_path()

g.visualize()