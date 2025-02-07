import os
os.system('pip install art')

import json
import time
import random
import sys
import re
from art import *
from mystery import main as mystery
import ctypes

os.system('cls' if os.name == 'nt' else 'clear')
print("Installing required packages...")
time.sleep(2)

print("Loading questions...")
time.sleep(1)
data = json.load(open("preguntas_1.json", "r"))
print("Loading scores...")
time.sleep(1)
try:
    scores = json.load(open("scoretable.json", "r"))
except:
    scores = []
    with open("scoretable.json", "w") as f:
        json.dump(scores, f)
os.system('cls' if os.name == 'nt' else 'clear')

def get_display_name():
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3
 
    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)
 
    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    return nameBuffer.value

def scoretable(mode, score=None):
    if mode == "show":
        print("""
███████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗   
██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╗
███████╗██║     ██║   ██║██████╔╝█████╗  ███████╗╚═╝
╚════██║██║     ██║   ██║██╔══██╗██╔══╝  ╚════██║██╗
███████║╚██████╗╚██████╔╝██║  ██║███████╗███████║╚═╝
╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝   

""")
        print("\n\n\nLoading scores...\n\n\n")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
███████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗   
██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╗
███████╗██║     ██║   ██║██████╔╝█████╗  ███████╗╚═╝
╚════██║██║     ██║   ██║██╔══██╗██╔══╝  ╚════██║██╗
███████║╚██████╗╚██████╔╝██║  ██║███████╗███████║╚═╝
╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝   

    """)
        sorted_data = sorted(scores, key=lambda x: x["score"], reverse=True)
        top = 0
        for i in sorted_data:
            top += 1
            if top < 11:
                print(f"⯀⯀⯀ {i['name']}: ------------------------------- {i['score']}% - {i['date']} ⯀⯀⯀\n\n")
            else:
                break
        input("\n\nPress Enter to continue...")
    elif mode == "add":
        name = get_display_name()
        scores.append({"name": name, "score": score, "date": time.strftime("%d/%m/%Y")})
        with open("scoretable.json", "w") as f:
            json.dump(scores, f)
        

def final(selections, questions, showflags=[], mode=None):
    print("""
        ███████╗██╗███╗   ██╗ █████╗ ██╗         ███████╗ ██████╗ ██████╗ ██████╗ ███████╗
        ██╔════╝██║████╗  ██║██╔══██╗██║         ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
        █████╗  ██║██╔██╗ ██║███████║██║         ███████╗██║     ██║   ██║██████╔╝█████╗  
        ██╔══╝  ██║██║╚██╗██║██╔══██║██║         ╚════██║██║     ██║   ██║██╔══██╗██╔══╝  
        ██║     ██║██║ ╚████║██║  ██║███████╗    ███████║╚██████╗╚██████╔╝██║  ██║███████╗
        ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
    """)
    score = 0
    for idx, question in enumerate(questions):  # Use idx instead of looping over dicts
        if question["ans"] == [selections[idx]]:
            score += 1
        else:
            for selected in selections[idx]:  # Iterate over selected options
                if selected in question["ans"]:
                    score += (1 / len(question["ans"]))
                else:
                    score -= (1 / len(question["opt"])) if score > 0 else 0
    print('\n')
    tprint(f"{(round(score * 100)/(len(questions)) if (round(score * 100)/(len(questions))) > 0 else 0)}% - {'PASS!' if ((score * 100)/(len(questions)) >= 75) else 'FAIL :('}", font="colossal")
    print(f'Total score: {round(score)}/{len(questions)}\n\n')
    if mode == "exam":
        scoretable("add", (round(score * 100))/(len(questions)))
    input("Press Enter to continue...")
    

def progress_bar(actual, total_questions, bar_length=50):
    progress = round((actual / total_questions) * bar_length)  # Scale to bar_length
    bar = "⯀" * progress + " " * (bar_length - progress)  # Fill the bar
    percentage = round((actual / total_questions) * 100, 2)  # Percentage
    print(f"\nQuiz progress: [{bar}] {percentage}%\n")

def action(mode, quant=None):
    score = 0
    questions = random.sample(range(0, 171), (65 if mode == "exam" else int(quant)))
    questions = [data[str(i)] for i in questions]
    actual = 0
    selections = dict()
    showflags = []
    while actual <= len(questions):
        currentq = questions[actual] if actual < len(questions) else None
        selections[actual] = [] if actual not in selections.keys() else selections[actual]
        print("Controls (input):'C' Check answers (practice mode only) | 'N' - Next question | 'N' - Previous question | 'exit' - Exit the quiz\n")
        progress_bar(actual, len(questions))
        print("""
            █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
            ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
        """)
        if actual == len(questions):
            sel = input("""
