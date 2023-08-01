
import random
import socket
import sys
import threading
from tkinter import *
from functools import partial
import pygame
from threading import *
from pygame.locals import *
from PIL import ImageTk, Image

c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
addr=input("Enter IP address: ")
c.connect((addr,9998))
nickname=input("Enter your name: ")

#Tkinter window
gui=Tk()
gui.geometry('500x395')
gui.title('wordle login')
img = ImageTk.PhotoImage(Image.open("w2.jpg"))
label = Label(gui, image = img).grid(row=0,column=0)
usernameLabel=Label(gui,text="Instructions :",font=('bold', 17),fg="orange").grid(row=1,column=0)
usernameLabel=Label(gui,text="1.You have to guess the Wordle in six goes or less.",font=('Arial', 13)).grid(row=2,column=0)
usernameLabel=Label(gui,text="2.A correct letter turns green.  ",font=('Arial', 13)).grid(row=3,column=0)
usernameLabel=Label(gui,text="3.A correct letter in the wrong place turns yellow. ",font=('Arial', 13)).grid(row=4,column=0)
usernameLabel=Label(gui,text="4.An incorrect letter turns gray.",font=('Arial', 13)).grid(row=5,column=0)
usernameLabel=Label(gui,text="5.Try to guess word as fast as you can.",font=('Arial', 13)).grid(row=6,column=0)

#initializing colours
white = (255,255,255)
aliceblue = (240,248,255)
yellow = (255,255,102)
grey1 = (3,3,3)
grey = (139,139,131)
darkgreen = (47,79,79)
black =(0,0,0)
green=(0,255,0)
lightGreen=(255,127,0)
powderblue=(176,224,230)
w2=(245,245,245)
red=(208,32,144)
blue=(0,0,238)
r1=(238,0,0)

#Method to check the score of the word
def checkGuess(turns, word, userGuess, window):
    renderList = ["","","","",""]
    score_card = [0,0,0,0,0]
    ront = pygame.font.SysFont("Helvetica neue", 40)
    spacing = 0
    guessColourCode = [grey,grey,grey,grey,grey]
    for x in range(0,5):
        if userGuess[x] in word:
            guessColourCode[x] = yellow

        if word[x] == userGuess[x]:
            guessColourCode[x] = green
            score_card[x] = 100  
    score = sum(score_card)
    l.append(score)
    if(score>=max(l)):
        def write():
                if(score==500):
                     message = '{} WON THE GAME !!'.format(nickname.upper())
                     c.send(message.encode('ascii')) 
                else:
                    message = '{}: Score is {}'.format(nickname.upper(),score)
                    c.send(message.encode('ascii')) 
        write_thread = threading.Thread(target=write)
        write_thread.start()

    list(userGuess)

    for x in range(0,5):
        renderList[x] = ront.render(userGuess[x], True, black)
        pygame.draw.rect(window, guessColourCode[x], pygame.Rect(60 +spacing, 50+ (turns*80), 50, 50))
        window.blit(renderList[x], (70 + spacing, 50 + (turns*80)))
        spacing+=80

    if guessColourCode == [green,green,green,green,green]:

     return True


