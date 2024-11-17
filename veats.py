from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import sqlite3

# Database setup
conn = sqlite3.connect("orders.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS orders
               (restaurant TEXT, item TEXT, quantity INTEGER)''')
conn.commit()

class LoginScreen(Screen):
    pass

class UserHomeScreen(Screen):
    def display_restaurants(self):
        self.ids.restaurant_list.clear_widgets()  # Clear existing list
        restaurants = ["Gazebo1", "Gazebo2", "Dakshin", "Lassi House"]
        for restaurant in restaurants:
            item = OneLineListItem(text=restaurant, on_release=lambda x=restaurant: self.select_restaurant(x))
            self.ids.restaurant_list.add_widget(item)

    def select_restaurant(self, restaurant):
        self.manager.get_screen('restaurant').restaurant_name = restaurant
        self.manager.current = 'restaurant'

class RestaurantScreen(Screen):
    restaurant_name = ""

    def on_enter(self):
        self.ids.restaurant_name.text = f"Welcome to {self.restaurant_name}"
        self.ids.menu_list.clear_widgets()
        menu_items = {"Pizza": 100, "Burger": 50, "Lassi": 30, "South Indian Thali": 120}
        for item, price in menu_items.items():
            menu_item = OneLineListItem(text=f"{item} - ₹{price}",
                                        on_release=lambda x=item: self.add_to_cart(x))
            self.ids.menu_list.add_widget(menu_item)

    def add_to_cart(self, item):
        def order_confirm_callback(*args):
            quantity = int(quantity_dialog.content_cls.ids.quantity_input.text)
            cursor.execute("INSERT INTO orders (restaurant, item, quantity) VALUES (?, ?, ?)",
                           (self.restaurant_name, item, quantity))
            conn.commit()
            quantity_dialog.dismiss()

        quantity_dialog = MDDialog(
            title=f"Add {item} to cart",
            type="custom",
            content_cls=QuantityInputDialog(),
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: quantity_dialog.dismiss()),
                MDFlatButton(text="ORDER", on_release=order_confirm_callback),
            ],
        )
        quantity_dialog.open()

class QuantityInputDialog(Screen):
    pass

class RestaurantSideScreen(Screen):
    def display_orders(self):
        self.ids.order_list.clear_widgets()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        for order in orders:
            order_item = OneLineListItem(text=f"{order[0]}: {order[1]} x{order[2]}")
            self.ids.order_list.add_widget(order_item)

class VEatApp(MDApp):
    def build(self):
        self.title = "V-Eats"
        return Builder.load_file('kivy_design.kv')

if __name__ == '__main__':
    VEatApp().run()
