class Order:
    def __init__(self):
        """
        Initializes an empty order.
        """
        self.order_items = []
        self.total_items = 0

    def add_item(self, item):
        """
        Adds an item to the order.
        :param item: The item to add.
        """
        self.order_items.append(item)
        self.total_items += 1
        print(f"Added: {item}")

    def remove_item(self, item):
        """
        Removes an item from the order if it exists.
        :param item: The item to remove.
        """
        if item in self.order_items:
            self.order_items.remove(item)
            self.total_items -= 1
            print(f"Removed: {item}")
        else:
            print(f"Item '{item}' not in order!")

    def display_order(self):
        """
        Displays the current order summary.
        :return: List of items in the order.
        """
        if not self.order_items:
            print("Your order is empty.")
            return []
        print("\nCurrent Order:")
        for i, item in enumerate(self.order_items, 1):
            print(f"{i}. {item}")
        return self.order_items

    def finalize_order(self):
        """
        Finalizes the order and displays the summary.
        """
        if not self.order_items:
            print("Cannot finalize an empty order.")
            return "Order not finalized."
        print("\nOrder Finalized!")
        print("Your final order:")
        self.display_order()
        return "Order finalized successfully."

# Test the Order class
if __name__ == "__main__":
    order = Order()
    order.add_item("Veg Sandwich")
    order.add_item("Coke")
    order.add_item("Brownie")

    order.display_order()

    order.remove_item("Coke")
    order.display_order()

    order.finalize_order()
