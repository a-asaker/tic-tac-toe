#!/usr/bin/env python3
#Coded by : A_Asaker

import os
from sys import platform

#Get The Platform To Know Either Using Curses Library Or Not
#pf==platform -not Power Factor- :D
pf='windows' if platform.find('win')!=-1 and platform != 'darwin' else 'unix'

#Graph Line
g_line="{:^5}|{:^5}|{:^5}"
#Spacer Line
s_line="{:^5}+{:^5}+{:^5}"
players=['X','Y']
role=0
end=0
score={'X':0,'Y':0}

#Use Curses Library In Case Of Linux Or Mac
if pf == 'unix':
 import curses
 stdscr = curses.initscr()
 curses.start_color()
 curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
 curses.cbreak()
 curses.echo()
 stdscr.keypad(1)

#Edited Print Function To Support Cross-Platform Usage
def print_crs(string,attr=None,x=None,y=None):
 if not pf=='windows':
  args=[i for i in [x,y,string,attr] if i is not None]
  stdscr.addstr(*args)
  stdscr.addstr("\n")
  stdscr.refresh()
 else:
  os.system('cls') if x is not None else ''
  print(string)

#Edited Input Function To Support Cross-Platform Usage
def input_crs(msg,length):
 if pf=='unix':
  stdscr.addstr(msg)
  stdscr.refresh()
  input_var=stdscr.getstr(length).decode()
  print_crs("")
 else:
  input_var=input(msg)
 return(input_var)
 
#Draw The Game Graph With The Last Played Turns
def print_game():
 print_crs(x=0,y=0,string="")
 for i in range(3):
  i-0 and i-3 and (stdscr.addstr("\t\t") if pf=='unix' else print("\t\t",end=''))
  i-0 and i-3 and print_crs(s_line.format("-"*5,"-"*5,"-"*5),curses.color_pair(1) if pf =='unix' else None)
  stdscr.addstr("\t\t") if pf=='unix' else print("\t\t",end='')
  print_crs(g_line.format(*game_vars[i]),curses.color_pair(1) if pf == 'unix' else None)

#Check If There Is A Winner
def check_for_winner(pl):
 global score
 n=3
 raws=[game_vars[raw] for raw in range(n)]
 cols=[]
 f_diam=[]
 s_diam=[]
 for z in range(n):
  cols.append([i[z] for i in game_vars])
  f_diam.append(raws[z][z])
  s_diam.append(raws[z][2-z])
 lines=raws+cols+[f_diam]+[s_diam]
 for line in lines:
  if all([i==pl for i in line]):
   print_crs("\n [#] Player {} Is The Winner".format(pl))
   score[pl]+=1
   return(1)
 return(0)

#Check If The Input Position Is Vaild
def check_input(inp):
 if len(inp)>3:
  print_crs(" [x] Too Long Input")
  return(0)
 try:
  raw=int(inp[0])-1
  col=int(inp[-1])-1
  if raw > 2 or col > 2:
   raise
  if game_vars[raw][col] in players:
   print_crs(" [x] This Position Is Already Played")
   return(0)
  else:return(1)
 except:
  print_crs(" [x] Not A Valid Position!")
  return(0)
  
#Get A Valid Input If The Checked Input Is Not A Valid Position
def get_valid_input(pl):
 valid=0
 while not valid:
  try:
   play=input_crs(" [!] Player {}, Please Enter A Valid Position => ".format(players[role]),3)
   check=check_input(play)
   if check:
    valid=1
    return(play)
  except Exception as e:
   stdscr.clear() if pf=='unix' else os.system('cls')
   print_game()

#Add X Or Y To the Game array
def edit_game(play,pl):
 global game_vars
 raw=int(play[0])-1
 col=int(play[-1])-1
 game_vars[raw][col]=pl
 
if __name__=="__main__":
 try:
  while not end:
   #Game Array
   game_vars=[['1-1','1-2','1-3'],['2-1','2-2','2-3'],['3-1','3-2','3-3']]
   winner=0
   #Number Of Plays
   plays_num=0
   while not winner:
    stdscr.clear() if pf=='unix' else os.system('cls')
    print_game()
    play=input_crs("\n > Player {} Turn => ".format(players[role]),3)
    play_chk=check_input(play)
    if play_chk:pass
    else:play=get_valid_input(players[role])
    edit_game(play,players[role])
    stdscr.clear() if pf=='unix' else os.system('cls')
    print_game()
    plays_num+=1
    winner=check_for_winner(players[role])
    if plays_num==9 and not winner:
     print_crs("\n [&] Drawn!")
     break
    role = not role
   ans=input_crs("\n [?] Whould You Like To Re-match?[y/n] ",1)
   if ans=='n':end=1
  #Remove All Curses Configurations
  if pf=='unix':
   curses.nocbreak()
   stdscr.keypad(0)
   curses.echo()
   curses.endwin()
  print("\n [*] Score:\n\n ~ Player[X]: {} Point/s\n ~ Player[Y]: {} Point/s\n".format(score['X'],score['Y'])) 
 except:
  if pf == 'unix':
   curses.nocbreak()
   stdscr.keypad(0)
   curses.echo()
   curses.endwin()
  exit(1)
