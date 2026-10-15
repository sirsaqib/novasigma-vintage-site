#!/usr/bin/env python3
"""Generate retail.html for Sigma Vintage Wear from index.html CSS + retail product data."""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))
index = open(os.path.join(BASE, "index.html")).read()
css = re.search(r"<style>(.*?)</style>", index, re.S).group(1)

# image files land in images/retail/ (renamed from Pexels downloads)
PRODUCTS = [
 ("r1", "Vintage Nike Swoosh Tee",        "Nike",           "T-Shirts",    "M",        18, "Light wash fade, no flaws",      "r1-tees.jpg"),
 ("r2", "Nike Vintage Hoodie",            "Nike",           "Hoodies",     "L",        35, "Excellent, soft fleece",          "r2-hoodies.jpg"),
 ("r3", "Adidas Trefoil Tee",             "Adidas",         "T-Shirts",    "M",        16, "Good, crisp print",               "r1-tees.jpg"),
 ("r4", "Adidas Track Top",               "Adidas",         "Jackets",     "L",        32, "Excellent, 3-stripe",             "r4-shirts-rack.jpg"),
 ("r5", "Levi's 501 Jeans",               "Levi's",         "Jeans",       "32W",      38, "Classic wash, excellent",         "r5-folded-jeans.jpg"),
 ("r6", "Levi's Trucker Jacket",          "Levi's",         "Jackets",     "M",        45, "Excellent, rigid denim",          "r6-levis-trucker.jpg"),
 ("r7", "Levi's Leather Trucker Jacket",  "Levi's",         "Jackets",     "L",        58, "Genuine leather, vintage patina", "r7-leather-jacket.jpg"),
 ("r8", "Carhartt Flannel Shirt",         "Carhartt",       "Shirts",      "L",        24, "Heavy flannel, excellent",        "r4-shirts-rack.jpg"),
 ("r9", "Tommy Flag Sweatshirt",          "Tommy Hilfiger", "Sweats",      "L",        28, "Flag logo, excellent",            "r9-sweatshirts.jpg"),
 ("r10","Tommy Hilfiger Polo",            "Tommy Hilfiger", "Shirts",      "M",        22, "Good, pique cotton",              "r10-polo.jpg"),
 ("r11","Champion Reverse Weave Hoodie",  "Champion",       "Hoodies",     "M",        30, "Excellent, heavy fleece",         "r2-hoodies.jpg"),
 ("r12","Champion C-Logo Tee",            "Champion",       "T-Shirts",    "S",        15, "Good, classic C print",           "r1-tees.jpg"),
]
BRANDS = ["All","Nike","Adidas","Levi's","Carhartt","Tommy Hilfiger","Champion"]
LOGOSLUGS = {"Nike":"nike","Adidas":"adidas","Levi's":"levis","Carhartt":"carhartt","Tommy Hilfiger":"tommy","Champion":"champion"}

# deep-link support: retail.html#nike etc.
slugmap = {"nike":"Nike","adidas":"Adidas","levis":"Levi's","carhartt":"Carhartt","tommy":"Tommy Hilfiger","champion":"Champion"}
cap_inner = ",".join(f'{k}:"{v}"' for k,v in slugmap.items())
json_brands_inner = ",".join(f'"{k}":1' for k in slugmap)

prods_js = ",\n".join(
    f'{{id:"{p[0]}",name:"{p[1]}",brand:"{p[2]}",cat:"{p[3]}",size:"{p[4]}",price:{p[5]},cond:"{p[6]}",img:"images/retail/{p[7]}"}}'
    for p in PRODUCTS)
chips = "\n".join(
    '<button class="chip" data-b="All">All</button>' if b=="All"
    else f'<button class="chip" data-b="{b}"><img src="images/logos/{LOGOSLUGS[b]}.webp" alt="{b}"></button>'
    for b in BRANDS)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Buy Vintage Clothing Online | Single Pieces — Sigma Vintage Wear</title>
