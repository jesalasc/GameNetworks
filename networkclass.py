
import networkx as nx

class Networks_Game:
    
    def __init__(self, students, Network = "Graph.txt", Round = 0):
        self.round = Round
        self.students = students
        self.pending_changes = {}
        self.game_size = len(students)
        for student in students:
            self.pending_changes[student] = True
        self.changes_made = 0
        #if Network == None:
        #    self.graph = nx.Graph()
        #    
        #else:
        self.graph = nx.read_edgelist(Network, create_using=nx.Graph())
        self.graph.add_nodes_from(self.students)
            
        
        
    def new_change(self, student, add1, add2, rem = None):
        decided = student.decided
        
        if add1 != add2 and (not decided):
            student.add_changes(add1, add2, rem)
            self.pending_changes[student.id] = False
            self.changes_made+=1
            return True,"Changes added."
        elif add1 == add2:
            return False,"New connections must be different."
        else:
            return False, "You already made changes."

    def apply_changes(self, students):
        
        if self.change_made == self.game_size and self.round > 0:
            to_add = []
            to_remove = []
            for student in students:
                to_add.append((student.id ,student.add1))
                to_add.append((student.id, student.add2))
                to_remove.append((student.id, student.rem))
            
            self.graph.remove_edges_from(to_remove)
            self.graph.add_edges_from(to_add)
            self.changes_made = 0
            self.round += 1
            return True
            
        elif self.change_made == self.game_size and self.round == 0:
            to_add = []
            for student in students:
                to_add.append((student.id ,student.add1))
                to_add.append((student.id, student.add2))
            
            self.graph.add_edges_from(to_add)
            self.changes_made = 0
            self.round += 1
            return True
        
        else:
            
            return False
    
    def connectionsOF(self, studentID):
        return list(self.graph.neighbors(studentID))
    
    def unconnectedOF(self, studentID):
        connected = self.connectionsOF(studentID)
        connected.append(studentID)
        return [x for x in self.students if (x not in connected)]
    
    def save_network(self):
        pass
    
    def compute_ranking(self):
        pass
        
        
        
class Student:
    
    def __init__(self, id):
        self.id = id
        self.add1 = None
        self.add2 = None
        self.rem = None
        self.decided = False
        
    def add_changes(self, add1, add2, rem= None):
        if not self.decided:
            self.add1 = add1
            self.add2 = add2
            self.rem = rem
            self.decided = True
            return True
        return False
    
    def reset_changes(self):
        self.add1 = None
        self.add2 = None
        self.rem = None
        self.decided = False
        
        
        
        