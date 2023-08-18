import tkinter as tk
import pandas as pd
import numpy as np
import tkinter.messagebox as tkm
import matplotlib.pyplot as plt

results = pd.read_csv("JEC Results.csv")

def meanclg():
    tkm.showinfo(title="Mean",message=(round(np.mean(results['SGPA']),3)))


def meanBr():
    brmean = ''
    for i in ['AI','CS','IT','EC','EE','CE','ME','MT']:
        brmean += f"{i} = {round(np.mean(results[results['Branch'] == i]['SGPA']),2)}\n"

    tkm.showinfo(title= 'Branches MEAN', message=brmean)


def sgpa():
    plt.scatter(results['Branch'], results['SGPA'],c='#F2A982')
    plt.xlabel('Branch')
    plt.ylabel('NO. Of Students')
    plt.title('Branch VS SGPA')
    plt.show()


def passcount():
    pas = results[results['Result'] != 'FAIL']['Result'].count()
    total = results['Result'].count()
    per = (pas/total)*100

    tkm.showinfo(title="Passed Percentage",message=f"PASSED % {str(round(per,2))}%")


def passbr():
    passs = ''
    for i in ['AI','CS','IT','EC','EE','CE','ME','MT']:
        branch = results[results['Branch'] == i]
        pas = branch['Result'].value_counts()['FAIL']
        total = branch['Branch'].value_counts()[i]
        per = ((total - pas)/total)*100
        passs += f'{i} : {str(round(per,2))}% \n'

    tkm.showinfo(title='PASS% BY BRANCH', message=passs)


def pcount():
    pas = results[results['Result'] != 'FAIL']['Result'].count()
    total = results['Result'].count()
    fail = total - pas

    tkm.showinfo(title="NUMBERS",message=f"PASS: {pas}\nFAIL: {fail}\nTOTAL: {total}")


def pbr():
    passs = ''
    for i in ['AI','CS','IT','EC','EE','CE','ME','MT']:
        branch = results[results['Branch'] == i]
        fail = branch['Result'].value_counts()['FAIL']
        total = branch['Branch'].value_counts()[i]
        pas = total - fail
        passs += f'{i}\nPASS: {pas} FAIL: {fail} TOTAL: {total}\n'

    tkm.showinfo(title='NUMBERS', message=passs)


def sgpaa(roll):
    sgpa = results[results['Roll'] == roll]['SGPA']
    sgpa = sgpa.item()
    tkm.showinfo(title=f"SGPA OF {roll}",message=sgpa)


def percentile(roll):
    sgpa = results[results['Roll'] == roll]['SGPA']
    sgpa = sgpa.item()

    lesser = results[results['SGPA'] <= sgpa]['SGPA'].count()
    total = results['SGPA'].count()

    per = round((lesser/total)*100,3)

    tkm.showinfo(title='PERCENTILE',message=str(per))


root = tk.Tk()
#Colors:-   #F2A982  #B74100
tk.Label(text="                JEC RESULT ANALYSIS               ",font="Arial 25 bold",bg='#B74100',fg='#F2A982').place(x=0,y=20)

tk.Label(text="----------------------------Functions----------------------------",font="Arial 20 bold",fg='#B74100',bg='#F2A982').place(x=0,y=90)

tk.Label(text="Mean SGPA of CLG",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=140)
tk.Label(text="Mean Values Of Branches",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=180)
tk.Label(text="SGPAs Analysis",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=220)
tk.Label(text="PASS percentage",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=260)
tk.Label(text="PASS% By Branch",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=300)
tk.Label(text="PASS PASS# FAIL No.",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=340)
tk.Label(text="P/P#/F No. Branch",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=380)

tk.Label(text="Percentile",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=480)
tk.Label(text="SGPA",font="Arial 17 bold",fg='#B74100',bg='#F2A982').place(x=10,y=520)


roll = tk.StringVar()
roll.set("ROLL NO.")


tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=meanclg).place(x=350,y=140)
tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=meanBr).place(x=350,y=180)
tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=sgpa).place(x=350,y=220)
tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=passcount).place(x=350,y=260)
tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=passbr).place(x=350,y=300)
tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=pcount).place(x=350,y=340)
tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=pbr).place(x=350,y=380)


tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=lambda: percentile(roll.get())).place(x=450,y=480)
tk.Entry(textvariable=roll,bg='#B74100',fg='#F2A982',font=6).place(x=200,y=480)
tk.Button(text="SHOW",bg='#B74100',fg='#F2A982',command=lambda: sgpaa(roll.get())).place(x=450,y=520)
tk.Entry(textvariable=roll,bg='#B74100',fg='#F2A982',font=6).place(x=200,y=520)


root.configure(bg='#F2A982')
root.geometry("650x650")
root.title("JEC RESULT ANALYSIS")
root.mainloop()