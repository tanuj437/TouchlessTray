import os
import json

class StorageManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_order(self, order):
        """Save the current order to a file."""
        try:
            with open(self.file_path, 'a') as file:
                json.dump(order, file)
                file.write("\n")
        except Exception as e:
            print(f"Error saving order: {e}")

    def load_orders(self):
        """Load all past orders from the file."""
        orders = []
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    for line in file:
                        order = json.loads(line.strip())
                        orders.append(order)
        except Exception as e:
            print(f"Error loading orders: {e}")
        return orders
