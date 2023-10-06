import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize mediapipe pose solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Take live camera input for pose detection
cap = cv2.VideoCapture(0)

# Set the desired frame rate (e.g., 2 frames per second)
frame_rate = 2  # Adjust as needed

# Threshold for crouch detection (adjust as needed)
crouch_threshold = 0.1  # You may need to fine-tune this value

# Threshold for choking detection (adjust as needed)
choking_threshold = 0.2  # You may need to fine-tune this value

# Number of frames to use for smoothing knee movement
smooth_window = 5
left_knee_buffer = [0] * smooth_window
right_knee_buffer = [0] * smooth_window

while True:
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.resize(img, (600, 400))

    results = pose.process(img)

    if results.pose_landmarks:
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow =  results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        left_elbow =  results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        left_foot_index = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        right_foot_index = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
        left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        neck = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

        left_knee_y = left_knee.y
        right_knee_y = right_knee.y

        left_knee_buffer.append(left_knee_y)
        right_knee_buffer.append(right_knee_y)

        left_knee_buffer.pop(0)
        right_knee_buffer.pop(0)

        prev_left_knee_y = 0
        prev_right_knee_y = 0

        left_wrist_distance = math.sqrt((left_wrist.x - neck.x) ** 2 + (left_wrist.y - neck.y) ** 2)
        right_wrist_distance = math.sqrt((right_wrist.x - neck.x) ** 2 + (right_wrist.y - neck.y) ** 2)

        hip_knee_distance = abs(left_hip.y - left_knee.y) + abs(right_hip.y - right_knee.y)

        if left_elbow.y > left_knee.y or right_elbow.y > right_knee.y:
            print("CRAWLING")

        if hip_knee_distance < crouch_threshold:
            print("Crouch position detected")

        if left_wrist_distance < choking_threshold and right_wrist_distance < choking_threshold:
            print("Choking action detected")

    mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                           mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                           mp_draw.DrawingSpec((255, 0, 255), 2, 2))

    cv2.imshow("Pose Estimation", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
