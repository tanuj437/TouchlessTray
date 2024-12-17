# Database Manager Class
import sqlite3
class DatabaseManager:
    def __init__(self, db_name="orders.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_order_table(self):
        """
        Create a table to store orders if it doesn't exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                items TEXT
            )
        ''')
        self.conn.commit()

    def insert_order(self, order):
        """
        Insert a new order into the database.
        Args:
            order: List of items in the order.
        """
        order_items = ', '.join(order)
        self.cursor.execute('INSERT INTO orders (items) VALUES (?)', (order_items,))
        self.conn.commit()

    def retrieve_orders(self):
        """
        Retrieve all saved orders from the database.
        Returns:
            List of tuples containing order records.
        """
        self.cursor.execute('SELECT * FROM orders')
        return self.cursor.fetchall()
