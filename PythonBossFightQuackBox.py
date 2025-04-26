import turtle
import random as r
import time
import math
from os import strerror
import pygame
import quackbox.leaderboard as lb

try:
   file = open("LevelUnlock.txt", "rt")
   maxLevel = int(file.read())
except IOError:
   file = open("LevelUnlock.txt", "wt")
   file.write("-1")
   maxLevel = -1
file.close()

#window
wn = turtle.Screen()
wn.setup(width = 1200, height = 650)
wn.title("Boss Fight")
wn.bgcolor("black")
wn.tracer(0)
turtle.hideturtle()

thing = turtle.Turtle()
thing.hideturtle()
thing.pendown()
thing.pensize(1)
thing.goto(0, 0)
thing.pencolor("white")

henry1 = turtle.Shape("compound")
henry2 = turtle.Shape("compound")
thing.begin_poly()

for i in range(55):
   thing.circle(50, 360)
   thing.setheading(i * 10)

thing.end_poly()
p = thing.get_poly()
henry1.addcomponent(p, "", "white")
wn.register_shape("henry", henry1)
henry2.addcomponent(p, "", "red")
wn.register_shape("hurt henry", henry2)

thing.clear()
thing.setheading(0)


#menu screen
level = 0
bb1 = turtle.Turtle()
bb1.hideturtle()
bb1.penup()
bb1.goto(-200, -100)
bb1.shape("square")
bb1.color("chartreuse")
bb1.shapesize(stretch_wid = 2.5, stretch_len = 2.5)

bb2 = turtle.Turtle()
bb2.hideturtle()
bb2.penup()
bb2.goto(0, -104)
bb2.shape("triangle")
bb2.color("white")
bb2.setheading(90)
bb2.shapesize(stretch_wid = 2, stretch_len = 2)

bb3 = turtle.Turtle()
bb3.hideturtle()
bb3.penup()
bb3.goto(200, -100)
bb3.shape("circle")
bb3.color("white")
bb3.shapesize(stretch_wid = 2, stretch_len = 2)

bb4 = turtle.Turtle()
bb4.hideturtle()
bb4.penup()
bb4.goto(0, 100)
bb4.shape("square")
bb4.color("white")
bb4.shapesize(stretch_wid = 2, stretch_len = 2)

wn.listen()
def bb1Click(x, y):
   global level
   level = 1
bb1.onclick(bb1Click)
def bb2Click(x, y):
   global level
   level = 2
bb2.onclick(bb2Click)
def bb3Click(x, y):
   global level
   level = 3
bb3.onclick(bb3Click)

def bb4Click(x, y):
   global level
   level = 4
bb4.onclick(bb4Click)

exitGame = turtle.Turtle()
exitGame.penup()
exitGame.color("white")
exitGame.setheading(180)
exitGame.goto(-500, 300)
exitGame.shapesize(stretch_wid = 2, stretch_len = 2)
def leave(x, y):
   turtle.bye()
exitGame.onclick(leave)
turtle.listen()
turtle.onkeypress(turtle.bye, "Escape")

menu_buttons = [exitGame, bb1, bb2, bb3, bb4]

#ui
tryAgain = turtle.Turtle()
tryAgain.color("white")
tryAgain.penup()
tryAgain.hideturtle()
yes = turtle.Turtle()
no = turtle.Turtle()
yes.hideturtle()
no.hideturtle()
yes.penup()
no.penup()
yes.shape("square")
no.shape("square")
yes.color("green")
no.color("red")
yes.shapesize(stretch_wid = 2, stretch_len = 2)
no.shapesize(stretch_wid = 2, stretch_len = 2)
yes.goto(-200, 0)
no.goto(200, 0)
playAgain = False
endGame = False
def yesClick(x, y):
   global playAgain
   playAgain = True
def noClick(x, y):
   global endGame
   endGame = True
def yesPress():
   global playAgain
   if yes.isvisible():
      playAgain = True
def noPress():
   global endGame
   if no.isvisible():
      endGame = True
yes.onclick(yesClick)
wn.onkeypress(yesPress, "Return")
no.onclick(noClick)
wn.onkeypress(noPress, "Delete")
#the floor
f = turtle.Turtle()
f.color("gray")
f.penup()
f.goto(-800, -311)
f.pensize(201)
f.hideturtle()


#reset
def reset():
   global loops, currently_firing, Pup, Pdown, Pleft, Pright, unableToMove, up, down, jump_time, down_time, lives, invincible
   #reset projectile
   currently_firing = False
   Pup = False
   Pdown = False
   Pleft = False
   Pright = False
   p.hideturtle()
   p.goto(1000, -300)
   #reset circle
   c.goto(-400, -200)
   unableToMove = True
   up = False
   down = False
   jump_time = 0
   down_time = 0
   invincible = 0
   if level != 4:
      c.hideturtle()
      #reset lives
      lives = 3
      life1.color("white")
      life2.color("white")
      life3.color("white")
      life1.hideturtle()
      life2.hideturtle()
      life3.hideturtle()
      lpen.clear()
   #reset floor
   f.penup()
   f.goto(-800, -311)
   f.clear()
   #reset ui type things
   loops = 0
   yes.hideturtle()
   no.hideturtle()
   tryAgain.clear()
   #reset boss health stuff
   p1.clear()
   p2.clear()
   p3.clear()

def endScreen():
   global playAgain
   yes.showturtle()
   no.showturtle()
   tryAgain.goto(-230, -80)
   tryAgain.write("yes: \nselect", font = ("Courier", 20, "normal"))
   tryAgain.goto(175, -80)
   tryAgain.write("no: \nstart", font = ("Courier", 20, "normal"))
   tryAgain.goto(-30, -60)
   tryAgain.write("retry?", font = ("Courier", 20, "normal"))
      
   while True:
      wn.update()
      event = pygame.event.poll()
      if event.type == pygame.JOYBUTTONDOWN:
         if event.button == 9:
            noClick(0, 0)
         elif event.button == 8:
            yesClick(0, 0)
      if playAgain or endGame:
         break
   playAgain = False


#Salty rage quit button
def giveUp():
   global lives
   if level != 0:
      lives = 0
wn.onkeypress(giveUp, "l")
wn.onkeypress(giveUp, "L")


#
#PYGAME
#
pygame.init()
pygame.joystick.init()
event = pygame.event.poll()
buttons = 10
joy = None
if event.type == pygame.JOYDEVICEADDED:
   joy = pygame.joystick.Joystick(event.device_index)
   buttons = joy.get_numbuttons()

def joy_inputs(event):
   global buttons, joy
   if event.type == pygame.JOYDEVICEADDED:
      print("Controller connected: " + str(event))
      joy = pygame.joystick.Joystick(event.device_index)
      buttons = joy.get_numbuttons()
      
   for i in range(buttons):
      button = joy.get_button(i)
      if button != 0:
         match i:
            case 0:
               projectileUp()
            case 1:
               projectile_right()
            case 3:
               projectile_left()
            case 2:
               projectile_down()
            case 4:
               left()
            case 5:
               right()
            case 8:
               jump()
            case 9:
               giveUp()

level_select = 1
def joy_menu(event):
   global level_select, level
   if event.type == pygame.JOYDEVICEADDED:
      print("Controller connected: " + str(event))
      joy = pygame.joystick.Joystick(event.device_index)
      buttons = joy.get_numbuttons()

   elif event.type == pygame.JOYBUTTONDOWN:
      if event.button == 4:
         menu_buttons[level_select].shapesize(stretch_wid = 2, stretch_len = 2)
         menu_buttons[level_select].color("white")
         level_select -= 1
         level_select %= maxLevel + 1
         menu_buttons[level_select].shapesize(stretch_wid = 2.5, stretch_len = 2.5)
         menu_buttons[level_select].color("chartreuse")
      elif event.button == 5:
         menu_buttons[level_select].shapesize(stretch_wid = 2, stretch_len = 2)
         menu_buttons[level_select].color("white")
         level_select += 1
         level_select %= maxLevel + 1
         menu_buttons[level_select].shapesize(stretch_wid = 2.5, stretch_len = 2.5)
         menu_buttons[level_select].color("chartreuse")

      elif event.button == 9:
         if(level_select == 0):
            turtle.bye()
         else:
            level = level_select
      

#projectile
p = turtle.Turtle()
p.shape("circle")
p.color("white")
p.shapesize(stretch_wid = 0.25, stretch_len = 0.25)
p.penup()
p.hideturtle()
p.goto(1000, -90)
#projectile stuff
currently_firing = False
wn.listen()
Pup = False
def projectileUp():
   global Pup
   global currently_firing
   if not Pdown and (not Pleft and not Pright):
      Pup = True
      currently_firing = True
wn.onkeypress(projectileUp, "Up")

Pdown = False
def projectile_down():
   global Pdown
   global currently_firing
   if not Pup and (not Pleft and not Pright):
      Pdown = True
      currently_firing = True
wn.onkeypress(projectile_down, "Down")

Pright = False
def projectile_right():
   global Pright
   global currently_firing
   if not Pleft and (not Pup and not Pdown):
      Pright = True
      currently_firing = True
wn.onkeypress(projectile_right, "Right")

Pleft = False
def projectile_left():
   global Pleft
   global currently_firing
   if not Pright and (not Pup and not Pdown):
      Pleft = True
      currently_firing = True
wn.onkeypress(projectile_left, "Left")

def projectile_movement():
   global currently_firing
   global Pup
   global Pdown
   global Pright
   global Pleft

   p.showturtle()

   if (p.ycor() > 300 or p.ycor() < -200) and currently_firing:
      Ypos = c.ycor()
      Xpos = c.xcor()
      p.goto(Xpos, Ypos)
   elif (p.xcor() > 550 or p.xcor() < -550) and currently_firing:
      Ypos = c.ycor()
      Xpos = c.xcor()
      p.goto(Xpos, Ypos)
   else:
      Ypos = p.ycor()
      Xpos = p.xcor()

   if Pup:
      Ypos += 15
   if Pdown:
      Ypos -= 15
   if Pright:
      Xpos += 15
   if Pleft:
      Xpos -= 15
   p.sety(Ypos)
   p.setx(Xpos)

   if Ypos > 300 or Ypos < -200:
      Pup = False
      Pdown = False
      currently_firing = False
      p.goto(800, 800)

      p.hideturtle()
      
   if Xpos > 550 or Xpos < -550:
      Pleft = False
      Pright = False
      currently_firing = False
      p.goto(800, 800)

      p.hideturtle()
      

#player object
c = turtle.Turtle()
c.color("white")
c.shape("circle")
c.hideturtle()
c.penup()
c.goto(-400, -200)
lives = 3
#movement for player
unableToMove = False
wn.listen()
def right():
   global unableToMove
   pos = c.xcor()
   if pos < 520:
      if not unableToMove:
         pos += 11
         c.setx(pos)
wn.onkeypress(right, "d")
wn.onkeypress(right, "D")
def left():
   global unableToMove
   pos = c.xcor()
   if pos > -520:
      if not unableToMove:
         pos -= 11
         c.setx(pos)
wn.onkeypress(left, "a")
wn.onkeypress(left, "A")
up = False
down = False
jump_time = 0
down_time = 0
def jump():
   if not unableToMove:
      global up
      up = True
wn.onkeypress(jump, "space")
def jump_timer():
    global up
    global down
    global jump_time
    global down_time
    if up and not down:
        y = c.ycor()
        y += 10
        c.sety(y)
        jump_time += 1
        
    if jump_time == 13:
        down = True
        jump_time = 0
        
    if down:
        y = c.ycor()
        y -= 10
        c.sety(y)
        down_time += 1
        
    if down_time == 13:
        down = False
        up = False
        down_time = 0
#life 1
life1 = turtle.Turtle()
life1.shape("circle")
life1.color("white")
life1.shapesize(stretch_wid = 0.5, stretch_len = 0.5)
life1.penup()
life1.goto(-500, 150)
life1.hideturtle()
#life 2
life2 = turtle.Turtle()
life2.shape("circle")
life2.color("white")
life2.shapesize(stretch_wid = 0.5, stretch_len = 0.5)
life2.penup()
life2.goto(-475, 150)
life2.hideturtle()
#life 3
life3 = turtle.Turtle()
life3.shape("circle")
life3.color("white")
life3.shapesize(stretch_wid = 0.5, stretch_len = 0.5)
life3.penup()
life3.goto(-450, 150)
life3.hideturtle()
#lpen
lpen = turtle.Turtle()
lpen.penup()
lpen.hideturtle()
lpen.goto(-520, 160)
lpen.pencolor("white")
#functions for lives
invincible = 0
def hurt():
   global lives, unableToMove, invincible
   z = lives
   if b.isvisible() == True:
      if c.ycor() <= b.ycor() + 90 and c.ycor() >= b.ycor() - 90:
         if c.xcor() <= b.xcor() + 90 and c.xcor() >= b.xcor() - 90:
            unableToMove = True
            lives -= 1
            invincible = 20
            if (c.xcor() < b.xcor() and c.xcor() > -360) or c.xcor() > 360:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            else:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            unableToMove = False

      if z == lives:
         if c.xcor() <= min1.xcor() + 10 and c.xcor() >= min1.xcor() - 10:
            if c.ycor() <= min1.ycor() + 10 and c.ycor() >= min1.ycor() - 10:
               if min1.isvisible():
                  unableToMove = True
                  lives -= 1
                  invincible = 20
                  if (c.xcor() < min1.xcor() and c.xcor() > -360) or c.xcor() > 360:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  else:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  unableToMove = False
      if z == lives:         
         if min2.isvisible():
            if c.ycor() <= min2.ycor() + 10 and c.ycor() >= min2.ycor() - 10:
               if c.xcor() <= min2.xcor() + 10 and c.xcor() >= min2.xcor() - 10:
                  unableToMove = True
                  lives -= 1
                  invincible = 20
                  if (c.xcor() < min2.xcor() and c.xcor() > -360) or c.xcor() > 360:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  else:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  unableToMove = False

   elif b2.isvisible() == True:
      if c.ycor() <= b2.ycor() and c.ycor() >= b2.ycor() - 80:
         if c.xcor() <= b2.xcor() + 80 and c.xcor() >= b2.xcor() - 80:
            unableToMove = True
            lives -= 1
            invincible = 20
            if (c.xcor() < b2.xcor() and c.xcor() > -360) or c.xcor() > 360:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            else:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            unableToMove = False
            
      elif c.ycor() <= b2.ycor() + 80 and c.ycor() >= b2.ycor():
         if c.xcor() <= b2.xcor() + 40 and c.xcor() >= b2.xcor() - 40:
            unableToMove = True
            lives -= 1
            invincible = 20
            if (c.xcor() < b2.xcor() and c.xcor() > -360) or c.xcor() > 360:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            else:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            unableToMove = False

      if z == lives:
         if tri1.isvisible():
            if c.xcor() < tri1.xcor() + 25 and c.xcor() > tri1.xcor() - 25:
               if c.ycor() < tri1.ycor() + 25 and c.ycor() > tri1.ycor() - 25:
                  unableToMove = True
                  lives -= 1
                  invincible = 20
                  if (c.xcor() < tri1.xcor() and c.xcor() > -360) or c.xcor() > 360:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  else:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  unableToMove = False


#stage 2 of boss 2
def s2b2hurt():
   global lives, unableToMove, invincible
   z = lives
   if trip1.isvisible():
      if c.xcor() < trip1.xcor() + 50 and c.xcor() > trip1.xcor() - 50:
         if c.ycor() < trip1.ycor() + 50 and c.ycor() > trip1.ycor() - 50:
               unableToMove = True
               lives -= 1
               invincible = 20
               if (c.xcor() < trip1.xcor() and c.xcor() > -360) or c.xcor() > 360:
                  c.color("red")
                  for i in range(5):
                     x = c.xcor()
                     x -= 17
                     y = c.ycor()
                     y += 5
                     c.goto(x, y)
                     wn.update()
                     time.sleep(1/30)
                  c.color("white")
                  for i in range(5):
                     x = c.xcor()
                     x -= 17
                     y = c.ycor()
                     y -= 5
                     c.goto(x, y)
                     wn.update()
                     time.sleep(1/30)
               else:
                  c.color("red")
                  for i in range(5):
                     x = c.xcor()
                     x += 17
                     y = c.ycor()
                     y += 5
                     c.goto(x, y)
                     wn.update()
                     time.sleep(1/30)
                  c.color("white")
                  for i in range(5):
                     x = c.xcor()
                     x += 17
                     y = c.ycor()
                     y -= 5
                     c.goto(x, y)
                     wn.update()
                     time.sleep(1/30)
               unableToMove = False

   if z == lives:
      if trip2.isvisible():
         if c.xcor() < trip2.xcor() + 50 and c.xcor() > trip2.xcor() - 50:
               if c.ycor() < trip2.ycor() + 50 and c.ycor() > trip2.ycor() - 50:
                  unableToMove = True
                  lives -= 1
                  invincible = 20
                  if (c.xcor() < trip2.xcor() and c.xcor() > -360) or c.xcor() > 360:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  else:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  unableToMove = False

   if z == lives:
      if trip3.isvisible():         
         if c.xcor() < trip3.xcor() + 50 and c.xcor() > trip3.xcor() - 50:
            if c.ycor() < trip3.ycor() + 50 and c.ycor() > trip3.ycor() - 50:
                  unableToMove = True
                  lives -= 1
                  invincible = 20
                  if (c.xcor() < trip3.xcor() and c.xcor() > -360) or c.xcor() > 360:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  else:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  unableToMove = False

   if z == lives:
      if trip4.isvisible():     
         if c.xcor() < trip4.xcor() + 50 and c.xcor() > trip4.xcor() - 50:
            if c.ycor() < trip4.ycor() + 50 and c.ycor() > trip4.ycor() - 50:
                  unableToMove = True
                  lives -= 1
                  invincible = 20
                  if (c.xcor() < trip4.xcor() and c.xcor() > -360) or c.xcor() > 360:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x -= 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  else:
                     c.color("red")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y += 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                     c.color("white")
                     for i in range(5):
                        x = c.xcor()
                        x += 17
                        y = c.ycor()
                        y -= 5
                        c.goto(x, y)
                        wn.update()
                        time.sleep(1/30)
                  unableToMove = False

