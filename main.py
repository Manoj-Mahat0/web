from flask import Flask, render_template, request, redirect, url_for, session, flash
import stripe

app = Flask(__name__)
app.secret_key = "supersecretkey"

stripe.api_key = "sk_test_51R4a3EFpfdDlifil6XCudM4upQ3uGEsha2sI40k26J4J3AKzRpMXG4JfFf1lad3zcWR2tecya1Tt0CY6oiz3g9jf0030ZpSxND"

# Product Data
products = [
    {
        "id": 1,
        "name": "iPhone 16",
        "price": 73400,
        "image": "https://m.media-amazon.com/images/I/71CSc3M2AGL.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: Apple's iPhone 16 continues the legacy of precision engineering, featuring an aerospace-grade aluminum or titanium frame with a sleek, minimalist design.\nMaterial: Crafted with a durable Ceramic Shield front and back, offering enhanced scratch and drop resistance. The display uses a Super Retina XDR panel with ProMotion for ultra-smooth visuals.\nUniqueness: Equipped with the latest A18 Bionic chip, advanced AI-powered photography, and a longer-lasting battery. iOS ecosystem integration ensures seamless connectivity across Apple devices.",
        "rating": 4.5
    },
    {
        "id": 2,
        "name": "MacBook Air M1",
        "price": 69400,
        "image": "https://m.media-amazon.com/images/I/71jG+e7roXL.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: Designed for portability and performance, the MacBook Air M1 is incredibly thin and lightweight while maintaining a robust unibody aluminum chassis.\nMaterial: High-quality recycled aluminum for a premium and eco-friendly build, complemented by a Retina display with True Tone technology.\nUniqueness: The M1 chip revolutionizes speed and efficiency, offering up to 18 hours of battery life. Silent, fanless cooling and macOS optimization ensure a seamless user experience.",
        "rating": 4.8
    },
    {
        "id": 3,
        "name": "Samsung Galaxy Watch",
        "price": 50000,
        "image": "https://m.media-amazon.com/images/I/71elbYR1eEL.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: A sleek, ergonomic smartwatch with a stainless steel or aluminum casing, paired with a comfortable silicone or leather strap.\nMaterial: Corning Gorilla Glass DX+ for scratch-resistant protection, high-quality AMOLED display for vibrant colors, and water resistance up to 5ATM.\nUniqueness: Advanced health tracking, ECG monitoring, and seamless Samsung ecosystem integration make it the perfect fitness and lifestyle companion.",
        "rating": 4.3
    },
    {
        "id": 4,
        "name": "Boat Rockerz 450",
        "price": 1400,
        "image": "https://m.media-amazon.com/images/I/51FNnHjzhQL.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: Stylish and lightweight over-ear headphones with a comfortable, cushioned headband and foldable design for portability.\nMaterial: High-grade plastic and premium foam ear cushions for extended wear. Durable, sweat-resistant coating for long-lasting use.\nUniqueness: Immersive sound with 40mm dynamic drivers, up to 15 hours of battery life, and dual connectivity (Bluetooth & AUX).",
        "rating": 4.6
    },
    {
        "id": 5,
        "name": "SONY PS5",
        "price": 55900,
        "image": "https://m.media-amazon.com/images/I/51QoWUMybjL.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: A futuristic, aerodynamic design with a two-tone finish and customizable faceplates for a unique aesthetic.\nMaterial: High-quality plastic and metal construction, with an advanced cooling system and a powerful AMD Ryzen processor.\nUniqueness: Supports ray tracing for ultra-realistic graphics, an ultra-fast SSD for near-instant loading, and a revolutionary DualSense controller with adaptive triggers and haptic feedback.",
        "rating": 4.9
    },
    {
        "id": 6,
        "name": "SONY 4K Smart TV",
        "price": 90400,
        "image": "https://m.media-amazon.com/images/I/81BENnbPpuL.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: A sleek, bezel-less design that maximizes screen-to-body ratio for an immersive viewing experience.\nMaterial: Premium metal frame with an anti-glare coating, high-dynamic range (HDR) display, and Dolby Vision support.\nUniqueness: Powered by the X1 Ultimate Processor for stunning clarity, MotionFlow technology for smooth visuals, and Android TV OS for smart connectivity.",
        "rating": 4.7
    },
    {
        "id": 7,
        "name": "JBL Bluetooth Speaker",
        "price": 20400,
        "image": "https://m.media-amazon.com/images/I/51waOv47fqL.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: A compact yet robust cylindrical or boxy design, built for portability and durability.\nMaterial: IP67-rated waterproof and dustproof body with a rubberized grip for shock resistance. High-performance fabric covering for premium aesthetics.\nUniqueness: Signature JBL bass, 360-degree sound, up to 20 hours of battery life, and PartyBoost pairing for stereo sound.",
        "rating": 4.4
    },
    {
        "id": 8,
        "name": "Canon DSLR Camera",
        "price": 40000,
        "image": "https://m.media-amazon.com/images/I/914hFeTU2-L.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: A professional-grade camera with an ergonomic grip, tactile control buttons, and a durable yet lightweight magnesium alloy body.\nMaterial: Weather-sealed construction for protection against dust and moisture, high-resolution LCD touchscreen, and precision glass optics.\nUniqueness: Advanced image processing, ultra-fast autofocus, 4K video recording, and interchangeable lenses for creative flexibility.",
        "rating": 4.8
    },
    {
        "id": 9,
        "name": "Mi Fitness Tracker",
        "price": 2000,
        "image": "https://m.media-amazon.com/images/I/61EclBYcocL.AC_UY327_FMwebp_QL65.jpg",
        "description": "Craftsmanship: A sleek and ultra-lightweight fitness band with a curved display and smooth silicone strap for all-day comfort.\nMaterial: Durable polycarbonate and scratch-resistant glass, with water resistance up to 50 meters.\nUniqueness: AI-powered health tracking, real-time heart rate monitoring, SpO2 measurement, and long battery life of up to 14 days.",
        "rating": 4.2
    },
    {
        "id": 10,
        "name": "Philips Robot Vacuum",
        "price": 5000,
        "image": "https://m.media-amazon.com/images/I/51el3Rs8whL.SX679.jpg",
        "description": "Craftsmanship: A compact, circular design with a slim profile, allowing it to navigate under furniture and tight spaces.\nMaterial: High-quality plastic and metal construction with anti-collision sensors and durable rubberized wheels.\nUniqueness: Intelligent mapping, automated scheduling, high-suction power, and voice assistant compatibility for hands-free cleaning.",
        "rating": 4.6
    }
]