You have finished the quiz. Do you want to see the answers? (Y/N): \n\n""")
            if sel.lower() == "y":
                os.system('cls' if os.name == 'nt' else 'clear')
                final(selections, questions, showflags, mode)
                os.system('cls' if os.name == 'nt' else 'clear')
                if mode == "exam":
                    print("Score added to the scoretable.")
                    input("Press Enter to continue...")
                break
            elif sel.lower() == "n":
                os.system('cls' if os.name == 'nt' else 'clear')
                actual -= 1
                continue
        else:
            print(currentq["q"].strip().upper() + ("?" if currentq["q"][-1].strip() not in [":", ".", "…", ";"] else "") + "\n") 
        print("""
            █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
            ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
        """)
        for i, a in enumerate(currentq["opt"]):
            print(f'{i} [{" " if i not in selections[actual] else "X"}]  {currentq["opt"][a].upper()}' + "\n")
        if mode == "practice" and actual in showflags:
            print(f"⯀⯀⯀ CORRECT OPTION NUMBER(S): {', '.join([str(i) for i in currentq['ans']])}")
            print(f"⯀⯀⯀ CORRECT ANSWER(S): {', '.join([currentq['opt'][str(i)].upper() for i in currentq['ans']])}")
            print("\n")
            if "exp" in currentq.keys():
                print(f"⯀⯀⯀ EXPLANATION: {currentq['exp']}")
        opt = input("Type N to continue..." if mode == 'practice' and actual in showflags else "Select an option: ")
        if opt.lower() == "exit":
            break
        elif opt.isdigit() and int(opt) in range(0, len(currentq["opt"])):
            if int(opt) in selections[actual]:
                selections[actual].remove(int(opt))
            else:
                selections[actual].append(int(opt))
        elif opt.lower() == "p" and actual > 0:
            actual -= 1
        elif opt.lower() == "n":
            actual += 1
        elif opt.lower() == "c" and mode == "practice":
            showflags.append(actual)
        os.system('cls' if os.name == 'nt' else 'clear')

def exam():
    print("""
            ███████╗██╗  ██╗ █████╗ ███╗   ███╗    ███╗   ███╗ ██████╗ ██████╗ ███████╗
            ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
            █████╗   ╚███╔╝ ███████║██╔████╔██║    ██╔████╔██║██║   ██║██║  ██║█████╗  
            ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  
            ███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗
            ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

In this mode, you will be asked a series of questions.
You won't be able to check the answers until the end in this mode.