def s3b2hurt():
   global lives, unableToMove, invincible
   z = lives
   if s3b2atk:
      di = math.sqrt((blast.xcor() - c.xcor())**2 + (blast.ycor() - c.ycor())**2)
      if di < blastSize/2 + 10:
            unableToMove = True
            lives -= 1
            invincible = 20
            if (c.xcor() < blast.xcor() and c.xcor() > -360) or c.xcor() > 360:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            else:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            unableToMove = False
   if s3b2atk2:
      if c.xcor() < beam.xcor() + 30 and c.xcor() > beam.xcor() - 30:
         if c.ycor() < beam.ycor() + 30 and c.ycor() > beam.ycor() - 30:
               unableToMove = True
               lives -= 1
               invincible = 20
               if (c.xcor() < beam.xcor() and c.xcor() > -360) or c.xcor() > 360:
                  c.color("red")
                  for i in range(5):
                     x = c.xcor()
                     x -= 17
                     y = c.ycor()
                     y += 5
                     c.goto(x, y)
                     wn.update()
                     time.sleep(1/30)
                  c.color("white")
                  for i in range(5):
                     x = c.xcor()
                     x -= 17
                     y = c.ycor()
                     y -= 5
                     c.goto(x, y)
                     wn.update()
                     time.sleep(1/30)
               else:
                  c.color("red")
                  for i in range(5):
                     x = c.xcor()
                     x += 17
                     y = c.ycor()
                     y += 5
                     c.goto(x, y)
                     wn.update()
                     time.sleep(1/30)
                  c.color("white")
                  for i in range(5):
                     x = c.xcor()
                     x += 17
                     y = c.ycor()
                     y -= 5
                     c.goto(x, y)
                     wn.update()
                     time.sleep(1/30)
               unableToMove = False


r1 = 12
r2 = 140
r3 = 100
r4 = 70
r5 = 100
def b3hurt():
   global lives, unableToMove, invincible
   z = lives
   if b3.isvisible() == True:
      di = math.sqrt((b3.xcor() - c.xcor())**2 + (b3.ycor() - c.ycor())**2)
      if di <= r1:
         unableToMove = True
         lives -= 1
         invincible = 20
         if (c.xcor() < b3.xcor() and c.xcor() > -360) or c.xcor() > 360:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         unableToMove = False
def b3s2hurt():
   global lives, unableToMove, invincible, end
   z = lives
   if b3.isvisible() == True:
      di = math.sqrt((b3.xcor() - c.xcor())**2 + (b3.ycor() - c.ycor())**2)
      if di <= r2 or (((s2b3atk2 and ast >= loops + 76) or (s2b3atk50p and not s2b3atk and ast >= loops + 76)) and di <= 200):
         if s2b3atk2:
            end = True
         unableToMove = True
         lives -= 1
         invincible = 20
         if (c.xcor() < b3.xcor() and c.xcor() > -360) or c.xcor() > 360:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         unableToMove = False

def b3s3hurt():
   global lives, unableToMove, invincible, end
   z = lives
   if b3.isvisible() == True:
      di = math.sqrt((b3.xcor() - c.xcor())**2 + (b3.ycor() - c.ycor())**2)
      if di <= r3:
         unableToMove = True
         lives -= 1
         invincible = 20
         if (c.xcor() < b3.xcor() and c.xcor() > -360) or c.xcor() > 360:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         unableToMove = False
      elif shooting or s3b3atk2:
         di = math.sqrt((shotPen.xcor() - c.xcor())**2 + (shotPen.ycor() - c.ycor())**2)
         if di <= 25:
            unableToMove = True
            lives -= 1
            invincible = 20
            if (c.xcor() < b3.xcor() and c.xcor() > -360) or c.xcor() > 360:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            else:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            unableToMove = False

def b3s4hurt():
   global lives, unableToMove, invincible, end
   z = lives
   if b3.isvisible() == True:
      di = math.sqrt((b3.xcor() - c.xcor())**2 + (b3.ycor() - c.ycor())**2)
      if di <= r4 or (s2b3atk2 and di <= 160 and ast >= 76):
         if s2b3atk2:
            end = True
         unableToMove = True
         lives -= 1
         invincible = 20
         if (c.xcor() < b3.xcor() and c.xcor() > -360) or c.xcor() > 360:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         unableToMove = False
      elif shooting or s3b3atk2:
         di = math.sqrt((shotPen.xcor() - c.xcor())**2 + (shotPen.ycor() - c.ycor())**2)
         if di <= 25:
            unableToMove = True
            lives -= 1
            invincible = 20
            if (c.xcor() < b3.xcor() and c.xcor() > -360) or c.xcor() > 360:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            else:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            unableToMove = False

def b3s5hurt():
   global lives, unableToMove, invincible, end
   z = lives
   if b3.isvisible() == True:
      di = math.sqrt((b3.xcor() - c.xcor())**2 + (b3.ycor() - c.ycor())**2)
      if di <= r5 or (s2b3atk2 and di <= 160 and ast >= 76):
         if s2b3atk2:
            end = True
         unableToMove = True
         lives -= 1
         invincible = 20
         if (c.xcor() < b3.xcor() and c.xcor() > -360) or c.xcor() > 360:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         unableToMove = False
      elif shooting or s3b3atk2:
         di = math.sqrt((shotPen.xcor() - c.xcor())**2 + (shotPen.ycor() - c.ycor())**2)
         if di <= 25:
            unableToMove = True
            lives -= 1
            invincible = 20
            if (c.xcor() < b3.xcor() and c.xcor() > -360) or c.xcor() > 360:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x -= 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            else:
               c.color("red")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y += 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
               c.color("white")
               for i in range(5):
                  x = c.xcor()
                  x += 17
                  y = c.ycor()
                  y -= 5
                  c.goto(x, y)
                  wn.update()
                  time.sleep(1/30)
            unableToMove = False

            
def lifeLoss():
   global lives
   if lives <= 2:
      life3.color("black")
      life3.hideturtle()
   if lives <= 1:
      life2.color("black")
      life2.hideturtle()
   if lives <= 0:
      life1.color("black")
      life1.hideturtle()

def hurtByEx():
   global lives
   global unableToMove
   global exX
   global exWid
   if (c.xcor() > -exX and c.xcor() < exX) and exWid != 1:
      rand = r.randint(1, 2)
      if rand == 1:
         lives -= 1
         c.goto(-500, c.ycor())
         unableToMove = True
         c.color("red")
         wn.update()
         time.sleep(1/5)
         c.color("white")
         wn.update()
      if rand == 2:
         lives -= 1
         c.goto(500, c.ycor())
         unableToMove = True
         c.color("red")
         wn.update()
         time.sleep(1/5)
         c.color("white")
         wn.update()
      unableToMove = False

def none1():
   return None

def invinciblePLSBlink(hurt1, hurt2 = none1, hurt3 = none1):
   global invincible
   if invincible == 0:
      hurt1()
      hurt2()
      hurt3()
   else:
      if invincible == 20:
         c.fillcolor("black")
      elif invincible == 16:
         c.fillcolor("white")
      elif invincible == 12:
         c.fillcolor("black")
      elif invincible == 8:
         c.fillcolor("white")
      elif invincible == 4:
         c.fillcolor("black")
      elif invincible == 1:
         c.fillcolor("white")
      invincible -= 1
            
   if lives == 1:
      if loops % 40 == 0:
         life1.fillcolor("white")
      elif loops % 20 == 0:
         life1.fillcolor("black")


   

#boss 1
b = turtle.Turtle()
b.pencolor("white")
b.shape("square")
b.hideturtle()
b.penup()
b.goto(0, 500)
b.shapesize(stretch_wid = 9, stretch_len = 9)
#boss movement and ai-ish stuff
bossHP = 80
def hurtBoss():
   global bossHP
   proposY = p.ycor()
   proposX = p.xcor()

   if b.isvisible() == True:
      if (proposY <= b.ycor() + 80 and proposY >= b.ycor() - 80
      and proposX <= b.xcor() + 80 and proposX >= b.xcor() - 80):
            b.pencolor("red")
            p.hideturtle()
            p.goto(530, 310)
            global Pup
            global Pdown
            global Pright
            global Pleft
            global currently_firing
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            bossHP -= 1
      elif b.pencolor() == "red":
         b.pencolor("white")

      if bossHP == 40 and p1.xcor() == 0:
         p1.forward(200)
      if bossHP == 20 and p3.xcor() == 100:
         p3.forward(100)
      if b.pencolor() == "red":
         p2.forward(5)

ast = 0 #attack start time
cooldown = 50
vibrate = False
atk1 = False
atk2 = False
atk3 = False

dist = 0
bosspos = 0
tarpos = 0
def bossAttack1():
   global atk1
   global ast
   global loops
   global cooldown
   global dist
   global bosspos
   global tarpos
   global vibrate
   if ast == 0:
      ast = loops
   if ast == loops:
      tarpos = c.xcor()
      bosspos = b.xcor()
      dist = tarpos - bosspos
      atk1 = True
      
   if ast < loops + 15 and ast != 0:
      newBossY = b.ycor() + 10
      newBossX = b.xcor() + (dist/15)
      b.goto(newBossX, newBossY)
      ast += 2
   elif ast != 0 and ast < loops + 20:
      newBossY = b.ycor() - 30
      b.sety(newBossY)
      ast += 2
   elif ast == loops + 20:
      ast = 0
      cooldown = 120
      atk1 = False
      vibrate = True
ex = turtle.Turtle()
ex.shape("circle")
ex.color("orange")
ex.penup()
ex.hideturtle()
ex.goto(0, -120)
exY = 10
exX = 10
exWid = 1
exLen = 1
def bossAttack2():
   global atk2
   global ast
   global loops
   global cooldown
   global dist
   global bosspos
   global tarpos
   global exY
   global exX
   global exWid
   global exLen
   global vibrate
   if ast == 0:
      ast = loops
   if ast == loops:
      tarpos = 0
      bosspos = b.xcor()
      dist = tarpos - bosspos
      atk2 = True
   if ast < loops + 10 and ast != 0:
      newBossY = b.ycor() + 10
      newBossX = b.xcor() + (dist/10)
      b.goto(newBossX, newBossY)
      ast += 2
   elif ast != 0 and ast < loops + 15:
      newBossY = b.ycor() - 20
      b.sety(newBossY)
      ast += 2
   elif ast != 0 and ast < loops + 38:
      ex.showturtle()
      ex.shapesize(stretch_wid = exWid, stretch_len = exLen)
      exWid += 2
      exLen += 2
      exY += 19
      exX += 19
      ast += 2
   elif ast == loops + 38:
      ast = 0
      cooldown = 150
      atk2 = False
      exWid = 1
      exLen = 1
      exY = 10
      exX = 10
      ex.shapesize(stretch_wid = exWid, stretch_len = exLen)
      ex.hideturtle()
      vibrate = True

min1 = turtle.Turtle()
min1.shape("square")
min1.pencolor("white")
min1.penup()
min1.goto(100, -200)
min1.hideturtle()
min1R = False
min1L = False
min2 = turtle.Turtle()
min2.shape("square")
min2.pencolor("white")
min2.penup()
min2.goto(-100, -200)
min2.hideturtle()
min2R = False
min2L = False
atk3 = False
def minionSummon():
   global atk3
   global min1R
   global min1L
   global min2R
   global min2L
   global cooldown
   bosscor = b.xcor()
   atk3 = True
   if bosscor < -200:
      min1R = True
      min1L = False
      min2R = True
      min2L = False
      min2.setx(b.xcor() + 100)
      min1.setx(b.xcor() + 50)
   elif bosscor > 200:
      min1R = False
      min1L = True
      min2R = False
      min2L = True
      min2.setx(b.xcor() - 100)
      min1.setx(b.xcor() - 50)
   else:
      min1R = True
      min1L = False
      min2R = False
      min2L = True
      min2.setx(b.xcor() - 50)
      min1.setx(b.xcor() + 50)
   atk3 = False
   cooldown = 50
   min1.showturtle()
   min2.showturtle()
def minionMove():
   global min1R
   global min1L
   global min2R
   global min2L
   if min1.xcor() < -510:
      min1R = True
      min1L = False
   if min1.xcor() > 510:
      min1R = False
      min1L = True
   if min2.xcor() < -510:
      min2R = True
      min2L = False
   if min2.xcor() > 510:
      min2R = False
      min2L = True

   if min1R:
      m1 = min1.xcor()
      m1 += 10
      min1.goto(m1, -200)
   elif min1L:
      m1 = min1.xcor()
      m1  -= 10
      min1.goto(m1, -200)
   if min2R:
      m2 = min2.xcor()
      m2 += 10
      min2.goto(m2, -200)
   elif min2L:
      m2 = min2.xcor()
      m2 -= 10
      min2.goto(m2, -200)
min2lives = 3
min1lives = 3
def hurtMinion():
   global min1lives
   global min2lives
   proposY = p.ycor()
   proposX = p.xcor()
   global Pup
   global Pdown
   global Pright
   global Pleft
   global currently_firing
   if min1.isvisible():
      if (proposY <= min1.ycor() + 10 and proposY >= min1.ycor() - 10
      and proposX <= min1.xcor() + 10 and proposX >= min1.xcor() - 10):
            p.hideturtle()
            p.goto(530, 310)
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            min1lives -= 1
      if min1lives == 0:
         min1.hideturtle()
         min1lives = 3

   if min2.isvisible():
      if (proposY <= min2.ycor() + 10 and proposY >= min2.ycor() - 10
      and proposX <= min2.xcor() + 10 and proposX >= min2.xcor() - 10):
            p.hideturtle()
            p.goto(530, 310)
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            min2lives -= 1
      if min2lives == 0:
         min2.hideturtle()
         min2lives = 3

def attack():
   global atk1
   global atk2
   global atk3
   if atk1:
      bossAttack1()
   elif atk2:
      bossAttack2()
   elif atk3:
      minionSummon()
   else:
      if (not min1.isvisible() and not min2.isvisible()):
         ran = r.randint(1, 3)
         if ran == 1:
            bossAttack1()
         elif ran == 2:
            bossAttack2()
         elif ran == 3:
            minionSummon()
      else:
         ran = r.randint(1, 2)
         if ran == 1:
            bossAttack1()
         elif ran == 2:
            bossAttack2()

#boss2
b2 = turtle.Turtle()
b2.pencolor("white")
b2.shape("triangle")
b2.penup()
b2.hideturtle()
b2.goto(0, -200)
b2.left(90)

lose = False
#dying effect
bdie1 = turtle.Turtle()
bdie1.penup()
bdie1.hideturtle()
bdie1.shape("triangle")
bdie1.pencolor("red")
bdie1.shapesize(stretch_wid = 7, stretch_len = 7)
bdie1.left(90)
#2
bdie2 = turtle.Turtle()
bdie2.penup()
bdie2.hideturtle()
bdie2.shape("triangle")
bdie2.pencolor("red")
bdie2.shapesize(stretch_wid = 7, stretch_len = 7)
bdie2.left(90)
#3
bdie3 = turtle.Turtle()
bdie3.penup()
bdie3.hideturtle()
bdie3.shape("triangle")
bdie3.pencolor("red")
bdie3.shapesize(stretch_wid = 7, stretch_len = 7)
bdie3.left(90)
#4
bdie4 = turtle.Turtle()
bdie4.penup()
bdie4.hideturtle()
bdie4.shape("triangle")
bdie4.pencolor("red")
bdie4.shapesize(stretch_wid = 7, stretch_len = 7)
bdie4.left(90)
#5
bdie5 = turtle.Turtle()
bdie5.penup()
bdie5.hideturtle()
bdie5.shape("triangle")
bdie5.pencolor("red")
bdie5.shapesize(stretch_wid = 7, stretch_len = 7)
bdie5.left(90)
#boss 2 movement and ai-ish stuff
boss2HP = 40
def hurtBoss2():
   global boss2HP, Pup, Pdown, Pright, Pleft, currently_firing, shieldDown
   proposY = p.ycor()
   proposX = p.xcor()

   if b2.isvisible() == True: 
      if (proposY <= b2.ycor() and proposY >= b2.ycor() - 80
      and proposX <= b2.xcor() + 80 and proposX >= b2.xcor() - 80):
            if b2.pencolor() != "pink" or Pdown:
               b2.pencolor("red")
               boss2HP -= 1
            p.hideturtle()
            p.goto(800, 310)
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            shieldDown = 0
      elif (proposY <= b2.ycor() + 80 and proposY >= b2.ycor()
      and proposX <= b2.xcor() + 40 and proposX >= b2.xcor() - 40):
            if b2.pencolor() != "pink" or Pdown:
               b2.pencolor("red")
               boss2HP -= 1
            p.hideturtle()
            p.goto(800, 310)
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            shieldDown = 0
      elif b2.pencolor() == "red":
         b2.pencolor("white")
      

      if boss2HP == 20 and p1.xcor() == 0:
         p1.forward(200)
      if b2.pencolor() == "red":
         p2.forward(10)
#teleport
def boss2teleport():
   if b2.xcor() > 0 and c.xcor() > 0:
      b2.fillcolor("purple")
      wn.update()
      b2.hideturtle()
      wn.update()
      b2.setx(-500)
      wn.update()
      b2.showturtle()
      wn.update()
      b2.fillcolor("black")
      wn.update()
   elif b2.xcor() < 0 and c.xcor() < 0:
      b2.fillcolor("purple")
      wn.update()
      b2.hideturtle()
      wn.update()
      b2.setx(500)
      wn.update()
      b2.showturtle()
      wn.update()
      b2.fillcolor("black")
      wn.update()
