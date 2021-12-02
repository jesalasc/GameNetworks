# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:27:11 2021

@author: jesal
"""

import networkclass as ntc
import pickle as pk
import json
import os

path = './'

users_config = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'user_' in file:
            users_config.append(os.path.join(r, file))

students = []

for user_file in users_config:
    
    with open(user_file, 'rb') as config_user_file:
     
        # Step 3
        students.append(pk.load(config_user_file))
        config_user_file.close()


with open('Users.txt') as f:
    data = f.read()
    Users = json.loads(data)
    f.close()

with open('Metadata.txt') as f:
    data = f.read()
    Metadata = json.loads(data)
    f.close()

graph_path = "Graph_Round"+str(Metadata["Round"])+".txt"

Game = ntc.Networks_Game(Users.keys(), graph_path, Round = Metadata["Round"])

Game.apply_changes(students)

Game.save_network("Graph_Round"+str(Game.round)+".txt")


with open('Metadata.txt', 'w') as fp:
    json.dump(Metadata, fp)
    fp.close()

for config_file in users_config:
    os.remove(config_file)
    
Metadata["Round"] = Game.round