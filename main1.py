import cv2
import mediapipe as mp
import time


class TouchlessTray:
    def __init__(self):
        # Initialize Mediapipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.drawing_utils = mp.solutions.drawing_utils

        # State management
        self.current_state = "MainMenu"  # Can be MainMenu, StartOrder, ViewOrder, Checkout
        self.order = {}  # Store ordered items with quantities and prices
        self.feedback_message = ""  # Temporary feedback message
        self.feedback_timer = 0  # Timer for feedback message display

    def detect_hand_position(self, frame):
        """Detects hand position and landmarks."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                # Get position of index fingertip
                index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = frame.shape
                x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                return x, y
        return None

    def display_feedback(self, frame):
        """Displays feedback messages for user actions."""
        if time.time() - self.feedback_timer < 2:  # Display message for 2 seconds
            cv2.putText(frame, self.feedback_message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    def render_main_menu(self, frame):
        """Renders the main menu."""
        cv2.rectangle(frame, (100, 50), (400, 150), (0, 255, 0), -1)
        cv2.putText(frame, "Start Order", (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(frame, (100, 200), (400, 300), (255, 0, 0), -1)
        cv2.putText(frame, "View Order", (150, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(frame, (100, 350), (400, 450), (0, 0, 255), -1)
        cv2.putText(frame, "Checkout", (150, 410), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(frame, (100, 500), (400, 600), (255, 255, 0), -1)
        cv2.putText(frame, "Exit", (200, 560), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    def render_start_order(self, frame):
        """Renders the order menu."""
        cv2.rectangle(frame, (100, 50), (400, 150), (0, 255, 0), -1)
        cv2.putText(frame, "Burger $5", (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(frame, (100, 200), (400, 300), (255, 0, 0), -1)
        cv2.putText(frame, "Pizza $8", (150, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(frame, (100, 350), (400, 450), (0, 0, 255), -1)
        cv2.putText(frame, "Back", (200, 410), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    def render_view_order(self, frame):
        """Renders the current order."""
        y = 50
        cv2.putText(frame, "Your Order:", (50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        y += 50
        for idx, (item, details) in enumerate(self.order.items()):
            cv2.putText(
                frame,
                f"{item}: {details['quantity']} x ${details['price']}  [Del: {idx+1}]",
                (50, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
            )
            y += 50

        cv2.rectangle(frame, (100, 500), (400, 600), (0, 0, 255), -1)
        cv2.putText(frame, "Back", (200, 560), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    def render_checkout(self, frame):
        """Renders the checkout menu."""
        total_cost = sum(details['quantity'] * details['price'] for details in self.order.values())
        cv2.putText(frame, f"Total: ${total_cost}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        cv2.rectangle(frame, (100, 200), (400, 300), (0, 255, 0), -1)
        cv2.putText(frame, "Confirm", (200, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(frame, (100, 350), (400, 450), (255, 0, 0), -1)
        cv2.putText(frame, "Back", (200, 410), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.rectangle(frame, (100, 500), (400, 600), (0, 0, 255), -1)
        cv2.putText(frame, "Exit", (200, 560), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    def add_to_order(self, item, price):
        """Adds an item to the order."""
        if item in self.order:
            self.order[item]["quantity"] += 1
        else:
            self.order[item] = {"quantity": 1, "price": price}
        self.feedback_message = f"Item Added: {item}"
        self.feedback_timer = time.time()

    def delete_from_order(self, idx):
        """Deletes an item from the order by index."""
        if idx < len(self.order):
            item = list(self.order.keys())[idx]
            del self.order[item]
            self.feedback_message = f"Item Removed: {item}"
            self.feedback_timer = time.time()

    # Rest of the implementation...


    def handle_selection(self, x, y):
        """Handles menu selections based on hand position."""
        if self.current_state == "MainMenu":
            if 50 < x < 250:
                if 100 < y < 200:
                    self.current_state = "StartOrder"
                elif 250 < y < 350:
                    self.current_state = "ViewOrder"
                elif 400 < y < 500:
                    self.current_state = "Checkout"
                elif 550 < y < 650:
                    return False  # Exit application

        elif self.current_state == "StartOrder":
            if 50 < x < 250:
                if 100 < y < 200:
                    self.add_to_order("Burger", 5)
                elif 250 < y < 350:
                    self.add_to_order("Pizza", 8)
                elif 400 < y < 500:
                    self.current_state = "MainMenu"

        elif self.current_state == "ViewOrder":
            if 500 < y < 600:
                self.current_state = "MainMenu"

        elif self.current_state == "Checkout":
            if 400 < y < 500:
                self.order = {}  # Clear the order
                self.current_state = "MainMenu"
            elif 550 < y < 650:
                self.current_state = "MainMenu"

        return True

    def add_to_order(self, item, price):
        """Adds an item to the order."""
        if item in self.order:
            self.order[item]["quantity"] += 1
        else:
            self.order[item] = {"quantity": 1, "price": price}

    def run(self):
        """Runs the main application loop."""
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            hand_pos = self.detect_hand_position(frame)

            if self.current_state == "MainMenu":
                self.render_main_menu(frame)
            elif self.current_state == "StartOrder":
                self.render_start_order(frame)
            elif self.current_state == "ViewOrder":
                self.render_view_order(frame)
            elif self.current_state == "Checkout":
                self.render_checkout(frame)

            if hand_pos:
                x, y = hand_pos
                if not self.handle_selection(x, y):
                    break

            cv2.imshow("Touchless Tray", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

# Run the application
app = TouchlessTray()
app.run()
