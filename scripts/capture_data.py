import cv2
import mediapipe as mp
import os
import csv

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# ---- CHANGE THIS LABEL EACH TIME YOU RECORD A NEW SIGN ----
SIGN_LABEL = "sorry"   # example: hello, thankyou, sorry etc.
# -----------------------------------------------------------

DATA_DIR = "../dataset"
SIGN_PATH = os.path.join(DATA_DIR, SIGN_LABEL)
os.makedirs(SIGN_PATH, exist_ok=True)

hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

sample_count = len(os.listdir(SIGN_PATH))

print("Press 's' to save sample | Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    landmark_row = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for lm in hand_landmarks.landmark:
                landmark_row.extend([lm.x, lm.y, lm.z])

    cv2.putText(frame, f"Samples: {sample_count}", (10,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Capture", frame)

    key = cv2.waitKey(1)

    if key == ord('s') and landmark_row:
        sample_count += 1
        file_path = os.path.join(SIGN_PATH, f"{SIGN_LABEL}_{sample_count}.csv")

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(landmark_row)

        print(f"Saved sample {sample_count}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()