#attacks
b2atk1 = False
def b2attack():
   global ast
   global loops
   global cooldown
   global b2atk1
   if ast == 0:
      ast = loops
   if ast == loops:
      b2.fillcolor("purple")
      b2atk1 = True
      ast += 2
   elif ast < loops + 2 and ast != 0:
      rightorleft = r.randint(1, 2)
      if rightorleft == 1:
         if c.xcor() < 400:
            b2.setx(c.xcor() + 100)
         else:
            b2.setx(c.xcor() - 100)
      else:
         if c.xcor() > -400:
            b2.setx(c.xcor() - 100)
         else:
            b2.setx(c.xcor() + 100)
      ast += 2
   elif ast != 0 and ast < loops + 11:
      b2.fillcolor("black")
      ast += 2
   elif ast < loops + 12:
      b2.fillcolor("purple")
      ast += 2
   elif ast < loops + 13:
      if c.xcor() < 0:
         b2.setx(500)
      else:
         b2.setx(-500)
      ast += 2
   elif ast < loops + 14:
      b2.fillcolor("black")
      ast = 0
      cooldown = 50
      b2atk1 = False

#attack2
b2atk2 = False
tri1 = turtle.Turtle()
tri1.penup()
tri1.shape("triangle")
tri1.pencolor("white")
tri1.shapesize(stretch_wid = 2, stretch_len = 2)
tri1.goto(1000, 1000)
tri1ang = 0
t1mt = 0
#tri1.goto(465, -190)
#tri1.shapesize(stretch_wid = 3.5, stretch_len = 3.5)

def b2attack2():
   global t1mt
   global loops
   global cooldown
   global b2atk2
   global tri1ang
   if t1mt == 0:
      t1mt = loops
      tri1.fillcolor("purple")
      tri1.goto(0, 100)
      b2atk2 = True
      if not b2atk1:
         cooldown = 70
      t1mt += 2
   elif t1mt < loops + 3 and t1mt != 0:
      tri1.fillcolor("black")
      t1mt += 2
   elif t1mt != 0 and t1mt < loops + 53:
      tri1.right(tri1ang)
      tri1ang = tri1.towards(c)
      tri1.left(tri1ang)
      t1mt += 2
   elif t1mt != 0 and t1mt < loops + 803:
      tri1.right(tri1ang)
      tri1ang = tri1.towards(c)
      tri1.left(tri1ang)
      tri1.forward(2)
      t1mt += 2
   elif t1mt < loops + 804:
      t1mt = 0
      b2atk2 = False
      tri1.goto(1000, 1000)
#stage 2 boss 2
#triangle 1
trip1 = turtle.Turtle()
trip1.shape("triangle")
trip1.shapesize(stretch_wid = 3.5, stretch_len = 3.5)
trip1.hideturtle()
trip1.penup()
trip1.goto(1000, 1000)
trip1.pencolor("white")
trip1.fillcolor("black")
trip1.left(90)
#triangle 2
trip2 = turtle.Turtle()
trip2.shape("triangle")
trip2.shapesize(stretch_wid = 3.5, stretch_len = 3.5)
trip2.hideturtle()
trip2.penup()
trip2.goto(1000, 1000)
trip2.pencolor("white")
trip2.fillcolor("black")
trip2.left(90)
#triangle 3
trip3 = turtle.Turtle()
trip3.shape("triangle")
trip3.shapesize(stretch_wid = 3.5, stretch_len = 3.5)
trip3.hideturtle()
trip3.penup()
trip3.goto(1000, 1000)
trip3.pencolor("white")
trip3.fillcolor("black")
trip3.right(90)
#triangle 4
trip4 = turtle.Turtle()
trip4.shape("triangle")
trip4.shapesize(stretch_wid = 3.5, stretch_len = 3.5)
trip4.hideturtle()
trip4.penup()
trip4.goto(1000, 1000)
trip4.pencolor("white")
trip4.fillcolor("black")
trip4.left(90)
spot1x, spot2x, spot3x, spot4x = -300, -100, 100, 300
spot1y, spot2y, spot3y, spot4y = 50, 100, 50, 100

tripl = [trip1, trip2, trip3, trip4]

#null turtles
null = turtle.Turtle()
null.penup()
null.hideturtle()
null.shapesize(stretch_wid = 3, stretch_len = 3)

tripHP1 = 5
tripHP2 = 5
tripHP3 = 5
tripHP4 = 5
def hurttrip():
   global tripHP1, tripHP2, tripHP3, tripHP4, Pup, Pdown, Pright, Pleft, currently_firing, boss2HP, tripl, s2b2atk1
   
   proposY = p.ycor()
   proposX = p.xcor()

   if trip1.isvisible() == True:
      if (proposY <= trip1.ycor() + 40 and proposY >= trip1.ycor() - 40
      and proposX <= trip1.xcor() + 40 and proposX >= trip1.xcor() - 40):
            p.hideturtle()
            p.goto(1500, 310)
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            if trip1.fillcolor() != "pink":
               tripHP1 -= 1
               trip1.pencolor("red")
      elif trip1.pencolor() == "red":
         trip1.pencolor("white")

      if tripHP1 == 0:
         trip1.fillcolor("purple")
         tripHP1 -= 1
      elif tripHP1 == -1:
         trip1.goto(1000, 1000)
         trip1.fillcolor("black")
         if not s2b2atk1:
            trip1.hideturtle()
            tripl.pop(tripl.index(trip1))
            tripl.append(null)
            tripHP1 = 0
            boss2HP -= 3
            if boss2HP <= 8 and p3.xcor() == 100:
               p3.forward(100)
            p2.forward(30)
         

         
   if trip2.isvisible() == True:
      if proposY <= trip2.ycor() + 40 and proposY >= trip2.ycor() - 40:
         if proposX <= trip2.xcor() + 40 and proposX >= trip2.xcor() - 40:
            p.hideturtle()
            p.goto(1500, 310)
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            if trip2.fillcolor() != "pink":
               tripHP2 -= 1
               trip2.pencolor("red")
      elif trip2.pencolor() == "red":
         trip2.pencolor("white")

      if tripHP2 == 0:
         trip2.fillcolor("purple")
         tripHP2 -= 1
      elif tripHP2 == -1:
         trip2.goto(1000, 1000)
         trip2.fillcolor("black")
         if not s2b2atk1:
            trip2.hideturtle()
            tripl.pop(tripl.index(trip2))
            tripl.append(null)
            tripHP2 = 0
            boss2HP -= 3
            if boss2HP <= 8 and p3.xcor() == 100:
               p3.forward(100)
            p2.forward(30)


   if trip3.isvisible() == True:
      if proposY <= trip3.ycor() + 40 and proposY >= trip3.ycor() - 40:
         if proposX <= trip3.xcor() + 40 and proposX >= trip3.xcor() - 40:
            p.hideturtle()
            p.goto(1500, 310)
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            if trip4.fillcolor() != "pink":
               tripHP3 -= 1
               trip3.pencolor("red")
      elif trip3.pencolor() == "red":
         trip3.pencolor("white")

      if tripHP3 == 0:
         trip3.fillcolor("purple")
         tripHP3 -= 1
      elif tripHP3 == -1:
         trip3.goto(1000, 1000)
         trip3.fillcolor("black")
         if not s2b2atk1:
            trip3.hideturtle()
            tripl.pop(tripl.index(trip3))
            tripl.append(null)
            tripHP3 = 0
            boss2HP -= 3
            if boss2HP <= 8 and p3.xcor() == 100:
               p3.forward(100)
            p2.forward(30)

   if trip4.isvisible() == True:
      if proposY <= trip4.ycor() + 40 and proposY >= trip4.ycor() - 40:
         if proposX <= trip4.xcor() + 40 and proposX >= trip4.xcor() - 40:
            p.hideturtle()
            p.goto(1500, 310)
            currently_firing = False
            Pup = False
            Pdown = False
            Pright = False
            Pleft = False
            if trip4.fillcolor() != "pink":
               tripHP4 -= 1
               trip4.pencolor("red")
      elif trip4.pencolor() == "red":
         trip4.pencolor("white")

      if tripHP4 == 0:
         trip4.fillcolor("purple")
         tripHP4 -= 1
      elif tripHP4 == -1:
         trip4.goto(1000, 1000)
         trip4.fillcolor("black")
         if not s2b2atk1:
            trip4.hideturtle()
            tripl.pop(tripl.index(trip4))
            tripl.append(null)
            tripHP4 = 0
            boss2HP -= 3
            if boss2HP <= 8 and p3.xcor() == 100:
               p3.forward(100)
            p2.forward(30)

s2b2atk1 = False
launchl = [False, False, False, False]
facing = 0
cx = 0
numFinished = 0
t1mt = 0
def tripatk1():
   global t1mt, cooldown, s2b2atk1, facing, cx, launchl, numFinished
   if t1mt == 0:
      t1mt = loops
      s2b2atk1 = True
      t1mt += 2
      tripl[0].fillcolor("purple")
   elif t1mt < loops + 2:
      tripl[0].goto(0, 100)
      t1mt += 2
   elif t1mt < loops + 11:
      tripl[0].fillcolor("black")
      tripl[0].forward(10)
      tripl[0].right(10)
      tripl[0].tilt(20)
      t1mt += 2
   elif t1mt < loops + 12:
      tripl[1].fillcolor("purple")
      t1mt += 2
   elif t1mt < loops + 13:
      tripl[1].goto(0, 100)
      t1mt += 2
   elif t1mt < loops + 22:
      tripl[1].fillcolor("black")
      tripl[0].forward(10)
      tripl[0].right(10)
      tripl[1].forward(10)
      tripl[1].right(10)
      tripl[0].tilt(20)
      tripl[1].tilt(20)
      t1mt += 2
   elif t1mt < loops + 23:
      tripl[2].fillcolor("purple")
      t1mt += 2
   elif t1mt < loops + 24:
      tripl[2].goto(0, 100)
      t1mt += 2
   elif t1mt < loops + 33:
      tripl[2].fillcolor("black")
      tripl[0].forward(10)
      tripl[0].right(10)
      tripl[1].forward(10)
      tripl[1].right(10)
      tripl[2].forward(10)
      tripl[2].right(10)
      tripl[0].tilt(20)
      tripl[1].tilt(20)
      tripl[2].tilt(20)
      t1mt += 2
   elif t1mt < loops + 34:
      tripl[3].fillcolor("purple")
      t1mt += 2
   elif t1mt < loops + 35:
      tripl[3].goto(0, 100)
      t1mt += 2
   elif t1mt < loops + 44:
      tripl[3].fillcolor("black")
      for i in range(len(tripl)):
         tripl[i].forward(10)
         tripl[i].right(10)
         tripl[i].tilt(20)
      t1mt += 2
   elif t1mt < loops + 53:
      for i in range(len(tripl)):
         tripl[i].forward(20)
         tripl[i].right(20)
         tripl[i].tilt(40)
      t1mt += 2
   elif t1mt < loops + 71:
      for i in range(len(tripl)):
         tripl[i].forward(20)
         tripl[i].right(20)
         tripl[i].forward(20)
         tripl[i].right(20)
         tripl[i].tilt(80)
      t1mt += 2
   elif t1mt < loops + 80:
      for i in range(len(tripl)):
         if i != 0:
            tripl[i].forward(20)
            tripl[i].right(20)
            tripl[i].forward(20)
            tripl[i].right(20)
            tripl[i].tilt(80)
      x1, y1 = c.xcor(), c.ycor()
      x2, y2 = tripl[0].xcor(), tripl[0].ycor()

      diffx, diffy = x1 - x2, abs(y1- y2)

      rad = diffx / diffy

      ang = math.degrees(math.atan(rad)) - 90
      if ang >= 0:
          ang -= 360
      facing = tripl[0].heading()
      if facing > 0:
          facing -= 360

      if (ang > facing - 40 and ang <= facing) or (ang > facing - 400 and ang <= facing - 360):
          launchl[0] = True
          t1mt = loops + 79
          tripl[0].setheading(tripl[0].towards(x1, y1))
          cx = c.xcor()
      else:
          tripl[0].forward(20)
          tripl[0].right(20)
          tripl[0].forward(20)
          tripl[0].right(20)
          tripl[0].tilt(80)
      t1mt += 2

   elif t1mt < loops + 89:
      tripl[0].tilt(80)
      tripl[0].forward(40)
      for i in range(len(tripl)):
         if i != 0 and i != 1:
            tripl[i].forward(20)
            tripl[i].right(20)
            tripl[i].forward(20)
            tripl[i].right(20)
            tripl[i].tilt(80)
      if c.xcor() < cx:
         x1, y1 = cx - 200, -200
      else:
         x1, y1 = cx + 200, -200
      x2, y2 = tripl[1].xcor(), tripl[1].ycor()

      diffx, diffy = x1 - x2, abs(y1- y2)

      rad = diffx / diffy

      ang = math.degrees(math.atan(rad)) - 90
      if ang >= 0:
          ang -= 360
      facing = tripl[1].heading()
      if facing > 0:
          facing -= 360

      if (ang > facing - 40 and ang <= facing) or (ang > facing - 400 and ang <= facing - 360):
          launchl[1] = True
          t1mt = loops + 88
          tripl[1].setheading(tripl[1].towards(x1, y1))
      else:
          tripl[1].forward(20)
          tripl[1].right(20)
          tripl[1].forward(20)
          tripl[1].right(20)
          tripl[1].tilt(80)
      t1mt += 2
   elif t1mt < loops + 98:
      tripl[0].forward(40)
      tripl[0].tilt(80)
      tripl[1].forward(40)
      tripl[1].tilt(80)
      tripl[3].forward(20)
      tripl[3].right(20)
      tripl[3].forward(20)
      tripl[3].right(20)
      if c.xcor() < cx:
         x1, y1 = cx + 200, -200
      else:
         x1, y1 = cx - 200, -200
      x2, y2 = tripl[2].xcor(), tripl[2].ycor()

      diffx, diffy = x1 - x2, abs(y1- y2)

      rad = diffx / diffy

      ang = math.degrees(math.atan(rad)) - 90
      if ang >= 0:
          ang -= 360
      facing = tripl[2].heading()
      if facing > 0:
          facing -= 360

      if (ang > facing - 40 and ang <= facing) or (ang > facing - 400 and ang <= facing - 360):
          launchl[2] = True
          t1mt = loops + 97
          tripl[2].setheading(tripl[2].towards(x1, y1))
      else:
          tripl[2].forward(20)
          tripl[2].right(20)
          tripl[2].forward(20)
          tripl[2].right(20)
          tripl[2].tilt(80)
      t1mt += 2
   elif t1mt < loops + 107:
      for i in range(len(tripl)):
         if i != 3:
            tripl[i].forward(40)
            tripl[i].tilt(40)
      if c.xcor() < cx:
         x1, y1 = cx - 125, -200
      else:
         x1, y1 = cx + 125, -200
      x2, y2 = tripl[3].xcor(), tripl[3].ycor()

      diffx, diffy = x1 - x2, abs(y1- y2)

      rad = diffx / diffy

      ang = math.degrees(math.atan(rad)) - 90
      if ang >= 0:
          ang -= 360

      facing = tripl[3].heading()
      if facing > 0:
          facing -= 360

      if (ang > facing - 40 and ang <= facing) or (ang > facing - 400 and ang <= facing - 360):
          launchl[3] = True
          t1mt = loops + 106
          tripl[3].setheading(tripl[3].towards(x1, y1))
      else:
          tripl[3].forward(20)
          tripl[3].right(20)
          tripl[3].forward(20)
          tripl[3].right(20)
          tripl[3].tilt(80)
      t1mt += 2
   elif t1mt < loops + 150:
      for i in range(len(tripl)):
         if tripl[i].ycor() > -250 and launchl[i]:
            tripl[i].forward(40)
            tripl[i].tilt(80)
         else:
            if launchl[i]:
               launchl[i] = False
               tripl[i].fillcolor("purple")
            else:
               tripl[i].goto(1000, 1000)
               numFinished += 1
      if numFinished == 4:
         t1mt = loops + 149
      t1mt += 2
   elif t1mt < loops + 151:
      trip1.goto(-300, 50)
      t1mt += 2
      for i in range(len(tripl)):
         tripl[i].tiltangle(0)
         tripl[i].setheading(270)
   elif t1mt < loops + 152:
      trip2.goto(-100, 100)
      trip1.fillcolor("black")
      t1mt += 2
   elif t1mt < loops + 153:
      trip3.goto(100, 50)
      trip2.fillcolor("black")
      t1mt += 2
   elif t1mt < loops + 154:
      trip4.goto(300, 100)
      trip3.fillcolor("black")
      t1mt += 2
   elif t1mt < loops + 155:
      trip4.fillcolor("black")
      t1mt = 0
      cooldown = 80
      s2b2atk1 = False
      facing = 0
      cx = 0
      launchl = [False, False, False, False]
      numFinished = 0

