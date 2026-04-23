"""
============================================================
  NOVA POLYMERS - Flask Backend (UPDATED)
  Added: MongoDB Integration, Admin Panel, Enquiry tracking
============================================================
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from functools import wraps
import threading
import os
from dotenv import load_dotenv
import resend

# Load environment variables from .env file if present
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "nova-polymers-2025")

# ── EMAIL CONFIGURATION ────────────────────────────────────────
resend.api_key = os.environ.get("RESEND_API_KEY", "re_WsYvKYX3_JPFV3aZzPr5xqtHkLRmTZKsr")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "fakelaptop150@gmail.com")

def send_enquiry_email(data):
    """Sends email notification using Resend API. Safe and non-blocking."""
    try:
        body = f"""<p>New Enquiry Received:</p>
        <p><strong>Name:</strong> {data.get('name')}</p>
        <p><strong>Phone:</strong> {data.get('phone')}</p>
        <p><strong>Email:</strong> {data.get('email', 'N/A')}</p>
        <p><strong>Company:</strong> {data.get('company', 'N/A')}</p>
        <p><strong>Product:</strong> {data.get('product', 'N/A')}</p>
        <p><strong>Message:</strong><br>{data.get('message')}</p>"""
        
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": RECIPIENT_EMAIL,
            "subject": f"New Enquiry from {data.get('name')} - Shraddha Products",
            "html": body
        })
        print(f"Enquiry email sent via Resend API: {response}")
    except Exception as e:
        print(f"Failed to send email via Resend SDK: {e}")

# ── MONGODB SETUP ──────────────────────────────────────────────
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
client = MongoClient(MONGO_URI)
db = client['shraddha_products']
enquiries_col = db['enquiries']
products_col = db['products']

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

# ── SEED DATABASE IF EMPTY ─────────────────────────────────────
try:
    if products_col.count_documents({}) == 0:
        print("Database empty. Seeding initial products...")
        for p in ALL_PRODUCTS:
            p["_id"] = ObjectId()
        products_col.insert_many(ALL_PRODUCTS)
except Exception as e:
    print(f"Warning: Could not connect to MongoDB at startup. Ensure MONGO_URI is set. Error: {e}")

# ── CONTEXT PROCESSOR ─────────────────────────────────────────
@app.context_processor
def inject_globals():
    return dict(company=COMPANY, categories=CATEGORIES)

# ── PUBLIC ROUTES ──────────────────────────────────────────────
@app.route("/")
def home():
    featured_ids = [
        "pvc-soft-caps", "pvc-soft-grips", "pvc-dip-moulded-plastisols",
        "busbar-end-caps", "cable-end-caps", "pvc-handle-grip",
        "pvc-busbar-insulating-shroud", "plastic-ball-valve-grip", "plastic-flange-cover"
    ]
    home_products = list(products_col.find({"id": {"$in": featured_ids}}))
    return render_template("index.html", banners=BANNERS, home_products=home_products, testimonials=TESTIMONIALS)

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
        # get all products in this category from MongoDB
        cat_products = list(products_col.find({"cat_id": cat_id}))
        home_products = list(products_col.find().limit(8))
        return render_template("products.html", current_cat=current_cat,
                               cat_products=cat_products, home_products=home_products)
    
    cat_products = list(products_col.find())
    home_products = list(products_col.find().limit(8))
    return render_template("products.html", current_cat=None,
                           cat_products=cat_products, home_products=home_products)

@app.route("/product/<product_id>")
def product_detail(product_id):
    # Try fetching by raw id (for seeded products) or string representation of ObjectId
    product = products_col.find_one({"id": product_id})
    if not product:
        try:
            product = products_col.find_one({"_id": ObjectId(product_id)})
        except:
            product = None

    if not product:
        return redirect(url_for("products"))
    
    # Related products
    related = list(products_col.find({"cat_id": product.get("cat_id"), "_id": {"$ne": product["_id"]}}).limit(6))
    if len(related) < 4:
        exclude_ids = [product["_id"]] + [r["_id"] for r in related]
        others = list(products_col.find({"_id": {"$nin": exclude_ids}}).limit(4 - len(related)))
        related.extend(others)
        
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
    
    name = data.get("name")
    phone = data.get("phone")
    message = data.get("message")
    
    # Validate required fields
    if not name or not phone or not message:
        return jsonify({"status": "error", "msg": "Missing required fields: Name, Phone, and Message are required."}), 400
        
    enquiry = {
        "name": name,
        "phone": phone,
        "email": data.get("email", ""),
        "company": data.get("company", ""),
        "product": data.get("product", ""),
        "message": message,
        "createdAt": datetime.now(),
        "status": "new"
    }
    
    enquiries_col.insert_one(enquiry)
    
    # Send email notification in the background
    threading.Thread(target=send_enquiry_email, args=(enquiry,)).start()
    
    return jsonify({"status": "success", "msg": "Enquiry received! We will contact you soon."})


# ── ADMIN PANEL ────────────────────────────────────────────────

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        admin_user = os.environ.get("ADMIN_USER", "admin")
        admin_pass = os.environ.get("ADMIN_PASS", "admin123")
        
        if username == admin_user and password == admin_pass:
            session['admin_logged_in'] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for("admin_login"))

@app.route("/admin")
def admin_redirect():
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    # Sort latest first
    enquiries = list(enquiries_col.find().sort("createdAt", -1))
    return render_template("admin_dashboard.html", enquiries=enquiries)

@app.route("/admin/enquiry/delete/<obj_id>", methods=["GET", "POST"])
@admin_required
def admin_delete_enquiry(obj_id):
    enquiries_col.delete_one({"_id": ObjectId(obj_id)})
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/enquiry/status/<obj_id>", methods=["POST"])
@admin_required
def admin_enquiry_status(obj_id):
    status = request.form.get("status", "contacted")
    enquiries_col.update_one({"_id": ObjectId(obj_id)}, {"$set": {"status": status}})
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/products")
@admin_required
def admin_products():
    products = list(products_col.find())
    return render_template("admin_products.html", products=products)

@app.route("/admin/product/add", methods=["GET", "POST"])
@admin_required
def admin_product_add():
    if request.method == "POST":
        product_data = {
            "name": request.form.get("name"),
            "cat_id": request.form.get("cat_id"),
            "cat_name": next((c["name"] for c in CATEGORIES if c["id"] == request.form.get("cat_id")), ""),
            "material": request.form.get("material"),
            "size": request.form.get("size"),
            "color": request.form.get("color"),
            "price": request.form.get("price"),
            "img": request.form.get("img"),
            "desc": request.form.get("desc"),
            "id": request.form.get("name").lower().replace(" ", "-") # Generate string ID
        }
        products_col.insert_one(product_data)
        return redirect(url_for("admin_products"))
    return render_template("admin_product_form.html", categories=CATEGORIES, action="Add")

@app.route("/admin/product/edit/<obj_id>", methods=["GET", "POST"])
@admin_required
def admin_product_edit(obj_id):
    product = products_col.find_one({"_id": ObjectId(obj_id)})
    if not product:
        return redirect(url_for("admin_products"))
        
    if request.method == "POST":
        product_data = {
            "name": request.form.get("name"),
            "cat_id": request.form.get("cat_id"),
            "cat_name": next((c["name"] for c in CATEGORIES if c["id"] == request.form.get("cat_id")), product.get('cat_name', '')),
            "material": request.form.get("material"),
            "size": request.form.get("size"),
            "color": request.form.get("color"),
            "price": request.form.get("price"),
            "img": request.form.get("img"),
            "desc": request.form.get("desc"),
            "id": request.form.get("id") or product.get("id", str(obj_id))
        }
        products_col.update_one({"_id": ObjectId(obj_id)}, {"$set": product_data})
        return redirect(url_for("admin_products"))
    return render_template("admin_product_form.html", product=product, categories=CATEGORIES, action="Edit")

@app.route("/admin/product/delete/<obj_id>", methods=["GET", "POST"])
@admin_required
def admin_product_delete(obj_id):
    products_col.delete_one({"_id": ObjectId(obj_id)})
    return redirect(url_for("admin_products"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
