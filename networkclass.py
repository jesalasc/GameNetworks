# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 09:58:06 2021

@author: jesal
"""
import networkx as nx

class Networks_Game:
    
    def __init__(self, Network = None, Round = 0, students):
        
        if Network == None:
            self.graph = nx.Graph()
        else:
            self.graph = Network
            
        self.round = Round
        self.students = students
        
        