s2b2atk2 = False
trip1timer = 0
trip2timer = 0
trip3timer = 0
trip4timer = 0
def tripatk2():
   global s2b2atk2, cooldown, t1mt, trip1timer, trip2timer, trip3timer, trip4timer
   if t1mt == 0:
      t1mt = loops
      s2b2atk2 = True
      t1mt += 2
      tripl[0].fillcolor("purple")
   elif t1mt < loops + 2:
      if c.xcor() < 0:
         tripl[0].goto(900, -190)
         tripl[0].setheading(180)
      else:
         tripl[0].goto(-900, -190)
         tripl[0].setheading(0)
      tripl[0].fillcolor("pink")
      tripl[1].fillcolor("purple")
      trip1timer = r.randint(43, 58)
      trip2timer = trip1timer + 30
      trip3timer = trip2timer + 30
      trip4timer = trip3timer + 30
      t1mt += 2
   elif t1mt < loops + 3:
      if c.xcor() < 0:
         tripl[1].goto(900, -190)
         tripl[1].setheading(180)
      else:
         tripl[1].goto(-900, -190)
         tripl[1].setheading(0)
      tripl[1].fillcolor("pink")
      tripl[2].fillcolor("purple")
      t1mt += 2
   elif t1mt < loops + 4:
      if c.xcor() < 0:
         tripl[2].goto(900, -190)
         tripl[2].setheading(180)
      else:
         tripl[2].goto(-900, -190)
         tripl[2].setheading(0)
      tripl[2].fillcolor("pink")
      tripl[3].fillcolor("purple")
      t1mt += 2
   elif t1mt < loops + 5:
      if c.xcor() < 0:
         tripl[3].goto(900, -190)
         tripl[3].setheading(180)
      else:
         tripl[3].goto(-900, -190)
         tripl[3].setheading(0)
      tripl[3].fillcolor("pink")
      t1mt += 2
   elif t1mt < loops + 15:
      t1mt += 2
   elif t1mt < loops + trip1timer:
      tripl[0].forward(80)
      t1mt += 2
   elif t1mt < loops + trip2timer:
      tripl[1].forward(80)
      t1mt += 2
   elif t1mt < loops + trip3timer:
      tripl[2].forward(80)
      t1mt += 2
   elif t1mt < loops + trip4timer:
      tripl[3].forward(80)
      t1mt += 2
   elif t1mt < loops + trip4timer + 1:
      for i in range(len(tripl)):
         tripl[i].fillcolor("purple")
         tripl[i].setheading(-90)
      trip1.goto(-300, 50)
      trip2.goto(-100, 100)
      trip3.goto(100, 50)
      trip4.goto(300, 100)
      t1mt += 2
   elif t1mt < loops + trip4timer + 2:
      for i in range(len(tripl)):
         tripl[i].fillcolor("black")
      s2b2atk2 = False
      trip1timer = 0
      trip2timer = 0
      trip3timer = 0
      trip4timer = 0
      t1mt = 0
      cooldown = 40

tripup1 = 0
tripup2 = 10
         
         
      
#stage 3 boss 2
blast = turtle.Turtle()
blast.hideturtle()
blast.pencolor("pink")
blastSize = 1
blast.pensize(blastSize)
s3b2atk = False
shieldDown = 0
def b2blastatk():
   global s3b2atk, cooldown, t1mt, blastSize, shieldDown
   if t1mt == 0:
      t1mt = loops + 2
      s3b2atk = True
      blast.penup()
      if c.xcor() < b2.xcor():
         blast.goto(-130, -170)
         blast.setheading(180)
      else:
         blast.goto(130, -170)
         blast.setheading(0)
      blast.pendown()
   elif t1mt <= loops + 17:
      blast.pensize(blastSize)
      blast.setx(blast.xcor())
      blastSize += 5
      t1mt += 2
   else:
      blast.forward(16)
      blast.clear()
      blast.forward(1)
      t1mt += 2
      if blast.xcor() >= 600 or blast.xcor() <= -600:
         blast.clear()
         blast.penup()
         blast.goto(1000, 1000)
         t1mt = 0
         s3b2atk = False
         cooldown = r.randint(30, 60)
         blastSize = 1
         blast.pensize(blastSize)
         shieldDown = 30
         
beam = turtle.Turtle()
beam.hideturtle()
beam.pencolor("pink")
beam.pensize(60)
energy = turtle.Turtle()
energy.hideturtle()
energy.pencolor("pink")
energySize = 1
energy.pensize(energySize)
hitspot = 250
s3b2atk2 = False
def b2beamatk():
   global s3b2atk2, cooldown, t1mt, energySize, shieldDown, hitspot
   if t1mt == 0:
      t1mt = loops + 2
      s3b2atk2 = True
      energy.penup()
      energy.goto(0, -80)
      energy.pendown()
   elif t1mt <= loops + 30:
      energy.clear()
      energy.sety(energy.ycor() + 2)
      energySize += 4
      energy.pensize(energySize)
      beam.penup()
      beam.goto(0, energy.ycor())
      beam.pendown()
      t1mt += 2
   elif t1mt <= loops + 70:
      beam.clear()
      hitspot2 = hitspot
      x = 0
      if c.xcor() < b2.xcor():
         hitspot2 *= -1
      beam.setheading(beam.towards(hitspot2, -200))
      while True:
         beam.forward(1)
         x += 1
         if x % 40 == 0:
            s3b2hurt()
         if beam.ycor() <= -190:
            break
      hitspot += 25
      energy.clear()
      energySize -= 1.5
      energy.pensize(energySize)
      energy.sety(energy.ycor())
      beam.penup()
      beam.goto(0, energy.ycor())
      beam.pendown()
      t1mt += 2
   else:
      beam.goto(1000, 1000)
      energy.clear()
      beam.clear()
      beam.penup()
      s3b2atk2 = False
      energy.pensize(1)
      energySize = 1
      shieldDown = 30
      t1mt = 0
      cooldown = 45
      hitspot = 250
      
      
      
      
#boss3
b3 = turtle.Turtle()
b3.pencolor("white")
b3.shape("circle")
b3.penup()
b3.hideturtle()
b3.goto(1000, -200)

#boss3 functions
attacking = False
boss3HP = 20
#r1 = 12
def hurtb3():
   global boss3HP
   proposY = p.ycor()
   proposX = p.xcor()

   di = math.sqrt((b3.xcor() - proposX)**2 + (b3.ycor() - proposY)**2)

   if b3.isvisible() == True:
      if di <= r1:
         b3.pencolor("red")
         p.hideturtle()
         p.goto(800, 310)
         global Pup
         global Pdown
         global Pright
         global Pleft
         global currently_firing
         currently_firing = False
         Pup = False
         Pdown = False
         Pright = False
         Pleft = False
         boss3HP -= 1
      elif b3.pencolor() == "red":
         b3.pencolor("white")

      if boss3HP == 10 and p1.xcor() == 0:
         p1.forward(200)
      if boss3HP == 5 and p3.xcor() == 100:
         p3.forward(100)
      if b3.pencolor() == "red":
         p2.forward(20)

b3up = False
def b3move():
   global loops, b3up, ast, Pright, Pleft
   if b3up == False and c.ycor() <= b3.ycor() + 20:
      if c.xcor() < b3.xcor():
         b3.setx(b3.xcor() - 6)
      else:
         b3.setx(b3.xcor() + 6)
   else:
      if c.xcor() < b3.xcor():
         b3.setx(b3.xcor() - 2)
      else:
         b3.setx(b3.xcor() + 2)
   if b3up == True and ast <= loops + 10:
      b3.sety(b3.ycor() + 10)
      ast += 2
   elif (p.xcor() >= b3.xcor() - 60 and p.xcor() <= b3.xcor() - 45) and Pright:
      if r.randint(1, 10) == 5:
         b3up = True
         ast = loops + 1
   elif (p.xcor() <= b3.xcor() + 60 and p.xcor() >= b3.xcor() + 45) and Pleft:
      if r.randint(1, 10) == 5:
         b3up = True
         ast = loops + 1
   elif b3up == True and ast > loops + 10:
      b3up = False
      ast = 0
   elif b3up == False and b3.ycor() > -200:
      b3.sety(b3.ycor() - 10)

#b3 s2
#r2 = 140
#variables for attacks
end = False
s2b3atk50p = False
armorList = ["white", "orange", "yellow", "green2", "LightSkyBlue", "MediumOrchid1", "HotPink1"]
armorLevel = 6
def hurtb3s2():
   global boss3HP, Pup, Pdown, Pright, Pleft, currently_firing, end, s2b3atk50p, armorLevel, armorList
   proposY = p.ycor()
   proposX = p.xcor()

   di = math.sqrt((b3.xcor() - proposX)**2 + (b3.ycor() - proposY)**2)
   if (((s2b3atk2 and ast > 76) or (s2b3atk50p and ast >= loops + 76))
   and (di < 190 and di > 170)):
         #time.sleep(1)
         shieldPen.circle(180, 10)
         dist = math.sqrt((shieldPen.xcor() - proposX)**2 + (shieldPen.ycor() - proposY)**2)
         if dist <= 30:
            return 5
         wn.update()
         #time.sleep(0.5)
         p.hideturtle()
         p.goto(800, 310)
         currently_firing = False
         Pup = False
         Pdown = False
         Pright = False
         Pleft = False
               
   if di <= r2-10:
      p.hideturtle()
      p.goto(800, 310)
      currently_firing = False
      Pup = False
      Pdown = False
      Pright = False
      Pleft = False
      if b3.fillcolor() != "pink":
         if not s2b3atk50p or (s2b3atk or s2b3atk2):
            boss3HP -= 1
            b3.pencolor("red")
            if s2b3atk2:
               end = True
         else:
            if armorLevel == 0:
               boss3HP -= 1
               b3.pencolor("red")
               end = True
            else:
               armorLevel -= 1
               b3.pencolor(armorList[armorLevel])
   elif b3.pencolor() == "red":
      b3.pencolor("white")

   if boss3HP == 100 and p1.xcor() == 0:
      p1.forward(400)
      s2b3atk50p = True
   if boss3HP == 50 and p3.xcor() == 200:
      p3.forward(200)
   if b3.pencolor() == "red":
      p2.forward(4)

s2b3atk = False
b3up = False
b3down = False
b3downCount = 0
heightCount = 0
jumptimes = 0
atksleft = 0

def b3s2atk():
   global boss3HP, ast, cooldown, s2b3atk, heightCount, b3up, b3down, b3downCount, jumptimes, atksleft, tarpos, bosspos, dist
   if ast == 0:
      ast = loops + 2
      s2b3atk = True
      jumptimes = r.randint(8, 15)
      heightCount = 24/(jumptimes + 2)*2
      b3up = True
      atksleft = jumptimes
   elif ast <= loops + (jumptimes * 16):
      if b3downCount == 8:
         b3down = True
         b3up = False
         b3.sety(b3.ycor() - heightCount)
         b3downCount -= 1
      elif b3down:
         b3.sety(b3.ycor() - heightCount)
         b3downCount -= 1
         if b3downCount == 0:
            b3down = False
            b3up = True
            heightCount += 24/(jumptimes + 2)
      elif b3up:
         b3.sety(b3.ycor() + heightCount)
         b3downCount += 1
      ast += 2
   elif ast <= loops + (jumptimes * 16) + 1:
      tarpos = c.xcor()
      bosspos = b3.xcor()
      dist = tarpos - bosspos
      ast += 2
   elif ast <= loops + (jumptimes * 16) + 8:
      newBossY = b3.ycor() + 48
      newBossX = b3.xcor() + (dist/14)
      b3.goto(newBossX, newBossY)
      ast += 2
   elif ast <= loops + (jumptimes * 16) + 15:
      newBossY = b3.ycor() - 48
      newBossX = b3.xcor() + (dist/14)
      b3.goto(newBossX, newBossY)
      ast += 2
   elif ast <= loops + (jumptimes * 16) + 16:
      ast += 2
   elif ast <= loops + (jumptimes * 16) + 17:
      atksleft -= 1
      ast += 2
      if atksleft > 0:
         ast = loops + (jumptimes * 16) + 2
   elif ast <= loops + (jumptimes * 16) + 18:
      s2b3atk = False
      b3up = False
      b3down = False
      b3downCount = 0
      heightCount = 0
      jumptimes = 0
      atksleft = 0
      tarpos = 0
      bosspos = 0
      dist = 0
      ast = 0
      cooldown = 150
      

      
s2b3atk2 = False
shieldPen = turtle.Turtle()
shieldPen.pencolor("pink")
shieldPen.pensize(20)
shieldPen.hideturtle()
shieldPen.penup()
shieldPen.goto(1000, 1000)
shieldAmount = 6
angle = 270
def b3s2atk2():
   global boss3HP, ast, cooldown, s2b3atk2, tarpos, bosspos, shieldAmount, angle, end
   if ast == 0:
      b3.fillcolor("pink")
      ast = loops + 2
      s2b3atk2 = True
      if c.xcor() >= 0:
         tarpos = -500
      else:
         tarpos = 500
      bosspos = b3.xcor()
   elif ast <= loops + 10:
      b3.setx(b3.xcor() + (tarpos - bosspos)/20)
      b3.sety(b3.ycor() + 20)
      ast += 2
   elif ast <= loops + 20:
      b3.setx(b3.xcor() + (tarpos - bosspos)/20)
      b3.sety(b3.ycor() - 20)
      ast += 2
   elif ast <= loops + 76:
      shieldPen.goto(b3.xcor(), b3.ycor() - 180)
      shieldPen.clear()
      shieldPen.pendown()
      shieldPen.circle(180, shieldAmount)
      shieldPen.penup()
      shieldPen.setheading(0)
      shieldAmount += 6
      ast += 2
   elif ast <= loops + 77:
      b3.fillcolor("black")
      ast += 2
   else:
      if end:
         shieldPen.goto(1000, 1000)
         shieldAmount = 6
         angle = 270
         shieldPen.setheading(0)
         shieldPen.clear()
         if bosspos != -2000:
            ast = loops + 81
            bosspos = -2000
            if c.xcor() > b3.xcor():
               tarpos = -5
            else:
               tarpos = 5
         if ast <= loops + 85:
            b3.goto(b3.xcor() + tarpos, b3.ycor() + 2)
         elif ast <= loops + 90:
            b3.goto(b3.xcor() + tarpos, b3.ycor() - 2)
         elif ast <= loops + 95:
            b3.goto(b3.xcor() + tarpos, b3.ycor() + 1)
         elif ast <= loops + 100:
            b3.goto(b3.xcor() + tarpos, b3.ycor() - 1)
         else:
            ast = 0
            tarpos = 0
            bosspos = 0
            end = False
            s2b3atk2 = False
            cooldown = 115
            return None
         
      else:    
         shieldPen.goto(b3.xcor(), b3.ycor())
         shieldPen.setheading(angle)
         shieldPen.forward(180)
         shieldPen.setheading(angle - 270)
         shieldPen.clear()
         shieldPen.pendown()
         shieldPen.circle(180, shieldAmount)
         shieldPen.penup()
         angle += 6
         if angle >= 360:
            angle -= 360
         if c.xcor() < b3.xcor():
            b3.setx(b3.xcor() - 3)
         else:
            b3.setx(b3.xcor() + 3)
      ast += 2

shieldJump = False    
def b3s2atk50p():
   global boss3HP, ast, cooldown, s2b3atk50p, tarpos, bosspos, shieldAmount, angle, end, shieldJump
   if ast == 0:
      b3.fillcolor("pink")
      ast = loops + 2
      s2b3atk50p = True
      if c.xcor() >= 0:
         tarpos = -500
      else:
         tarpos = 500
      bosspos = b3.xcor()
   elif ast <= loops + 10:
      b3.setx(b3.xcor() + (tarpos - bosspos)/20)
      b3.sety(b3.ycor() + 20)
      ast += 2
   elif ast <= loops + 20:
      b3.setx(b3.xcor() + (tarpos - bosspos)/20)
      b3.sety(b3.ycor() - 20)
      ast += 2
   elif ast <= loops + 76:
      shieldPen.goto(b3.xcor(), b3.ycor() - 180)
      shieldPen.clear()
      shieldPen.pendown()
      shieldPen.circle(180, shieldAmount)
      shieldPen.penup()
      shieldPen.setheading(0)
      shieldAmount += 6
      ast += 2
   elif ast <= loops + 77:
      b3.fillcolor("black")
      b3.pencolor(armorList[armorLevel])
      ast += 2
   else:
      if end:
         shieldPen.goto(1000, 1000)
         shieldAmount = 6
         angle = 270
         shieldPen.setheading(0)
         shieldPen.clear()
         if bosspos != -2000:
            ast = loops + 81
            bosspos = -2000
            if c.xcor() > b3.xcor():
               tarpos = -5
            else:
               tarpos = 5
         if ast <= loops + 85:
            b3.goto(b3.xcor() + tarpos, b3.ycor() + 2)
         elif ast <= loops + 90:
            b3.goto(b3.xcor() + tarpos, b3.ycor() - 2)
         elif ast <= loops + 95:
            b3.goto(b3.xcor() + tarpos, b3.ycor() + 1)
         elif ast <= loops + 100:
            b3.goto(b3.xcor() + tarpos, b3.ycor() - 1)
         else:
            ast = 0
            tarpos = 0
            bosspos = 0
            end = False
            s2b3atk50p = False
            cooldown = 50
            return None
         
      else:
         if not shieldJump:
            if c.xcor() < b3.xcor():
               b3.setx(b3.xcor() - 5)
               if b3.xcor() <= -300:
                  shieldJump = True
                  ast = loops + 81
            else:
               b3.setx(b3.xcor() + 5)
               if b3.xcor() >= 300:
                  shieldJump = True
                  ast = loops + 81
         else:
            if ast <= loops + 101:
               b3.sety(b3.ycor() + 50)
            elif ast <= loops + 102:
               if b3.xcor() < 0:
                  b3.setx(-450)
               else:
                  b3.setx(450)
            elif ast <= loops + 122:
               b3.sety(b3.ycor() - 50)
               b3.fillcolor("pink")
            elif ast <= loops + 123:
               shieldJump = False
               b3.fillcolor("black")
         shieldPen.goto(b3.xcor(), b3.ycor())
         shieldPen.setheading(angle)
         shieldPen.forward(180)
         shieldPen.setheading(angle - 270)
         shieldPen.clear()
         shieldPen.pendown()
         shieldPen.circle(180, shieldAmount)
         shieldPen.penup()
         angle += 6
         if angle >= 360:
            angle -= 360
         
      ast += 2

