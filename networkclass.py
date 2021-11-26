# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 09:58:06 2021

@author: jesal
"""
import networkx as nx

class Networks_Game:
    
    def __init__(self, students, Network = None, Round = 0):
        
        if Network == None:
            self.graph = nx.Graph()
            self.graph
        else:
            self.graph = Network
            
        self.round = Round
        self.students = students
        self.pending_changes = {}
        self.game_size = len(students)
        self.students_ids = []
        for student in students:
            self.pending_changes[student.id] = True
            self.students_ids.append(student.id)
        self.changes_made = 0
        
    def new_change(self, student, add1, add2, rem = None):
        connected_to = self.graph.neighbors(student.id)
        if self.round > 0:
            if add1 in connected_to and add1 in connected_to and rem in connected_to:
                student.add_changes(add1, add2, rem)
                self.pending_changes[student.id] = False
                self.changes_made+=1
                return True
        else:
            if add1 in connected_to and add1 in connected_to:
                student.add_changes(add1, add2, rem)
                self.pending_changes[student.id] = False
                self.changes_made+=1
                return True

    def apply_changes(self):
        
        if self.change_made == self.game_size and self.round > 0:
            to_add = []
            to_remove = []
            for student in self.students:
                to_add.append((student.id ,student.add1))
                to_add.append((student.id, student.add2))
                to_remove.append((student.id, student.rem))
            
            self.graph.remove_edges_from(to_remove)
            self.graph.add_edges_from(to_add)
            self.changes_made = 0
            self.round += 1
            
        elif self.change_made == self.game_size and self.round == 0:
            to_add = []
            for student in self.students:
                to_add.append((student.id ,student.add1))
                to_add.append((student.id, student.add2))
            
            self.graph.add_edges_from(to_add)
            self.changes_made = 0
            self.round += 1
        
        else:
            
            return False
        
        
class Student:
    
    def __init__(self, id):
        self.id = id
        self.add1 = None
        self.add2 = None
        self.rem = None
        self.decided = False
        
    def add_changes(self, add1, add2, rem):
        if not self.decided:
            self.add1 = add1
            self.add2 = add2
            self.rem = rem
            self.decided = True
            return True
        return False
        
        
        
        