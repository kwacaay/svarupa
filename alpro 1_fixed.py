import streamlit as st
import random
import hashlib
from datetime import datetime
from supabase import create_client, Client

# ─────────────────────────────────────────────
#  SUPABASE SETUP
# ─────────────────────────────────────────────

@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

# ─────────────────────────────────────────────
#  PASSWORD HASHING
# ─────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SVARUPA",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg:         #0D0D0D;
    --bg2:        #141414;
    --bg3:        #1C1C1C;
    --card:       #1A1A1A;
    --gold:       #C9A84C;
    --gold-light: #E8C97A;
    --gold-dim:   #7A6030;
    --white:      #F0EDE6;
    --grey:       #6B6B6B;
    --grey2:      #3A3A3A;
}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main {
    background-color: var(--bg) !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] { background: var(--bg2) !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: var(--white) !important; }

.stButton > button {
    background: var(--gold) !important;
    color: #0D0D0D !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1.4rem !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: var(--gold-light) !important; color: #0D0D0D !important; }

input, .stTextInput input, .stNumberInput input {
    background: var(--bg3) !important;
    color: var(--white) !important;
    border: 1px solid var(--grey2) !important;
    border-radius: 0 !important;
    font-family: 'Inter', sans-serif !important;
}
input:focus { border-color: var(--gold) !important; box-shadow: none !important; }

.stRadio label { color: var(--grey) !important; font-size: 0.85rem !important; }
.stRadio [data-baseweb="radio"] svg { fill: var(--gold) !important; }

[data-baseweb="select"] > div {
    background: var(--bg3) !important;
    border-color: var(--grey2) !important;
    border-radius: 0 !important;
    color: var(--white) !important;
}

.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: 0.05em;
    border-bottom: 1px solid var(--gold-dim);
    padding-bottom: 0.4rem;
    margin: 1.5rem 0 0.8rem 0;
}

.hero-block {
    background: var(--bg2);
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    border-left: 3px solid var(--gold);
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--white);
    line-height: 1.1;
    margin: 0;
}
.hero-sub {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    color: var(--gold);
    font-size: 1rem;
    margin-top: 0.5rem;
}

.product-img-wrap {
    width: 100%;
    aspect-ratio: 3/4;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    position: relative;
    overflow: hidden;
}
.product-img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.product-card {
    background: var(--card);
    margin-bottom: 0.6rem;
    overflow: hidden;
}
.product-body { padding: 0.75rem 0.85rem; }
.product-name { font-weight: 600; color: var(--white); font-size: 0.85rem; line-height: 1.3; }
.product-meta { color: var(--grey); font-size: 0.7rem; margin: 0.2rem 0; }
.product-price { color: var(--gold); font-family: 'Cormorant Garamond', serif; font-size: 1rem; font-weight: 700; }
.product-rating { color: #C9A84C; font-size: 0.72rem; }

.gold-divider { height: 1px; background: var(--gold-dim); margin: 1rem 0; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--gold-dim); }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  PRODUCT IMAGE
# ─────────────────────────────────────────────

CATEGORY_STYLE = {
    "Atasan":    {"c1": "#2a2a2a", "c2": "#1a1a1a", "emoji": "👕"},
    "Bawahan":   {"c1": "#1e1e2e", "c2": "#12121f", "emoji": "👖"},
    "Dress":     {"c1": "#2e1e2a", "c2": "#1f1215", "emoji": "👗"},
    "Outerwear": {"c1": "#2c2216", "c2": "#1c1c1c", "emoji": "🧥"},
    "Sepatu":    {"c1": "#2a2810", "c2": "#1a1a14", "emoji": "👟"},
    "Tas":       {"c1": "#2a1a14", "c2": "#1a0e0a", "emoji": "👜"},
}

PRODUCT_IMAGE_PATH = {
    1:  "image/linen blazer.jpeg",
    2:  "image/cargo pants.jpeg",
    3:  "image/knit sweater.jpeg",
    4:  "image/flowy maxi .jpeg",
    5:  "image/chinos.jpeg",
    6:  "image/turtleneck.jpeg",
    7:  "image/straight jeans.jpeg",
    8:  "image/a line dress.jpeg",
    9:  "image/coat.jpeg",
    10: "image/satin dress.jpeg",
    11: "image/vest.jpeg",
    12: "image/shoes.jpeg",
    13: "image/leather bag.jpeg",
    14: "image/white tee.jpeg",
    15: "image/trousers.jpeg",
    16: "image/blazer.jpeg",
}