#s3 b3
#r3 = 100
def hurtb3s3():
   global boss3HP, Pup, Pdown, Pright, Pleft, currently_firing#, end, s2b3atk50p, armorLevel, armorList
   proposY = p.ycor()
   proposX = p.xcor()

   di = math.sqrt((b3.xcor() - proposX)**2 + (b3.ycor() - proposY)**2)
   
   if di <= r3:
      p.hideturtle()
      p.goto(800, 310)
      currently_firing = False
      Pup = False
      Pdown = False
      Pright = False
      Pleft = False
      if b3.fillcolor() != "pink":
         if True:
            boss3HP -= 1
            b3.pencolor("red")
            if s2b3atk2:
               end = True
         else:
            if armorLevel == 0:
               boss3HP -= 1
               b3.pencolor("red")
               end = True
            else:
               armorLevel -= 1
               b3.pencolor(armorList[armorLevel])
   elif b3.pencolor() == "red":
      b3.pencolor("white")

   if boss3HP == 25 and p1.xcor() == 0:
      p1.forward(300)
      s2b3atk50p = True
   if boss3HP == 12 and p3.xcor() == 156:
      p3.forward(144)
   if b3.pencolor() == "red":
      p2.forward(12)


def b3s3move():
   if c.xcor() < b3.xcor() + 18 and c.xcor() > b3.xcor() - 18:
      pass
   elif c.xcor() < b3.xcor():
      b3.setx(b3.xcor() - 9)
   else:
      b3.setx(b3.xcor() + 9)

#passive attack
shotPen = turtle.Turtle()
shotPen.hideturtle()
shotPen.penup()
shooting = False
astpassive = 0
cooldownpassive = 0
shotx, shoty = 0, 0
def b3shoot():
   global shooting, astpassive, cooldownpassive, shotx, shoty
   if astpassive == 0:
      shotx = b3.xcor()
      shoty = b3.ycor()
      shotPen.goto(shotx, shoty)
      shooting = True
      astpassive += 1
      shotPen.pendown()
      shotPen.dot(50, "pink")
      shotPen.penup()
   elif not (shoty > -215 and shoty < -185):
      astpassive += 1
      shoty -= 15
      shotPen.goto(shotx, shoty)
      shotPen.clear()
      shotPen.pendown()
      shotPen.dot(50, "pink")
      shotPen.penup()
   else:
      shotPen.hideturtle()
      shotPen.penup()
      shotPen.clear()
      shooting = False
      astpassive = 0
      cooldownpassive = 45
      shotPen.goto(800, 1000)
   
      


#attack 2
class HenryClone():
   henries = []
   def __init__(self):
      HenryClone.henries.append(self)
      self.thing = turtle.Turtle()
      self.thing.penup()
      self.thing.hideturtle()
      self.thing.shape("circle")
      self.thing.goto(1000, 1000)
      self.thing.pencolor("white")
      self.health = 1
      self.jst = 0
      self.henryup = False
      
   def prep(self):
      self.thing.goto(b3.xcor(), b3.ycor() - 120)
      self.thing.showturtle()
      self.thing.pencolor("pink")
      self.health = 1
      global moveThem
      moveThem = False
      
   def check(self):
      proposY = p.ycor()
      proposX = p.xcor()
      if math.sqrt((self.thing.xcor() - proposX)**2 + (self.thing.ycor() - proposY)**2) < 12 and self.health > 0:
         global Pup, Pdown, Pright, Pleft, currently_firing
         p.hideturtle()
         p.goto(800, 310)
         currently_firing = False
         Pup = False
         Pdown = False
         Pright = False
         Pleft = False
         if self.thing.pencolor() != "pink":
            self.health -= 1
            self.thing.pencolor("red")
      elif self.thing.pencolor() == "red":
         self.thing.pencolor("white")
      if self.health <= 0:
         self.thing.hideturtle()

   def hurtC(self):
      global lives, unableToMove, invincible
      if math.sqrt((self.thing.xcor() - c.xcor())**2 + (self.thing.ycor() - c.ycor())**2) < 13 and self.health > 0:
         unableToMove = True
         lives -= 1
         invincible = 20
         if (c.xcor() < thing.xcor() and c.xcor() > -360) or c.xcor() > 360:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         unableToMove = False
         return 0

   def reset(self):
      self.thing.hideturtle()
      self.thing.goto(1000, 1000)
      self.thing.pencolor("white")
      self.health = 1
      self.jst = 0
      self.henryup = False
      global moveThem
      moveThem = False

   def hmove(self):
      global loops, Pright, Pleft
      if self.henryup == False and c.ycor() <= self.thing.ycor() + 20:
         if c.xcor() < self.thing.xcor():
            self.thing.setx(self.thing.xcor() - 5)
         else:
            self.thing.setx(self.thing.xcor() + 5)
      else:
         if c.xcor() < self.thing.xcor():
            self.thing.setx(self.thing.xcor() - 5)
         else:
            self.thing.setx(self.thing.xcor() + 5)
      if self.henryup == True and self.jst <= loops + 10:
         self.thing.sety(self.thing.ycor() + 10)
         self.jst += 2
      elif (p.xcor() >= self.thing.xcor() - 60 and p.xcor() <= self.thing.xcor() - 45) and Pright and not self.henryup:
         if r.randint(1, 10) == 5:
            self.henryup = True
            self.jst = loops + 1
      elif (p.xcor() <= self.thing.xcor() + 60 and p.xcor() >= self.thing.xcor() + 45) and Pleft and not self.henryup:
         if r.randint(1, 10) == 5:
            self.henryup = True
            self.jst = loops + 1
      elif self.henryup == True and self.thing.ycor() != -200:
         self.thing.sety(self.thing.ycor() - 10)
         self.jst += 2
      else:
         self.henryup = False
         self.jst = 0
            
henryList = [HenryClone() for i in range(15)]

s3b3atk = False
henryNum = 0
moveThem = False
def moveHenries():
   global moveThem
   if moveThem:
      x = True
      for h in HenryClone.henries:
         h.hmove()
         if h.thing.isvisible():
            x = False
      for henry in HenryClone.henries:
         henry.check()
      if x:
         for h in HenryClone.henries:
            h.reset()
         moveThem = False
         
def checkallforhurt():
   for henry in HenryClone.henries:
       if henry.hurtC() == False:
            break
def b3s3atk():
   global s3b3atk, ast, cooldown, henryNum, moveThem, attacking
   if ast == 0:
      for henry in HenryClone.henries:
         henry.prep()
      s3b3atk = True
      attacking = True
      ast += 1
   elif ast <= 12:
      HenryClone.henries[henryNum].thing.goto(b3.xcor(), b3.ycor())
      HenryClone.henries[henryNum].thing.setheading(270 - ast * 2 * (henryNum + 1))
      HenryClone.henries[henryNum].thing.forward(120)
      ast += 1
   elif ast == 13:
      if henryNum < 14:
         henryNum += 1
         ast = 1
      else:
         ast += 1
   elif ast <= 73:
      for henry in HenryClone.henries:
         henry.thing.goto(b3.xcor(), b3.ycor())
         henry.thing.right(6)
         henry.thing.forward(120)
      ast += 1
   elif ast <= 77:
      if henryNum != 0:
         for i in range(henryNum - 1):
            HenryClone.henries[i].thing.goto(b3.xcor(), b3.ycor())
            HenryClone.henries[i].thing.right(6)
            HenryClone.henries[i].thing.forward(120)
      if True:
         for i in range(henryNum, 15):
            if HenryClone.henries[i].thing.ycor() == -200 or HenryClone.henries[i].henryup:
               HenryClone.henries[i].hmove()
            elif HenryClone.henries[i].thing.ycor() < -190 and HenryClone.henries[i].thing.ycor() > -210 and not HenryClone.henries[i].henryup:
               HenryClone.henries[i].thing.sety(-200)
               HenryClone.henries[i].thing.pencolor("white")
            else:
               if HenryClone.henries[i].thing.ycor() > -100 :
                  HenryClone.henries[i].thing.setheading(HenryClone.henries[i].thing.towards(c.xcor(), c.ycor()))
               HenryClone.henries[i].thing.forward(20)
      ast += 1
   elif ast == 78:
      for h in HenryClone.henries:
         if h.thing.ycor() != -200 or h.henryup:
            ast = 74
      if henryNum != 0:
         henryNum -= 1
      if ast != 74:
         ast += 1
   elif ast == 79:
      moveThem = True
      cooldown = 300
      ast = 0
      s3b3atk = False
      attacking = False
      henryNum = 0
      

   for henry in HenryClone.henries:
      henry.check()

s3b3atk2 = False
offset = 0
def b3s3atk2():
   global tarpos, bosspos, invincible, ast, cooldown, s3b3atk2, offset, attacking
   if ast == 0:
      attacking = True
      s3b3atk2 = True
      if c.xcor() <= 0:
         tarpos = -600
      else:
         tarpos = 600
      bosspos = tarpos - b3.xcor()
      ast += 1
   elif ast <= 11:
      b3.setx(b3.xcor() + bosspos/10)
      ast += 1
   elif ast <= 85:
      shotPen.clear()
      if tarpos < 0:
         b3.setx(b3.xcor() + 15)
      else:
         b3.setx(b3.xcor() - 15)
      shotPen.goto(b3.xcor(), b3.ycor())
      shotPen.dot(100, "pink")
      shotPen.goto(b3.xcor(), b3.ycor() - offset)
      i = invincible
      shotPen.dot(50, "pink")
      while shotPen.ycor() >= -200:
         shotPen.sety(shotPen.ycor() - 40)
         shotPen.dot(50, "pink")
         invinciblePLSBlink(b3s3hurt)
         invincible = i
      f.setx(-800)
      f.clear()
      f.pendown()
      f.forward(1600)
      f.penup()
      offset += 5
      if offset == 40:
         offset = 0
      ast += 1
   elif ast == 86:
      offset = 0
      s3b3atk2 = False
      tarpos = 0
      bosspos = 0
      ast = 0
      shotPen.clear()
      shotPen.goto(800, 1000)
      attacking = False
      cooldown = 150
      

#b3 s4
b3s4attacks = []
b3s4attacks.append(b3s3atk2)
b3s4attacks.append(b3s3atk)

displaceShield = 0
def passiveShield():
   if not s2b3atk2 and not s2b3atk:
      global displaceShield
      shieldPen.setheading(0)
      shieldPen.goto(b3.xcor(), b3.ycor() - 150)
      shieldPen.circle(150, displaceShield)
      shieldPen.clear()
      shieldPen.pendown()
      shieldPen.circle(150, 180)
      shieldPen.penup()
      displaceShield += 6
      if displaceShield == 360:
         displaceShield = 0
      
         
         
def hurtb3s4():
   global boss3HP, Pup, Pdown, Pright, Pleft, currently_firing, end#, s2b3atk50p, armorLevel, armorList
   proposY = p.ycor()
   proposX = p.xcor()

   di = math.sqrt((b3.xcor() - proposX)**2 + (b3.ycor() - proposY)**2)
   if (not s2b3atk2 and not s2b3atk
   and di < 160 and di > 140):
         shieldPen.circle(150, 15)
         for i in range(9):
            shieldPen.circle(150, 15)
            dist = math.sqrt((shieldPen.xcor() - proposX)**2 + (shieldPen.ycor() - proposY)**2)
            if dist <= 30:
               shieldPen.circle(150, 210)
               for j in range(i, 9):
                  shieldPen.circle(150, 15)
               return 5

         shieldPen.circle(150, 210)
         p.hideturtle()
         p.goto(800, 310)
         currently_firing = False
         Pup = False
         Pdown = False
         Pright = False
         Pleft = False
   elif (s2b3atk2 and ast > 76
   and di < 160 and di > 140):
         shieldPen.circle(150, 10)
         dist = math.sqrt((shieldPen.xcor() - proposX)**2 + (shieldPen.ycor() - proposY)**2)
         if dist <= 30:
            return 5
         wn.update()
         p.hideturtle()
         p.goto(800, 310)
         currently_firing = False
         Pup = False
         Pdown = False
         Pright = False
         Pleft = False
               
   if di <= r4:
      p.hideturtle()
      p.goto(800, 310)
      currently_firing = False
      Pup = False
      Pdown = False
      Pright = False
      Pleft = False
      if b3.fillcolor() != "pink" and b3.pencolor() != "pink":
         if True:
            boss3HP -= 1
            b3.pencolor("red")
            if s2b3atk2:
               end = True
         else:
            if armorLevel == 0:
               boss3HP -= 1
               b3.pencolor("red")
               end = True
            else:
               armorLevel -= 1
               b3.pencolor(armorList[armorLevel])
   elif b3.pencolor() == "red":
      b3.pencolor("white")

   if boss3HP == 25 and p1.xcor() == 0:
      p1.forward(300)
      s2b3atk50p = True
   if boss3HP == 12 and p3.xcor() == 156:
      p3.forward(144)
   if b3.pencolor() == "red":
      p2.forward(12)

def s4s2atk():
   global ast, cooldown, s2b3atk, jumptimes, atksleft, attacking
   if ast == 0:
      shieldPen.clear()
      ast = 1
      s2b3atk = True
      attacking = True
      jumptimes = r.randint(10, 20)
      atksleft = jumptimes
      b3.fillcolor("purple")
   elif ast <= 20:
      if ast % 2 == 0:
         b3.fillcolor("purple")
      else:
         b3.fillcolor("black")
      ast += 1
   elif ast == 21:
      b3.goto(c.xcor(), 100)
      ast += 1
   elif ast <= 35:
      b3.fillcolor("black")
      b3.sety(b3.ycor() - 20)
      ast += 1
   elif ast == 36:
      b3.fillcolor("purple")
      if atksleft > 0:
         atksleft -= 1
         ast = 21
      else:
         ast += 1
   elif ast == 37:
      b3.goto(c.xcor(), 100)
      ast += 1
   elif ast == 38:
      b3.fillcolor("black")
      s2b3atk = False
      attacking = False
      jumptimes = 0
      atksleft = 0
      ast = 0
      cooldown = 150
b3s4attacks.append(s4s2atk)

def s4s2atk2():
   global boss3HP, ast, cooldown, s2b3atk2, tarpos, bosspos, shieldAmount, angle, end, attacking
   if ast == 0:
      shieldPen.clear()
      if b3.shape() == "henry":
         b3.pendown()
         b3.dot(r5 * 2 + 2, "pink")
         b3.dot(r5 * 2 - 2, "black")
         b3.penup()
      b3.fillcolor("pink")
      ast = 1
      s2b3atk2 = True
      attacking = True
      if c.xcor() >= 0:
         tarpos = -500
      else:
         tarpos = 500
      bosspos = b3.xcor()
   elif ast <= 20:
      b3.clear()
      b3.setx(b3.xcor() + (tarpos - bosspos)/20)
      b3.sety(b3.ycor() - 8)
      if b3.shape() == "henry":
         b3.pendown()
         b3.dot(r5 * 2 + 2, "pink")
         b3.dot(r5 * 2 - 2, "black")
         b3.penup()
      ast += 1
   elif ast <= 76:
      b3.clear()
      shieldPen.goto(b3.xcor(), b3.ycor() - 150)
      shieldPen.clear()
      shieldPen.pendown()
      shieldPen.circle(150, shieldAmount)
      shieldPen.penup()
      shieldPen.setheading(0)
      shieldAmount += 6
      ast += 1
      if b3.shape() == "henry":
         b3.pendown()
         b3.dot(r5 * 2 + 2, "pink")
         b3.dot(r5 * 2 - 2, "black")
         b3.penup()
   elif ast <= 77:
      b3.clear()
      b3.fillcolor("black")
      ast += 1
   else:
      if end:
         shieldPen.goto(1000, 1000)
         shieldAmount = 6
         angle = 270
         shieldPen.setheading(0)
         shieldPen.clear()
         if bosspos != -2000:
            ast = 81
            bosspos = -2000
         if ast <= 82:
            b3.fillcolor("purple")
            if b3.shape() == "henry":
               b3.pendown()
               b3.dot(r5 * 2 + 2, "purple")
               b3.penup()
         elif ast <= 83:
            b3.clear()
            b3.goto(c.xcor(), 100)
            if b3.shape() == "henry":
               b3.pendown()
               b3.dot(r5 * 2 + 2, "purple")
               b3.penup()
         elif ast <= 84:
            b3.clear()
            b3.fillcolor("black")
         else:
            ast = 0
            tarpos = 0
            bosspos = 0
            end = False
            s2b3atk2 = False
            attacking = False
            cooldown = 100
            return None
         
      else:    
         shieldPen.goto(b3.xcor(), b3.ycor())
         shieldPen.setheading(angle)
         shieldPen.forward(150)
         shieldPen.setheading(angle - 270)
         shieldPen.clear()
         shieldPen.pendown()
         shieldPen.circle(150, shieldAmount)
         shieldPen.penup()
         angle += 6
         if angle >= 360:
            angle -= 360
         if c.xcor() < b3.xcor():
            b3.setx(b3.xcor() - 4)
         else:
            b3.setx(b3.xcor() + 4)
      ast += 1
b3s4attacks.append(s4s2atk2)


#s4.5
#r5 = 100
def breathe():
   global t1mt, r5
   if t1mt <= 60:
      t1mt += 1
      r5 = (1 + t1mt/240)*100
      b3.shapesize(r5/100, r5/100)
   elif t1mt <= 120:
      t1mt += 1
      r5 = (1.25 - (t1mt - 60)/240)*100
      b3.shapesize(r5/100, r5/100)
   elif t1mt == 121:
      t1mt = 0
      b3.shapesize(1, 1)