To answer the questions, type the number of the answer you think is correct to select it. (If there's more than one correct answer, you can select them one by one)
If you want to deselect an answer, type the number of the answer again.

To go to the next question, type 'N'.
To go back to the previous question, type 'P'.

To exit the exam, type 'exit'.

Good luck!

    """)
    input("Press Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')
    action("exam")

def practice():
    print("""
            ██████╗ ██████╗  █████╗  ██████╗████████╗██╗ ██████╗███████╗    ███╗   ███╗ ██████╗ ██████╗ ███████╗
            ██╔══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██║██╔════╝██╔════╝    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
            ██████╔╝██████╔╝███████║██║        ██║   ██║██║     █████╗      ██╔████╔██║██║   ██║██║  ██║█████╗  
            ██╔═══╝ ██╔══██╗██╔══██║██║        ██║   ██║██║     ██╔══╝      ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  
            ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║╚██████╗███████╗    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗
            ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝╚══════╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

In this mode, you will be asked a series of questions.
You will be able to check the answers. Press 'C' to check the answers.

Scores will NOT be recorded in this mode.

To answer the questions, type the number of the answer you think is correct to select it. (If there's more than one correct answer, you can select them one by one)
If you want to deselect an answer, type the number of the answer again.

To go to the next question, type 'N'.
To go back to the previous question, type 'P'.

To exit the exam, type 'exit'.

""")
    quant = input("Select how many questions do you want to answer (1-171): ")
    if not quant.isdigit() or int(quant) < 1 or int(quant) > 171:
        print("Invalid input, asshole.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        practice()
    os.system('cls' if os.name == 'nt' else 'clear')    
    action("practice", quant)

print("""
                    ⠀              ⣠⣤⣶⣶⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣷⣤⠀⠈⠙⢿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⠆⠰⠶⠀⠘⢿⣿⣿⣿⣿⣿⣆⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⠏⠀⢀⣠⣤⣤⣀⠙⣿⣿⣿⣿⣿⣷⡀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⢠⠋⢈⣉⠉⣡⣤⢰⣿⣿⣿⣿⣿⣷⡈⢿⣿⣿⣿⣿⣷⡀
                    ⠀⠀⠀⠀⠀⠀⠀⡴⢡⣾⣿⣿⣷⠋⠁⣿⣿⣿⣿⣿⣿⣿⠃⠀⡻⣿⣿⣿⣿⡇
                    ⠀⠀⠀⠀⠀⢀⠜⠁⠸⣿⣿⣿⠟⠀⠀⠘⠿⣿⣿⣿⡿⠋⠰⠖⠱⣽⠟⠋⠉⡇
                    ⠀⠀⠀⠀⡰⠉⠖⣀⠀⠀⢁⣀⠀⣴⣶⣦⠀⢴⡆⠀⠀⢀⣀⣀⣉⡽⠷⠶⠋⠀
                    ⠀⠀⠀⡰⢡⣾⣿⣿⣿⡄⠛⠋⠘⣿⣿⡿⠀⠀⣐⣲⣤⣯⠞⠉⠁⠀⠀⠀⠀⠀
                    ⠀⢀⠔⠁⣿⣿⣿⣿⣿⡟⠀⠀⠀⢀⣄⣀⡞⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⡜⠀⠀⠻⣿⣿⠿⣻⣥⣀⡀⢠⡟⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⢰⠁⠀⡤⠖⠺⢶⡾⠃⠀⠈⠙⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠈⠓⠾⠇⠀⠀

             ██████╗ ██╗   ██╗██╗███████╗███████╗ █████╗ 
            ██╔═══██╗██║   ██║██║╚══███╔╝╚══███╔╝██╔══██╗
            ██║   ██║██║   ██║██║  ███╔╝   ███╔╝ ███████║
            ██║▄▄ ██║██║   ██║██║ ███╔╝   ███╔╝  ██╔══██║
            ╚██████╔╝╚██████╔╝██║███████╗███████╗██║  ██║
            ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ 
""")
input("Press Enter to continue...")
os.system('cls' if os.name == 'nt' else 'clear')

while True:
    print("""
            ███╗   ███╗ █████╗ ██╗███╗   ██╗    ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
            ████╗ ████║██╔══██╗██║████╗  ██║    ████╗ ████║██╔════╝████╗  ██║██║   ██║
            ██╔████╔██║███████║██║██╔██╗ ██║    ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
            ██║╚██╔╝██║██╔══██║██║██║╚██╗██║    ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
            ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║    ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
            ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝                                                             
    """)
    print("""
                                    1 - Exam mode
                                    2 - Practice mode
                                    3 - See scores
                                    4 - Exit

                                    69 - ????


    """)

    choice = input("                            Use numbers to select an option: ")
    if choice == "4":
        exit()
    elif choice == "69":
        mystery()
        exit()
    elif choice == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        exam()
    elif choice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        practice()
    elif choice == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        scoretable('show')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Invalid choice, dumbass.")
        time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')



                                                                                  

