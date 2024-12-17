class Menu:
    def __init__(self):
        """
        Initializes the menu with predefined categories and items.
        """
        self.categories = ["Sandwiches", "Drinks", "Desserts"]
        self.items = {
            "Sandwiches": ["Veg Sandwich", "Chicken Sandwich", "Club Sandwich"],
            "Drinks": ["Coke", "Pepsi", "Lemonade", "Water"],
            "Desserts": ["Brownie", "Ice Cream", "Cake Slice"]
        }
        self.current_category = None
        self.current_items = []

    def display_categories(self):
        """
        Returns the list of available categories.
        :return: List of categories.
        """
        return self.categories

    def select_category(self, category):
        """
        Sets the current category and fetches the items under it.
        :param category: The category to be selected.
        :return: List of items under the selected category.
        """
        if category in self.categories:
            self.current_category = category
            self.current_items = self.items[category]
            return self.current_items
        else:
            raise ValueError(f"Category '{category}' does not exist.")

    def display_items(self):
        """
        Returns the items of the currently selected category.
        :return: List of items in the current category.
        """
        if not self.current_category:
            raise ValueError("No category selected.")
        return self.current_items

    def highlight_option(self, option_index):
        """
        Highlights the given item in the current category.
        :param option_index: Index of the item to highlight.
        :return: The highlighted item.
        """
        if not self.current_items:
            raise ValueError("No items available to highlight.")
        if 0 <= option_index < len(self.current_items):
            return f"Highlighting: {self.current_items[option_index]}"
        else:
            raise IndexError("Invalid option index.")

# Test the Menu class
if __name__ == "__main__":
    menu = Menu()
    print("Available Categories:")
    print(menu.display_categories())

    category = "Sandwiches"
    print(f"\nSelected Category: {category}")
    items = menu.select_category(category)
    print(f"Items in '{category}': {items}")

    option_index = 1
    print(f"\n{menu.highlight_option(option_index)}")