def main():
    pygame.init()
    file = open("wordList.txt","r")
    wordList = file.readlines()
    word = wordList[random.randint(0, len(wordList)-1)].upper()
    height = 650
    width = 500
    global l
    l=[100]
    global flag
    flag = False
    turns = 0
    global flag1
    flag1 = False
    win = False
    flag2 = False
    guess = ""

    window = pygame.display.set_mode((width, height))
    counter, text = 150, '150'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1600)
    font = pygame.font.SysFont('Consolas', 30)
    clock = pygame.time.Clock()
    window.fill(w2)
    
    ront = pygame.font.SysFont("Helvetica neue", 38)
    kont = pygame.font.SysFont("Alternate Gothic", 40)
    bigFont = pygame.font.SysFont("Helvetica neue", 80)
    sont = pygame.font.SysFont("Helvetica neue", 42)
    #lont= pygame.font.SysFont("Helvetica neue", 41)

    youWin = bigFont.render("You Win!",       True, lightGreen)
    youLose = bigFont.render("You Lose!",     True, r1)
    playAgain = bigFont.render("Play Again?", True, lightGreen)
    TryAgain = bigFont.render("Try Again!", True, r1)
    answer = kont.render("Your Word is :", True, red)
    
    print(word)

    for x in range(0,5):
         for y in range(0,6):
             pygame.draw.rect(window, grey1, pygame.Rect(60+(x*80), 50+(y*80), 50, 50),2)
    pygame.draw.rect(window, black, pygame.Rect(500, 0, 300, 650))

    reGuess = kont.render(nickname.upper(), True, blue)
    window.blit(reGuess, (116, 11))
    reG = kont.render(word[:5], True, lightGreen )
    reGue = ront.render("Player: ", True, red)
    window.blit(reGue, (20, 12))
    reGu = ront.render("Timer:  ", True, red)
    window.blit(reGu, (300, 12))
    pygame.display.set_caption("Wordle!")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
                
           
            if event.type == pygame.USEREVENT:
                if win != True and flag1 != True:
                    counter -= 1
                text = str(counter).rjust(3) if counter > 0 else 'boom!'
                if(counter==0):
                    #If time completed  automatically lose the game
                    window.blit(reG, (273, 420))
                    window.blit(answer,(80,420))
                    window.blit(youLose,(90,200))
                    window.blit(TryAgain,(78,300))
                    flag2=True
        
            if event.type == pygame.KEYDOWN:
                guess+=event.unicode.upper()
                
                if(str(guess[-1]).isalpha() == False):
                    guess = guess[:-1]

                if event.key == K_RETURN and win == True:
                    main()

        
                if event.key == K_RETURN and flag1 == True:
                    main()
                
                
                if event.key == K_RETURN and flag2 == True:
                    main()


                if event.key == K_RETURN and turns == 6:
                    main()

                if(len(guess) > 5):
                    n = len(guess)
                    guess = guess[:5]

                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                    
                if event.key == K_RETURN and len(guess) > 4:
                    win = checkGuess(turns, word, guess, window)
                    turns+=1
                    guess = ""
                    window.fill(white,(0,500, 500, 200))
        window.fill(w2,(380,10,80,30))
        window.blit(font.render(text, True, (0, 0, 0)), (380, 12))
        window.fill(darkgreen,(0,512, 500, 200))
        renderGuess = sont.render(guess, True, white)
        window.blit(renderGuess, (180, 535))

        if win == True:
            flag = True
            window.blit(youWin,(90,200))
            window.blit(playAgain,(60,300))

        if win == True:
             flag = True
             def write():
                #sending message to server that player win the game
                message = 'win the game'
                c.send(message.encode('ascii')) 
        
             write_thread = threading.Thread(target=write)
             write_thread.start()

        if turns == 6 and win != True:
            #If six chances completed automatically lose the game
            flag1 = True
            #window.fill(w2,(272, 420,85,22))
            window.blit(reG, (273, 420))
            window.blit(answer,(80,420))
            window.blit(youLose,(90,200))
            window.blit(TryAgain,(85,300))
        


        def write():
             while True:
                message = '{}: {}'.format(nickname,input(''))
                c.send(message.encode('ascii')) 
        write_thread = threading.Thread(target=write)
        write_thread.start()
        
        def receive():
            while True:
                try:
                    # Receive Message From Server
                    # If 'NICK' Send Nickname
                    message = c.recv(1024).decode('ascii')
                    global flag1
                    flag1 = False
                    if message == 'NICK':
                        c.send(nickname.encode('ascii'))
                    elif message == 'win the game' and flag == False:
                            window.blit(youLose,(90,200))
                            window.blit(TryAgain,(85,300))
                            flag1=True
                            break
                    elif message != "win the game":
                        print(message)
                    else:
                        break
                except:
                    # Close Connection When Error
                    c.close()
                    break
            
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
        
        if(flag1==True):
            window.blit(reG, (273, 420))
            window.blit(answer,(80,420))

        pygame.display.flip()
        clock.tick(60)
        pygame.display.update()

loginbutton=Button(gui,text="Start the game",command=lambda: [gui.destroy(),main()],fg="white",bg="green",font=('Arial', 11)).grid(row=11,column=0)
try:
    button=Button(gui,text="Exit",command=gui.destroy,fg="white",bg="red",font=('Arial', 9)).grid(row=13,column=0)
except:
    print("game completed")
    gui.destroy()
gui.mainloop()
