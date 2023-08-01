
import random
import socket
import sys
import threading
from tkinter import *

import pygame
from pygame.locals import *

nickname = input("Enter your name: ")
c=socket.socket()
c.connect(('localhost',9998))
#if(c.recv(1024).decode()=="player2 win the name"):
    # window.blit(youLose,(90,200))
    # window.blit(player2winthegame,(60,300)) 
pygame.init()
score = 0
white = (255,255,255)
aliceblue = (240,248,255)
yellow = (255,255,102)
grey = (211, 211, 211)
black = (0,0,0)
green=(0,255,0)
lightGreen=(153,255,204)

font = pygame.font.SysFont("Helvetica neue", 40)
bigFont = pygame.font.SysFont("Helvetica neue", 80)
sont = pygame.font.SysFont("Helvetica neue", 18)

youWin = bigFont.render("You Win!",       True, lightGreen)
youLose = bigFont.render("You Lose!",     True, lightGreen)
playAgain = bigFont.render("Play Again?", True, lightGreen)
TryAgain = bigFont.render("Try Again!", True, lightGreen)
Chatroom = font.render("CHAT ROOM", True, black)


def checkGuess(turns, word, userGuess, window):
    renderList = ["","","","",""]
    spacing = 0
    guessColourCode = [grey,grey,grey,grey,grey]
    score_card = [0,0,0,0,0]
    for x in range(0,5):
        if userGuess[x] in word:
            guessColourCode[x] = yellow

        if word[x] == userGuess[x]:
            guessColourCode[x] = green
            score_card[x] = 100

    global score
    score = sum(score_card)
    list(userGuess)
    #pygame.display.update()

    for x in range(0,5):
        renderList[x] = font.render(userGuess[x], True, black)
        pygame.draw.rect(window, guessColourCode[x], pygame.Rect(60 +spacing, 50+ (turns*80), 50, 50))
        window.blit(renderList[x], (70 + spacing, 50 + (turns*80)))
        spacing+=80

    if guessColourCode == [green,green,green,green,green]:

     return True

#def show_score(x,y,window):
    #renderSpace = font.render("Score : "+str(score), True, black)
    #window.blit(renderSpace, (x,y))
    #pygame.display.update()

      


def main():
    file = open("wordList.txt","r")
    wordList = file.readlines()
    word = wordList[random.randint(0, len(wordList)-1)].upper()
    height = 650
    width = 820
    flag = False
    x = 0
    FPS = 30
    clock = pygame.time.Clock()
    global score
    window = pygame.display.set_mode((width, height))
    window.fill(white)
    guess = ""
    text=""
    #input_rect=pygame.Rect(505,500, 315, 190)

    print(word)

    for x in range(0,5):
        for y in range(0,6):
            pygame.draw.rect(window, grey, pygame.Rect(60+(x*80), 50+(y*80), 50, 50),2)
    pygame.draw.rect(window, black, pygame.Rect(500, 0, 300, 650))

    pygame.display.set_caption("Wordle!")
    score = 0
    turns = 0
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                guess+=event.unicode.upper()
                text+=event.unicode.lower()
                
                if(str(guess[-1]).isalpha() == False):
                    guess = guess[:-1]
                    text=text[:-1]

                if event.key == K_RETURN and win == True:
                    main()

                if event.key == K_RETURN and turns == 6:
                    main()

                if(len(guess) > 5):
                    n = len(guess)
                    guess = guess[:5]

                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                    text = text[:-1]
                    

                if event.key == K_RETURN and len(guess) > 4:
                    win = checkGuess(turns, word, guess, window)
                    turns+=1
                    guess = ""
                    window.fill(white,(0,500, 500, 200))
      
        window.fill(black,(0,512, 500, 200))
        window.fill(aliceblue,(500,0,320,650))
        window.fill(yellow,(500,0,320,90))
        window.fill(black,(500,0,3,650))
        window.fill(grey,(505,512, 315, 200))
        #window.fill(white,(720,600, 80,50 ))
        #pygame.draw.rect(window,grey,input_rect)
        window.blit(Chatroom,(575,30))
        renderGuess = font.render(guess, True, grey)
        window.blit(renderGuess, (180, 535))
        reGuess = sont.render(text, True, black)
        window.blit(reGuess, (505, 510))
        #renderScore = font.render("Score : "+str(score), True, black)
        #renderScore = font.render(, True, black)
        #window.blit(renderScore, (180, 15))

        if win == True:
            flag = True
            window.blit(youWin,(90,200))
            window.blit(playAgain,(60,300))
        if win == True:
             flag = True
             def write():
                message = 'win the game'
                # message = str(c[4])
                c.send(message.encode('ascii')) 
        
                #print(message)
             write_thread = threading.Thread(target=write)
             write_thread.start()
        def write():
             while True:
                message = '{}: {}'.format(nickname,input(''))
                c.send(message.encode('ascii')) 
        write_thread = threading.Thread(target=write)
        write_thread.start()
        if turns == 6 and win != True:
            window.blit(youLose,(90,200))
            window.blit(TryAgain,(75,300))
        
        def receive():
            while True:
                if flag == False:
                    try:
                        # Receive Message From Server
                        # If 'NICK' Send Nickname
                        if flag == False:
                            message = c.recv(1024).decode('ascii')
                            if message == 'NICK':
                                c.send(nickname.encode('ascii'))
                            elif message == 'win the game' and flag == False:
                                window.blit(youLose,(90,200))
                                window.blit(TryAgain,(75,300))
                            elif message != 'win the game':
                                renderGue = sont.render(message, True, black)
                                window.blit(renderGue, (507, 200))
                                print(message)
                    except:
                        # Close Connection When Error
                        print("An error occured!")
                        c.close()
                        break
            
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
        #show_score(180,15,window)
        pygame.display.update()
        clock.tick(FPS)
main()
