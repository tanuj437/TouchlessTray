import cv2
import logging
from core.gesture import HandDetector
from core.menu import MenuManager
from core.order import OrderManager
from storage.database import DatabaseManager
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="application_debug.log",  # Logs will be saved to this file
    filemode="w",
)

def main():
    print("Starting the application")

    try:
        # Initialize required components
        print("Initializing components")
        hand_detector = HandDetector()
        menu = MenuManager()
        order_manager = OrderManager()
        database_manager = DatabaseManager("orders.db")
        database_manager.create_order_table()
        print("Components initialized successfully")

        # Start the camera
        logging.debug("Accessing the camera")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Cannot access the camera")
            print("Error: Cannot access the camera")
            return

        selected_option = None

        while True:
            ret, frame = cap.read()
            if not ret:
                logging.error("Cannot read frame from the camera")
                print("Error: Cannot read frame from the camera")
                break

            # Flip the frame for natural interaction
            frame = cv2.flip(frame, 1)

            # Detect hand landmarks
            landmarks = hand_detector.detect_hand(frame)
            hand_detector.draw_hand_landmarks(frame, landmarks)

            # Log detected landmarks
            if landmarks:
                logging.debug(f"Detected landmarks: {landmarks}")

            # Get hand position if landmarks are detected
            if landmarks:
                hand_position = hand_detector.get_hand_position(landmarks, frame.shape)

                # Highlight menu options based on hand position
                if hand_position:
                    logging.debug(f"Hand position detected at: {hand_position}")
                    x, y = hand_position
                    selected_option = menu.highlight_option(x, y, frame)

                # If fist gesture detected, select the highlighted option
                if selected_option and cv2.waitKey(1) & 0xFF == ord('s'):
                    logging.info(f"Item selected: {selected_option}")
                    order_manager.add_item(selected_option)
                    print(f"Added to order: {selected_option}")

            # Display the current menu
            menu.display_menu(frame)

            # Show the frame
            cv2.imshow("Hand Gesture Menu", frame)

            # Check for user input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Quit the application
                logging.info("Quitting the application")
                break
            elif key == ord('v'):  # View current order
                logging.info("Viewing the current order")
                print("Current Order:")
                for item in order_manager.get_order():
                    print(f"- {item}")
            elif key == ord('c'):  # Confirm and save the order
                logging.info("Saving the current order")
                database_manager.insert_order(order_manager.get_order())
                print("Order saved!")
                order_manager.reset_order()

    except Exception as e:
        logging.exception("An error occurred: %s", e)
    finally:
        # Release resources
        logging.info("Releasing resources and closing the application")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