def hurtb3s5():
   global boss3HP, Pup, Pdown, Pright, Pleft, currently_firing, end#, s2b3atk50p, armorLevel, armorList
   proposY = p.ycor()
   proposX = p.xcor()

   di = math.sqrt((b3.xcor() - proposX)**2 + (b3.ycor() - proposY)**2)

   if s2b3atk2 and ast > 76:
      if di < 160 and di > 140:
         shieldPen.circle(150, 10)
         dist = math.sqrt((shieldPen.xcor() - proposX)**2 + (shieldPen.ycor() - proposY)**2)
         if dist <= 30:
            return 5
         wn.update()
         p.hideturtle()
         p.goto(800, 310)
         currently_firing = False
         Pup = False
         Pdown = False
         Pright = False
         Pleft = False
         
   if di <= r5:
      p.hideturtle()
      p.goto(800, 310)
      currently_firing = False
      Pup = False
      Pdown = False
      Pright = False
      Pleft = False
      if b3.fillcolor() != "pink":
         if True:
            boss3HP -= 1
            b3.shape("hurt henry")
            if s2b3atk2:
               end = True
         else:
            if armorLevel == 0:
               boss3HP -= 1
               b3.shape("hurt henry")
               end = True
            else:
               armorLevel -= 1
               b3.pencolor(armorList[armorLevel])
   elif b3.shape() == "hurt henry":
      b3.shape("henry")

   if boss3HP == 30 and p1.xcor() == 0:
      p1.forward(300)
      s2b3atk50p = True
   if boss3HP == 15 and p3.xcor() == 150:
      p3.forward(150)
   if b3.shape() == "hurt henry":
      p2.forward(10)

endPen = turtle.Turtle()
endPen.hideturtle()
endPen.penup()
endPen.pencolor("white")
endPen.pensize(22)

def b3s5shoot():
   global shooting, astpassive, cooldownpassive, shotx, shoty
   if astpassive == 0:
      shotx = b3.xcor()
      shoty = b3.ycor()
      shotPen.goto(shotx, shoty)
      shooting = True
      astpassive += 1
      shotPen.pendown()
      shotPen.dot(50, "pink")
      shotPen.penup()
   elif not (shoty > -215 and shoty < -185):
      astpassive += 1
      shoty -= 20
      shotPen.goto(shotx, shoty)
      shotPen.clear()
      shotPen.pendown()
      shotPen.dot(50, "pink")
      shotPen.penup()
   else:
      shotPen.hideturtle()
      shotPen.penup()
      shotPen.clear()
      shooting = False
      astpassive = 0
      cooldownpassive = 30
      shotPen.goto(800, 1000)
      
b3s5attacks = [b3s3atk, b3s3atk2, s4s2atk2]
thing.pencolor("white")
thing.begin_poly()
thing.circle(50, 120)
thing.end_poly()
thingy = turtle.Shape("compound")
thingy.addcomponent(p, "", "white")
wn.register_shape("120 circle", thing.get_poly())
thing.clear()

class s5projectile():
   shots = []
   def __init__(self):
      self.thing = turtle.Turtle()
      self.thing.penup()
      self.thing.hideturtle()
      self.thing.shape("120 circle")
      self.thing.goto(1000, 1000)
      self.thing.color("white")
      self.thing.tiltangle(120)
      s5projectile.shots.append(self)
   def hurtC(self):
      global lives, unableToMove, invincible
      if math.sqrt((self.thing.xcor() + 50 - c.xcor())**2 + (self.thing.ycor() - c.ycor())**2) < 45 and c.ycor() <= self.thing.ycor() + 5:
         unableToMove = True
         lives -= 1
         invincible = 20
         if (c.xcor() < self.thing.xcor() and c.xcor() > -360) or c.xcor() > 360:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x -= 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            c.color("red")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y += 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
            c.color("white")
            for i in range(5):
               x = c.xcor()
               x += 17
               y = c.ycor()
               y -= 5
               c.goto(x, y)
               wn.update()
               time.sleep(1/30)
         unableToMove = False
         return 0
   def reset(self):
      self.thing.penup()
      self.thing.hideturtle()
      self.thing.shape("120 circle")
      self.thing.goto(1000, 1000)
      self.thing.pencolor("white")

pro1 = s5projectile()
pro2 = s5projectile()
pro3 = s5projectile()
pro4 = s5projectile()
pro5 = s5projectile()
pro6 = s5projectile()


s5b3atk = False
targetlocations = [400, 200, 0, -100, -300, -500]
def b3s5atk():
   global ast, cooldown, s5b3atk, attacking, bosspos
   if ast == 0:
      attacking = True
      s5b3atk = True
      ast += 1
      bosspos = 0 - b3.xcor()
   elif ast <= 10:
      b3.setx(b3.xcor() + bosspos/10)
      ast += 1
   elif ast <= 30:
      b3.tiltangle(b3.tiltangle() + 18)
      ast += 1
   elif ast == 31:
      for i in range(6):
         s5projectile.shots[i].thing.showturtle()
         s5projectile.shots[i].thing.goto(b3.xcor(), b3.ycor())
         s5projectile.shots[i].thing.setheading(s5projectile.shots[i].thing.towards(targetlocations[i], -200))
         s5projectile.shots[i].thing.forward(100)
      ast += 1
   elif ast <= 76:
      cancel = True
      for shot in s5projectile.shots:
         shot.thing.forward(20)
         if shot.thing.ycor() <= -200:
            shot.reset()
         else:
            cancel = False
      if cancel:
         ast = 76
      ast += 1
   else:
      attacking = False
      s5b3atk = False
      ast = 0
      cooldown = 200
      for shot in s5projectile.shots:
         shot.reset()

def checkb3s5atk():
   for shot in s5projectile.shots:
      shot.hurtC()
   
b3s5attacks.append(b3s5atk)
      
      
def b3s5atk2():
   global ast, cooldown, s2b3atk, jumptimes, atksleft, attacking
   if ast == 0:
      shieldPen.clear()
      ast = 1
      s2b3atk = True
      attacking = True
      jumptimes = r.randint(10, 20)
      atksleft = jumptimes
      b3.pendown()
      b3.dot(r5 * 2 + 2, "purple")
      b3.penup()
   elif ast <= 20:
      if ast % 2 == 0:
         b3.pendown()
         b3.dot(r5 * 2 + 2, "purple")
         b3.penup()
      else:
         b3.clear()
      ast += 1
   elif ast == 21:
      b3.goto(c.xcor(), 100)
      ast += 1
   elif ast <= 38:
      b3.clear()
      b3.sety(b3.ycor() - 13)
      ast += 1
   elif ast == 39:
      b3.pendown()
      b3.dot(r5 * 2 + 2, "purple")
      b3.penup()
      if atksleft > 0:
         atksleft -= 1
         ast = 21
      else:
         ast += 1
   elif ast == 40:
      b3.goto(c.xcor(), 100)
      ast += 1
   elif ast == 41:
      b3.clear()
      s2b3atk = False
      attacking = False
      jumptimes = 0
      atksleft = 0
      ast = 0
      cooldown = 100   

b3s5attacks.append(b3s5atk2)

def b3s5atk3():
   global atk2, ast, loops, cooldown, dist, bosspos, tarpos, exY, exX, exWid, exLen, attacking
   if ast == 0:
      ast = loops
   if ast == loops:
      tarpos = 0
      bosspos = b3.xcor()
      dist = tarpos - bosspos
      atk2 = True
      attacking = True
      ast += 2
   elif ast != 0 and ast < loops + 15:
      newBossY = b3.ycor() - 15
      newBossX = b3.xcor() + (dist/15)
      b3.goto(newBossX, newBossY)
      ast += 2
   elif ast != 0 and ast < loops + 38:
      ex.showturtle()
      ex.shapesize(stretch_wid = exWid, stretch_len = exLen)
      exWid += 2
      exLen += 2
      exY += 19
      exX += 19
      ast += 2
   elif ast == loops + 38:
      exWid = 1
      exLen = 1
      exY = 10
      exX = 10
      ex.shapesize(stretch_wid = exWid, stretch_len = exLen)
      ex.hideturtle()
      b3.pendown()
      b3.dot(r5 * 2 + 2, "purple")
      b3.penup()
      ast += 2
   elif ast == loops + 39:
      b3.clear()
      b3.goto(0, 100)
      b3.pendown()
      b3.dot(r5 * 2 + 2, "purple")
      b3.penup()
      ast += 2
   elif ast == loops + 40:
      b3.clear()
      ast = 0
      cooldown = 200
      atk2 = False
      attacking = False
      exWid = 1
      exLen = 1
      exY = 10
      exX = 10
      ex.shapesize(stretch_wid = exWid, stretch_len = exLen)
      ex.hideturtle()

b3s5attacks.append(b3s5atk3)


def combine():
   checkb3s5atk()
   checkallforhurt()

      
youWin = False
      
      
#spot1x, spot2x, spot3x, spot4x = -300, -100, 100, 300
#spot1y, spot2y, spot3y, spot4y = 50, 100, 50, 100  

p1 = turtle.Turtle()
p1.pensize(7)
p1.speed(0)
p3 = turtle.Turtle()
p3.speed(0)
p3.pensize(7)
p2 = turtle.Turtle()
p2.pensize(7)
p2.speed(0)

#game end pen
gpen = turtle.Turtle()
gpen.hideturtle()
gpen.color("white")
gpen.penup()
gpen.goto(-100, 0)
waittoend = 0

def startThings(boss):
   #things for before the game starts
   lpen.write("Lives:", font = ("Courier", 12, "normal"))
   boss.showturtle()
   c.showturtle()
   p.showturtle()
   life1.showturtle()
   life2.showturtle()
   life3.showturtle()
   f.pendown()
   f.forward(1800)
   turtle.hideturtle()

      
loops = 0
#tutorial
if True:
   exitGame.hideturtle()
   p3.pencolor("white")
   unableToMove = True
   p3.penup()
   p3.hideturtle()
   c.goto(0, -200)
   p3.goto(-100, 100)
   p3.pendown()
   p3.write("This is you.", font = ("Courier", 12, "normal"))
   c.showturtle()
   wn.update()
   time.sleep(1)
   cx = c.xcor()
   goneLeft = False
   goneRight = False
   p3.clear()
   p3.write("Press the left and right triggers to move left and right respectively.", font = ("Courier", 12, "normal"))
   unableToMove = False
   while not (goneLeft and goneRight):
      time.sleep(1/30)
      wn.update()
      joy_inputs(pygame.event.poll())
      jump_timer()
      projectile_movement()
      if cx < c.xcor():
         goneRight = True
      if cx > c.xcor():
         goneLeft = True
      cx = c.xcor()
   unableToMove = True
   p3.clear()
   p3.write("Good job.", font = ("Courier", 12, "normal"))
   wn.update()
   time.sleep(1)
   wasUp = False
   p3.clear()
   p3.write("Press the select button to jump.", font = ("Courier", 12, "normal"))
   unableToMove = False
   while True:
      time.sleep(1/30)
      wn.update()
      jump_timer()
      joy_inputs(pygame.event.poll())
      projectile_movement()
      if up:
         wasUp = True
      elif down_time == 0 and wasUp:
         break
   unableToMove = True
   p3.clear()
   p3.write("Well done.", font = ("Courier", 12, "normal"))
   wn.update()
   time.sleep(1)
   p3.clear()
   p3.write("Press a button (X, Y, A, B) to shoot in the button\'s direction.", font = ("Courier", 12, "normal"))
   unableToMove = False
   while True:
      time.sleep(1/30)
      wn.update()
      jump_timer()
      joy_inputs(pygame.event.poll())
      projectile_movement()
      if Pup or Pright or Pleft or Pdown:
         wasUp = False
      elif not (wasUp or p.isvisible()):
         break
   unableToMove = True
   p3.clear()
   p3.write("Excellent.", font = ("Courier", 12, "normal"))
   wn.update()
   time.sleep(1)
   wasUp = False
   p3.clear()
   henry16 = HenryClone()
   henry16.thing.showturtle()
   henry16.thing.goto(400, -200)
   HenryClone.henries.pop(15)
   while henry16.health > 0:
      
      #reset lives
      lives = 3
      life1.showturtle()
      life2.showturtle()
      life3.showturtle()
      life1.color("white")
      life2.color("white")
      life3.color("white")
      lpen.write("Lives:", font = ("Courier", 12, "normal"))
         
      lives = 3
      p3.write("\tNow kill the enemy.\nDon\'t lose all of your lives -- you only get three.", font = ("Courier", 12, "normal"))
      unableToMove = False
      henry16.thing.goto(400, -200)
      henry16.health = 3
      unableToMove = False
      while henry16.health > 0 and lives > 0:
         wn.update()
         time.sleep(1/30)

         jump_timer()
         joy_inputs(pygame.event.poll())
         projectile_movement()
          
         henry16.check()
         henry16.hmove()
          
         invinciblePLSBlink(henry16.hurtC)
            
         lifeLoss()
                
         loops += 1
      #reset projectile
      currently_firing = False
      Pup = False
      Pdown = False
      Pleft = False
      Pright = False
      p.hideturtle()
      p.goto(1000, -300)
      #reset circle
      c.goto(0, -200)
      up = False
      down = False
      jump_time = 0
      down_time = 0
      invincible = 0
      

   while True:
      wn.update()
      time.sleep(1/30)
      
      jump_timer()
      joy_inputs(pygame.event.poll())
      projectile_movement()
         
      if ast == 0:
         p3.clear()
         p3.write("You should now be ready.", font = ("Courier", 12, "normal"))
         ast += 1
      elif ast <= 60:
         ast += 1
      elif ast == 61:
         p3.clear()
         p3.write("Also, this is the easy version of the game.", font = ("Courier", 12, "normal"))
         ast += 1
      elif ast <= 100:
         ast += 1
      elif ast == 101:
         p3.clear()
         p3.write("Goodbye.", font = ("Courier", 12, "normal"))
         ast += 1
      elif ast <= 127:
         ast += 1
      else:
         ast = 0
         p3.clear()
         unableToMove = True
         break
      
   reset()
   if maxLevel < 1:
      maxLevel = 1
      file = open("LevelUnlock.txt", "wt")
      file.write(str(maxLevel))
      file.close()