import os
import base64


def make_placeholder_svg(category: str, label: str) -> str:
    style = CATEGORY_STYLE.get(category, CATEGORY_STYLE["Atasan"])
    c1, c2 = style["c1"], style["c2"]
    short = (label or category).upper()[:18]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="530" viewBox="0 0 400 530">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="530" fill="url(#g)"/>
  <rect x="30" y="30" width="340" height="470" fill="none" stroke="#7A6030" stroke-opacity="0.35" stroke-width="1"/>
  <text x="200" y="250" font-size="64" text-anchor="middle" dominant-baseline="middle">{style['emoji']}</text>
  <text x="200" y="320" font-family="Inter, sans-serif" font-size="13" letter-spacing="3"
        fill="#7A6030" text-anchor="middle" dominant-baseline="middle">{short}</text>
</svg>"""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"


def get_img_url(product) -> str:
    pid = product["id"]
    path = PRODUCT_IMAGE_PATH.get(pid)
    if path and os.path.exists(path):
        return path
    return make_placeholder_svg(product.get("category", "Atasan"), product.get("name", ""))


# ─────────────────────────────────────────────
#  PRODUCT DATABASE
# ─────────────────────────────────────────────
PRODUCTS = [
    {"id": 1,  "name": "Oversized Linen Blazer",   "brand": "SVARUPA", "price": 489000, "category": "Atasan",    "gender": "Unisex", "fit": "oversized", "desc": "Blazer linen premium, potongan longgar modern.",           "rating": 4.8, "stock": 12},
    {"id": 2,  "name": "Wide-Leg Cargo Pants",      "brand": "SVARUPA", "price": 379000, "category": "Bawahan",   "gender": "Unisex", "fit": "oversized", "desc": "Cargo pants dengan banyak kantong fungsional.",            "rating": 4.7, "stock": 8},
    {"id": 3,  "name": "Boxy Knit Sweater",         "brand": "SVARUPA", "price": 325000, "category": "Atasan",    "gender": "Unisex", "fit": "oversized", "desc": "Sweater rajut tebal, kotak dan nyaman.",                  "rating": 4.6, "stock": 15},
    {"id": 4,  "name": "Flowy Maxi Skirt",          "brand": "SVARUPA", "price": 299000, "category": "Bawahan",   "gender": "Wanita", "fit": "oversized", "desc": "Rok maxi ringan, cocok untuk semua bentuk tubuh.",         "rating": 4.9, "stock": 10},
    {"id": 5,  "name": "Slim Tapered Chinos",       "brand": "SVARUPA", "price": 359000, "category": "Bawahan",   "gender": "Pria",   "fit": "slim",      "desc": "Chinos slim fit dengan bahan stretch.",                   "rating": 4.7, "stock": 20},
    {"id": 6,  "name": "Fitted Ribbed Turtleneck",  "brand": "SVARUPA", "price": 249000, "category": "Atasan",    "gender": "Unisex", "fit": "slim",      "desc": "Turtleneck ribbed yang mempertegas siluet.",              "rating": 4.8, "stock": 18},
    {"id": 7,  "name": "Straight Cut Jeans",        "brand": "SVARUPA", "price": 429000, "category": "Bawahan",   "gender": "Unisex", "fit": "slim",      "desc": "Denim straight klasik, serba cocok.",                     "rating": 4.6, "stock": 25},
    {"id": 8,  "name": "A-Line Mini Dress",         "brand": "SVARUPA", "price": 345000, "category": "Dress",     "gender": "Wanita", "fit": "slim",      "desc": "Dress A-line elegan untuk tampilan kasual.",              "rating": 4.9, "stock": 7},
    {"id": 9,  "name": "Longline Coat",             "brand": "SVARUPA", "price": 699000, "category": "Outerwear", "gender": "Unisex", "fit": "oversized", "desc": "Coat panjang dengan detail belahan belakang.",            "rating": 4.9, "stock": 5},
    {"id": 10, "name": "Satin Slip Dress",          "brand": "SVARUPA", "price": 389000, "category": "Dress",     "gender": "Wanita", "fit": "slim",      "desc": "Slip dress satin premium, tampil mewah.",                "rating": 4.8, "stock": 9},
    {"id": 11, "name": "Utility Vest",              "brand": "SVARUPA", "price": 275000, "category": "Atasan",    "gender": "Unisex", "fit": "oversized", "desc": "Vest utility dengan banyak kantong.",                    "rating": 4.5, "stock": 14},
    {"id": 12, "name": "Lace-Up Oxford Shoes",      "brand": "SVARUPA", "price": 589000, "category": "Sepatu",    "gender": "Unisex", "fit": "all",       "desc": "Oxford klasik bertali, bahan kulit sintetis premium.",    "rating": 4.7, "stock": 11},
    {"id": 13, "name": "Leather Crossbody Bag",     "brand": "SVARUPA", "price": 459000, "category": "Tas",       "gender": "Unisex", "fit": "all",       "desc": "Tas selempang kulit dengan gesper emas.",                "rating": 4.8, "stock": 6},
    {"id": 14, "name": "Classic White Tee",         "brand": "SVARUPA", "price": 149000, "category": "Atasan",    "gender": "Unisex", "fit": "slim",      "desc": "Kaos putih premium 100% cotton combed.",                 "rating": 4.6, "stock": 50},
    {"id": 15, "name": "Pleated Wide Trousers",     "brand": "SVARUPA", "price": 415000, "category": "Bawahan",   "gender": "Unisex", "fit": "oversized", "desc": "Celana plisket lebar bergaya retro modern.",             "rating": 4.7, "stock": 13},
    {"id": 16, "name": "Structured Blazer",         "brand": "SVARUPA", "price": 549000, "category": "Atasan",    "gender": "Unisex", "fit": "slim",      "desc": "Blazer berstruktur untuk tampilan profesional.",          "rating": 4.8, "stock": 8},
]

PAYMENT_METHODS = ["Transfer Bank", "E-Wallet", "COD", "Virtual Account"]

# ─────────────────────────────────────────────
#  AUTH FUNCTIONS (Supabase)
# ─────────────────────────────────────────────

def register_user(email: str, password: str):
    """Return (success: bool, error_message: str|None)."""
    try:
        hashed = hash_password(password)
        supabase.table("users").insert({"email": email, "password": hashed}).execute()
        return True, None
    except Exception as e:
        err = str(e)
        if "duplicate" in err.lower() or "unique" in err.lower():
            return False, "Email sudah terdaftar."
        return False, f"Gagal mendaftar: {err}"


def login_user(email: str, password: str):
    """Return user row dict atau None."""
    try:
        hashed = hash_password(password)
        res = supabase.table("users").select("*").eq("email", email).eq("password", hashed).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        st.error(f"Error login: {e}")
        return None


# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────

def init_state():
    defaults = {
        "cart": {},
        "wishlist": set(),
        "orders": [],
        "page": "home",
        "bmi_result": None,
        "user_name": "Guest",
        "user_gender": "Unisex",
        "logged_in": False,
        "user_email": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# ─────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────

def page_login():
    st.markdown(
        """
    <div style="text-align:center;padding:2rem 0 1rem 0;">
        <h1 style="font-family:'Cormorant Garamond',serif;font-size:2.5rem;
            color:#C9A84C;letter-spacing:0.15em;">✦ SVARUPA ✦</h1>
        <p style="color:#6B6B6B;font-size:0.8rem;letter-spacing:0.2em;text-transform:uppercase;">
            Curated For Your Unique Shape</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Masuk", key="btn_login", use_container_width=True):
            user = login_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Email atau password salah.")

    with tab2:
        reg_email = st.text_input("Email Baru", key="reg_email")
        reg_password = st.text_input("Password Baru", type="password", key="reg_pass")
        if st.button("Daftar", key="btn_register", use_container_width=True):
            if reg_email and reg_password:
                ok, err = register_user(reg_email, reg_password)
                if ok:
                    st.success("Akun berhasil dibuat! Silakan login.")
                else:
                    st.error(err)
            else:
                st.warning("Isi email dan password terlebih dahulu.")

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def fmt_price(p):
    return f"Rp {p:,}".replace(",", ".")