@app.route('/')
def home():
    return render_template('base.html', products=products)

@app.route('/cart')
def cart():
    cart_items = session.get("cart", {})

    total_price = sum(
        (float(item['price'].replace('₹', '').replace(',', '')) if isinstance(item['price'], str) else item['price'])
        * item['quantity'] 
        for item in cart_items.values()
    )

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return render_template('product_details.html', product=product)
    return "Product not found", 404

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("Please fill in all fields", "danger")
        else:
            # Here you can add code to send the message via email or save it to a database.
            flash("Your message has been sent successfully!", "success")
            return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy_now', methods=['POST'])
def buy_now():
    name = request.form.get('name')
    address = request.form.get('address')

    if not name or not address:
        flash("Please enter all details!", "error")
        return redirect(url_for('cart'))

    cart_items = session.get("cart", {})

    if not cart_items:
        flash("Your cart is empty!", "error")
        return redirect(url_for('cart'))

    line_items = []
    for item in cart_items.values():
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": item["name"]},
                "unit_amount": int(item["price"] * 100),
            },
            "quantity": item["quantity"],
        })

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=url_for("payment_success", _external=True),
        cancel_url=url_for("cart", _external=True),
    )

    return redirect(checkout_session.url, code=303)

@app.route('/payment_success')
def payment_success():
    session["cart"] = {}
    flash("Payment successful! Your order has been placed.", "success")
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get("cart", {})
    product = next((p for p in products if p["id"] == product_id), None)
    
    if product:
        product_id_str = str(product_id)
        if product_id_str in cart:
            cart[product_id_str]["quantity"] += 1
        else:
            cart[product_id_str] = {"name": product["name"], "price": product["price"], "quantity": 1}

    session["cart"] = cart
    session.modified = True  
    flash(f"{product['name']} added to cart!", "success")
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:product_id>/<action>')
def update_cart(product_id, action):
    cart = session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if action == "increase":
            cart[product_id_str]["quantity"] += 1
        elif action == "decrease" and cart[product_id_str]["quantity"] > 1:
            cart[product_id_str]["quantity"] -= 1
        elif action == "remove":
            del cart[product_id_str]

    session["cart"] = cart
    session.modified = True
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
