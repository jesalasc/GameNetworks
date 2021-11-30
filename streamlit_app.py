# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:28:14 2021

@author: jesal
"""


import streamlit as st
import networkclass as ntc
import json

def check_identity(ID, PASSWORD):
    
    # reading the data from the file
    with open('Users.txt') as f:
        data = f.read()
        Users = json.loads(data)
        f.close()

    if ID in Users.keys():
        if Users[ID] == PASSWORD:
            return True, Users.keys()
        else:
            st.write("Wrong Password")
            return False, None
    else:
        st.write("Wrong ID")
        return False, None
    return False, None

def Init_Game(ID_List, Round):
    students_list = []
    for ID in ID_List:
        students_list.append(ntc.Student(ID))
    Game = ntc.Networks_Game(students_list,"Graph.txt")
    return Game

def main():
    
    if 'LogedIn' not in st.session_state:
        st.session_state.LogedIn = False
    
    st.title("Game of Networks")
    
    
    placeholder = st.empty()
    if not st.session_state.LogedIn:
        with placeholder.container():
            "Introduce your user id and password:"
            
            USER_ID = st.text_input("Enter your student ID", "", 8,"USER_ID")
            
            PASSWORD = st.text_input("Enter your password", "", 8,"PASSWORD")
            
            LOGIN = st.button("ENTER", "Login_Button")
            
            if LOGIN:
                attempt,ID_List = check_identity(USER_ID, PASSWORD)
                if attempt:
                    st.write("Log in successful")
                    st.session_state.LogedIn = True
                    with open('Metadata.txt') as f:
                        data = f.read()
                        Metadata = json.loads(data)
                        f.close()
                    st.sessionstate.Game = Init_Game(ID_List, Metadata["Round"])
                    st.sessionstate.User = ntc.Student(USER_ID)
                else:
                    st.write("Log in failed")
    
    else:
        placeholder.empty()
        Round = st.sessionstate.Game.Round
        st.title("Game of Networks Round: " + Round )
        
        if Round == 0:
            Available = st.sessionstate.Game.unconnectedOF(st.sessionstate.User.id)
            "Choose 2 connections to add"
            "Connection 1"
            add1 = st.selectbox("Add this connection", Available)
            "Connection 2"
            add2 = st.selectbox("Add this connection", Available)
            st.buttom("SELECT", "add button")

        
        else:
            Available = st.sessionstate.Game.unconnectedOF(st.sessionstate.User.id)
            Connected = st.sessionstate.Game.connectionsOF(st.sessionstate.User.id)
            "Choose 2 connections to add and one connection to remove"
            "Connection 1"
            add1 = st.selectbox("Add this connection", Available)
            "Connection 2"
            add2 = st.selectbox("Add this connection", Available)
            "Remove Connection"
            rem = st.selectbox("Add this connection", Connected)
            st.buttom("SELECT", "add button")
        
main()