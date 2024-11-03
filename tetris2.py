#Tetris Game, written in Python 3.6.5
#Version: 1.0
#Date: 26.05.2018

import pygame #version 1.9.3
import random
import math
import sys
import cv2
import mediapipe as mp
from enum import Enum


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Stores the different positions
Direction = Enum('Direction', [('UP', 1), ('DOWN', 2), ('LEFT', 3), ('RIGHT', 4), ('NEUTRAL', 5)])

# Gets the average position
def avg2tuple(points) -> tuple:
  avg_x = 0.0
  avg_y = 0.0
  for point in points:
    avg_x += point[0]
    avg_y += point[1]
  
  avg_x /= len(points)
  avg_y /= len(points)
  
  # print('average x coord: ' + str(avg_x) + ' --- average y coord: ' + str(avg_y))
  return [avg_x, avg_y]

time_ms = 0
palms = []
cap = cv2.VideoCapture(0)
hands=mp_hands.Hands()
print_once = 1 == 1

rTop = 0.25
rBottom = 0.25
rRight = 0.15
rLeft = 0.15

cTop = 0
cBottom = 0
cRight = 0
cLeft = 0

center = [2]
curPos = [2]

currentDirection = Direction.NEUTRAL