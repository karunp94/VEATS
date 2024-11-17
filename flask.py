from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "veats_secret"

# Menu data for 4 stalls
stalls = {
    "Stall 1": {"Burger": 5, "Fries": 3, "Cola": 2},
    "Stall 2": {"Pizza": 8, "Garlic Bread": 4, "Pasta": 7},
    "Stall 3": {"Tacos": 6, "Nachos": 4, "Quesadilla": 7},
    "Stall 4": {"Coffee": 3, "Donut": 2, "Bagel": 4}
}

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
            total += stalls[stall][item] * qty
    return render_template("cart.html", cart=cart, stalls=stalls, total=total)

@app.route("/checkout", methods=["POST"])
def checkout():
    global cart
    cart = {}
    flash("Payment successful! Thank you for using VEATS.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
