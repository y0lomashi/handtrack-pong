import pygame
import random
import cv2
import mediapipe as mp
import threading

import settings as s


def update_fps():
    # *function to display fps counter
    # settting font for fps counter
    font = pygame.font.SysFont("Arial", 18)
    # finding fps amount
    fps = str(int(clock.get_fps()))
    # creating fps text
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def p1_handle_event(event):
    # managing events with computer player
    global p1_move_up, p1_move_down

    if event.type == pygame.KEYDOWN:
        if event.key == P1_UP:
            p1_move_up = True
            p1_move_down = False
        elif event.key == P1_DOWN:
            p1_move_down = True
            p1_move_up = False
    elif event.type == pygame.KEYUP:
        if event.key == P1_UP:
            p1_move_up = False
        elif event.key == P1_DOWN:
            p1_move_down = False


def p1_update():
    # do nothing
    pass


def human_handle_event(event):
    # handling events with human player
    global p2_move_up, p2_move_down

    if event.type == pygame.KEYDOWN:
        if event.key == P2_UP:
            p2_move_up = True
            p2_move_down = False
        elif event.key == P2_DOWN:
            p2_move_down = True
            p2_move_up = False
    elif event.type == pygame.KEYUP:
        if event.key == P2_UP:
            p2_move_up = False
        elif event.key == P2_DOWN:
            p2_move_down = False


def human_update():
    # do nothing
    pass


def random_handle_event(event):
    # do nothing
    pass


def random_update():
    # computer moves randomly
    global p2_move_up, p2_move_down
    move = random.randint(1, 2)

    if move == 1:  # up
        p2_move_up = True
        p2_move_down = False
    elif move == 2:  # down
        p2_move_up = False
        p2_move_down = True
    else:  # stop
        p2_move_up = False
        p2_move_down = False


def following_handle_event(event):
    # do nothing
    pass


def following_update():
    # computer follows position of ball
    global p2_move_up, p2_move_down

    if ball_y < p2_pad_y + 50:
        p2_move_up = True
        p2_move_down = False
    elif ball_y > p2_pad_y + 50:
        p2_move_up = False
        p2_move_down = True
    else:  # stop
        p2_move_up = False
        p2_move_down = False


# * --- main ---

# initialize game
pygame.init()

# setup display
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 1000, 720
screen = pygame.display.set_mode(DISPLAY_SIZE)

# set window caption
pygame.display.set_caption("Handtracking Pong by Curtis Li")

# clock
clock = pygame.time.Clock()

# hide cursor
pygame.mouse.set_visible(False)

# buttons
P1_UP = pygame.K_w
P1_DOWN = pygame.K_s
P2_UP = pygame.K_UP
P2_DOWN = pygame.K_DOWN

# other constants
PLAYER_PAD_LENGTH = 100
PLAYER_PAD_SPEED = 7.5
PLAYER_PAD_WIDTH = 10
BALL_RADIUS = 6

# player scores
p1_score = 0
p2_score = 0

# ball speed is split into x and y axis
ball_speed_x = 7.5
ball_speed_y = 7.5

# ball coordinates
ball_x = 400
ball_y = 300

# player pad y's
p1_pad_y = 300
p2_pad_y = 300

# player move flags
p1_move_up = False
p1_move_down = False
p2_move_up = False
p2_move_down = False

# computer's playing mode
if s.p2_type == "random":
    # computer will simulate random movements
    p2_handle_event = random_handle_event
    p2_update = random_update
elif s.p2_type == "following":
    # computer will follow ball's position
    p2_handle_event = following_handle_event
    p2_update = following_update
elif s.p2_type == "human":
    # human will click keys
    p2_handle_event = human_handle_event
    p2_update = human_update

# Global variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
# For webcam input:
cap = cv2.VideoCapture(0)
# Set fps
cap.set(cv2.CAP_PROP_FPS, 30)
cfps = int(cap.get(cv2.CAP_PROP_FPS))
# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Handtracking position variables
left_y = 0
right_y = 0
position = [0, 0, 0]


def fullTrack(postition):
    """
    This function is used to track the hand and draw the landmarks on the
    screen.
    """
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
                if len(results.multi_handedness) > 1:
                    # * Hand point is 9
                    # AKA .landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                    hand1 = results.multi_hand_landmarks[
                        0].landmark[9]
                    hand2 = results.multi_hand_landmarks[
                        1].landmark[9]

                    # Getting y coordinates of the hand points
                    if hand1.x > hand2.x:
                        postition[0] = hand1.y * image_height
                        postition[1] = hand2.y * image_height
                    else:
                        postition[0] = hand2.y * image_height
                        position[1] = hand1.y * image_height
                else:
                    hand1 = results.multi_hand_landmarks[0].landmark[9]
                    # Getting y coordinates of the hand points
                    position[0] = hand1.y * image_height

                for hand_landmarks in results.multi_hand_landmarks:
                    # Drawing landmarks on the screen
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            # Flip the image horizontally for a selfie-view display.
            position[2] = image
        cap.release()

