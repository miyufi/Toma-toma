# Imports from libraries
from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA
import streamlit as st
from PIL import Image

import csv
import random
import time

# Assign questions to lists tsaka para di na rin makalat
q1 = ["Question 1", "(aa + bb)(a + b)*(a + b + ab + ba)(a + b + ab + ba)*(aa + bab)*(a + b + aa)(a + b + bb + aa)*"]
q2 = ["Question 2", "((101 + (111)* + 100) + (1 + 0 + 11)*)(1 + 0 + 01)*(111 + 000 + 101)(1 + 0)*"]

# Assigned empty lists for string generation
genlist = []
ran = []

# Reads csvfile that contains combinations of 01 and ab
with open('Generators/Binary.csv', newline = '') as csvfile:
    binary = list(csv.reader(csvfile))

with open('Generators/ABCombi.csv', newline = '') as csvfile:
    abcombi = list(csv.reader(csvfile))

# Tab Title and Favicon
st.set_page_config(page_title = "Toma-toma", page_icon = "💻", layout = "centered")

# Title
st.write("<h1 style = 'text-align: center'>Toma-toma 💻</h1>", unsafe_allow_html = True)

# Input
st.subheader('Select Automata Question')
choice = st.selectbox("", [q1[0], q2[0]])
    
# DFA coding from visual DFA library
if choice == q1[0]:
    st.subheader('Regular Expression:')
    st.write("<p style = 'text-align: center;'</p>" + q1[1], unsafe_allow_html = True)
    dfa = VisualDFA(
    states = {"q0", "q1", "q2", "q3", "q4", "q5", "T"},
    input_symbols = {"a", "b"},
    transitions = {
        "q0" : {"a" : "q1", "b" : "q2"},
        "q1" : {"a" : "q3", "b" : "T"},
        "q2" : {"a" : "T", "b" : "q3"},
        "q3" : {"a" : "q4", "b" : "q4"},
        "q4" : {"a" : "q5", "b" : "q5"},
        "q5" : {"a" : "q5", "b" : "q5"},
        "T" : {"a" : "T", "b" : "T"},
    },
    initial_state = "q0",
    final_states = {"q5"},
    )

if choice == q2[0]:
    st.subheader('Regular Expression:')
    st.write("<p style = 'text-align: center;'</p>" + q2[1], unsafe_allow_html = True)
    dfa = VisualDFA(
    states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"},
    input_symbols = {"0", "1"},
    transitions = {
        "q0" : {"0" : "q2", "1" : "q1"},
        "q1" : {"0" : "q5", "1" : "q3"},
        "q2" : {"0" : "q4", "1" : "q1"},
        "q3" : {"0" : "q5", "1" : "q6"},
        "q4" : {"0" : "q6", "1" : "q1"},
        "q5" : {"0" : "q4", "1" : "q6"},
        "q6" : {"0" : "q6", "1" : "q6"},
    },
    initial_state = "q0",
    final_states = {"q6"},
    )

try:         
    graph = dfa.show_diagram() # Assigns the dfa graph to the variable then renders in lines starting from 164
    col1, col2 = st.beta_columns([1,1]) # Format
    temp = st.empty # Placeholder
    st.sidebar.subheader("Actions:")
    actions = st.sidebar.selectbox("", ["String Checker", "Generate Random Strings", "CFG"]) # selection box from streamlit
    with st.sidebar.form(key = 'my_form'): # Form
        if actions == "String Checker":
            st.markdown("### Input Strings")
            inpt = st.text_input("")
            check = st.form_submit_button('Check')
            
        elif actions == "Generate Random Strings":
            st.markdown("### Number of strings to generate")
            inpt = str(st.number_input("", value = 0))
            check = st.form_submit_button('Generate')

        elif actions == "CFG":
            inpt = "0"
            check = st.form_submit_button('Show CFG')

        # Pangremove lang ng mga kalat sa iinput ng user kunwari spaces at quotation marks
        inpt = inpt.replace(" ", "")
        inpt = inpt.replace("\"", "")
        
        # Kapag walang ininput at nagcheck, eto lalabas
        if check and not inpt:
            st.write("Please input a string!")

        # Code for string checking
        elif actions == "String Checker" and check:
            try: # Naka try catch kasi nageerror kapag wala 
                accept = dfa.input_check(inpt) # Checks input if accepted sa dfa na napili sa taas
                if "[Accepted]" in accept:
                    out = "Accepted."
                else:
                    out = "Not Accepted."
                input_list = list(inpt) # Logic for animation, nagcycycle through lang sa ininput ng user para magkaroon ng "animation"
                length = len(input_list)
                temp = st.empty
                for x in range(length):
                    graph = dfa.show_diagram(input_list[0])
                    input_list[0:2] = [''.join(input_list[0:2])]
                    graph.format = "png"
                    graph.render("tomatoma")
                    image = Image.open('tomatoma.png')
                    with col1: # kaya nakacol 1 siya para mapunta siya sa gitna imbis na sa sidebar
                        temp = st.image(image, width = 700)
                        time.sleep(2)
                        temp.empty()
                    
            except:
                out = "Not Accepted."
            st.write("The String `" + inpt + "` is " + out)

        elif actions == "Generate Random Strings" and check: # Random strings generation logic
            tem = 0 # Placeholder
            if int(inpt) > 0:
                if choice == q1[0]: 
                    while tem <= int(inpt): # So ang ginagawa ng loop na to is kumukuha siya ng random galing sa csv files na abcombi at binary tapos ichecheck sa dfa
                        ran = random.choice(abcombi)
                        acc = dfa.input_check(ran[0])
                        if "[Accepted]" in acc: # Kapag accepted then +1 tapos extend sa list na genlist
                            tem = tem + 1
                            genlist.extend(ran)

                elif choice == q2[0]:
                    while tem <= int(inpt):
                        ran = random.choice(binary)
                        acc = dfa.input_check(ran[0])
                        if "[Accepted]" in acc:
                            tem = tem + 1
                            genlist.extend(ran)
                st.write(genlist[1:]) # Print lahat ng mga accepted depende sa kung gaano kadami ininput ng user 
            else:
                st.write("Enter a Positive Integer.")

        elif actions == "CFG" and check: # Normal na pangprint lang talaga ng CFG, walang special kahit format wala hahahaha 
            st.write("CFG:")
            if choice == q1[0]:
                st.write("S -> PQ")
                st.write("P -> aa | bb")
                st.write("Q -> aR | bR")
                st.write("R -> aT | bT")
                st.write("T -> aT | bT | ^")

            elif choice == q2[0]:
                st.write("S -> PQP")
                st.write("P -> 0P | 1P | ^")
                st.write("Q -> 111 | 101 | 000")

    graph.format = "png" # Pangchange ng format ng render kasi kapag hindi chinange, magiging pdf
    graph.render("tomatoma") # Name ng png image
    st.subheader("DFA:") 
    image = Image.open('tomatoma.png') # Ioopen lang image
    st.image(image, width = 700) # Print image
        
except: # If wala to, laging may error sa simula ng streamlit kaya naglagay ng placeholder para magload lagi ng maayos at walang errors
    st.empty()
