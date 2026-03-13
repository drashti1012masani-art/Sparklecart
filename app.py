from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ===================== USER SITE =====================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/category/gold")
def gold():
    return render_template("gold.html")

@app.route("/category/silver")
def silver():
    return render_template("silver.html")

@app.route("/category/diamond")
def diamond():
    return render_template("diamond.html")

# PRODUCTS PAGE
@app.route("/products")
def products():
    return render_template("products.html", admin_products_list=admin_products_list)

@app.route("/about")
def about():
    return render_template("about.html")


# ===================== ADMIN PANEL =====================

UPLOAD_FOLDER = 'static/images/products'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


admin_products_list = [
    {"id":1,"name":"Gold Ring","price":1200,"images":["g1.jpg","g2.jpg"],"category":"gold"},
    {"id":2,"name":"Silver Necklace","price":800,"images":["s1.jpg","s2.jpg"],"category":"silver"},
]

users_list = [
    {"id":1,"name":"Rahul","email":"rahul@gmail.com"},
    {"id":2,"name":"Neha","email":"neha@gmail.com"}
]

orders_list = [
    {"id":1,"user":"Rahul","product":"Gold Ring","status":"Shipped"},
    {"id":2,"user":"Neha","product":"Silver Necklace","status":"Processing"}
]


# ================= DASHBOARD =================

@app.route("/admin")
def admin_dashboard():

    gold = len([p for p in admin_products_list if p["category"]=="gold"])
    silver = len([p for p in admin_products_list if p["category"]=="silver"])
    diamond = len([p for p in admin_products_list if p["category"]=="diamond"])

    return render_template(
        "admin/dashboard.html",
        gold=gold,
        silver=silver,
        diamond=diamond,
        users=len(users_list),
        orders=len(orders_list)
    )


# ================= PRODUCTS =================

@app.route("/admin/products")
def admin_products():
    return render_template("admin/products.html", products=admin_products_list)


@app.route("/admin/products/add", methods=["GET","POST"])
def add_product():

    if request.method == "POST":

        new_id = len(admin_products_list) + 1
        name = request.form["name"]
        price = request.form["price"]
        category = request.form["category"]

        files = request.files.getlist("images")
        filenames = []

        for f in files:
            if f.filename != "":
                filename = secure_filename(f.filename)
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                f.save(path)
                filenames.append(filename)

        admin_products_list.append({
            "id":new_id,
            "name":name,
            "price":price,
            "category":category,
            "images":filenames
        })

        return redirect(url_for("admin_products"))

    return render_template("admin/add_product.html")


@app.route("/admin/products/delete/<int:product_id>")
def delete_product(product_id):

    global admin_products_list

    for p in admin_products_list:
        if p["id"] == product_id:
            for img in p["images"]:
                path = os.path.join(app.config["UPLOAD_FOLDER"], img)
                if os.path.exists(path):
                    os.remove(path)

    admin_products_list = [p for p in admin_products_list if p["id"] != product_id]

    return redirect(url_for("admin_products"))


# ================= USERS =================

@app.route("/admin/users")
def admin_users():
    return render_template("admin/users.html", users=users_list)


# ================= ORDERS =================

@app.route("/admin/orders")
def admin_orders():
    return render_template("admin/orders.html", orders=orders_list)


# ================= TRACKING =================

@app.route("/admin/tracking")
def tracking():
    return render_template("admin/tracking.html", orders=orders_list)



if __name__ == "__main__":
    app.run(debug=True)

    from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy cart storage (for demo only)
cart = []

@app.route('/products')
def products_page():
    # Example product list structure with rating & images
    admin_products_list = [
        {
            "id": 1,
            "name": "Awesome Product",
            "price": 799,
            "images": ["g1.jpg", "s2.jpg", "d3.jpg"],
            "rating": 4
        },
        {
            "id": 2,
            "name": "Another Product",
            "price": 499,
            "images": ["g5.jpg"],
            "rating": 5
        },
    ]
    return render_template('products.html', admin_products_list=admin_products_list)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Here, add logic to add product to session cart or DB
    cart.append(product_id)
    return redirect(url_for('products_page'))

if __name__ == '__main__':
    app.run(debug=True)