#* Multithreading used to improve performance of the program
# Start the thread
thread = threading.Thread(target=fullTrack, args=(position, ))
thread.start()

# * --- game logic ---
while True:
    left_y = position[0]
    right_y = position[1]
    # keydowns and keyups raise and lower player paddles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            exit()
        # get players keys
        p1_handle_event(event)
        p2_handle_event(event)

    # get other changes
    p1_update()
    p2_update()

    # move player pads to hand position
    if left_y < p1_pad_y - 20:
        p1_move_up = True
        p1_move_down = False
    elif left_y > p1_pad_y + 20:
        p1_move_up = False
        p1_move_down = True
    else:  # stop
        p1_move_up = False
        p1_move_down = False
    # move player pads to key press
    if p1_move_up:
        p1_pad_y -= PLAYER_PAD_SPEED
        if p1_pad_y < 0:
            p1_pad_y = 0
    elif p1_move_down:
        p1_pad_y += PLAYER_PAD_SPEED
        if p1_pad_y > DISPLAY_HEIGHT - PLAYER_PAD_LENGTH:
            p1_pad_y = DISPLAY_HEIGHT - PLAYER_PAD_LENGTH
    # move player pads to hand position
    if right_y < p2_pad_y - 20:
        p2_move_up = True
        p2_move_down = False
    elif right_y > p2_pad_y + 20:
        p2_move_up = False
        p2_move_down = True
    else:  # stop
        p2_move_up = False
        p2_move_down = False
    # move player pads to key press
    if p2_move_up:
        p2_pad_y -= PLAYER_PAD_SPEED
        if p2_pad_y < 0:
            p2_pad_y = 0
    elif p2_move_down:
        p2_pad_y += PLAYER_PAD_SPEED
        if p2_pad_y > DISPLAY_HEIGHT - PLAYER_PAD_LENGTH:
            p2_pad_y = DISPLAY_HEIGHT - PLAYER_PAD_LENGTH

    # move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # check ball position
    # if out screen vertically, flip ball_speed_y
    if ball_y < 0 or ball_y > DISPLAY_HEIGHT - BALL_RADIUS:
        ball_speed_y = -ball_speed_y

    # if out screen horizontally, check whether player pad is there or not
    # if not, release the ball at the center towards scoring player
    if ball_x < 10:
        if p1_pad_y < ball_y < p1_pad_y + PLAYER_PAD_LENGTH:
            ball_speed_x = -ball_speed_x
        else:
            p2_score += 1
            ball_x = 400
            ball_y = 300
            ball_speed_x = 5
            ball_speed_y = 5
    elif ball_x > DISPLAY_WIDTH-10:
        if p2_pad_y < ball_y < p2_pad_y + PLAYER_PAD_LENGTH:
            ball_speed_x = -ball_speed_x
        else:
            p1_score += 1
            ball_x = 400
            ball_y = 300
            ball_speed_x = -5
            ball_speed_y = -5

    # clear the screen
    screen.fill(pygame.Color(0, 0, 0, 255))

    # draw ball
    pygame.draw.circle(screen, pygame.Color(255, 255, 255, 255),
                       (ball_x, ball_y), BALL_RADIUS)

    # draw P1 pad
    pygame.draw.rect(
        screen,
        pygame.Color(255, 255, 255, 255),
        (0, p1_pad_y, PLAYER_PAD_WIDTH, PLAYER_PAD_LENGTH),
    )

    # draw P2 pad
    pygame.draw.rect(
        screen,
        pygame.Color(255, 255, 255, 255),
        (
            DISPLAY_WIDTH - PLAYER_PAD_WIDTH,
            p2_pad_y,
            PLAYER_PAD_WIDTH,
            PLAYER_PAD_LENGTH,
        ),
    )

    # draw center line
    pygame.draw.rect(
        screen,
        pygame.Color(255, 255, 255, 255),
        (DISPLAY_WIDTH / 2, 0, 1, DISPLAY_HEIGHT),
    )

    # draw player scores
    # create font
    score_font = pygame.font.Font(None, 30)

    # draw p1 score
    p1_score_text = str(p1_score)
    p1_score_render = score_font.render(p1_score_text, 1,
                                        pygame.Color(255, 255, 255, 255))
    screen.blit(p1_score_render, (DISPLAY_WIDTH / 2 - 50, 50))

    # draw p2 score
    p2_score_text = str(p2_score)
    p2_score_render = score_font.render(p2_score_text, 1,
                                        pygame.Color(255, 255, 255, 255))
    screen.blit(p2_score_render, (DISPLAY_WIDTH / 2 + 50, 50))

    # update fps counter
    screen.blit(update_fps(), (10, 0))

    # pygame.display.flip() is called in order to update graphics properly
    pygame.display.flip()

    # tick the clock for certain amount of fps
    clock.tick(60)
    cv2.imshow('MediaPipe Hands', cv2.flip(position[2], 1))
    if cv2.waitKey(5) & 0xFF == 27:
        break