def get_product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)


def cart_total():
    return sum(get_product(pid)["price"] * qty for pid, qty in st.session_state.cart.items() if get_product(pid))


def cart_count():
    return sum(st.session_state.cart.values())


def add_to_cart(pid):
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
    st.toast("✓ Ditambahkan ke keranjang!", icon="🛒")


def toggle_wishlist(pid):
    if pid in st.session_state.wishlist:
        st.session_state.wishlist.discard(pid)
        st.toast("Dihapus dari wishlist")
    else:
        st.session_state.wishlist.add(pid)
        st.toast("♥️ Ditambahkan ke wishlist!")


def go_to(page):
    st.session_state.page = page
    st.rerun()


# ─────────────────────────────────────────────
#  COMPONENTS
# ─────────────────────────────────────────────

def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def gold_divider():
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)


def render_product_image(product):
    img_url = get_img_url(product)
    st.image(img_url, use_container_width=True)


def product_card(product, key_prefix="p"):
    pid = product["id"]
    in_wish = pid in st.session_state.wishlist

    render_product_image(product)

    stars = "★" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))
    st.markdown(
        f"""
    <div class="product-card">
        <div class="product-body">
            <div class="product-name">{product['name']}</div>
            <div class="product-meta">{product['category']} · {product['gender']}</div>
            <div class="product-rating">{stars} {product['rating']}</div>
            <div class="product-price">{fmt_price(product['price'])}</div>
            <div style="color:#3A3A3A;font-size:0.68rem;margin-top:0.15rem;">Stok: {product['stock']}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 2])
    with c1:
        wish_label = "♥" if in_wish else "♡"
        if st.button(wish_label, key=f"wish_{key_prefix}_{pid}"):
            toggle_wishlist(pid)
            st.rerun()
    with c2:
        if st.button("+ Keranjang", key=f"cart_{key_prefix}_{pid}"):
            add_to_cart(pid)
            st.rerun()


def product_grid(products, key_prefix="grid"):
    if not products:
        st.markdown(
            '<p style="color:#6B6B6B;font-style:italic;">Tidak ada produk ditemukan.</p>',
            unsafe_allow_html=True,
        )
        return

    for i in range(0, len(products), 2):
        cols = st.columns(2, gap="small")
        for j, col in enumerate(cols):
            if i + j < len(products):
                with col:
                    product_card(products[i + j], key_prefix=key_prefix)


# ─────────────────────────────────────────────
#  HEADER + NAV
# ─────────────────────────────────────────────

def render_header():
    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        st.markdown(
            """
        <h1 style="text-align:center;font-family:'Cormorant Garamond',serif;
            font-size:2rem;color:#C9A84C;letter-spacing:0.15em;margin:0.5rem 0 0 0;">
            ✦ SVARUPA ✦
        </h1>
        <p style="text-align:center;color:#7A6030;font-size:0.8rem;
            letter-spacing:0.2em;margin:0 0 0.5rem 0;text-transform:uppercase;">
            CURATED FOR YOUR UNIQUE SHAPE
        </p>
        """,
            unsafe_allow_html=True,
        )
    with c3:
        n = cart_count()
        if st.button(f"🛒 {n}", key="header_cart"):
            go_to("cart")

    st.markdown('<div class="gold-divider" style="margin-top:0"></div>', unsafe_allow_html=True)


def render_nav():
    pages = ["🏠 Home", "✨ Stylist", "♡ Wishlist", "🛒 Keranjang", "📦 Pesanan"]
    page_keys = ["home", "recom", "wishlist", "cart", "orders"]

    cols = st.columns(5)
    for col, label, key in zip(cols, pages, page_keys):
        with col:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                go_to(key)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGES
# ─────────────────────────────────────────────

def page_home():
    st.markdown(
        """
    <div class="hero-block">
        <p class="hero-title">DEFINE YOUR<br>STYLE.</p>
        <p class="hero-sub">Fashion premium untuk jiwa modern.</p>
        <p style="color:#6B6B6B;font-size:0.85rem;margin-top:0.5rem;">
            🧥 &nbsp; 👗 &nbsp; 👖 &nbsp; 👠 &nbsp; 👜 &nbsp; 🧣
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    section_title("Kategori")
    cats = [("👕", "Atasan"), ("👖", "Bawahan"), ("👗", "Dress"), ("🧥", "Outerwear"), ("👟", "Sepatu"), ("👜", "Tas")]
    cols = st.columns(6)
    for col, (emoji, name) in zip(cols, cats):
        with col:
            st.markdown(
                f"""
                <div style="background:#1A1A1A;text-align:center;padding:0.7rem 0.3rem;cursor:pointer;">
                    <div style="font-size:1.4rem">{emoji}</div>
                    <div style="color:#6B6B6B;font-size:0.65rem;margin-top:0.3rem">{name}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    section_title("✦ Editor's Pick")
    picks = [p for p in PRODUCTS if p["rating"] >= 4.8][:4]
    product_grid(picks, "home_pick")

    section_title("Semua Produk")
    product_grid(PRODUCTS, "home_all")


def page_recom():
    section_title("✦ Personal Stylist — Rekomendasi Untukmu")
    st.markdown(
        """
    <p style="color:#6B6B6B;font-style:italic;font-size:0.85rem;text-align:center;margin-bottom:1rem;">
        Masukkan data tubuhmu, dan kami akan merekomendasikan gaya fashion yang paling cocok untukmu.
    </p>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div style="background:#1A1A1A;padding:1rem;border-left:3px solid #7A6030;margin-bottom:1rem;">', unsafe_allow_html=True)
        st.markdown('<p style="color:#C9A84C;font-size:1.1rem;font-weight:700;">📏 Data Tubuh</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Nama kamu", placeholder="e.g. Rina")
            height = st.number_input("Tinggi (cm)", min_value=100.0, max_value=250.0, value=165.0, step=0.5)
        with c2:
            weight = st.number_input("Berat (kg)", min_value=30.0, max_value=200.0, value=60.0, step=0.5)
            age = st.number_input("Usia", min_value=10, max_value=100, value=25)

        gender = st.radio("Gender", ["Pria", "Wanita", "Unisex"], horizontal=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Hitung BMI & Lihat Rekomendasi ✦", use_container_width=True):
            bmi = weight / ((height / 100) ** 2)
            name_display = name.strip() or "Kamu"

            if bmi < 18.5:
                cat, cat_color = "Underweight", "#7AA3D4"
                tips = "Pilih pakaian yang menambah volume dan kesan penuh."
                fits = ["oversized", "all"]
                style_tips = [
                    "✓ Oversized & layering memberikan kesan tubuh lebih berisi",
                    "✓ Garis horizontal di pakaian membantu kesan melebar",
                    "✓ Warna-warna bold & pattern besar sangat cocok",
                    "✓ Wide-leg pants memberi keseimbangan proporsi",
                ]
            elif bmi < 25:
                cat, cat_color = "Normal", "#3D7A5A"
                tips = "Hampir semua siluet cocok — eksplorasi gaya sesukamu!"
                fits = ["slim", "oversized", "all"]
                style_tips = [
                    "✓ Slim fit mempertegas proporsi tubuh idealmu",
                    "✓ Straight cut klasik selalu elegan di tubuhmu",
                    "✓ Bereksperimen dengan layer dan siluet baru",
                    "✓ Monochrome look terlihat sangat tajam di tubuhmu",
                ]
            elif bmi < 30:
                cat, cat_color = "Overweight", "#D4A944"
                tips = "Pilih potongan yang memberi kesan panjang & elegan."
                fits = ["oversized", "all"]
                style_tips = [
                    "✓ Vertical lines dan warna gelap menciptakan kesan ramping",
                    "✓ Pakaian well-fitted (bukan ketat) lebih flattering",
                    "✓ V-neck dan scoop neck memberi kesan leher lebih panjang",
                    "✓ Monochrome dari atas ke bawah elongates the body",
                ]
            else:
                cat, cat_color = "Obese", "#B04040"
                tips = "Pilih pakaian well-fitted yang nyaman dan percaya diri!"
                fits = ["oversized", "all"]
                style_tips = [
                    "✓ Pakaian yang pas (bukan ketat, bukan terlalu longgar) terbaik",
                    "✓ Dark solid colors memberikan kesan sleek",
                    "✓ Empire waistline sangat flattering",
                    "✓ Invest pada kualitas kain — drape yang baik kunci segalanya",
                ]

            st.session_state.bmi_result = {
                "bmi": bmi, "cat": cat, "cat_color": cat_color,
                "name": name_display, "tips": tips,
                "style_tips": style_tips, "fits": fits, "gender": gender,
            }
            st.session_state.user_name = name_display
            st.session_state.user_gender = gender
            st.rerun()

    if st.session_state.bmi_result:
        r = st.session_state.bmi_result
        gold_divider()

        st.markdown(
            f"""
        <div style="background:#1A1A1A;padding:1.5rem;text-align:center;margin-bottom:1rem;">
            <p style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;
                color:#F0EDE6;margin:0 0 0.5rem 0;">Hai, {r['name']}! 👋</p>
            <div style="font-family:'Cormorant Garamond',serif;font-size:3.5rem;
                font-weight:700;color:{r['cat_color']};line-height:1;">{r['bmi']:.1f}</div>
            <div style="color:#6B6B6B;font-size:0.75rem;margin-bottom:0.5rem;">BMI Score</div>
            <span style="background:{r['cat_color']};color:#0D0D0D;
                padding:0.2rem 1rem;font-weight:700;font-size:0.8rem;
                letter-spacing:0.1em;text-transform:uppercase;">{r['cat']}</span>
            <p style="font-family:'Cormorant Garamond',serif;font-style:italic;
                color:#C9A84C;margin-top:0.8rem;font-size:0.95rem;">{r['tips']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown('<div style="background:#1C1C1C;padding:1rem 1.2rem;margin-bottom:1rem;">', unsafe_allow_html=True)
        st.markdown('<p style="color:#E8C97A;font-weight:600;font-size:0.85rem;margin:0 0 0.5rem 0">Style Tips Untukmu</p>', unsafe_allow_html=True)
        for tip in r["style_tips"]:
            st.markdown(f'<p style="color:#F0EDE6;font-size:0.82rem;margin:0.2rem 0">{tip}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        section_title("✦ Rekomendasi Untukmu")
        recs = [
            p for p in PRODUCTS
            if (p["fit"] in r["fits"])
            and (p["gender"] == "Unisex" or p["gender"] == r["gender"] or r["gender"] == "Unisex")
        ]

        key = f"recom_{r['gender']}"
        if st.session_state.get("recom_key") != key:
            random.shuffle(recs)
            st.session_state.recom_ids = [p["id"] for p in recs[:8]]
            st.session_state.recom_key = key

        recom_products = [get_product(pid) for pid in st.session_state.recom_ids if get_product(pid)]
        product_grid(recom_products, "recom")


def page_wishlist():
    section_title("♥️ Wishlist Saya")

    if not st.session_state.wishlist:
        st.markdown(
            """
        <div style="text-align:center;padding:4rem 1rem;">
            <div style="font-size:3rem">♡</div>
            <p style="color:#6B6B6B;font-style:italic;">Wishlist masih kosong</p>
            <p style="color:#3A3A3A;font-size:0.8rem">Klik ♡ di produk untuk menambahkan</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    items = [get_product(pid) for pid in st.session_state.wishlist if get_product(pid)]
    st.markdown(f'<p style="color:#6B6B6B;font-size:0.8rem">{len(items)} item tersimpan</p>', unsafe_allow_html=True)
    product_grid(items, "wish")

    gold_divider()
    if st.button("🗑 Hapus Semua Wishlist", key="clear_wish"):
        st.session_state.wishlist.clear()
        st.rerun()


def page_cart():
    section_title("🛒 Keranjang Belanja")

    if not st.session_state.cart:
        st.markdown(
            """
        <div style="text-align:center;padding:4rem 1rem;">
            <div style="font-size:3rem">🛒</div>
            <p style="color:#6B6B6B;font-style:italic;">Keranjang masih kosong</p>
            <p style="color:#3A3A3A;font-size:0.8rem">Yuk tambahkan produk favoritmu!</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("Mulai Belanja →", key="cart_shop"):
            go_to("home")
        return

    for pid, qty in list(st.session_state.cart.items()):
        p = get_product(pid)
        if not p:
            continue
        with st.container():
            c_thumb, c_info, c_qty, c_sub = st.columns([1, 3, 2, 2])
            with c_thumb:
                st.image(get_img_url(p), use_container_width=True)
            with c_info:
                st.markdown(
                    f'<p style="font-weight:600;color:#F0EDE6;margin:0;font-size:0.85rem">{p["name"]}</p>'
                    f'<p style="color:#6B6B6B;font-size:0.72rem;margin:0.1rem 0">{p["category"]} · {p["gender"]}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p style="color:#C9A84C;font-family:\'Cormorant Garamond\',serif;font-size:0.95rem;margin:0">{fmt_price(p["price"])}</p>',
                    unsafe_allow_html=True,
                )
            with c_qty:
                q_cols = st.columns([1, 1, 1])
                with q_cols[0]:
                    if st.button("−", key=f"cartdec_{pid}"):
                        if st.session_state.cart.get(pid, 0) > 1:
                            st.session_state.cart[pid] -= 1
                        else:
                            del st.session_state.cart[pid]
                        st.rerun()
                with q_cols[1]:
                    st.markdown(f'<p style="text-align:center;margin-top:0.4rem;color:#F0EDE6">{qty}</p>', unsafe_allow_html=True)
                with q_cols[2]:
                    if st.button("+", key=f"cartinc_{pid}"):
                        st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                        st.rerun()
            with c_sub:
                st.markdown(
                    f'<p style="text-align:right;color:#7A6030;font-size:0.85rem;margin-top:0.4rem">{fmt_price(p["price"] * qty)}</p>',
                    unsafe_allow_html=True,
                )

        st.markdown('<div style="height:1px;background:#1C1C1C;margin:0.2rem 0"></div>', unsafe_allow_html=True)

    gold_divider()

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f'<p style="color:#6B6B6B;font-size:0.82rem">{cart_count()} item dalam keranjang</p>', unsafe_allow_html=True)
    with c2:
        st.markdown(
            f'<p style="text-align:right;font-family:\'Cormorant Garamond\',serif;'
            f'font-size:1.4rem;font-weight:700;color:#C9A84C">{fmt_price(cart_total())}</p>',
            unsafe_allow_html=True,
        )

    gold_divider()
    payment = st.selectbox("Metode Pembayaran", PAYMENT_METHODS, key="pay_method")

    if st.button("Checkout Sekarang →", use_container_width=True, key="checkout_btn"):
        order = {
            "id": f"SVR-{random.randint(10000, 99999)}",
            "items": dict(st.session_state.cart),
            "total": cart_total(),
            "date": datetime.now().strftime("%d %b %Y, %H:%M"),
            "status": "Diproses",
            "payment": payment,
        }
        st.session_state.orders.append(order)
        st.session_state.cart.clear()
        st.toast(f"✓ Pesanan #{order['id']} berhasil dibuat!", icon="📦")
        go_to("orders")

    if st.button("Kosongkan Keranjang", key="clear_cart_btn"):
        st.session_state.cart.clear()
        st.rerun()


def page_orders():
    section_title("📦 Pesanan Saya")

    if not st.session_state.orders:
        st.markdown(
            """
        <div style="text-align:center;padding:4rem 1rem;">
            <div style="font-size:3rem">📦</div>
            <p style="color:#6B6B6B;font-style:italic;">Belum ada pesanan</p>
            <p style="color:#3A3A3A;font-size:0.8rem">Pesanan kamu akan muncul di sini.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("Mulai Belanja →", key="orders_shop"):
            go_to("home")
        return

    STATUS_COLORS = {
        "Diproses": "#D4A944",
        "Dikemas": "#7AA3D4",
        "Dikirim": "#7AB87A",
        "Selesai": "#3D7A5A",
        "Dibatalkan": "#B04040",
    }
    STATUS_FLOW = ["Diproses", "Dikemas", "Dikirim", "Selesai"]

    for order in reversed(st.session_state.orders):
        sc = STATUS_COLORS.get(order.get("status"), "#6B6B6B")
        payment = order.get("payment", "-")

        st.markdown(
            f"""
        <div style="background:#1C1C1C;padding:0.6rem 1rem;display:flex;
            justify-content:space-between;align-items:center;margin-top:0.8rem;">
            <span style="color:#F0EDE6;font-weight:600;font-size:0.9rem">#{order['id']}</span>
            <span style="background:{sc};color:#0D0D0D;padding:0.15rem 0.7rem;
                font-size:0.7rem;font-weight:700;letter-spacing:0.08em">{order['status']}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown('<div style="background:#1A1A1A;padding:0.8rem 1rem;">', unsafe_allow_html=True)

            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f'<p style="color:#6B6B6B;font-size:0.75rem;margin:0">📅 {order["date"]}</p>', unsafe_allow_html=True)
            with c2:
                st.markdown(
                    f'<p style="text-align:right;font-family:\'Cormorant Garamond\',serif;'
                    f'font-size:1.1rem;font-weight:700;color:#C9A84C;margin:0">{fmt_price(order["total"])}</p>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                f'<p style="color:#6B6B6B;font-size:0.75rem;margin:0.4rem 0 0 0;">'
                f'💳 <span style="color:#F0EDE6;">{payment}</span></p>',
                unsafe_allow_html=True,
            )

            for pid, qty in order["items"].items():
                p = get_product(pid)
                if p:
                    st.markdown(
                        f'<p style="color:#F0EDE6;font-size:0.8rem;margin:0.2rem 0">'
                        f'{p["name"]} <span style="color:#6B6B6B">×{qty}</span></p>',
                        unsafe_allow_html=True,
                    )

            if order["status"] in STATUS_FLOW:
                step_idx = STATUS_FLOW.index(order["status"])
                dots = ""
                for i, _s in enumerate(STATUS_FLOW):
                    color = "#C9A84C" if i <= step_idx else "#3A3A3A"
                    dots += f'<span style="color:{color}">●</span>'
                    if i < len(STATUS_FLOW) - 1:
                        lc = "#C9A84C" if i < step_idx else "#3A3A3A"
                        dots += f'<span style="color:{lc}"> ─── </span>'
                st.markdown(f'<p style="margin:0.6rem 0 0.1rem 0;font-size:0.75rem">{dots}</p>', unsafe_allow_html=True)

                labels = "".join(
                    f'<span style="color:{"#C9A84C" if i <= step_idx else "#3A3A3A"};'
                    f'font-size:0.65rem;margin-right:1.5rem">{s}</span>'
                    for i, s in enumerate(STATUS_FLOW)
                )
                st.markdown(f'<p>{labels}</p>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        if order["status"] not in ("Selesai", "Dibatalkan"):
            btn_cols = st.columns([2, 1, 1])
            status_idx = STATUS_FLOW.index(order["status"]) if order["status"] in STATUS_FLOW else -1

            if order["status"] == "Dikirim":
                with btn_cols[0]:
                    if st.button("✓ Pesanan Diterima", key=f"recv_{order['id']}"):
                        order["status"] = "Selesai"
                        st.rerun()
            elif status_idx < len(STATUS_FLOW) - 1:
                with btn_cols[0]:
                    if st.button("Simulasi Status →", key=f"next_{order['id']}"):
                        order["status"] = STATUS_FLOW[status_idx + 1]
                        st.rerun()

            if order["status"] == "Diproses":
                with btn_cols[2]:
                    if st.button("Batalkan", key=f"cancel_{order['id']}"):
                        order["status"] = "Dibatalkan"
                        st.rerun()

        st.markdown('<div style="height:1px;background:#1C1C1C;margin:0.5rem 0"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN RENDER
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    page_login()
    st.stop()

render_header()
render_nav()

page = st.session_state.page
if page == "home":
    page_home()
elif page == "recom":
    page_recom()
elif page == "wishlist":
    page_wishlist()
elif page == "cart":
    page_cart()
elif page == "orders":
    page_orders()
else:
    page_home()
