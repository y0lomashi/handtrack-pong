
# ! Test file for handtracking model


import cv2
import mediapipe as mp


# Global variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def fullTrack():
    """
    This function is used to track the hand and draw the landmarks on the
    screen.
    """
    global cx, cy
    # For webcam input:
    cap = cv2.VideoCapture(0)
    # Set size of webcam window
    cap.set(3, 1280)
    cap.set(4, 720)
    # Set max num of hands detected
    # Set the percentage confidence needed to detect a hand (0-1)
    with mp_hands.Hands(model_complexity=0,
                        max_num_hands=1,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not
            # writeable to pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            # *Convert image to pixel measurement
            image_height, image_width, _ = image.shape
            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Getting x,y coordinates of the hand points
                    for ids, landmrk in enumerate(hand_landmarks.landmark):
                        # Changing 0-1 value to x,y pixel values
                        cx, cy = (landmrk.x * image_width, landmrk.y
                                  * image_height)
                        # id 9 is the bottom of the middle finger
                        # (closest to palm)
                        if ids == 9:
                            print(ids, cx, cy)
                    # Drawing landmarks on the screen
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()


fullTrack()
