import os
import tkinter
from datetime import datetime
from random import randint
from time import time

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Iestatījumi zinātniskiem grafikiem
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

# Galvenie mainīgie
GARUMS, PLATUMS = 800, 600
RĀDIUSS = 30
REIZES = 10

def attiestīt():
    '''Aizved uz spēles sākuma logu.'''
    audekls.place_forget()
    audekls.unbind_all('<Button-1>')
    TekstsApraksts.place(relx=0.5, rely=0.35, anchor='center')
    IevadesLauks.place(relx=0.5, rely=0.4, anchor='center')
    PogaSākt.place(relx=0.5, rely=0.5, anchor='center')

def sāktSpēli():
    '''Uzsāk spēli.'''
    global REIZES

    # Pārbauda ievades lauku
    try:
        REIZES = int(IevadesLauks.get())
        if REIZES <= 10:
            REIZES = 10
    except ValueError:
        REIZES = 10  # Noklusējuma vērtība

    # Notīra logu
    TekstsApraksts.place_forget()
    IevadesLauks.place_forget()
    PogaSākt.place_forget()

    # Pievieno audeklu, kur viss tiek zīmēts:
    audekls.place(relx=0.5, rely=0.5, anchor='center')

    audekls.bind('<Button-1>', gājiens)

    global izpildītas_r, laiks
    izpildītas_r = 0
    laiks = time()
    laiki.clear()
    attālumi.clear()

def gājiens(notikums):
    '''Pārbauda, vai uzspiests uz apļa.'''
    if 'current' in audekls.gettags(aplis):
        global aplis_x, aplis_y, izpildītas_r, laiks
        laiki.append(time() - laiks)
        laiks = time()
        attālums = np.sqrt((notikums.x - aplis_x)**2 + (notikums.y - aplis_y)**2)
        attālumi.append(attālums)
        
        aplis_x = randint(RĀDIUSS, GARUMS - RĀDIUSS)
        aplis_y = randint(RĀDIUSS, PLATUMS - RĀDIUSS)
        audekls.moveto(aplis, aplis_x - RĀDIUSS, aplis_y - RĀDIUSS)
        izpildītas_r += 1

        if izpildītas_r == REIZES:
            pabeigtSpēli()

def pabeigtSpēli():
    '''Aprēķina statistiku un parāda rezultātus.'''
    attiestīt()
    parādītStatistiku()

def parādītStatistiku():
    '''Attēlo grafikus par spēles rezultātiem.'''
    apļu_numuri = np.arange(1, len(laiki) + 1)
    vid_attālums = np.mean(attālumi)
    vid_laiks = np.mean(laiki)

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Spēles rezultātu analīze', fontsize=16)

    # 1. Apļa numurs pret attālumu līdz centram
    axs[0, 0].plot(apļu_numuri, attālumi, marker='o', linestyle='-', color='b')
    axs[0, 0].axhline(vid_attālums, color='r', linestyle='--', label=f'Vidējais attālums: {vid_attālums:.2f}')
    axs[0, 0].set_title('Attālumu līdz centram')
    axs[0, 0].set_xlabel('Apļa numurs')
    axs[0, 0].set_ylabel('Attālums (px)')
    axs[0, 0].legend()

    # 2. Apļa numurs pret reakcijas laiku
    axs[0, 1].plot(apļu_numuri, laiki, marker='o', linestyle='-', color='g')
    axs[0, 1].axhline(vid_laiks, color='r', linestyle='--', label=f'Vidējais laiks: {vid_laiks:.2f}s')
    axs[0, 1].set_title('Reakcijas laiku')
    axs[0, 1].set_xlabel('Apļa numurs')
    axs[0, 1].set_ylabel('Reakcijas laiks (s)')
    axs[0, 1].legend()

    # 3. Gausa sadalījums (attālumi)
    sns.histplot(attālumi, kde=True, color='blue', ax=axs[1, 0], bins=10)
    axs[1, 0].axvline(vid_attālums, color='r', linestyle='--', label=f'Vidējais: {vid_attālums:.2f}')
    axs[1, 0].set_title('Attāluma sadalījums (Gausa)')
    axs[1, 0].set_xlabel('Attēlums')
    axs[1, 0].set_ylabel('Biežums')
    axs[1, 0].legend()

    # 4. Gausa sadalījums (reakcijas laiki)
    sns.histplot(laiki, kde=True, color='green', ax=axs[1, 1], bins=10)
    axs[1, 1].axvline(vid_laiks, color='r', linestyle='--', label=f'Vidējais: {vid_laiks:.2f}s')
    axs[1, 1].set_xlabel('Reakcijas laiks (s)')
    axs[1, 1].set_ylabel('Biežums')
    axs[1, 1].set_title('Reakcijas laika sadalījums (Gausa)')
    axs[1, 1].legend()

    fig.tight_layout()
    fig.subplots_adjust(top=0.9)
    fig.show()

    #Izveido rezultātu mapi, ja tādas nav:
    try:
        os.mkdir('Rezultāti')
    except:
        pass
    #Saglabā grafiku
    fig.savefig(f'Rezultāti/{str(time())}.pdf')

# Spēles logs:
logs = tkinter.Tk()
logs.title('Cik lēns tu esi?')
logs.geometry(f'{GARUMS}x{PLATUMS}+0+0')
logs.resizable(width=False, height=False)

# Sākuma ekrāna elementi
TekstsApraksts = tkinter.Label(logs, text='Ievadiet apļu skaitu, ar kuriem vēlaties spēlēt (min:10):', font=("Helvetica", 12))
IevadesLauks = tkinter.Entry(logs, font=("Helvetica", 14))
IevadesLauks.insert(0, "10")

PogaSākt = tkinter.Button(logs, text='Sākt spēli', command=sāktSpēli)
audekls = tkinter.Canvas(logs, width=GARUMS, height=PLATUMS, bg='white')

# Izveido apli:
aplis_x = randint(RĀDIUSS, GARUMS - RĀDIUSS)
aplis_y = randint(RĀDIUSS, PLATUMS - RĀDIUSS)
aplis = audekls.create_oval(
    aplis_x - RĀDIUSS, aplis_y - RĀDIUSS,
    aplis_x + RĀDIUSS, aplis_y + RĀDIUSS,
    fill='black', outline='black'
)

# Ar spēli saistītie mainīgie:
izpildītas_r = 0
laiks = 0
laiki = []
attālumi = []

attiestīt()
logs.mainloop()
