#Required things
#1.Mediapipe
#2.OpenCV
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Gets the average position
def palmAvg(points):
  avg_x = 0.0
  avg_y = 0.0
  for point in points:
    avg_x += point[0]
    avg_y += point[1]
  
  avg_x /= len(points)
  avg_y /= len(points)
  
  print('average x coord: ' + str(avg_x) + ' --- average y coord: ' + str(avg_y))

def avgPalmPos(palms):
  avg_x = 0.0
  avg_y = 0.0
  for point in palms:
    avg_x += point[0]
    avg_y += point[1]
  
  avg_x /= len(palms)
  avg_y /= len(palms)
  
  print('average x coord: ' + str(avg_x) + ' --- average y coord: ' + str(avg_y))



cap = cv2.VideoCapture(0)
hands=mp_hands.Hands()
print_once = 1 == 1
while cap.isOpened():
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
      if print_once:
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
        
        palmAvg(palm_coordinates)                 


      # for index in palm_indexes:
      #   print(index)
      #   print(results.multi_hand_landmarks[0])
      print_once = 1==0

      #displays joints
      for hand_landmarks in results.multi_hand_landmarks:                                                                         
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,mp_hands.HAND_CONNECTIONS)
    
    cv2.imshow('MediaPipe Hands', image)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