<meta name="description" content="Shop hand-picked vintage clothing online — single pieces from Nike, Adidas, Levi's, Carhartt, Tommy Hilfiger & Champion. Every item graded & photographed.">
<link rel="canonical" href="https://sigmavintagewear.com/retail.html">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}
/* retail extras */
.retail-hero{{background:var(--ink) url('images/retail/hero-rack.webp') center/cover;position:relative;padding:110px 0 90px;overflow:hidden}}
.retail-hero::before{{content:"";position:absolute;inset:0;background:linear-gradient(120deg,rgba(20,16,12,.88),rgba(20,16,12,.45))}}
.retail-hero::after{{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 80% 20%,rgba(193,80,46,.28),transparent 60%)}}
.retail-hero h1{{font-size:clamp(46px,7vw,92px);margin-bottom:12px;position:relative;z-index:2}}
.retail-hero p{{color:rgba(255,255,255,.78);max-width:600px;position:relative;z-index:2;font-size:17px}}
.fbar{{position:sticky;top:67px;z-index:50;background:rgba(244,239,230,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:14px 0}}
.fbar-inner{{display:flex;gap:10px;overflow-x:auto;scrollbar-width:none;padding:2px}}
.fbar-inner::-webkit-scrollbar{{display:none}}
.chip{{flex:0 0 auto;background:#fff;border:1px solid var(--ink);color:var(--ink);border-radius:999px;padding:9px 20px;font-size:13.5px;font-weight:600;cursor:pointer;font-family:'Inter';transition:.25s;display:flex;align-items:center;justify-content:center;min-width:64px;min-height:44px}}
.chip img{{height:24px;width:auto;max-width:96px;object-fit:contain;display:block}}
.chip.active{{border-color:var(--rust);box-shadow:0 0 0 2px var(--rust);background:#fff;color:var(--ink)}}
.chip:hover{{border-color:var(--ink)}}
.rgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}}
@media(max-width:900px){{.rgrid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:600px){{.rgrid{{grid-template-columns:1fr}}}}
.size-tag{{position:absolute;top:14px;right:14px;background:var(--ink);color:#fff;font-size:11px;font-weight:700;letter-spacing:1px;padding:6px 12px;border-radius:999px}}
.qtyrow{{display:flex;align-items:center;gap:10px}}
.qbtn{{width:32px;height:32px;border-radius:50%;border:1px solid var(--line);background:#fff;font-size:18px;cursor:pointer;line-height:1}}
.cart-item{{display:flex;gap:12px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px;margin-bottom:10px}}
.cart-item img{{width:60px;height:60px;object-fit:cover;border-radius:8px}}
</style>
</head>
<body>
<div class="ticker" aria-hidden="true"><div class="ticker-track"><span>Hand-picked single pieces</span><span class="dot">◆</span><span>Every item graded &amp; photographed</span><span class="dot">◆</span><span>Ships worldwide</span><span class="dot">◆</span><span>Hand-picked single pieces</span><span class="dot">◆</span><span>Every item graded &amp; photographed</span><span class="dot">◆</span><span>Ships worldwide</span><span class="dot">◆</span></div></div>
<header class="site-header"><div class="header-inner">
<a class="brand" href="index.html"><img class="brand-mark" src="images/logo.png" alt="Sigma Vintage Wear logo"><span class="brand-name">SIGMA<small>VINTAGE WEAR</small></span></a>
<nav class="nav"><a class="nl" href="index.html#bales">Wholesale</a><a class="nl" href="retail.html">Retail</a><a class="nl" href="index.html#brands">Brands</a><a class="nl" href="blog.html">Blog</a><a class="nl" href="index.html#faq">FAQ</a><a class="nl" href="index.html#contact">Contact</a></nav>
<div style="display:flex;gap:10px;align-items:center"><button class="btn" onclick="openCart()" style="padding:11px 24px">Cart (<span id="cartN">0</span>)</button><button class="burger" onclick="document.getElementById('drawer').classList.add('open');document.getElementById('drawerOv').classList.add('open')">☰</button></div>
</div></header>
<div class="drawer-overlay" id="drawerOv" onclick="document.getElementById('drawer').classList.remove('open');this.classList.remove('open')"></div>
<aside class="drawer" id="drawer"><button class="drawer-close" onclick="document.getElementById('drawer').classList.remove('open');document.getElementById('drawerOv').classList.remove('open')">×</button>
<nav><a href="index.html">Home</a><a href="index.html#bales">Wholesale Bales</a><a href="retail.html">Retail Shop</a><a href="blog.html">Blog</a><a href="index.html#brands">Brands</a><a href="index.html#contact">Contact</a></nav></aside>

<section class="retail-hero"><div class="wrap">
<h1 class="display">Retail.<br>Hand-picked vintage.</h1>
<p>Single pieces, not bales. Every item is hand-selected, graded and photographed — what you see is exactly what ships.</p>
</div></section>

<div class="fbar"><div class="wrap"><div class="fbar-inner" id="brandChips">{chips}</div></div></div>

<section class="sec"><div class="wrap">
<div class="sec-head"><div class="kicker">Single pieces</div><h2 class="sec-title display">Shop the drop</h2>
<p class="sec-sub">Filter by brand. Add to cart and check out on WhatsApp.</p></div>
<div class="rgrid" id="rgrid"></div>
</div></section>

<section class="sec" style="background:var(--sand);padding-top:70px"><div class="wrap">
<div class="size-note"><b>How retail works:</b> prices are per piece in USD. Shipping is calculated at checkout based on your country — message us on WhatsApp and we confirm the total before you pay. Not the right size? New pieces land every week.</div>
<div style="text-align:center;margin-top:36px"><p style="margin-bottom:14px;color:#5c554b">Buying for a store? Get bulk pricing instead.</p><a class="btn btn-dark" href="index.html#bales">Shop wholesale bales →</a></div>
</div></section>

<footer><div class="wrap">
<div class="foot-grid"><div class="foot-brand"><span class="brand-name" style="color:#fff">SIGMA<small>VINTAGE WEAR</small></span>
<p>Graded vintage clothing — wholesale bales &amp; hand-picked retail, from Karachi to the world.</p></div>
<div><h4>Shop</h4><a href="index.html#bales">Wholesale bales</a><a href="retail.html">Retail shop</a><a href="index.html#brands">Shop by brand</a><a href="index.html#calculator">Profit calculator</a></div>
<div><h4>Brands</h4><a href="brand-nike.html">Nike vintage</a><a href="brand-adidas.html">Adidas vintage</a><a href="brand-levis.html">Levi's vintage</a><a href="brand-carhartt.html">Carhartt vintage</a><a href="brand-tommy.html">Tommy Hilfiger vintage</a><a href="brand-champion.html">Champion vintage</a></div>
<div><h4>Company</h4><a href="index.html#process">Our process</a><a href="index.html#payments">Payment terms</a><a href="index.html#faq">FAQ</a><a href="index.html#contact">Contact</a></div></div>
<div class="foot-bottom"><span>© 2026 Sigma Vintage Wear · Karachi, Pakistan</span><span>Retail prices in USD</span></div>
</div></footer>

<div class="iq-overlay" id="cartOv" onclick="closeCart()"></div>
<aside class="iq" id="cart"><div class="iq-head"><h3>Your Cart</h3><button class="iq-close" onclick="closeCart()">×</button></div>
<div class="iq-items" id="cartItems"></div>
<div class="iq-foot"><div class="iq-total"><span>Total</span><span id="cartTotal">$0</span></div>
<button class="btn" style="width:100%" onclick="checkout()">Checkout on WhatsApp</button></div></aside>

<script>
const WA="923231926873";
const BRANDMAP={{{cap_inner}}};
const JSON_BRANDS={{{json_brands_inner}}};
const FALLBACK_PRODUCTS=[
{prods_js}
];
let PRODUCTS=FALLBACK_PRODUCTS.slice();
/* Central CMS: admin panel publishes to data/products.json */
fetch("data/products.json").then(r=>{{if(!r.ok)throw 0;return r.json();}}).then(all=>{{
  const rt=all.filter(p=>p.type==="retail");
  if(rt.length){{PRODUCTS=rt;render();renderCart();}}
}}).catch(()=>{{}});
let brand="All", cart={{}};
function render(){{
  const g=document.getElementById("rgrid");
  const list=PRODUCTS.filter(p=>brand==="All"||p.brand===brand);
  g.innerHTML=list.map(p=>`
  <article class="pcard"><div class="pcard-img"><img src="${{p.img}}" alt="${{p.name}}" loading="lazy">
  <span class="size-tag">Size ${{p.size}}</span>
  <div class="pcard-quick"><button class="add-btn" style="width:100%;padding:13px" onclick="addCart('${{p.id}}')">+ Add to Cart</button></div></div>
  <div class="pcard-body"><div class="pcard-cat">${{p.brand}} · ${{p.cat}}</div><h3>${{p.name}}</h3>
  <div class="pcard-spec">${{p.cond}}</div>
  <div class="pcard-foot"><div class="price">$${{p.price}}<small> / piece</small></div>
  <button class="add-btn" onclick="addCart('${{p.id}}')">Add +</button></div></div></article>`).join("");
  document.querySelectorAll(".chip").forEach(c=>c.classList.toggle("active",c.dataset.b===brand));
}}
document.getElementById("brandChips").addEventListener("click",e=>{{
  const c=e.target.closest(".chip"); const b=c&&c.dataset.b; if(b){{brand=b;render();}}
}});
function addCart(id){{cart[id]=(cart[id]||0)+1;renderCart();openCart();}}
function chQty(id,d){{cart[id]=(cart[id]||0)+d;if(cart[id]<=0)delete cart[id];renderCart();}}
function renderCart(){{
  const box=document.getElementById("cartItems"),n=Object.values(cart).reduce((a,b)=>a+b,0);
  document.getElementById("cartN").textContent=n;
  const ids=Object.keys(cart);
  box.innerHTML=ids.length?ids.map(id=>{{const p=PRODUCTS.find(x=>x.id===id);return `
  <div class="cart-item"><img src="${{p.img}}" alt=""><div style="flex:1"><div style="font-weight:700;font-size:13.5px">${{p.name}}</div>
  <div style="font-size:13px;color:var(--rust);font-weight:700">$${{p.price}} · ${{p.size}}</div></div>
  <div class="qtyrow"><button class="qbtn" onclick="chQty('${{id}}',-1)">−</button><b>${{cart[id]}}</b><button class="qbtn" onclick="chQty('${{id}}',1)">+</button></div></div>`;}}).join("")
  :`<div class="iq-empty">Your cart is empty.<br>Add some vintage pieces.</div>`;
  const tot=ids.reduce((s,id)=>s+PRODUCTS.find(x=>x.id===id).price*cart[id],0);
  document.getElementById("cartTotal").textContent="$"+tot;
}}
function openCart(){{renderCart();document.getElementById("cart").classList.add("open");document.getElementById("cartOv").classList.add("open");}}
function closeCart(){{document.getElementById("cart").classList.remove("open");document.getElementById("cartOv").classList.remove("open");}}
function checkout(){{
  const ids=Object.keys(cart); if(!ids.length)return alert("Cart is empty.");
  const lines=ids.map((id,i)=>{{const p=PRODUCTS.find(x=>x.id===id);return `${{i+1}}. ${{p.name}} (${{p.size}}) x${{cart[id]}} — $${{p.price*cart[id]}}`;}});
  const tot=ids.reduce((s,id)=>s+PRODUCTS.find(x=>x.id===id).price*cart[id],0);
  const msg=`Assalam-o-Alaikum! I want to order (retail):\\n\\n${{lines.join("\\n")}}\\n\\nTotal: $${{tot}}\\nPlease confirm shipping to my country.`;
  window.open("https://wa.me/"+WA+"?text="+encodeURIComponent(msg),"_blank");
}}
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add("on");io.unobserve(e.target);}}}}),{{threshold:.12}});
document.querySelectorAll(".rv").forEach(el=>io.observe(el));
render();renderCart();
function applyHash(){{const h=location.hash.replace("#","");if(h&&JSON_BRANDS){{brand=BRANDMAP[h]||'All';render();}}}}
applyHash();window.addEventListener("hashchange",applyHash);
</script>
<a class=\"wa-float\" href=\"https://wa.me/923231926873?text=Assalam-o-Alaikum%21%20I%20have%20a%20question%20about%20Sigma%20Vintage%20Wear.\" target=\"_blank\" rel=\"noopener\" aria-label=\"Chat on WhatsApp\"><svg viewBox=\"0 0 32 32\"><path d=\"M16 3C9.4 3 4 8.4 4 15c0 2.4.7 4.6 2 6.5L4 29l7.7-2c1.8 1 3.9 1.6 6.1 1.6h.1c6.6 0 12-5.4 12-12S22.6 3 16 3zm0 21.8c-1.9 0-3.7-.5-5.3-1.5l-.4-.2-4.6 1.2 1.2-4.4-.3-.4c-1-1.6-1.6-3.5-1.6-5.5 0-5.4 4.4-9.8 9.9-9.8s9.9 4.4 9.9 9.8-4.5 9.8-9.8 9.8zm5.4-7.3c-.3-.2-1.8-.9-2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.2-.7-1.7-1-2.4-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.2-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.2-.6-.4z\"/></svg></a>
</body>
</html>"""

open(os.path.join(BASE, "retail.html"), "w").write(page)
print("wrote retail.html", len(page)//1024, "KB")
