import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, detection_confidence=0.7, max_hands=2):
        """
        Initializes the HandTracker with Mediapipe Hands module.
        :param detection_confidence: Minimum confidence value for hand detection.
        :param max_hands: Maximum number of hands to detect.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    def find_hands(self, image, draw=True):
        """
        Processes the input image to find hands and draw landmarks if required.
        :param image: Input image in which hands need to be detected.
        :param draw: Boolean flag to draw landmarks on the image.
        :return: Processed image with or without landmarks.
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_image)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return image

    def find_positions(self, image):
        """
        Finds the positions of hand landmarks.
        :param image: Input image to process.
        :return: List of landmark positions [(id, x, y)] and bounding box [x_min, y_min, x_max, y_max].
        """
        lm_list = []
        bbox = []

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                h, w, _ = image.shape
                x_min, y_min = w, h
                x_max, y_max = 0, 0

                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((id, cx, cy))

                    x_min, y_min = min(x_min, cx), min(y_min, cy)
                    x_max, y_max = max(x_max, cx), max(y_max, cy)

                bbox = [x_min, y_min, x_max, y_max]

        return lm_list, bbox

    def fingers_up(self, lm_list):
        """
        Determines which fingers are up based on landmark positions.
        :param lm_list: List of landmark positions [(id, x, y)].
        :return: List of binary values (1 for finger up, 0 for finger down).
        """
        if not lm_list:
            return []

        fingers = []

        # Thumb
        fingers.append(1 if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1] else 0)

        # Other fingers
        for i in range(1, 5):
            fingers.append(1 if lm_list[self.tip_ids[i]][2] < lm_list[self.tip_ids[i] - 2][2] else 0)

        return fingers

# Test the HandTracker class
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = tracker.find_hands(frame)
        lm_list, bbox = tracker.find_positions(frame)

        if lm_list:
            fingers = tracker.fingers_up(lm_list)
            print(f"Fingers up: {fingers}")

        cv2.imshow("Hand Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
