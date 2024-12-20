'''Cik lēns Tu esi? Izveidot datorspēli, kas spēlētājam liek īsā laika sprīdī uzklikšķināt uz melna
apļa, kas parādās uz monitora gadījuma rakstura vietā. Pēc spēles beigšanas, programma aprēķina
statistisko analīzi (tai skaitā Gausa sadalījumu) tam, cik tuvu apļa centram spēlētājs klikšķinājis
un cik ātri viņš to spējis izdarīt. Programmas gala funkcionalitāte: Izpildot izveidoto Python
programmu, atveras grafiskais logs. Šajā grafiskajā logā lietotājs var spēlēt aprakstīto spēli. Pēc
spēles beigšanas, Python faila mapē saglabājas PDF grafiki ar aprakstīto statistisko analīzi.'''

import os
import tkinter
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np

from random import randint
from time import time

sad_gauss = lambda x, mu, s: np.exp(-np.square((x-mu)/s)/2) / np.sqrt(2*s)

#Galvenie mainīgie
GARUMS, PLATUMS = 800, 600
RĀDIUSS = 30
REIZES = 10

def attiestīt():
    '''Aizved uz spēles sākuma logu.'''
    audekls.place_forget()
    audekls.unbind_all('<Button-1>')
    PogaSākt.place(relx=0.5,rely=0.5, anchor='center')

def sāktSpēli():
    '''Uzsāk spēli.'''
    #Notīra logu
    PogaSākt.place_forget()

    #Pievieno audeklu, kur viss tiek zīmēts:
    audekls.place(relx=0.5,rely=0.5, anchor='center')

    #Notīra un paslēpj grafiku:
    ax_laiks.clear()
    ax_att.clear()
    
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
        laiki.append(time()-laiks)
        laiks = time()
        attālumi.append(np.sqrt((notikums.x-aplis_x)**2+(notikums.y-aplis_y)**2))
        
        aplis_x = randint(RĀDIUSS, GARUMS -RĀDIUSS)
        aplis_y = randint(RĀDIUSS, PLATUMS-RĀDIUSS)
        audekls.moveto(aplis,
            aplis_x-RĀDIUSS,
            aplis_y-RĀDIUSS
        )
        izpildītas_r += 1

        #Spēles beigas
        if izpildītas_r==REIZES:
            #Sarēķina statistiku:
            N_stabiņi = int(2*REIZES**(1/3)+1)#Stabiņu skaits pēc Rīsa likuma
            
            S_laiks = REIZES*(np.max(laiki)-np.min(laiki))/N_stabiņi#Gausa sadalījuma izstiepšana
            laiki_ = np.linspace(np.min(laiki), np.max(laiki))#Smukākam Gausa sadalījumam
            t_vid = np.average(laiki)
            t_std_nov = np.std(laiki)

            S_att = REIZES*(np.max(attālumi)-np.min(attālumi))/N_stabiņi#Gausa sadalījuma izstiepšana
            attālumi_ = np.linspace(np.min(attālumi), np.max(attālumi))#Smukākam Gausa sadalījumam
            a_vid = np.average(attālumi)
            a_std_nov = np.std(attālumi)

            #Liekam šeit, jo "Axes" objekti tiek pilnībā notīrīti
            ax_att.set(
                title='Attālumi'
            )
            ax_laiks.set(
                title='Laiki'
            )

            #Laiks
            ax_laiks.hist(laiki, bins=N_stabiņi)
            ax_laiks.annotate(
                text=f'Vidēji: {t_vid: .2f} s', 
                xy=(0.65, 0.9),
                xycoords='axes fraction'
            )
            ax_laiks.annotate(
                text=f'Std. nov.: {t_std_nov: .2f} s', 
                xy=(0.65, 0.85),
                xycoords='axes fraction'
            )
            ax_laiks.plot(laiki_, S_laiks*sad_gauss(laiki_, t_vid, t_std_nov))
            #Attālums
            ax_att.hist(attālumi, bins=N_stabiņi)
            ax_att.annotate(
                text=f'Vidēji: {a_vid: .2f} px', 
                xy=(0.65, 0.9),
                xycoords='axes fraction'
            )
            ax_att.annotate(
                text=f'Std. nov.: {a_std_nov: .2f} px', 
                xy=(0.65, 0.85),
                xycoords='axes fraction'
            )
            ax_att.plot(attālumi_, S_att*sad_gauss(attālumi_, a_vid, a_std_nov))
            
            fig.show()
            # try:
                

            attiestīt()

#Spēles logs:
logs = tkinter.Tk()
logs.title('Cik lēns tu esi?')
logs.geometry(f'{GARUMS}x{PLATUMS}+0+0')
logs.resizable(width=False, height=False)

PogaSākt = tkinter.Button(logs, text='Sākt spēli', command=sāktSpēli)
audekls = tkinter.Canvas(logs, width=GARUMS, height=PLATUMS, bg='white')

#Izveido apli:
aplis_x = randint(RĀDIUSS, GARUMS-RĀDIUSS)
aplis_y = randint(RĀDIUSS, PLATUMS-RĀDIUSS)
aplis = audekls.create_oval(
    aplis_x-RĀDIUSS,aplis_y-RĀDIUSS,
    aplis_x+RĀDIUSS,aplis_y+RĀDIUSS,
    fill='black', outline='black'
)

#Ar spēli saistītie mainīgie:
izpildītas_r = 0
laiks = 0
laiki = []
attālumi = []

#Histrogramma
ax_att: Axes
ax_laiks: Axes
fig, (ax_laiks,ax_att) = plt.subplots(
    ncols=2,
    num='Cik lēns tu esi? Apkopojums',
    figsize=(10,6)
)


attiestīt()
logs.mainloop()

