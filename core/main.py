import cv2
import numpy as np
import mediapipe as mp
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def fingers_up(lm_list, tip_ids):
    """Check which fingers are up."""
    fingers = []
    if lm_list[tip_ids[0]][1] < lm_list[tip_ids[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    for i in range(1, 5):
        if lm_list[tip_ids[i]][2] < lm_list[tip_ids[i] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def find_position(img, results, hand_no=0):
    """Find hand position and landmarks."""
    lm_list = []
    if results.multi_hand_landmarks:
        my_hand = results.multi_hand_landmarks[hand_no]
        for id, lm in enumerate(my_hand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([id, cx, cy])
    return lm_list

def draw_menu(img):
    """Draw a virtual menu on the screen."""
    menu_height = 100
    colors = [(0, 255, 0), (0, 255, 255), (255, 0, 0), (0, 0, 255)]
    labels = ["Start Order", "View Order", "Cancel Order", "Exit"]
    for i, (color, label) in enumerate(zip(colors, labels)):
        x1, y1 = i * 150, 0
        x2, y2 = x1 + 150, menu_height
        cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        cv2.putText(img, label, (x1 + 10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return [(i * 150, (i + 1) * 150) for i in range(len(colors))]

def main():
    logging.info("Starting Touchless Tray Application")

    cap = cv2.VideoCapture(0)
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logging.error("Failed to capture frame")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        menu_positions = draw_menu(frame)  # Draw menu on the frame

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = find_position(frame, results)

            if lm_list:
                x1, y1 = lm_list[8][1:]  # Tip of the index finger

                for i, (x_start, x_end) in enumerate(menu_positions):
                    if x_start < x1 < x_end and y1 < 100:
                        if i == 0:
                            logging.info("Start Order selected")
                            cv2.putText(frame, "Order Started", (200, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        elif i == 1:
                            logging.info("View Order selected")
                            cv2.putText(frame, "Viewing Order", (200, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        elif i == 2:
                            logging.info("Cancel Order selected")
                            cv2.putText(frame, "Order Cancelled", (200, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        elif i == 3:
                            logging.info("Exiting Application")
                            cap.release()
                            cv2.destroyAllWindows()
                            return

        cv2.imshow("Touchless Tray", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    logging.info("Application Closed")

if __name__ == "__main__":
    main()
