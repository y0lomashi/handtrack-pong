
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
    global left_hand, right_hand
    # For webcam input:
    cap = cv2.VideoCapture(0)
    # Set size of webcam window
    cap.set(3, 1280)
    cap.set(4, 720)
    # Set max num of hands detected
    # Set the percentage confidence needed to detect a hand (0-1)
    with mp_hands.Hands(model_complexity=0,
                        max_num_hands=2,
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
                if len(results.multi_handedness) == 2:
                    for i in range(len(results.multi_handedness)):
                        if results.multi_handedness[i].classification[0].label == "Left":
                            # * Hand point is 9
                            # AKA .landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                            left_hand = results.multi_hand_landmarks[i].landmark[9]
                        else:
                            right_hand = results.multi_hand_landmarks[i].landmark[9]
                    # Getting y coordinates of the hand points
                    left_y = left_hand.y * image_height
                    right_y = right_hand.y * image_height
                else:
                    left_hand = results.multi_hand_landmarks[0].landmark[9]
                    # Getting y coordinates of the hand points
                    left_y = left_hand.y * image_height
                
                for hand_landmarks in results.multi_hand_landmarks:                    
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
