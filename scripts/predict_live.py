import cv2
import mediapipe as mp
import numpy as np
import joblib
import traceback

try:
    print("Loading model...")
    model = joblib.load("models/sign_model.pkl")
    print("Model loaded.")

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mp_hands.Hands(max_num_hands=2)

    print("Opening camera...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        raise Exception("Camera did not open")

    print("Camera opened. Starting loop...")

    while True:
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Frame not received")
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        landmark_row = []

        if results.multi_hand_landmarks:
            hands_detected = []

            for hand_landmarks in results.multi_hand_landmarks:
                single_hand = []
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    single_hand.extend([lm.x, lm.y, lm.z])

                hands_detected.append(single_hand)

            # ---- FORCE FIXED INPUT SIZE (126 FEATURES) ----
            if len(hands_detected) == 1:
                # One hand → pad second hand with zeros
                landmark_row = hands_detected[0] + [0] * 63

            elif len(hands_detected) >= 2:
                # Two hands → use first two hands
                landmark_row = hands_detected[0] + hands_detected[1]

            # Only predict if size is exactly what model expects
            if len(landmark_row) == 126:
                prediction = model.predict([landmark_row])[0]
                cv2.putText(frame, prediction, (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        cv2.imshow("Prediction", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except Exception:
    print("\n==== ERROR OCCURRED ====")
    traceback.print_exc()
    input("\nPress ENTER so the window doesn't close...")