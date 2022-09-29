import cv2
import mediapipe as mp
import pyautogui
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
def rightclick():
    pyautogui.mouseDown(button='right')
    pyautogui.mouseUp(button='right')
def leftclick():
  pyautogui.mouseDown(button='left')
  pyautogui.mouseUp(button='left')
#def scrolll():


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image,0)
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    imageHeight, imageWidth, _ = image.shape

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:

        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        for point in mp_hands.HandLandmark:
          normalizedLandmark = hand_landmarks.landmark[point]
          pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,normalizedLandmark.y, imageWidth,imageHeight)

        if int((hand_landmarks.landmark[point.THUMB_TIP].x) * 100) == int((hand_landmarks.landmark[point.INDEX_FINGER_MCP].x) * 100):
           rightclick()

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:

        break
cap.release()