#main
start_time = 0
end_time = 0
timer = 0
while True:
   while level == 0:
      bb1.showturtle()
      
      if maxLevel >= 4:
         bb4.showturtle()
         bb3.showturtle()
         bb2.showturtle()
         if bb4.shape() == "square":
            bb4.shape("triangle")
            bb4.setheading(90)
            bb4.sety(bb4.ycor() - 4)
         elif bb4.shape() == "triangle":
            bb4.shape("circle")
            bb4.setheading(0)
            bb4.sety(bb4.ycor() + 4)
         elif bb4.shape() == "circle":
            bb4.shape("square")
      elif maxLevel >= 3:
         bb3.showturtle()
         bb2.showturtle()
      elif maxLevel >= 2:
         bb2.showturtle()
      
      exitGame.showturtle()
      joy_menu(pygame.event.poll())
      wn.update()
      if level != 0:
         bb1.hideturtle()
         bb2.hideturtle()
         bb3.hideturtle()
         bb4.hideturtle()
         exitGame.hideturtle()
      
   while level == 1 or level == 4:
      startThings(b)
         
      
      #begin scene thing
      unableToMove = True
      for i in range(20):
         b.sety(b.ycor() - 31)
         wn.update()
         time.sleep(1/30)

      #pen1
      p1.penup()
      p1.hideturtle()
      p1.goto (-200, 200)
      p1.pensize(7)

      #pen3
      p3.penup()
      p3.hideturtle()
      p3.color("white")
      p3.goto(-130, 215)

      #life bar animation
      p1.speed(0)
      p1.pencolor("green")
      p1.pendown()
      for i in range(20):
         p1.forward(20)
         if i % 2 == 0:
            b.setx(b.xcor() - 1)
         else:
            b.setx(b.xcor() + 1)
         wn.update()
         time.sleep(1/30)
      p1.penup()
      p1.goto(0, 200)
      p1.pendown()
      p1.color("yellow")

      p3.write("The Ninety Degree Nightmare", font = ("Courier", 12, "normal"))
      p3.goto(100, 200)
      p3.color("red")
      p3.pendown()

      #pen2
      p2.penup()
      p2.hideturtle()
      p2.goto (-200, 200)
      p2.pencolor("white")
      p2.pendown()

      start_time = time.time()

      unableToMove = False
      #main loop
      loops = 0
      while True:
          wn.update()
          time.sleep(1/30)

          hurtBoss()
          jump_timer()
          joy_inputs(pygame.event.poll())
          projectile_movement()

          if vibrate == True or loops < 40:
             if loops % 2:
                b.setx(b.xcor() + 1)
             else:
                b.setx(b.xcor() - 1)

          if cooldown < 30:
             vibrate = False

          minionMove()
          hurtMinion()
          
          if cooldown > 0:
             cooldown -= 1
          elif cooldown == 0:
             attack()

          invinciblePLSBlink(hurt)
          hurtByEx()
          lifeLoss()
          
                
          loops += 1

          if bossHP == 0:
             youWin = True
             unableToMove = True
             break
          if lives <=0:
             youWin = False
             unableToMove = True
             break

      #you win
      if youWin:
         blast.clear()
         bossDie = 9
         for i in range(36):
            b.shapesize(stretch_wid = bossDie, stretch_len = bossDie)
            b.right(10)
            bossDie -= 0.25
            wn.update()
            time.sleep(1/30)
         b.hideturtle()
         ex.hideturtle()
         min1.hideturtle()
         min2.hideturtle()
         b.hideturtle()
         if level != 4:
            end_time = time.time()
            timer = float(int((end_time - start_time)*100))/100
            gpen.write("You win!\nYour time: " + str(timer), font = ("Courier", 20, "normal"))
            try:
               lb.add_leaderboard_entry("b1 time", timer)
            except Exception:
               pass
            if maxLevel == 1:
               maxLevel = 2
               file = open("LevelUnlock.txt", "wt")
               file.write(str(maxLevel))
               file.close()
         wn.update()
      #you lose
      else:
         c.fillcolor("white")
         ex.hideturtle()
         wn.update()
         gpen.write("You lose.", font = ("Courier", 20, "normal"))
         wn.update()

      time.sleep(1)

      if level != 4 or youWin == False:
         endScreen()

      reset()

      #reset boss health stuff
      b.hideturtle()
      bossHP = 80

      #reset boss
      b.goto(0, 500)
      b.shapesize(stretch_wid = 9, stretch_len = 9)
      b.hideturtle()
      b.pencolor("white")
      #reset boss attack 1
      ast = 0
      cooldown = 50
      vibrate = False
      atk1 = False
      #reset boss attack 2
      atk2 = False
      ex.hideturtle()
      exY = 10
      exX = 10
      exWid = 1
      exLen = 1
      #reset boss attack 3
      atk3 = False
      min1.hideturtle()
      min1R = False
      min1L = False
      min2.hideturtle()
      min2R = False
      min2L = False
      min2lives = 3
      min1lives = 3

      #reset game end
      gpen.clear()
      bossDie = 9
      
      wn.update()

      if endGame:
         level = 0
         break
      if level == 4:
         break
   
   if lives == 0 and level == 4:
      level = 0
      reset()
      level = 4
      continue

   elif lives == 0:
      reset()
      
   while level == 2 or level == 4:
      startThings(b2)
      b2.sety(-200)
      
      #begin scene thing
      unableToMove = True
      b2size = 1
      for i in range(6):
         b2size += 1
         b2.shapesize(stretch_wid = b2size, stretch_len = b2size)
         b2.sety(b2.ycor() + 5)
         wn.update()
         time.sleep(1/30)
      b2.fillcolor("purple")
      wn.update()
      time.sleep(1/30)
      b2.hideturtle()
      wn.update()
      time.sleep(1/30)
      b2.setx(500)
      wn.update()
      time.sleep(1/30)
      b2.showturtle()
      wn.update()
      time.sleep(1/30)
      b2.fillcolor("black")
      wn.update()
      time.sleep(1/30)
      
      #pen1
      p1.penup()
      p1.hideturtle()
      p1.goto (-200, 200)
      p1.pensize(7)

      #pen3
      p3.penup()
      p3.hideturtle()
      p3.color("white")

      #life bar animation
      p1.speed(0)
      p1.pencolor("green")
      p1.pendown()
      for i in range(20):
         p1.forward(20)
         wn.update()
         time.sleep(1/30)
      p1.penup()
      p1.goto(0, 200)
      p1.pendown()
      p1.color("yellow")

      p3.goto(-75, 215)
      p3.write("The Acute Killer", font = ("Courier", 12, "normal"))
      p3.goto(100, 200)
      p3.color("red")
      p3.pendown()

      #pen2
      p2.penup()
      p2.hideturtle()
      p2.goto (-200, 200)
      p2.pencolor("white")
      p2.pendown()

      if(level != 4):
         start_time = time.time()
      

      unableToMove = False
      #main loop
      loops = 0

      while True:
         wn.update()
         time.sleep(1/30)

         hurtBoss2()
         if b2atk1 == False:
            boss2teleport()
         jump_timer()
         joy_inputs(pygame.event.poll())
         projectile_movement()

         if b2atk2:
            b2attack2()

         if cooldown > 0:
            cooldown -= 1
         elif cooldown == 0:
            ran = r.randint(1, 2)
            if ran == 2 and not b2atk2:
               b2attack2()
            else:
               b2attack() 

         invinciblePLSBlink(hurt)
         lifeLoss()

         loops += 1

         if boss2HP == 20:
            break
         lose = False
         if lives <= 0:
            youWin = False
            unableToMove = True
            lose = True
            break

      if not lose:
         unableToMove = True
         ast = 0
         t1mt = 0
         cooldown = 50
         b2atk1 = False
         b2atk2 = False
         tri1.goto(1000, 1000)
         tri1.fillcolor("black")
         b2.fillcolor("purple")
         wn.update()
         time.sleep(1/30)
         if c.xcor() <= 0:
            b2.setx(500)
            wn.update()
            time.sleep(1/30)
            b2.fillcolor("black")
            wn.update()
            time.sleep(1/30)
            time.sleep(1/2)
            trip1.goto(465, -190)
            trip2.goto(535, -190)
            trip3.goto(500, -170)
            trip4.goto(500, -130)
         else:
            b2.setx(-500)
            wn.update()
            time.sleep(1/30)
            b2.fillcolor("black")
            wn.update()
            time.sleep(1/30)
            trip1.goto(-465, -190)
            trip2.goto(-535, -190)
            trip3.goto(-500, -170)
            trip4.goto(-500, -130)
         trip1.showturtle()
         trip2.showturtle()
         trip3.showturtle()
         trip4.showturtle()
         b2.goto(1000, 1000)
         b2.hideturtle()
         wn.update()
         time.sleep(1/3)
         dist1x, dist2x, dist3x, dist4x = (spot1x - trip1.xcor()) / 60, (spot2x - trip2.xcor()) / 60, (spot3x - trip3.xcor()) / 60, (spot4x - trip4.xcor()) / 60
         dist1y, dist2y, dist3y, dist4y = (spot1y - trip1.ycor()) / 60, (spot2y - trip2.ycor()) / 60, (spot3y - trip3.ycor()) / 60, (spot4y - trip4.ycor()) / 60
         for i in range(60):
            trip1.goto(trip1.xcor() + dist1x, trip1.ycor() + dist1y)
            trip2.goto(trip2.xcor() + dist2x, trip2.ycor() + dist2y)
            trip3.goto(trip3.xcor() + dist3x, trip3.ycor() + dist3y)
            trip4.goto(trip4.xcor() + dist4x, trip4.ycor() + dist4y)
            trip1.left(3)
            trip2.left(3)
            trip4.left(3)
            wn.update()
            time.sleep(1/30)
         unableToMove = False

      while True:
         if lose:
            break
         wn.update()
         time.sleep(1/30)

         jump_timer()
         joy_inputs(pygame.event.poll())
         projectile_movement()

         if s2b2atk2:
            tripatk2()
         if s2b2atk1:
            tripatk1()

         if cooldown > 0:
            cooldown -= 1
         elif cooldown == 0:
            if r.randint(1, 2) == 1 and (s2b2atk1 == False and s2b2atk2 == False):
               tripatk1()
            elif s2b2atk1 == False and s2b2atk2 == False:
               tripatk2()

         invinciblePLSBlink(s2b2hurt)
         lifeLoss()
         hurttrip()

         loops += 1

         if lives <= 0:
            youWin = False
            unableToMove = True
            lose = True
            break
         if boss2HP == 8:
            break
            lose = False
      if not lose:
         unableToMove = True
         ast = 0
         t1mt = 0
         cx = 0
         facing = 0
         s2b2atk1 = False
         s2b2atk2 = False
         cooldown = 50
         trip1.showturtle()
         trip2.showturtle()
         trip3.showturtle()
         trip4.showturtle()
         trip1.goto(-35, -190)
         trip1.left(180)
         wn.update()
         time.sleep(1/30)
         trip2.goto(35, -190)
         trip2.left(180)
         wn.update()
         time.sleep(1/30)
         trip4.goto(0, -130)
         trip4.left(180)
         wn.update()
         time.sleep(1/30)
         trip3.goto(0, -170)
         wn.update()
         time.sleep(1/30)
         b2.goto(0, -170)
         b2.showturtle()
         b2.pencolor("white")
         trip1.hideturtle()
         trip1.goto(1000, 1000)
         trip2.hideturtle()
         trip2.goto(1000, 1000)
         trip3.hideturtle()
         trip3.goto(1000, 1000)
         trip4.hideturtle()
         trip4.goto(1000, 1000)
         b2.pencolor("pink")
         hurt()
         lifeLoss()
         wn.update()
         time.sleep(1/2)
         unableToMove = False
      #main loop
      while True:
         wn.update()
         time.sleep(1/30)

         if boss2HP <= 0:
            youWin = True
            lose = False
            unableToMove = True
            beam.clear()
            energy.clear()
            blast.clear()
            break
         if lives <= 0:
            youWin = False
            unabletomove = True
            lose = True
            break

         invinciblePLSBlink(s3b2hurt, hurt)
         
         lifeLoss()

         if shieldDown > 0:
            b2.pencolor("white")
            shieldDown -= 1
         hurtBoss2()
         jump_timer()
         joy_inputs(pygame.event.poll())
         projectile_movement()
         if shieldDown == 0:
            b2.pencolor("pink")

         if cooldown > 0:
            cooldown -= 1
         elif cooldown == 0:
            if r.randint(1, 2) == 1 and (s3b2atk == False and s3b2atk2 == False):
               b2blastatk()
            elif s3b2atk == False and s3b2atk2 == False:
               b2beamatk()

         if s3b2atk:
            b2blastatk()
         elif s3b2atk2:
            b2beamatk()

         
         loops += 1
         

      #you win
      if youWin:
         b2.pencolor("red")
         for i in range(60):
            if i % 2 == 0:
               b2.setx(b2.xcor()-1)
            else:
               b2.setx(b2.xcor()+1)
            wn.update()
            time.sleep(1/30)
         for i in range(15):
            if i == 0 or i == 5 or i == 10:
               bdie1.showturtle()
               bdie1.goto(b2.xcor(), b2.ycor())
            if i == 1 or i == 6 or i == 11:
               bdie2.showturtle()
               bdie2.goto(b2.xcor(), b2.ycor())
            if i == 2 or i == 7 or i == 12:
               bdie3.showturtle()
               bdie3.goto(b2.xcor(), b2.ycor())
            if i == 3 or i == 8 or i == 13:
               bdie4.showturtle()
               bdie4.goto(b2.xcor(), b2.ycor())
            if i == 4 or i == 9 or i == 14:
               bdie5.showturtle()
               bdie5.goto(b2.xcor(), b2.ycor())
            for i in range(10):
               b2.right(6)
               b2.goto(b2.xcor() + 7, b2.ycor() + 4)
               wn.update()
               time.sleep(1/60)
         bdie1.hideturtle()
         wn.update()
         time.sleep(1/4)
         bdie2.hideturtle()
         wn.update()
         time.sleep(1/4)
         bdie3.hideturtle()
         wn.update()
         time.sleep(1/4)
         bdie4.hideturtle()
         wn.update()
         time.sleep(1/4)
         bdie5.hideturtle()
         wn.update()
         time.sleep(1/4)
         b2.hideturtle()
         wn.update()
            
         if level != 4:
            end_time = time.time()
            timer = float(int((end_time - start_time)*100))/100
            gpen.write("You win!\nYour time: " + str(timer), font = ("Courier", 20, "normal"))
            try:
               lb.add_leaderboard_entry("b2 time", timer)
            except Exception:
               pass
            if maxLevel == 2:
               maxLevel = 3
               file = open("LevelUnlock.txt", "wt")
               file.write(str(maxLevel))
               file.close()
         wn.update()
      #you lose
      else:
         c.fillcolor("white")
         gpen.write("You lose.", font = ("Courier", 20, "normal"))
         blast.clear()
         beam.clear()
         wn.update()

      time.sleep(1)

      b2.hideturtle()

      if level != 4 or not youWin:
         endScreen()

      reset()

      #reset boss health stuff
      boss2HP = 40

      #reset boss
      b2.goto(0, 500)
      b2.shapesize(stretch_wid = 7, stretch_len = 7)
      b2.hideturtle()
      b2.pencolor("white")
      b2.setheading(90)
      #reset boss health stuff
      boss2HP = 40
      p1.clear()
      p2.clear()
      p3.clear()
      #reset boss attack 1
      b2atk1 = False
      ast = 0
      cooldown = 50

      #reset tri1
      tri1.goto(1000, 1000)
      tri1.fillcolor("black")
      t1mt = 0
      b2atk2 = False

      #reset trips
      tripl = [trip1, trip2, trip3, trip4]
      for i in range(len(tripl)):
         tripl[i].hideturtle()
         tripl[i].goto(1000, 1000)
         tripl[i].fillcolor("black")
         tripl[i].pencolor("white")
      tripHP1 = 5
      tripHP2 = 5
      tripHP3 = 5
      tripHP4 = 5
      trip1.setheading(90)
      trip2.setheading(90)
      trip3.setheading(270)
      trip4.setheading(90)
      for i in range(len(tripl)):
         tripl[i].tiltangle(0)

      #reset trips atk
      t1mt = 0
      s2b2atk1 = False
      s2b2atk2 = False
      cx = 0
      numFinished = 0
      facing = 0
      launchl = [False, False,  False, False]

      #reset b2 blast
      blast.hideturtle()
      blast.pencolor("pink")
      blastSize = 1
      blast.pensize(blastSize)
      s3b2atk = False

      blast.clear()
      #reset b2 beam
      beam.clear()
      energy.clear()
      energySize = 1
      energy.pensize(energySize)
      hitspot = 300
      s3b2atk2 = False
      shieldDown = 0
      
      #reset game end
      gpen.clear()
      waittoend = 0
      
      wn.update()

      if endGame:
         level = 0
         break
      if level == 4:
         break
   

   if lives == 0 and level == 4:
      level = 0
      reset()
      level = 4
      continue

   elif lives == 0:
      reset()
   
   while level == 3 or level == 4:
      startThings(b3)
      b3.sety(-200)
         
      
      #begin scene thing
      unableToMove = True
      for i in range(70):
         b3.setx(b3.xcor() - 7)
         wn.update()
         time.sleep(1/30)

      #pen1
      p1.penup()
      p1.hideturtle()
      p1.goto (-200, 200)
      p1.pensize(7)

      #pen3
      p3.penup()
      p3.hideturtle()
      p3.color("white")
      p3.goto(-75, 215)

      #life bar animation
      p1.speed(0)
      p1.pencolor("green")
      p1.pendown()
      for i in range(20):
         p1.forward(20)
         wn.update()
         time.sleep(1/30)
      p1.penup()
      p1.goto(0, 200)
      p1.pendown()
      p1.color("yellow")

      p3.write("Pointless Henry", font = ("Courier", 12, "normal"))
      p3.goto(100, 200)
      p3.color("red")
      p3.pendown()

      #pen2
      p2.penup()
      p2.hideturtle()
      p2.goto (-200, 200)
      p2.pencolor("white")
      p2.pendown()

      if(level != 4):
         start_time = time.time()

      unableToMove = False
      #main loop
      loops = 0
      while True:
          wn.update()
          time.sleep(1/30)

          hurtb3()
          jump_timer()
          joy_inputs(pygame.event.poll())
          projectile_movement()
          b3move()

          invinciblePLSBlink(b3hurt)
            
          lifeLoss()
                
          loops += 1

          if boss3HP == 0:
             unableToMove = True
             break
          lose = False
          if lives <= 0:
             youWin = False
             unableToMove = True
             lose = True
             break

      if not lose:
         
         if c.xcor() > b3.xcor():
            
            b3.fillcolor("red")
            for i in range(5):
               x = b3.xcor()
               x -= 17
               y = b3.ycor()
               y += 5
               b3.goto(x, y)
               wn.update()
               time.sleep(1/30)
            for i in range(5):
               x = b3.xcor()
               x -= 17
               y = b3.ycor()
               y -= 5
               b3.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            b3.fillcolor("red")
            for i in range(5):
               x = b3.xcor()
               x += 17
               y = b3.ycor()
               y += 5
               b3.goto(x, y)
               wn.update()
               time.sleep(1/30)
            for i in range(5):
               x = b3.xcor()
               x += 17
               y = b3.ycor()
               y -= 5
               b3.goto(x, y)
               wn.update()
               time.sleep(1/30)
         b3.pencolor("white")
         for i in range(56):
            if i % 8 == 0:
               b3.fillcolor("red")
            elif i % 4 == 0:
               b3.fillcolor("black")
            wn.update()
            time.sleep(1/30)
         p1.clear()
         p2.clear()
         p3.clear()
         boss3HP = 200

         b3size = 1
         for i in range(96):
            b3size += 0.125
            b3.shapesize(stretch_wid = b3size, stretch_len = b3size)
            b3.sety(b3.ycor() + 1.25)
            wn.update()
            time.sleep(1/30)
            if i % 8 == 0:
               b3.fillcolor("red")
            elif i % 4 == 0:
               b3.fillcolor("black")
               
         #pen1
         p1.penup()
         p1.hideturtle()
         p1.goto (-400, 200)
         p1.pensize(7)

         #pen3
         p3.penup()
         p3.hideturtle()
         p3.color("white")
         p3.goto(-25, 215)

         #life bar animation
         p1.speed(0)
         p1.pencolor("green")
         p1.pendown()
         for i in range(40):
            p1.forward(20)
            wn.update()
            time.sleep(1/30)
         p1.penup()
         p1.goto(0, 200)
         p1.pendown()
         p1.color("yellow")

         p3.write("Henry", font = ("Courier", 12, "normal"))
         p3.goto(200, 200)
         p3.color("red")
         p3.pendown()

         #pen2
         p2.penup()
         p2.hideturtle()
         p2.goto (-400, 200)
         p2.pencolor("white")
         p2.pendown()
         wn.update()

         while b3.ycor() > -80:
            b3.sety(b3.ycor() - 10)
            time.sleep(1/30)
            wn.update()
      
         unableToMove = False

         cooldown = 75
         
      while True:
          wn.update()
          time.sleep(1/30)

          if boss3HP == 0:
             unableToMove = True
             break
          lose = False
          if lives <= 0:
             youWin = False
             unableToMove = True
             lose = True
             break
            
          hurtb3s2()
          jump_timer()
          joy_inputs(pygame.event.poll())
          projectile_movement()
          if s2b3atk:
             b3s2atk()
          elif s2b3atk2:
             b3s2atk2()
          elif s2b3atk50p:
             b3s2atk50p()
          if cooldown == 0 and not s2b3atk50p:
             if r.randint(1, 2) == 1 and (s2b3atk == False and s2b3atk2 == False):
                b3s2atk()
             elif s2b3atk == False and s2b3atk2 == False:
                b3s2atk2()             
          elif cooldown > 0:
             cooldown -= 1
          

          invinciblePLSBlink(b3s2hurt)
            
          lifeLoss()
                
          loops += 1

      if not lose:

         b3size -= 3
         b3.shapesize(stretch_wid = b3size, stretch_len = b3size)
         b3.sety(b3.ycor() - 10)
         wn.update()
         time.sleep(1/30)

         if c.xcor() > b3.xcor():
            b3.fillcolor("red")
            for i in range(5):
               x = b3.xcor()
               x -= 17
               y = b3.ycor()
               y += 5
               b3.goto(x, y)
               wn.update()
               time.sleep(1/30)
            for i in range(5):
               x = b3.xcor()
               x -= 17
               y = b3.ycor()
               y -= 5
               b3.goto(x, y)
               wn.update()
               time.sleep(1/30)
         else:
            b3.fillcolor("red")
            for i in range(5):
               x = b3.xcor()
               x += 17
               y = b3.ycor()
               y += 5
               b3.goto(x, y)
               wn.update()
               time.sleep(1/30)
            for i in range(5):
               x = b3.xcor()
               x += 17
               y = b3.ycor()
               y -= 5
               b3.goto(x, y)
               wn.update()
               time.sleep(1/30)
         b3.pencolor("white")
         b3.fillcolor("black")
         b3.sety(b3.ycor() - 2)
         wn.update()
         time.sleep(1/30)
         p1.clear()
         p2.clear()
         p3.clear()
         boss3HP = 50

         while b3.ycor() < 100:
            b3.sety(b3.ycor() + 4)
            time.sleep(1/30)
            wn.update()
         
         #pen1
         p1.penup()
         p1.hideturtle()
         p1.goto (-300, 200)
         p1.pensize(7)

         #pen3
         p3.penup()
         p3.hideturtle()
         p3.color("white")
         p3.goto(-40, 215)

         #life bar animation
         p1.speed(0)
         p1.pencolor("green")
         p1.pendown()
         for i in range(40):
            p1.forward(15)
            wn.update()
            time.sleep(1/30)
         p1.penup()
         p1.goto(0, 200)
         p1.pendown()
         p1.color("yellow")

         p3.write("High Henry", font = ("Courier", 12, "normal"))
         p3.goto(156, 200)
         p3.color("red")
         p3.pendown()

         #pen2
         p2.penup()
         p2.hideturtle()
         p2.goto (-300, 200)
         p2.pencolor("white")
         p2.pendown()
         wn.update()
      
         unableToMove = False

         cooldown = 75

         ast = 0

         while True:
             wn.update()
             time.sleep(1/30)

             if boss3HP == 0:
                unableToMove = True
                break
             lose = False
             if lives <= 0:
                youWin = False
                unableToMove = True
                lose = True
                break

             
             hurtb3s3()
             jump_timer()
             joy_inputs(pygame.event.poll())
             projectile_movement()
             
             if s3b3atk:
                b3s3atk()
             elif s3b3atk2:
                b3s3atk2()
             else:
                b3s3move()
                if cooldownpassive == 0 and not shooting:
                   b3shoot()
                elif not shooting:
                   cooldownpassive -= 1
             if cooldown == 0  and (s3b3atk == False and s3b3atk2 == False):
                if r.randint(1, 2) == 1:
                   b3s3atk()
                else:
                   b3s3atk2()
             elif cooldown > 0:
                cooldown -= 1

             if shooting:
                b3shoot()
             
             moveHenries()
             
             

             invinciblePLSBlink(b3s3hurt, checkallforhurt)
               
             lifeLoss()
                   
             loops += 1

      for h in HenryClone.henries:
         h.reset()
      gg = r.randint(1, 5)
      if not lose:
         if gg != 1: #True Henry
            for i in range(39):
               b3size -= 0.25
               b3.shapesize(stretch_wid = b3size, stretch_len = b3size)
               if i % 8 == 0:
                  b3.fillcolor("red")
               elif i % 4 == 0:
                  b3.fillcolor("black")
               wn.update()
               time.sleep(1/30)
            for i in range(40):
               if i % 4 == 0:
                  b3.fillcolor("red")
                  b3size -= 0.5
                  b3.shapesize(stretch_wid = b3size, stretch_len = b3size)
               elif i % 2 == 0:
                  b3.fillcolor("black")
                  b3size += 0.5
                  b3.shapesize(stretch_wid = b3size, stretch_len = b3size)
               wn.update()
               time.sleep(1/30)
            b3size += 0.25
            b3.fillcolor("black")
            for i in range(13):
               b3size += 0.5
               b3.shapesize(stretch_wid = b3size, stretch_len = b3size)
               wn.update()
               time.sleep(1/30)

            for i in range(1, 31):
               shieldPen.setheading(0)
               shieldPen.goto(b3.xcor(), b3.ycor() - 150)
               shieldPen.circle(150, displaceShield)
               shieldPen.clear()
               shieldPen.pendown()
               shieldPen.circle(150, i * 6)
               shieldPen.penup()
               wn.update()
               time.sleep(1/30)

            b3.pencolor("white")
            b3.fillcolor("black")
            wn.update()
            time.sleep(1/30)
            p1.clear()
            p2.clear()
            p3.clear()
            boss3HP = 50

            while b3.ycor() < 100:
               b3.sety(b3.ycor() + 4)
               time.sleep(1/30)
               wn.update()
            
            #pen1
            p1.penup()
            p1.hideturtle()
            p1.goto (-300, 200)
            p1.pensize(7)

            #pen3
            p3.penup()
            p3.hideturtle()
            p3.color("white")
            p3.goto(-40, 215)

            #life bar animation
            p1.speed(0)
            p1.pencolor("green")
            p1.pendown()
            for i in range(40):
               p1.forward(15)
               wn.update()
               time.sleep(1/30)
            p1.penup()
            p1.goto(0, 200)
            p1.pendown()
            p1.color("yellow")

            p3.write("True Henry", font = ("Courier", 12, "normal"))
            p3.goto(156, 200)
            p3.color("red")
            p3.pendown()

            #pen2
            p2.penup()
            p2.hideturtle()
            p2.goto (-300, 200)
            p2.pencolor("white")
            p2.pendown()
            wn.update()
         
            unableToMove = False

            cooldown = 75

            ast = 0
            
            while True:
                wn.update()
                time.sleep(1/30)

                if boss3HP == 0:
                   unableToMove = True
                   youWin = True
                   break
                lose = False
                if lives <= 0:
                   youWin = False
                   unableToMove = True
                   lose = True
                   break

                passiveShield()
                hurtb3s4()
                jump_timer()
                joy_inputs(pygame.event.poll())
                projectile_movement()

                
                
                if s3b3atk:
                   b3s3atk()
                elif s3b3atk2:
                   b3s3atk2()
                elif s2b3atk2:
                   s4s2atk2()
                elif s2b3atk:
                   s4s2atk()
                else:
                   b3s3move()
                   if cooldownpassive == 0 and not shooting:
                      b3shoot()
                   elif not shooting:
                      cooldownpassive -= 1
                if cooldown == 0  and not attacking:
                   b3s4attacks[r.randint(0, 3)]()
                elif cooldown > 0:
                   cooldown -= 1
                   
                

                if shooting:
                   b3shoot()
                
                moveHenries()
                
                

                invinciblePLSBlink(b3s4hurt, checkallforhurt)
                  
                lifeLoss()
                      
                loops += 1

         else: #Biblically Accurate Henry
            shotPen.clear()
            for i in range(39):
               b3size -= 0.25
               b3.shapesize(stretch_wid = b3size, stretch_len = b3size)
               if i % 8 == 0:
                  b3.fillcolor("red")
               elif i % 4 == 0:
                  b3.fillcolor("black")
               wn.update()
               time.sleep(1/30)
            if lives == 1:
               choose = life1
            elif lives == 2:
               choose = life2
            else:
               choose = life3 
            dist = choose.xcor() - b3.xcor()
            di = choose.ycor() - b3.ycor()
            for i in range(60):
               choose.setx(choose.xcor() - dist/60)
               choose.sety(choose.ycor() - di/60)
               wn.update()
               time.sleep(1/30)

            lives -= 1
            lifeLoss()
            wn.update()
            time.sleep(1/30)
            b3.hideturtle()
            wn.update()
            time.sleep(0.25)
            b3.showturtle()
            b3.color("white")

            b3size = 0

            for i in range(4):
               b3size += 50
               b3.shapesize(stretch_wid = b3size, stretch_len = b3size)
               wn.update()
               time.sleep(1/30)

            time.sleep(0.5)
            b3size = 1
            b3.shape("henry")
            b3.shapesize(b3size, b3size)
            wn.update()
            time.sleep(0.125)

            '''if lives == 1:
               choose = life1
            elif lives == 2:
               choose = life2
            else:
               choose = life3 

            dist = choose.xcor() - b3.xcor()
            di = choose.ycor() - b3.ycor()
            for i in range(60):
               choose.setx(choose.xcor() - dist/60)
               choose.sety(choose.ycor() - di/60)
               wn.update()
               time.sleep(1/30)

            lives -= 1
            lifeLoss()'''
                  

            b3.pencolor("white")
            b3.fillcolor("black")
            wn.update()
            time.sleep(1/30)
            p1.clear()
            p2.clear()
            p3.clear()
            boss3HP = 60

            while b3.ycor() < 100:
               b3.sety(b3.ycor() + 4)
               time.sleep(1/30)
               wn.update()
            
            #pen1
            p1.penup()
            p1.hideturtle()
            p1.goto (-300, 200)
            p1.pensize(7)

            #pen3
            p3.penup()
            p3.hideturtle()
            p3.color("white")
            p3.goto(-115, 215)

            #life bar animation
            p1.speed(0)
            p1.pencolor("green")
            p1.pendown()
            for i in range(40):
               p1.forward(15)
               wn.update()
               time.sleep(1/30)
            p1.penup()
            p1.goto(0, 200)
            p1.pendown()
            p1.color("yellow")

            p3.write("Biblically Accurate Henry", font = ("Courier", 12, "normal"))
            p3.goto(150, 200)
            p3.color("red")
            p3.pendown()

            #pen2
            p2.penup()
            p2.hideturtle()
            p2.goto (-300, 200)
            p2.pencolor("white")
            p2.pendown()
            wn.update()
         
            unableToMove = False

            cooldown = 75

            ast = 0

            while True:
                wn.update()
                time.sleep(1/30)

                if boss3HP == 0:
                   unableToMove = True
                   youWin = True
                   break
                lose = False
                if lives <= 0:
                   youWin = False
                   unableToMove = True
                   lose = True
                   break

                breathe()
                hurtb3s5()
                jump_timer()
                joy_inputs(pygame.event.poll())
                projectile_movement()
                
                if s3b3atk:
                   b3s3atk()
                elif s3b3atk2:
                   b3s3atk2()
                elif s2b3atk2:
                   s4s2atk2()
                elif s2b3atk:
                   b3s5atk2()
                elif s5b3atk:
                   b3s5atk()
                elif atk2:
                   b3s5atk3()
                else:
                   b3s3move()
                   if cooldownpassive == 0 and not shooting:
                      b3shoot()
                   elif not shooting:
                      cooldownpassive -= 1
                if cooldown <= 0  and not attacking:
                   b3s5attacks[r.randint(0, 5)]()
                elif cooldown > 0:
                   cooldown -= 2
                
                   
                

                if shooting:
                   b3s5shoot()
                
                moveHenries()
                
                

                invinciblePLSBlink(b3s5hurt, combine, hurtByEx)
                  
                lifeLoss()
                      
                loops += 1

      #you win
      if youWin:
         
         if maxLevel == 3:
            maxLevel = 4
            file = open("LevelUnlock.txt", "wt")
            file.write(str(maxLevel))
            file.close()
         elif level == 4 and maxLevel == 4:
            maxLevel = 5
            file = open("LevelUnlock.txt", "wt")
            file.write(str(maxLevel))
            file.close()
         shotPen.clear()
         for h in HenryClone.henries:
            h.reset()
         wn.update()
         if gg != 1:
            b3.fillcolor("red")
            for i in range(16):
               b3.shapesize(7 - i * 0.25, 7 - i * 0.25)
               wn.update()
               time.sleep(1/30)
            for i in range(15):
               HenryClone.henries[i].thing.showturtle()
               HenryClone.henries[i].thing.fillcolor("red")
               HenryClone.henries[i].thing.goto(b3.xcor(), b3.ycor())
               HenryClone.henries[i].thing.setheading(i * 24)
               HenryClone.henries[i].thing.forward(50)
            b3.hideturtle()
            for i in range(10):
               for h in HenryClone.henries:
                  h.thing.forward(80)
               wn.update()
               time.sleep(1/30)
            for h in HenryClone.henries:
               HenryClone.henries[i].thing.fillcolor("black")
               h.reset()
         else:
            b3.shape("henry")
            c.fillcolor("black")
            wn.update()
            time.sleep(1/30)
            di = c.xcor()
            for i in range(60):
               c.sety(c.ycor() + 1)
               c.setx(c.xcor() - di/60)
               b3s3move()
               wn.update()
               time.sleep(1/30)
            thing.penup()
            thing.goto(b3.xcor(), b3.ycor())
            thing.setheading(0)
            thing.pendown()
            thing.pencolor("white")
            b3.hideturtle()
            for i in range(55):
               thing.circle(50, 360)
               thing.setheading(i * 10)
            thing.pencolor("black")
            thing.pensize(20)
            for i in range(60):
               endPen.clear()
               thing.penup()
               endPen.penup()
               endPen.goto(c.xcor(), c.ycor())
               thing.goto(c.xcor(), c.ycor())
               endPen.pendown()
               thing.pendown()
               endPen.setheading(i * 2 + 30)
               thing.setheading(i * 2 + 30)
               endPen.forward(1000)
               wn.update()
               thing.forward(1000)
               wn.update()
               time.sleep(1/30)
            endPen.clear()
            thing.clear()
            for i in range(6):
               c.sety(c.ycor() - 10)
               wn.update()
               time.sleep(1/30)
            time.sleep(0.125)
            
               
         b3.hideturtle()
         wn.update()
         end_time = time.time()
         timer = float(int((end_time - start_time)*100))/100
         gpen.write("  You win!\nYour time: " + str(timer), font = ("Courier", 20, "normal"))
         try:
            if(level == 3):
               lb.add_leaderboard_entry("b3 time", timer)
            elif(level == 4):
               lb.add_leaderboard_entry("b4 time", timer)
         except Exception:
            pass            

         wn.update()
      #you lose
      else:
         c.fillcolor("white")
         gpen.write("You lose.", font = ("Courier", 20, "normal"))
         wn.update()

      time.sleep(1)

      b3.hideturtle()

      shieldPen.clear()
      wn.update()
      for h in HenryClone.henries:
         h.reset()
      for shot in s5projectile.shots:
         shot.reset()
      ex.hideturtle()

      endScreen()

      reset()

      #reset boss
      b3.goto(1000, -200)
      b3.shapesize(stretch_wid = 1, stretch_len = 1)
      b3size = 1
      b3.hideturtle()
      b3.pencolor("white")
      b3.fillcolor("black")
      #reset boss health stuff
      boss3HP = 20
      #reset boss attack and s1 movement
      ast = 0
      cooldown = 50
      vibrate = False
      b3up = False
      #reset boss attack 1
      s2b3atk = False
      b3up = False
      b3down = False
      b3downCount = 0
      heightCount = 0
      jumptimes = 0
      atksleft = 0
      #reset boss attack 2
      s2b3atk2 = False
      shieldPen.penup()
      shieldPen.goto(1000, 1000)
      shieldAmount = 6
      angle = 270
      shieldPen.clear()

      #reset boss attack 3
      s2b3atk50p = False
      armorList = ["white", "orange", "yellow", "green2", "LightSkyBlue", "MediumOrchid1", "HotPink1"]
      armorLevel = 6
      shieldJump = False

      #reset boss attack 4
      
      s3b3atk = False
      henryNum = 0
      #moveThem = False
      
      #reset boss attack 5 & passive
      s3b3atk2 = False
      offset = 0
      tarpos = 0
      bosspos = 0
      shotPen.clear()
      shotx = 0
      shoty = 0
      astpassive = 0
      cooldownpassive = 0

      #s4 resets
      attacking = False

      #s5 resets
      b3.shape("circle")
      s5b3atk = False
      for shot in s5projectile.shots:
         shot.reset()
      life1.goto(-500, 150)
      life2.goto(-475, 150)
      life3.goto(-450, 150)
      t1mt = 0
      r5 = 100
      b3.clear()
      ast = 0
      atk2 = False
      attacking = False
      exWid = 1
      exLen = 1
      exY = 10
      exX = 10
      ex.shapesize(stretch_wid = exWid, stretch_len = exLen)
      
      
      #reset game end
      gpen.clear()
      
      
      wn.update()

      if endGame:
         level = 0
         reset()
         break
      if level == 4:
         level = 0
         reset()
         level = 4
         break

   endGame = False

   if lives == 0 and level == 4:
      level = 0
      reset()
      level = 4

   elif lives == 0:
      reset()

    
