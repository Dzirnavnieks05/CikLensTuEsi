'''Cik lēns Tu esi? Izveidot datorspēli, kas spēlētājam liek īsā laika sprīdī uzklikšķināt uz melna
apļa, kas parādās uz monitora gadījuma rakstura vietā. Pēc spēles beigšanas, programma aprēķina
statistisko analīzi (tai skaitā Gausa sadalījumu) tam, cik tuvu apļa centram spēlētājs klikšķinājis
un cik ātri viņš to spējis izdarīt. Programmas gala funkcionalitāte: Izpildot izveidoto Python
programmu, atveras grafiskais logs. Šajā grafiskajā logā lietotājs var spēlēt aprakstīto spēli. Pēc
spēles beigšanas, Python faila mapē saglabājas PDF grafiki ar aprakstīto statistisko analīzi.'''

import tkinter
from random import randint
from time import time
##from matplotlib import pyplot as plt

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

    
    audekls.bind('<Button-1>', gājiens)

    global izpildītas_r, laiks
    izpildītas_r = 0
    laiks = time()

##    fig.set_visible(False)
##    ax[0].clear()
##    ax[1].clear()


def gājiens(notikums):
    '''Pārbauda, vai uzspiests uz apļa.'''
    if 'current' in audekls.gettags(aplis):
        global aplis_x, aplis_y, izpildītas_r, laiks
        laiki.append(time()-laiks)
        laiks = time()
        attālumi.append((notikums.x-aplis_x)**2+(notikums.y-aplis_y)**2)
        
        aplis_x = randint(RĀDIUSS, GARUMS -RĀDIUSS)
        aplis_y = randint(RĀDIUSS, PLATUMS-RĀDIUSS)
        audekls.moveto(aplis,
            aplis_x-RĀDIUSS,
            aplis_y-RĀDIUSS
        )
        izpildītas_r += 1

        if izpildītas_r==REIZES:
            print('Viss')
            print(laiki)
            print(attālumi)

##            ax[0].bar(laiki, int(2*REIZES**(1/3)+1))
##            fig.show()
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

##fig, ax = plt.subplots(2, 1)
##ax[0].set(
##    title='Reakcijas laiks'
##)
##ax[1].set(
##    title='Attālums no centra'
##)



attiestīt()
logs.mainloop()

