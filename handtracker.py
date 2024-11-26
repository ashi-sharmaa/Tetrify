#Required things
#1.Mediapipe
#2.OpenCV
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

timems = 0
palms = []
cap = cv2.VideoCapture(0)
hands=mp_hands.Hands()
hands.max_num_hands = 1
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
while timems > -1:
    success, image = cap.read()
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    results = hands.process(image)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

    #renders results
    if results.multi_hand_landmarks:
      #prints to terminal coordinates
      #0, 1, 5, 9, 13, 17
      if timems > 50 and timems < 100: 
        print('Getting avgs')
        palm_indexes = [0, 1, 5, 9, 13, 17]
        palm_coordinates = []
        for hand_landmarks in results.multi_hand_landmarks:
           # Here is getting coordinates
          landmark_index = 0
          arr_index = 0
          for ids, landmrk in enumerate(hand_landmarks.landmark):
              if landmark_index in palm_indexes:
                #add to the list of relevant coordinates
                palm_coordinates.append([landmrk.x, landmrk.y])
                arr_index = arr_index + 1
              landmark_index = landmark_index + 1
        print(palm_coordinates)
        
        palms.append(avg2tuple(palm_coordinates))
        
      if timems == 120:
        print('output pos')
        center = avg2tuple(palms)
        print(center)
        cTop = center[1] - rTop
        cBottom = center[1] + rBottom
        cRight = center[0] + rRight
        cLeft = center[0] - rLeft
        

      if timems > 150:
        palm_indexes = [0, 1, 5, 9, 13, 17]
        palm_coordinates = []
        for hand_landmarks in results.multi_hand_landmarks:
           # Here is getting coordinates
          landmark_index = 0
          arr_index = 0
          for ids, landmrk in enumerate(hand_landmarks.landmark):
              if landmark_index in palm_indexes:
                #add to the list of relevant coordinates
                palm_coordinates.append([landmrk.x, landmrk.y])
                arr_index = arr_index + 1
              landmark_index = landmark_index + 1
        # print(palm_coordinates)
        
        curPos = avg2tuple(palm_coordinates)
        
        if curPos[1] < cTop and currentDirection != Direction.UP: 
          print('Top')
          currentDirection = Direction.UP
        elif curPos[1] > cBottom and currentDirection != Direction.DOWN: 
          print('Bottom')
          currentDirection = Direction.DOWN
        elif curPos[0] < cLeft and currentDirection != Direction.LEFT: 
          print('Left')
          currentDirection = Direction.LEFT
        elif curPos[0] > cRight and currentDirection != Direction.RIGHT: 
          print('Right')
          currentDirection = Direction.RIGHT
        elif not (curPos[1] < cTop or curPos[1] > cBottom or curPos[0] < cLeft or curPos[0] > cRight):
          #no direction condition is passed
          currentDirection = Direction.NEUTRAL
        
      
      #displays joints
      for hand_landmarks in results.multi_hand_landmarks:                                                                         
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,mp_hands.HAND_CONNECTIONS)
    
    cv2.imshow('MediaPipe Hands', image)
    timems = timems + 1
    if timems < 150:
      print(str(timems))
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

