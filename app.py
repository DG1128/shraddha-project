"""
============================================================
  NOVA POLYMERS - Flask Backend (UPDATED)
  Added: individual product pages + enquiry modal support
============================================================
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.secret_key = "nova-polymers-2025"

# ── COMPANY DATA ──────────────────────────────────────────────
COMPANY = {
    "name": "Shraddha Products",
    "tagline": "Quality PVC & Dip Moulding Solutions",
    "email": "info@plastindustriesindia.com",
    "phone1": "+91-	08048774087",
    "address": "167, Vijay Industrial Estate, Near Bhikshukgruh, Odhav, Ahmedabad, Gujarat, India - 382415",
    "contact_person": "Mr. Jitendra H Patel",
    "established": "2000",
    "nature": "Manufacturer, Trader, Wholesale Supplier & Service Provider",
    "employees": "Upto 25 People",
    "turnover": "Rs. 5 - 10 Crore",
    "market": "Pan India",
    "gst": "24AGPPP9704P1ZJ",
    "whatsapp": "91-9824283688",
    "city": "Odhav, Ahmedabad",
    "state": "Gujarat",
}

# ── CATEGORIES ────────────────────────────────────────────────
CATEGORIES = [
    {"id": "dip-moulded-caps",         "name": "Dip Moulded Caps",            "url": "/products/dip-moulded-caps",
     "sub": [
         {"name": "Dip Moulded Vinyl Caps",     "url": "/product/dip-moulded-vinyl-caps"},
         {"name": "E-Z Tab Plastic Caps",        "url": "/product/ez-tab-plastic-caps"},
         {"name": "PVC Battery Terminal Caps",   "url": "/product/pvc-battery-terminal-caps"},
         {"name": "PVC Dip Molded Caps",         "url": "/product/pvc-dip-molded-caps"},
         {"name": "PVC Grab Tab Caps",           "url": "/product/pvc-grab-tab-caps"},
     ]},
    {"id": "pvc-dip-moulding-products","name": "PVC Dip Moulding Products",   "url": "/products/pvc-dip-moulding-products",
     "sub": [
         {"name": "Dip Moulded PVC Coating",    "url": "/product/dip-moulded-pvc-coating"},
         {"name": "Dip Moulded PVC Cones",      "url": "/product/dip-moulded-pvc-cones"},
         {"name": "PVC Cap Covers",             "url": "/product/pvc-cap-covers"},
         {"name": "PVC Dip Molded Grips",       "url": "/product/pvc-dip-molded-grips"},
         {"name": "PVC Dip Moulded Plastisols", "url": "/product/pvc-dip-moulded-plastisols"},
     ]},
    {"id": "end-caps",                 "name": "End Caps",                    "url": "/products/end-caps",
     "sub": [
         {"name": "Busbar End Caps",        "url": "/product/busbar-end-caps"},
         {"name": "Cable End Caps",         "url": "/product/cable-end-caps"},
         {"name": "Pipe End Caps",          "url": "/product/pipe-end-caps"},
         {"name": "PVC Multishape End Caps","url": "/product/pvc-multishape-end-caps"},
     ]},
    {"id": "handle-grips",             "name": "Handle Grips",                "url": "/products/handle-grips",
     "sub": [
         {"name": "Ball Valve Handle Grip",         "url": "/product/ball-valve-handle-grip"},
         {"name": "Dip Molded Bicycle Handle Grip", "url": "/product/dip-molded-bicycle-handle-grip"},
         {"name": "PVC Handle Grip",                "url": "/product/pvc-handle-grip"},
     ]},
    {"id": "pvc-bellows",              "name": "PVC Dip Moulding Bellows",    "url": "/products/pvc-bellows",
     "sub": [
         {"name": "PVC Dip Moulded Flexible Bellows","url": "/product/pvc-dip-moulded-flexible-bellows"},
         {"name": "PVC Moulded Bellows",             "url": "/product/pvc-moulded-bellows"},
     ]},
    {"id": "pvc-shrouds",              "name": "PVC Shrouds",                 "url": "/products/pvc-shrouds",
     "sub": [
         {"name": "PVC Busbar Insulating Shroud","url": "/product/pvc-busbar-insulating-shroud"},
         {"name": "PVC Cable Glands Shroud",    "url": "/product/pvc-cable-glands-shroud"},
     ]},
    {"id": "ball-valve-grip",          "name": "Plastic Ball Valve Grip",     "url": "/product/plastic-ball-valve-grip",  "sub": []},
    {"id": "flange-cover",             "name": "Plastic Flange Cover / PCD",  "url": "/product/plastic-flange-cover",     "sub": []},
    {"id": "pvc-plastisol",            "name": "PVC Plastisol",               "url": "/product/pvc-plastisol",            "sub": []},
]

# ── ALL INDIVIDUAL PRODUCTS ────────────────────────────────────
ALL_PRODUCTS = [
    {
        "id": "pvc-soft-caps",
        "name": "PVC Soft Caps",
        "cat_id": "dip-moulded-caps",
        "cat_name": "Dip Moulded Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-soft-caps-1583297113-5323648.jpeg",
        "price": "₹ 5.00 - 15.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Plastic Caps", "material": "PVC", "shape": "Round / Square",
        "color": "All Colors Available", "feature": "Fine Finish, Good Quality, Light Weight",
        "packaging": "Box", "head_code": "Round, Square, Rectangular",
        "desc": "Premium quality PVC Soft Caps manufactured using high-grade PVC material. These caps are widely used in industrial, automotive, and electrical applications. Available in multiple sizes and colors as per customer requirement.",
    },
    {
        "id": "pvc-soft-grips",
        "name": "PVC Soft Grips",
        "cat_id": "pvc-dip-moulding-products",
        "cat_name": "PVC Dip Moulding Products",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-soft-grips-1583297324-5323667.jpeg",
        "price": "₹ 8.00 - 20.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Handle Grips", "material": "PVC", "shape": "Cylindrical",
        "color": "Black, Red, Blue, Green", "feature": "Ergonomic, Non-Slip, Durable",
        "packaging": "Box", "head_code": "Cylindrical",
        "desc": "Dip moulded PVC Soft Grips offering excellent grip and comfort. Suitable for tools, bicycles, and industrial equipment handles. Non-slip surface for safe handling.",
    },
    {
        "id": "pvc-dip-moulded-plastisols",
        "name": "PVC Dip Moulded Plastisols",
        "cat_id": "pvc-dip-moulding-products",
        "cat_name": "PVC Dip Moulding Products",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-dip-moulded-plastisols-1583297345-5323668.jpeg",
        "price": "₹ 10.00 - 30.00 / Kg",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "PVC Compound", "material": "PVC Plastisol", "shape": "Liquid",
        "color": "All Colors", "feature": "High Quality, Industrial Grade, Custom Formulation",
        "packaging": "Drum / Container", "head_code": "N/A",
        "desc": "Industrial-grade PVC Dip Moulded Plastisols for coating and moulding applications. Custom formulations available for specific industrial requirements.",
    },
    {
        "id": "busbar-end-caps",
        "name": "Busbar End Caps",
        "cat_id": "end-caps",
        "cat_name": "End Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/busbar-end-caps-1583297425-5323675.jpg",
        "price": "₹ 3.00 - 12.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "End Caps", "material": "PVC", "shape": "Rectangular / Square",
        "color": "Black, Red, Yellow", "feature": "Insulating, Flame Retardant, Durable",
        "packaging": "Box", "head_code": "Rectangular",
        "desc": "PVC Busbar End Caps provide insulation and protection for busbar ends in electrical panels. Flame retardant material ensures safety in high-voltage environments.",
    },
    {
        "id": "cable-end-caps",
        "name": "Cable End Caps",
        "cat_id": "end-caps",
        "cat_name": "End Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/cable-end-caps-1583297440-5323677.jpeg",
        "price": "₹ 2.00 - 8.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "End Caps", "material": "PVC", "shape": "Cylindrical",
        "color": "Black, Grey", "feature": "Waterproof, Dust-proof, Flexible",
        "packaging": "Box", "head_code": "Round, Cylindrical",
        "desc": "PVC Cable End Caps protect cable ends from moisture, dust, and mechanical damage. Available in various sizes for different cable diameters.",
    },
    {
        "id": "pvc-handle-grip",
        "name": "PVC Handle Grip",
        "cat_id": "handle-grips",
        "cat_name": "Handle Grips",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-handle-grip-1583297526-5323686.jpeg",
        "price": "₹ 10.00 - 25.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Handle Grip", "material": "PVC", "shape": "Cylindrical / Ergonomic",
        "color": "Black, Red, Blue, Yellow", "feature": "Anti-Slip, Ergonomic, Weather Resistant",
        "packaging": "Box", "head_code": "Cylindrical",
        "desc": "Dip moulded PVC Handle Grips for tools, industrial equipment and bicycles. Anti-slip surface and ergonomic design for comfortable, safe grip.",
    },
    {
        "id": "pvc-busbar-insulating-shroud",
        "name": "PVC Busbar Insulating Shroud",
        "cat_id": "pvc-shrouds",
        "cat_name": "PVC Shrouds",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-busbar-insulating-shroud-1583297627-5323698.jpeg",
        "price": "₹ 15.00 - 50.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Insulating Shroud", "material": "PVC", "shape": "Custom",
        "color": "Red, Black, Yellow", "feature": "High Voltage Insulation, Flame Retardant, Flexible",
        "packaging": "Box", "head_code": "Custom",
        "desc": "PVC Busbar Insulating Shrouds provide electrical insulation for busbars in switchgear panels. High dielectric strength and flame retardant properties.",
    },
    {
        "id": "plastic-ball-valve-grip",
        "name": "Plastic Ball Valve Grip",
        "cat_id": "ball-valve-grip",
        "cat_name": "Plastic Ball Valve Grip",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/plastic-ball-valve-grip-1583297689-5323704.jpeg",
        "price": "₹ 12.00 - 35.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Valve Grip", "material": "PVC / Plastic", "shape": "T-Bar / Lever",
        "color": "Black, Red, Blue", "feature": "Easy Operation, Durable, Chemical Resistant",
        "packaging": "Box", "head_code": "T-Bar, Lever",
        "desc": "Precision moulded Plastic Ball Valve Grips for easy valve operation. Chemical resistant material suitable for industrial plumbing and fluid control systems.",
    },
    {
        "id": "plastic-flange-cover",
        "name": "Plastic Flange Cover / PCD",
        "cat_id": "flange-cover",
        "cat_name": "Plastic Flange Cover / PCD",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/plastic-flange-cover-1583297702-5323706.jpeg",
        "price": "₹ 20.00 - 80.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Flange Cover", "material": "PVC / Plastic", "shape": "Round / Circular",
        "color": "Yellow, Blue, Black", "feature": "Weather Proof, Corrosion Resistant, Dimensional Accuracy",
        "packaging": "Box", "head_code": "Circular",
        "desc": "Plastic Flange Cover / PCD (Pitch Circle Diameter) covers protect pipe flanges from dust, corrosion and mechanical damage during storage and transport.",
    },
    {
        "id": "dip-moulded-vinyl-caps",
        "name": "Dip Moulded Vinyl Caps",
        "cat_id": "dip-moulded-caps",
        "cat_name": "Dip Moulded Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-soft-caps-1583297113-5323648.jpeg",
        "price": "₹ 8.00 - 12.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Vinyl Caps", "material": "PVC Vinyl", "shape": "Round",
        "color": "Black, Red, Blue, Yellow, Green, Orange", "feature": "Fine Finish, Good Quality, Light Weight",
        "packaging": "Box", "head_code": "Round, Cylindrical",
        "desc": "Dip Moulded Vinyl Caps for bolt and stud protection. Made using high quality vinyl PVC compound with excellent flexibility and durability.",
    },
    {
        "id": "ez-tab-plastic-caps",
        "name": "E-Z Tab Plastic Caps",
        "cat_id": "dip-moulded-caps",
        "cat_name": "Dip Moulded Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-soft-caps-1583297113-5323648.jpeg",
        "price": "₹ 5.00 - 10.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Plastic Caps", "material": "PVC", "shape": "Round",
        "color": "Black", "feature": "Fine Finish, Easy Remove, Light Weight",
        "packaging": "Box", "head_code": "Round, Cylindrical",
        "desc": "E-Z Tab Plastic Caps with easy-pull tab for quick removal. Ideal for protecting threaded ends, pipes and fittings during transport and storage.",
    },
    {
        "id": "pvc-battery-terminal-caps",
        "name": "PVC Battery Terminal Caps",
        "cat_id": "dip-moulded-caps",
        "cat_name": "Dip Moulded Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/busbar-end-caps-1583297425-5323675.jpg",
        "price": "₹ 6.00 - 18.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Battery Caps", "material": "PVC", "shape": "Round / Rectangular",
        "color": "Red, Black", "feature": "Insulating, Short-Circuit Protection, Durable",
        "packaging": "Box", "head_code": "Round, Rectangular",
        "desc": "PVC Battery Terminal Caps protect battery terminals from short circuit and corrosion. Standard sizes fit most automotive and industrial batteries.",
    },
    {
        "id": "pvc-dip-molded-caps",
        "name": "PVC Dip Molded Caps",
        "cat_id": "dip-moulded-caps",
        "cat_name": "Dip Moulded Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-soft-caps-1583297113-5323648.jpeg",
        "price": "₹ 4.00 - 14.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Dip Molded Caps", "material": "PVC", "shape": "Round / Square",
        "color": "All Colors", "feature": "Flexible, Durable, High Quality",
        "packaging": "Box", "head_code": "Round, Square",
        "desc": "PVC Dip Molded Caps manufactured using dip moulding process for consistent wall thickness and quality. Available in all standard sizes.",
    },
    {
        "id": "pvc-grab-tab-caps",
        "name": "PVC Grab Tab Caps",
        "cat_id": "dip-moulded-caps",
        "cat_name": "Dip Moulded Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-soft-caps-1583297113-5323648.jpeg",
        "price": "₹ 6.00 - 16.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Grab Tab Caps", "material": "PVC", "shape": "Round with Tab",
        "color": "Black, Red, Yellow", "feature": "Easy Removal, Secure Fit, Durable",
        "packaging": "Box", "head_code": "Round with Tab",
        "desc": "PVC Grab Tab Caps with integrated tab for easy removal. Perfect for protecting hydraulic fittings and thread ends in automotive and industrial applications.",
    },
    {
        "id": "pipe-end-caps",
        "name": "Pipe End Caps",
        "cat_id": "end-caps",
        "cat_name": "End Caps",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/cable-end-caps-1583297440-5323677.jpeg",
        "price": "₹ 5.00 - 20.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Pipe End Caps", "material": "PVC", "shape": "Round",
        "color": "Black, Grey, Red", "feature": "Waterproof, Dust-proof, Easy Fit",
        "packaging": "Box", "head_code": "Round",
        "desc": "PVC Pipe End Caps for sealing and protecting pipe ends. Available for various pipe diameters. Prevents contamination and damage during storage.",
    },
    {
        "id": "pvc-cable-glands-shroud",
        "name": "PVC Cable Glands Shroud",
        "cat_id": "pvc-shrouds",
        "cat_name": "PVC Shrouds",
        "img": "https://2.wlimg.com/product_images/bc-small/2024/10/82426/watermark/pvc-busbar-insulating-shroud-1583297627-5323698.jpeg",
        "price": "₹ 10.00 - 40.00 / Piece(s)",
        "business_type": "Manufacturer, Supplier, Trader",
        "type": "Cable Gland Shroud", "material": "PVC", "shape": "Conical",
        "color": "Black, Grey", "feature": "IP67 Protection, Flexible, UV Resistant",
        "packaging": "Box", "head_code": "Conical",
        "desc": "PVC Cable Glands Shroud provides IP67 protection for cable gland entries. Flexible PVC construction accommodates cable movement without stress.",
    },
]

# ── HOMEPAGE PRODUCT RANGE ─────────────────────────────────────
HOME_PRODUCTS = [p for p in ALL_PRODUCTS if p["id"] in [
    "pvc-soft-caps","pvc-soft-grips","pvc-dip-moulded-plastisols",
    "busbar-end-caps","cable-end-caps","pvc-handle-grip",
    "pvc-busbar-insulating-shroud","plastic-ball-valve-grip","plastic-flange-cover"
]]

# ── BANNER SLIDES ─────────────────────────────────────────────
BANNERS = [
    {"label": "Dip Moulded Caps",           "cat": "dip-moulded-caps"},
    {"label": "PVC Dip Moulding Products",  "cat": "pvc-dip-moulding-products"},
    {"label": "End Caps",                   "cat": "end-caps"},
    {"label": "Handle Grips",               "cat": "handle-grips"},
    {"label": "PVC Shrouds",                "cat": "pvc-shrouds"},
]

# ── TESTIMONIALS ──────────────────────────────────────────────
TESTIMONIALS = [
    {"name": "Amit Patel",   "company": "Patel Electricals, Surat",       "msg": "Shraddha Products has been supplying us PVC shrouds and end caps for 4 years. Excellent quality and always on-time delivery. Highly recommended for bulk orders."},
    {"name": "Suresh Mehta", "company": "AutoCom Industries, Vadodara",   "msg": "We source dip moulded caps and handle grips from Shraddha Products. The products are durable and dimensionally accurate. Very professional team."},
    {"name": "Rajesh Kumar", "company": "Om Plastic Industries, Ahmedabad",    "msg": "Best manufacturer in Gujarat for PVC products. Their plastisol quality is top-notch and the pricing is very competitive. Will continue ordering."},
]

# ── CONTEXT PROCESSOR ─────────────────────────────────────────
@app.context_processor
def inject_globals():
    return dict(company=COMPANY, categories=CATEGORIES)

# ── ROUTES ────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html", banners=BANNERS, home_products=HOME_PRODUCTS, testimonials=TESTIMONIALS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/products")
@app.route("/products/<cat_id>")
def products(cat_id=None):
    current_cat = None
    if cat_id:
        current_cat = next((c for c in CATEGORIES if c["id"] == cat_id), None)
        if not current_cat:
            return redirect(url_for("products"))
        # get all products in this category
        cat_products = [p for p in ALL_PRODUCTS if p["cat_id"] == cat_id]
        return render_template("products.html", current_cat=current_cat,
                               cat_products=cat_products, home_products=HOME_PRODUCTS)
    return render_template("products.html", current_cat=None,
                           cat_products=[], home_products=HOME_PRODUCTS)

# ── INDIVIDUAL PRODUCT DETAIL PAGE ────────────────────────────
@app.route("/product/<product_id>")
def product_detail(product_id):
    product = next((p for p in ALL_PRODUCTS if p["id"] == product_id), None)
    if not product:
        return redirect(url_for("products"))
    # related products (same category, exclude current)
    related = [p for p in ALL_PRODUCTS if p["cat_id"] == product["cat_id"] and p["id"] != product_id][:6]
    # if not enough, add from other categories
    if len(related) < 4:
        others = [p for p in ALL_PRODUCTS if p["id"] != product_id and p not in related]
        related += others[:4 - len(related)]
    return render_template("product_detail.html", product=product, related=related)

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html", testimonials=TESTIMONIALS)

# ── API: Enquiry ───────────────────────────────────────────────
@app.route("/api/enquiry", methods=["POST"])
def api_enquiry():
    data = request.get_json(silent=True) or request.form.to_dict()
    print("New Enquiry:", data)
    return jsonify({"status": "success", "msg": "Enquiry received! We will contact you soon."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
