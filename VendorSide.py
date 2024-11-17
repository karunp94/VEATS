from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "veats_secret"

# Menu data for 4 stalls
stalls = {
    "Stall 1": {"Burger": {"price": 5, "stock": True}, "Fries": {"price": 3, "stock": True}, "Cola": {"price": 2, "stock": True}},
    "Stall 2": {"Pizza": {"price": 8, "stock": True}, "Garlic Bread": {"price": 4, "stock": True}, "Pasta": {"price": 7, "stock": True}},
    "Stall 3": {"Tacos": {"price": 6, "stock": True}, "Nachos": {"price": 4, "stock": True}, "Quesadilla": {"price": 7, "stock": True}},
    "Stall 4": {"Coffee": {"price": 3, "stock": True}, "Donut": {"price": 2, "stock": True}, "Bagel": {"price": 4, "stock": True}}
}

# Order queue for vendors to process
orders = []

# Cart to store selected items
cart = {}

@app.route("/")
def home():
    return render_template("home.html", stalls=stalls)

@app.route("/menu/<stall_name>")
def menu(stall_name):
    if stall_name not in stalls:
        flash("Invalid stall selected!")
        return redirect(url_for("home"))
    return render_template("menu.html", stall_name=stall_name, menu=stalls[stall_name])

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    stall_name = request.form["stall_name"]
    item = request.form["item"]
    quantity = int(request.form["quantity"])

    # Check stock
    if not stalls[stall_name][item]["stock"]:
        flash(f"{item} is out of stock!")
        return redirect(url_for("menu", stall_name=stall_name))

    if stall_name not in cart:
        cart[stall_name] = {}

    if item in cart[stall_name]:
        cart[stall_name][item] += quantity
    else:
        cart[stall_name][item] = quantity

    flash(f"{quantity}x {item} added to cart!")
    return redirect(url_for("menu", stall_name=stall_name))

@app.route("/cart")
def view_cart():
    total = 0
    for stall, items in cart.items():
        for item, qty in items.items():
            total += stalls[stall][item]["price"] * qty
    return render_template("cart.html", cart=cart, stalls=stalls, total=total)

@app.route("/checkout", methods=["POST"])
def checkout():
    global cart
    orders.append(cart.copy())  # Add cart to order queue
    cart = {}
    flash("Order placed successfully! Thank you for using VEATS.")
    return redirect(url_for("home"))

@app.route("/vendor")
def vendor_dashboard():
    return render_template("vendor.html", stalls=stalls, orders=orders)

@app.route("/accept_order", methods=["POST"])
def accept_order():
    order_index = int(request.form["order_index"])
    if 0 <= order_index < len(orders):
        orders.pop(order_index)  # Remove the accepted order
        flash("Order accepted!")
    else:
        flash("Invalid order index!")
    return redirect(url_for("vendor_dashboard"))

@app.route("/remove_item", methods=["POST"])
def remove_item():
    stall_name = request.form["stall_name"]
    item_name = request.form["item_name"]

    if stall_name in stalls and item_name in stalls[stall_name]:
        stalls[stall_name][item_name]["stock"] = False  # Mark item as out of stock
        flash(f"{item_name} from {stall_name} marked as out of stock!")
    else:
        flash("Invalid stall or item!")
    return redirect(url_for("vendor_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
