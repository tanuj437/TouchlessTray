import cv2
import mediapipe as mp
import sqlite3

# Hand Gesture Detection Class
class HandDetector:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.7):
        self.hands = mp.solutions.hands.Hands(
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.drawing_utils = mp.solutions.drawing_utils

    def detect_hand(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results.multi_hand_landmarks

    def draw_hand_landmarks(self, frame, landmarks):
        if landmarks:
            for hand_landmarks in landmarks:
                self.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                )
        return frame

    def get_hand_position(self, landmarks, frame_shape):
        if not landmarks:
            return None
        hand_landmarks = landmarks[0]
        height, width, _ = frame_shape
        x = int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].x * width)
        y = int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].y * height)
        return x, y

# Menu Class
class Menu:
    def __init__(self):
        self.items = ["Sandwich", "Drinks", "Salad"]
        self.suboptions = {
            "Sandwich": ["White Bread", "Whole Wheat Bread", "Gluten-Free Bread"],
            "Drinks": ["Coke", "Water", "Lemonade"],
            "Salad": ["Caesar", "Greek", "Garden"]
        }
        self.selected_option = None

    def display_menu(self, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        for idx, item in enumerate(self.items):
            cv2.putText(frame, item, (50, 50 + (idx * 40)), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        if self.selected_option:
            cv2.putText(frame, f"Selected: {self.selected_option}", (50, 350), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

    def highlight_option(self, x, y, frame):
        option_idx = int(y // 50)
        if 0 <= option_idx < len(self.items):
            self.selected_option = self.items[option_idx]
            return self.selected_option
        return None

# Order Manager Class
class OrderManager:
    def __init__(self):
        self.order = []

    def add_item(self, item):
        self.order.append(item)

    def get_order(self):
        return self.order

    def reset_order(self):
        self.order = []

# Database Manager Class
class DatabaseManager:
    def __init__(self, db_name="orders.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_order_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                               (order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                items TEXT)''')
        self.conn.commit()

    def insert_order(self, order):
        order_items = ', '.join(order)
        self.cursor.execute('''INSERT INTO orders (items) VALUES (?)''', (order_items,))
        self.conn.commit()

    def retrieve_orders(self):
        self.cursor.execute('''SELECT * FROM orders''')
        return self.cursor.fetchall()

# Main Application
def main():
    hand_detector = HandDetector()
    menu = Menu()
    order_manager = OrderManager()
    database_manager = DatabaseManager("orders.db")
    database_manager.create_order_table()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the camera")
        return

    selected_option = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame from the camera")
            break

        frame = cv2.flip(frame, 1)

        landmarks = hand_detector.detect_hand(frame)
        hand_detector.draw_hand_landmarks(frame, landmarks)

        if landmarks:
            hand_position = hand_detector.get_hand_position(landmarks, frame.shape)

            if hand_position:
                x, y = hand_position
                selected_option = menu.highlight_option(x, y, frame)

        menu.display_menu(frame)

        cv2.imshow("Hand Gesture Menu", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit the application
            break
        elif key == ord('s') and selected_option:  # Select the item
            order_manager.add_item(selected_option)
            print(f"Added to order: {selected_option}")
        elif key == ord('v'):  # View current order
            print("Current Order:")
            for item in order_manager.get_order():
                print(f"- {item}")
        elif key == ord('c'):  # Confirm and save the order
            database_manager.insert_order(order_manager.get_order())
            print("Order saved!")
            order_manager.reset_order()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
