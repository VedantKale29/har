import cv2
import mediapipe as mp
import numpy as np

# Initialize mediapipe pose solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Take live camera input for pose detection
cap = cv2.VideoCapture(0)

# Read each frame/image from the capture object
while True:
    ret, img = cap.read()
    # Resize image/frame so we can accommodate it on our screen
    img = cv2.resize(img, (600, 400))

    # Do Pose detection
    results = pose.process(img)

    # Check if pose landmarks are detected
    if results.pose_landmarks:
        # Access specific landmarks (e.g., left shoulder and right shoulder)
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow =  results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]

        # Print the coordinates of the left and right shoulders
        #print("Left Shoulder - X:", left_shoulder.x, "Y:", left_shoulder.y)
        #print("Right Shoulder - X:", right_shoulder.x, "Y:", right_shoulder.y)

        # Add your conditional statements based on landmark positions
        # Example: Check if the left shoulder is above a certain y-coordinate
        if left_shoulder.y < right_elbow.y :
            print("Boom")
        else :
            print("Hi")

    # Draw the detected pose on the original video/live stream
    mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                           mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                           mp_draw.DrawingSpec((255, 0, 255), 2, 2)
                           )

    # Display pose on the original video/live stream
    cv2.imshow("Pose Estimation", img)

    cv2.waitKey(1)
