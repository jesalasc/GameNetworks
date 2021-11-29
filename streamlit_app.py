# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:28:14 2021

@author: jesal
"""


import streamlit as st
#import networkclass as ntc
import json

def check_identity(ID, PASSWORD):
    
    # reading the data from the file
    with open('Users.txt') as f:
        data = f.read()
        Users = json.loads(data)
        f.close()

    if ID in Users.keys():
        if Users[ID] == PASSWORD:
            return True
    return False

def main():
    
    """
    # Game of networks
    Introduce your user id and password:
    """
  

    
    USER_ID = st.text_input("Enter your student ID", "", 8,"USER_ID")
    
    PASSWORD = st.text_input("Enter your password", "", 8,"PASSWORD")
    
    LOGIN = st.button("ENTER",None, check_identity, (USER_ID, PASSWORD))
    
    if LOGIN:
        st.writ("Login success")