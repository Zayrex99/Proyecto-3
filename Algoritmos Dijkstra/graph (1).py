from node import Node
from edge import Edge
from queue import PriorityQueue
import math

class Graph:
    def __init__(self,id="grafo", directed=False, auto=False):
        """
        Constructor
        """
        self.id=id
        self.nodes={}
        self.edges={}
        self.directed= directed
        self.auto=auto


    def addNode(self, id):
        """
        Agrega nodo al grafo, en caso de que no exista lo crea, si existe, regresa el nodo
        encontrado en el diccionario
        :param id= Node Id
        :return: node
        """
        new_node=self.nodes.get(id)
        if new_node is None:
            new_node=Node(id)
            self.nodes[new_node.id]=new_node
        return new_node

    def addEdge(self, source, target):
        """
        Agregar una arista al grafo, los nodos deben ser agregados con anterioridad, si no,
        levanta una excepcion
        :param source: Node source
        :param target: Node target
        """

        #Si los nodos no se encuentran en el grafo, levantar excepcion
        if self.nodes.get(source) is None or self.nodes.get(target) is None:
            raise Exception("Nodos no encontrados en el grafo, por favor agregarlos primero")

        #nodos en grafo
        nodeSource=self.nodes[source]
        nodeTarget=self.nodes[target]

        #crear el id de la arista
        idAux=str(source)+' -> '+str(target)

        #Si el grafo es no dirigido, checar que no se repitan los vertices en el diccionario
        repeated=False
        autoAux=False
        if not self.directed:
            idAuxNotDirected=str(target) + ' -> ' +str(source)
            aux=self.edges.get(idAuxNotDirected)
            if not(aux is None):
                repeated=True
        
        #Si el grafo es no autociclico, checar que source y target no sean iguales
        if not self.auto:
            if source is target:
                #print(source, target)
                autoAux=True
        
        new_edge= self.edges.get(idAux)
        
        """
        chequeo para grafo no dirigido y no autociclico.
        si la arista es nueva (no se encuentra en el grafo) y los nodos no son repetidos
        agrega nueva arista
        """
        if new_edge is None and repeated is False and autoAux is False:
            new_edge= Edge(idAux, nodeSource, nodeTarget)
            self.edges[new_edge.id]=new_edge
            nodeSource.attr.get("neighbors").append(nodeTarget)
            nodeTarget.attr.get("neighbors").append(nodeSource)
            nodeSource.attr.get("edges").append(new_edge)
            nodeTarget.attr.get("edges").append(new_edge)
            
        return new_edge


    def getDegree(self, id):
        """
        Obtener el grado de nodo
        :param: id: Node id
        :return: Node degree
        """
        node=self.nodes.get(id)
        if node is None:
            return 0
        return len(node.attr["neighbors"])
    
    def getNode(self, id):
        """
        Encontrar nodo en el grafo
        :param id: Node id to find
        :return: found node
        """
        return self.nodes.get(id)

    def getTotalNodes(self):
        """
        Obtener el total de nodos en el grafo
        :return: total nodes
        """
        nodes=self.nodes
        if nodes is None:
            return 0
        return len(self.nodes)
    
    def getTotalEdges(self):
        """
        Obtener el total de aristas del grafo
        :return: total edges
        """
        edges=self.edges
        if edges is None:
            return 0
        return len(self.edges)
    
    ######GV files######
    def saveGV(self):
        """
        Crea el archivo .gv que posteriormente sera usado para la creacion de los grafos
        """

        #creacion del string gv
        graph=''
        graph+='digraph '+self.id+' {\n'
        
        for nodo in self.nodes:
            graph+=str(nodo)+';\n'

        for key, value in self.edges.items():
            graph+= value.id+';\n'

        graph+='}'

        #se escribe y salva el archivo
        name=self.id+'.gv'
        file = open(name, "w")
        file.write(graph)
        file.close()
        #se imprime q el file fue creado para saber cuando termina
        print('File GraphViz: '+name+' was created\n')
    

    def saveGVwithLabels(self):
        """
        Crea el archivo .gv con etiquetas que posteriormente sera usado para la creacion de los grafos
        """

        #creacion del string gv
        graph=''
        graph+='digraph '+self.id+' {\n'
        for key, value in self.nodes.items():
            graph+='\"nodo_'+str(value.id)+' ('+str(value.attr["distance"])+')\";\n'
        for key, value in self.edges.items(): 
            graph+= '\"nodo_'+str(value.source.id)+' ('+str(value.source.attr["distance"])+')\" -> '+'\"nodo_'+str(value.target.id)+' ('+str(value.target.attr["distance"])+')\" [weight='+str(value.attr["weight"])+'];\n'
        graph+='}'

        #se escribe y salva el archivo
        name=self.id+'.gv'
        f = open(name, "w")
        f.write(graph)
        f.close()
        
        #se imprime q el file fue creado para saber cuando termina
        print('File GraphViz: '+name+' was created\n')


    ############Proyecto 2 (BFS, DFS iterativo y DFS recursivo)###################   
    #BFS
    def BFS(self,s):
        """
        BFS
        :param s: nodo raiz
        """
        try:
            name = self.id + '_BFS_'+str(s)
            #Objeto grafo bfs
            bfsGraph = Graph(name)
            #Fila para el algoritmo BFS
            queue = []
            #Obtener objeto nodo a partir de nodo raiz
            s=self.nodes[s]
            # Agreagr nodo a la fila 
            queue.append(s)
            #Poner al nodo como visitado
            s.attr["visitedBFS"] = True
            #Agregar nodo a grafo BFS
            bfsGraph.addNode(s.id) 
            #Mientras encuentre nodos en la fila
            while queue: 
                #Sacar el primer objeto nodo de la fila 
                s = queue.pop(0)               
                #Obtener los vecinos del nodo s
                neighbors = s.attr["neighbors"]
                #Iterar los vecinos del nodo s
                for nodeNeighbor in neighbors:
                    #Si el nodo aún no ha sido visitado
                    if not (nodeNeighbor.attr["visitedBFS"]):
                        #Agregar nodo a la fila
                        queue.append(nodeNeighbor)
                        #Poner al nodo como visitado
                        nodeNeighbor.attr["visitedBFS"] = True
                        #Agregar nodo a grafo BFS
                        bfsGraph.addNode(nodeNeighbor.id) 
                        #Agregar arista a grafo BFS
                        bfsGraph.addEdge(s.id,nodeNeighbor.id) 
            return bfsGraph
        except:
            print("Por favor agrega un nodo raiz valido")


    #DFS iterativo
    def DFS_I(self,s):
        """
        DFS iterativo
        :param s: nodo raiz
        """
        try:              
            name =  self.id +'_DFS_I_'+str(s)
            #Generar objeto grafo
            dfs_i_Graph = Graph(name)
            # Pila para el algoritmo DFS
            stack = []
            #Obtener objeto nodo a partir de nodo raiz
            s=self.nodes[s]
            #Agregar nodo a la pila
            stack.append(s)
            #agregar nodo s al grafo DFSI
            dfs_i_Graph.addNode(s.id)
            while stack:
                # Remover un elemento de la pila y asignarlo a s
                s = stack.pop()
                # Si no ha sido visitado marcarlo como visitado
                if not s.attr["visitedDFSI"]:
                    s.attr["visitedDFSI"] = True
                #Obtener los vecinos del nodo s
                neighbors = s.attr["neighbors"]
                #Iterar vecinos
                for neighbor in neighbors:
                    # Si un vecino no ha sido visitado, entrar
                    if not neighbor.attr["visitedDFSI"]:
                        #Agregar nodo al grafo DFSI
                        dfs_i_Graph.addNode(neighbor.id)
                        #Agregar nodo a la pila
                        stack.append(neighbor)
                        #Agregar el nodo raiz del actual nodo al atributo rootNodeDFSI 
                        neighbor.attr["rootNodeDFSI"]=s.id
                        ##dfs_i_Graph.addEdge(s.id,neighbor.id)
            #Iterar nodos para agregar aristas a los nodos
            for key, node in self.nodes.items():
                if node.attr["rootNodeDFSI"]>-1:
                    #Agregar arista
                    dfs_i_Graph.addEdge(key,node.attr["rootNodeDFSI"])
            return dfs_i_Graph
        except:
            print("Por favor agrega un nodo raiz valido")


    #DFS recursivo
    def DFS_R(self,s):
        """
        DFS recursivo usuario
        :param s: nodo raiz
        """
        try: 
            name = self.id +'_DFS_R_'+str(s)
            #Generar objeto grafo
            dfs_r_Graph = Graph(name)
            # Crear un conjunto de nodos visitados vacio
            visited = set()
            #Obtener objeto nodo a partir de nodo raiz
            s=self.nodes[s]
            # Llamar la funcion recursiva dfsRecursive
            self.dfsRecursive(visited,s,dfs_r_Graph)
            return dfs_r_Graph
        except:
            print("Por favor agrega un nodo raiz valido")

    def dfsRecursive(self,visited,node,dfs_r_Graph):
        """
        Auxiliar DFS recursivo 
        :param visited: nodos visitados
        :param node: nodo a trabajar
        :param dfs_r_Graph: grafica final
        """
        # Marcar el nodo como visitado
        visited.add(node.id)
        #Agregar nodo a grafo DFS    
        dfs_r_Graph.addNode(node.id) 
        #Obtener los vecinos del nodo s
        neighbors = node.attr["neighbors"]

        #Recorrer de manera recursiva los vecinos del nodo
        for neighbor in neighbors:
            #Si nodo no esta en el conjunto visitado
            if neighbor.id not in visited:
                #llamer recursivamente a dfsRecursive
                self.dfsRecursive(visited, neighbor, dfs_r_Graph)
                #Agregar arista
                dfs_r_Graph.addEdge(node.id,neighbor.id)
    

    #########Proyecto 3 - Algoritmo de Dijkstra###############
    def Dijkstra(self, s):
        """
        Algoritmo Dijkstra
        :param s: nodo raiz donde empieza el algoritmo
        """
        #Crear cola de prioridades
        q=PriorityQueue()
        #Crear lista S vacia
        S=[]
        dijkstraGraph=None
        #Obtener objeto nodo a partir de nodo raiz
        nodeSource=self.nodes[s]
        #Poner en cero la distancia de nodo raiz
        nodeSource.attr["distance"]=0
        #igualar d a la distancia raiz
        d=nodeSource.attr["distance"]
        #agregar a la cola de prioridades distancia, nodo. esto se hace para mapear de acuerdo al nodo, obtener su distancia
        q.put((d, nodeSource.id))
        
        #mientras la cola de prioridades no este vacia ejecutar
        while not q.empty():
            #obtener elemento de la cola de prioridades de acuerdo a la distancia
            u = q.get()
            #obtener el objeto nodo, este sera el nodo U
            u=self.nodes[u[1]]
            #agrega a la lista el id del nodo que es visitado 
            S.append(u.id)
            #obtener el id de las aristas que se conectan con u
            edges_u_v = u.attr["edges"]

            #obtener aristas conectadas a u
            for edge in edges_u_v:

                #si el id del nodo target es igual al nodo u, v sera el nodo fuente
                if edge.target.id == u.id:
                    v= edge.source
                #de otra manera v sera el target
                else:
                    v=edge.target 
                #si el nodo V no se encuentra en la lista de visitados
                if v.id not in S:
                    #d= distancia nodo U + peso de la arista que conecta u,v
                    d=u.attr["distance"] + edge.attr["weight"]
                    #si la distancia de v es mayor a d
                    if v.attr["distance"] > d:   
                        #asignar a v el padre, el cual sera u                     
                        v.attr["parent"]=u.id
                        #asignar distancia a v
                        v.attr["distance"]=d
                        #asignar peso de arista para construir el grafo Dikstra posteriormente
                        v.attr["edgeWeight"]=edge.attr["weight"]
                        #agregar a la cola de prioridades el nodo v y su peso
                        q.put((d, v.id))
        #auxiliar para crear arbol dijkstra        
        aux=False
        
        #mientras la lista no este vacia
        while S:
            #sacar nodo Id de la lista
            nodeId=S.pop()
            #obtener nodo objeto a partir del id
            node=self.nodes[nodeId]
            #obtener nodo padre
            nodeParent=node.attr["parent"]
            #si es la primera vez que se entra
            if not aux:
                #crear el arbol dijkstra
                name= self.id+ "_Dijkstra" + "_nodeSource_"+ str(s) 
                dijkstraGraph = Graph(name)
                #poner el auxiliar a verdadero para que no vuelva a entrar
                aux=True
            
            #si el nodoPadre no es None
            if nodeParent is not None:                
                #agregar nodo al grafo dijkstra, si ya esta, regresa nodo objeto
                nodeAux=dijkstraGraph.addNode(node.id)
                #si la distancia es inf, entonces aun no se ha asignado
                if math.isinf(nodeAux.attr["distance"]):
                    #asignar la distancia del nodo dijkstra igual a la distancia del nodo del grafo original
                    nodeAux.attr["distance"]=node.attr["distance"]
                #agregar nodo padre al arbol dijkstra
                dijkstraGraph.addNode(nodeParent)
                #agregar arista, nodoSource= nodo Padre, nodoTarget= nodo
                dijkstraGraph.addEdge(nodeParent, node.id)
                #poner el peso de la arista del grafo dijkstra igual al peso de la arista del grafo original
                dijkstraGraph.setEdgeWeight(node.attr["edgeWeight"],nodeParent, node.id)
            #Si el nodo padre es none, entonces es el nodo raiz que el usuario asigno
            else:
                #poner en cero la distancia del nodo raiz del grafo dijkstra
                nodeAux=dijkstraGraph.getNode(nodeId)
                nodeAux.attr["distance"]=0
            #poner en inf (valor original) a la distancia del nodo del grafo original
            node.attr["distance"]=float('inf')
        #regresar 
        return dijkstraGraph
    

    def setEdgeWeight(self,weight, source, target):
        """
        Funcion que asigna el peso de una arista
        :param weight: peso
        :param source: nodo fuente
        :param target: nodo objetivo
        """
        #crear el id de la arista
        idAux=str(source)+' -> '+str(target)
        #obtener la arista objeto
        aux=self.edges.get(idAux)
        #si arista existe
        if aux is not None:
            #asignar a la arista el peso
            aux.attr["weight"]=weight
