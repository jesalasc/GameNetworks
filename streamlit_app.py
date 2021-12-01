# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:28:14 2021

@author: jesal
"""


import streamlit as st
import networkclass as ntc
import json
import pickle as pk

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
    
    Game = ntc.Networks_Game(ID_List,"Graph.txt", Round)
    return Game

def Log_in():
    
    placeholder = st.container()

    with placeholder:
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
                    st.session_state.Game = Init_Game(ID_List, Round = Metadata["Round"])
                    try:
                         with open('user_'+USER_ID+".config", 'rb') as config_user_file:
 
                             # Step 3
                             st.session_state.User = pk.load(config_user_file)
                             config_user_file.close()
                    except:
                        st.session_state.User = ntc.Student(USER_ID)
                    placeholder.empty()
                else:
                    st.write("Log in failed")
def Changes_screen():
    Round = st.session_state["Game"].round
    st.title("Game of Networks Round: " + str(Round))
    
    if Round == 0:
        with st.form("NewConnections"):
            Available = st.session_state.Game.unconnectedOF(st.session_state.User.id)
            "Choose 2 connections to add"
            "Connection 1"
            add1 = st.selectbox("Add this connection", Available, key= "add1")
            "Connection 2"
            add2 = st.selectbox("Add this connection", Available, key= "add2")
            submitted = st.form_submit_button("Submit")
            if submitted:
                
                SUBMISSION, MESSAGE = st.session_state.Game.new_change(st.session_state.User, add1, add2)
                st.write(MESSAGE)
                if SUBMISSION:
                    with open('user_'+st.session_state.User.id+".config", 'wb') as config_user_file:
 
                        # Step 3
                        pk.dump(st.session_state.User, config_user_file)
                        config_user_file.close()
                    st.empty()

    
    else:
        with st.form("NewConnections"):
            Available = st.session_state.Game.unconnectedOF(st.session_state.User.id)
            Connected = st.session_state.Game.connectionsOF(st.session_state.User.id)
            "Choose 2 connections to add"
            "Connection 1"
            add1 = st.selectbox("Add this connection", Available, key= "add1")
            "Connection 2"
            add2 = st.selectbox("Add this connection", Available, key= "add2")
            "Remove Connection"
            rem = st.selectbox("Add this connection", Connected, key = "rem")
            submitted = st.form_submit_button("Submit")
            
            if submitted:                  
                SUBMISSION,MESSAGE = st.session_state.Game.new_change(st.session_state.User, add1, add2, rem)
                st.write(MESSAGE)
                if SUBMISSION:
                    with open('user_'+st.session_state.User.id+".config", 'wb') as config_user_file:
 
                        # Step 3
                        pk.dump(st.session_state.User, config_user_file)
                        config_user_file.close()
                    st.empty()
          
    reset = st.container()
    with reset:
        st.button("Reset changes", key="ResetBut")
        if st.session_state.ResetBut:
            st.session_state.User.reset_changes()
            with open('user_'+st.session_state.User.id+".config", 'wb') as config_user_file:
 
                    # Step 3
                    pk.dump(st.session_state.User, config_user_file)
                    config_user_file.close()
            st.write("Your changes were reset.")
            
                
def Visualization():
    pass


def main():
    
    st.title("Game of Networks")

    if 'LogedIn' not in st.session_state:
        st.session_state.LogedIn = False
        
        
    if st.session_state.LogedIn == False:
        Log_in()
    
    else:
        Changes_screen()
        Visualization()
        
        
            
        
main()