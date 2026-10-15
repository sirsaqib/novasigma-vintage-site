#!/usr/bin/env python3
"""Generate brand pages for Sigma Vintage Wear from index.html CSS + brand data."""
import re, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
index = open(os.path.join(BASE, "index.html")).read()
css = re.search(r"<style>(.*?)</style>", index, re.S).group(1)

IMG = {
 "denim":   "images/media-generation-denim-stack-0-0d57813b-f507-4249-98c7-aedd43def70e.jpg",
 "tees":    "images/media-generation-tees-stack-0-42fb06d3-ae96-453f-a521-762aa0a49093.jpg",
 "flannel": "images/media-generation-flannel-jackets-0-4956d4c4-bf27-4ed5-8510-a09960d58bd6.jpg",
 "leather": "images/media-generation-leather-jackets-0-300884f7-a43f-4b13-87b2-f2313a45dfe6.jpg",
 "sorting": "images/media-generation-sorting-hands-0-4c39a63a-a739-4402-8077-88d7312dcb73.jpg",
 "bale":    "images/media-generation-bale-closeup-0-b5d495c7-5459-4fb5-9f79-5c8d2ac77ab6.jpg",
 "ship":    "images/media-generation-container-loading-0-f4802f2c-c2b4-4ef0-ad33-703b5d592f12.jpg",
 "nike1": "images/wholesale/w-b-nike-1.jpg",
 "nike2": "images/wholesale/w-b-nike-2.jpg",
 "nike3": "images/wholesale/w-b-nike-3.jpg",
 "adidas1": "images/wholesale/w-b-adidas-1.jpg",
 "adidas2": "images/wholesale/w-b-adidas-2.jpg",
 "adidas3": "images/wholesale/w-b-adidas-3.jpg",
 "levis1": "images/wholesale/w-b-levis-1.jpg",
 "levis2": "images/wholesale/w-b-levis-2.jpg",
 "levis3": "images/wholesale/w-b-levis-3.jpg",
 "carhartt1": "images/wholesale/w-b-carhartt-1.jpg",
 "carhartt2": "images/wholesale/w-b-carhartt-2.jpg",
 "carhartt3": "images/wholesale/w-b-carhartt-3.jpg",
 "tommy1": "images/wholesale/w-b-tommy-1.jpg",
 "tommy2": "images/wholesale/w-b-tommy-2.jpg",
 "tommy3": "images/wholesale/w-b-tommy-3.jpg",
 "champion1": "images/wholesale/w-b-champion-1.jpg",
 "champion2": "images/wholesale/w-b-champion-2.jpg",
 "champion3": "images/wholesale/w-b-champion-3.jpg",
}

BRANDS = [
 dict(slug="nike", name="Nike",
      story="The swoosh moves faster than anything in vintage. Our Nike sorts pull single-stitch tees, 90s hoodies and track jackets — hand-checked, honestly graded, ready for your rails.",
      cats=[("T-Shirts","From $6.20/pc","nike1"),("Hoodies & Sweats","From $14/pc","nike2"),
            ("Track Jackets","From $15/pc","nike3"),("Shorts","From $5.50/pc","nike1")],
      prods=[
        ("50x Nike Vintage T-Shirts Bundle","Grade A","50 pcs","$310","nike1","Single-stitch & retro prints. Sizes S–XL assorted."),
        ("30x Nike Hoodies Bundle","Grade A","30 pcs","$420","nike2","Pullover & zip hoodies. Sizes S–XL assorted."),
        ("25x Nike Track Jackets Bundle","Grade A/B","25 pcs","$380","nike3","Full-zip track tops. Sizes M–XL."),
      ]),
 dict(slug="adidas", name="Adidas",
      story="Trefoil classics and 3-stripe staples with massive pull in EU streetwear. Our Adidas bundles are sorted by our team in Karachi and graded piece by piece.",
      cats=[("T-Shirts","From $5.90/pc","adidas1"),("Hoodies","From $13.50/pc","adidas2"),
            ("Track Tops","From $14.50/pc","adidas3"),("Shorts","From $5/pc","adidas1")],
      prods=[
        ("50x Adidas T-Shirts Bundle","Grade A","50 pcs","$295","adidas1","Trefoil & 3-stripe tees. Sizes S–XL assorted."),
        ("30x Adidas Hoodies Bundle","Grade A","30 pcs","$405","adidas2","Fleece hoodies. Sizes S–XL assorted."),
        ("25x Adidas Track Tops Bundle","Grade A/B","25 pcs","$365","adidas3","Tiro & retro track tops. Sizes M–XL."),
      ]),
 dict(slug="levis", name="Levi's",
      story="The backbone of every vintage store. 501s, trucker jackets and denim shorts — the most requested vintage on earth, sorted and graded in bulk.",
      cats=[("501 Jeans","From $13/pc","levis1"),("Denim Jackets","From $16/pc","levis2"),
            ("Denim Shorts","From $6.50/pc","levis3"),("Denim Shirts","From $8/pc","levis1")],
      prods=[
        ("40x Levi's 501 Jeans Bundle","Grade A","40 pcs","$520","levis1","Original 501s, mixed washes. Waists 28–38 assorted."),
        ("30x Levi's Denim Jackets Bundle","Grade A","30 pcs","$480","levis2","Trucker & rider jackets. Sizes S–XL assorted."),
        ("40x Levi's Denim Shorts Bundle","Grade B","40 pcs","$260","levis3","Cutoffs & shorts. Waists 26–36 assorted."),
      ]),
 dict(slug="carhartt", name="Carhartt",
      story="Workwear is luxury now. Duck canvas jackets, overalls and beanies with the best resale margins in the game — premium vintage, honestly graded.",
      cats=[("Work Jackets","From $22/pc","carhartt1"),("Overalls","From $18/pc","carhartt2"),
            ("Beanies & Accessories","From $6/pc","carhartt3"),("T-Shirts","From $6/pc","carhartt1")],
      prods=[
        ("25x Carhartt Work Jackets Bundle","Grade A/B","25 pcs","$550","carhartt1","Detroit & chore coats. Sizes M–XXL."),
        ("30x Carhartt Beanies Bundle","Grade A","30 pcs","$180","carhartt2","Knit beanies, mixed colours. One size."),
        ("40x Carhartt T-Shirts Bundle","Grade A","40 pcs","$240","carhartt3","Pocket & logo tees. Sizes S–XL assorted."),
      ]),
 dict(slug="tommy", name="Tommy Hilfiger",
      story="90s flag-logo everything. Tommy sweatshirts, polos and Harrington jackets are pure nostalgia stock — and nostalgia sells.",
      cats=[("Sweatshirts","From $11/pc","tommy1"),("Polo Shirts","From $7.25/pc","tommy2"),
            ("Harrington Jackets","From $16.40/pc","tommy3"),("Jeans","From $9/pc","tommy1")],
      prods=[
        ("30x Tommy Sweatshirts Bundle","Grade A","30 pcs","$330","tommy1","Flag-logo crews. Sizes S–XL assorted."),
        ("40x Tommy Polo Shirts Bundle","Grade A","40 pcs","$290","tommy2","Pique polos. Sizes S–XL assorted."),
        ("25x Tommy Harrington Jackets Bundle","Grade A/B","25 pcs","$410","tommy3","Light jackets. Sizes M–XL."),
      ]),
 dict(slug="champion", name="Champion",
      story="Reverse Weave is a streetwear essential. Champion hoodies, tees and sweats move in volume — perfect for high-turnover resellers.",
      cats=[("Hoodies","From $12/pc","champion1"),("T-Shirts","From $5.60/pc","champion2"),
            ("Sweatpants","From $10/pc","champion3"),("Shorts","From $5/pc","champion1")],
      prods=[
        ("30x Champion Hoodies Bundle","Grade A","30 pcs","$360","champion1","Reverse Weave & basic hoodies. Sizes S–XL."),
        ("50x Champion T-Shirts Bundle","Grade A","50 pcs","$280","champion2","C-logo & script tees. Sizes S–XL assorted."),
        ("30x Champion Sweatpants Bundle","Grade A/B","30 pcs","$300","champion3","Fleece joggers. Sizes S–XL assorted."),
      ]),
]

OTHERS = [(b["slug"], b["name"]) for b in BRANDS]

def page(b):
    slug, name = b["slug"], b["name"]
    others = " · ".join(f'<a href="brand-{s}.html" style="color:var(--gold)">{n}</a>' for s, n in OTHERS if s != slug)
    cats = "\n".join(
        f'<a class="cat-tile rv" href="#listings"><img src="{IMG[img]}" alt="{name} vintage {c}" loading="lazy"><div><h4>{c}</h4><span>{pr}</span></div></a>'
        for c, pr, img in b["cats"])
    prods = []
    for i, (pn, grade, pcs, price, img, desc) in enumerate(b["prods"]):
        prods.append(f"""
    <article class="pcard">
      <div class="pcard-img"><img src="{IMG[img]}" alt="{html.escape(pn)}" loading="lazy">
        <span class="grade-badge{' gb-b' if grade!='Grade A' else ''}">{grade}</span>
        <div class="pcard-quick"><button class="add-btn" style="width:100%;padding:13px" onclick="addIq({i})">+ Add to Inquiry</button></div></div>
      <div class="pcard-body"><div class="pcard-cat">{name} · Wholesale bundle</div><h3>{pn}</h3>
        <div class="pcard-spec">{pcs} · {desc}</div>
        <div class="pcard-foot"><div class="price">{price}<small> / bundle</small></div>
        <button class="add-btn" onclick="addIq({i})">Add +</button></div></div>
    </article>""")
    prods_html = "\n".join(prods)
    faq_json = f'''{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Where can I buy {name} vintage clothing wholesale?","acceptedAnswer":{{"@type":"Answer","text":"Sigma Vintage Wear supplies {name} vintage bundles in bulk from Karachi, shipping FOB worldwide to the USA, UK and EU."}}}}]}}'''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} Vintage Wholesale | Bulk {name} Bales & Bundles — Sigma Vintage Wear</title>
<meta name="description" content="Buy {name} vintage clothing wholesale — graded bundles of {name} tees, hoodies, jackets & more. FOB Karachi, ships to USA, UK & EU.">
<link rel="canonical" href="https://sigmavintagewear.com/brand-{slug}.html">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{faq_json}</script>
<style>{css}</style>
</head>
<body>
<div class="ticker" aria-hidden="true"><div class="ticker-track"><span>{name} vintage in stock</span><span class="dot">◆</span><span>FOB Karachi</span><span class="dot">◆</span><span>Ships to USA · UK · EU</span><span class="dot">◆</span><span>{name} vintage in stock</span><span class="dot">◆</span><span>FOB Karachi</span><span class="dot">◆</span><span>Ships to USA · UK · EU</span><span class="dot">◆</span></div></div>
<header class="site-header"><div class="header-inner">
<a class="brand" href="index.html"><img class="brand-mark" src="images/logo.png" alt="Sigma Vintage Wear logo"><span class="brand-name">SIGMA<small>VINTAGE WEAR</small></span></a>
<nav class="nav"><a class="nl" href="index.html#bales">Bales</a><a class="nl" href="retail.html">Retail</a><a class="nl" href="index.html#brands">Brands</a><a class="nl" href="index.html#grades">Grades</a><a class="nl" href="blog.html">Blog</a><a class="nl" href="index.html#faq">FAQ</a><a class="nl" href="index.html#contact">Contact</a></nav>
<div style="display:flex;gap:10px;align-items:center"><button class="btn" onclick="openIq()" style="padding:11px 24px">Get a Quote</button><button class="burger" onclick="document.getElementById('drawer').classList.add('open');document.getElementById('drawerOv').classList.add('open')">☰</button></div>
</div></header>
<div class="drawer-overlay" id="drawerOv" onclick="document.getElementById('drawer').classList.remove('open');this.classList.remove('open')"></div>
<aside class="drawer" id="drawer"><button class="drawer-close" onclick="document.getElementById('drawer').classList.remove('open');document.getElementById('drawerOv').classList.remove('open')">×</button>
<nav><a href="index.html">Home</a><a href="index.html#bales">Bales</a><a href="retail.html">Retail</a><a href="blog.html">Blog</a><a href="index.html#brands">Brands</a><a href="index.html#contact">Contact</a></nav></aside>

<section class="bp-hero"><div class="wrap bp-hero-inner">
<div class="blogo-wrap"><img src="images/logos/{slug}.webp" alt="{name} logo"></div>
<h1 class="display">{name} vintage<br>wholesale</h1>
<p>{b["story"]}</p>
<div class="bp-stats"><div><b>Grade A/B</b><span>Honest grading</span></div><div><b>FOB Karachi</b><span>Worldwide shipping</span></div><div><b>1 bundle</b><span>Minimum order</span></div></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div class="kicker rv">Categories</div><h2 class="sec-title display rv">Shop {name} by category</h2></div>
<div class="cat-tiles">{cats}</div>
</div></section>

<section class="sec" id="listings" style="background:var(--sand);padding-top:80px"><div class="wrap">
<div class="sec-head"><div class="kicker rv">Live listings</div><h2 class="sec-title display rv">{name} bundles</h2>
<p class="sec-sub rv">Sizes are assorted S–XL unless stated — size ratios available on request before you order.</p></div>
<div class="prod-scroll rv" id="bpListings">{"".join(prods)}</div>
</div></section>

<section class="sec" style="background:var(--ink);color:#fff;padding:70px 0"><div class="wrap" style="display:flex;align-items:center;gap:32px;flex-wrap:wrap;justify-content:space-between">
<div style="flex:1;min-width:260px"><div class="kicker" style="color:var(--gold)">Retail</div>
<h2 class="display" style="font-size:clamp(28px,3.5vw,44px);margin-bottom:8px">Want single {name} pieces?</h2>
<p style="color:rgba(255,255,255,.75)">Hand-picked {name} items, priced per piece.</p></div>
<a class="btn" href="retail.html#{slug}">Shop {name} retail →</a>
</div></section>

<section class="sec"><div class="wrap">
<div class="size-note rv"><b>Size guide:</b> vintage bundles come in assorted sizes (mostly S–XL, some M–XXL for workwear). Need a specific size run? Message us on WhatsApp before ordering and we will pull it.</div>
<div class="sec-head" style="margin-top:50px"><div class="kicker rv">Keep exploring</div><h2 class="sec-title display rv" style="font-size:clamp(30px,4vw,48px)">Also shop</h2>
<p class="sec-sub rv">{others}</p></div>
<div style="text-align:center;margin-top:10px"><a class="btn" href="index.html">← Back to homepage</a></div>
</div></section>

<footer><div class="wrap">
<div class="foot-grid"><div class="foot-brand"><span class="brand-name" style="color:#fff">SIGMA<small>VINTAGE WEAR</small></span>
<p>Graded vintage clothing wholesale from Karachi to the world.</p></div>
<div><h4>Shop</h4><a href="index.html#bales">All bales</a><a href="retail.html">Retail shop</a><a href="index.html#brands">Shop by brand</a><a href="index.html#calculator">Profit calculator</a></div>
<div><h4>Brands</h4>{"".join(f'<a href="brand-{s}.html">{n} vintage</a>' for s,n in OTHERS)}</div>
<div><h4>Company</h4><a href="index.html#process">Our process</a><a href="index.html#payments">Payment terms</a><a href="index.html#contact">Contact</a></div></div>
<div class="foot-bottom"><span>© 2026 Sigma Vintage Wear · Karachi, Pakistan</span><span>All prices USD, FOB Karachi</span></div>
</div></footer>

<div class="iq-overlay" id="iqOv" onclick="closeIq()"></div>
<aside class="iq" id="iq"><div class="iq-head"><h3>Your Inquiry</h3><button class="iq-close" onclick="closeIq()">×</button></div>
<div class="iq-items" id="iqItems"></div>
<div class="iq-foot"><div class="iq-total"><span>Estimated total</span><span id="iqTotal">$0</span></div>
<button class="btn" style="width:100%" onclick="sendIq()">Send Inquiry on WhatsApp</button></div></aside>
<button class="fab" onclick="openIq()">🧺 Inquiry <span class="cnt" id="fabCnt">0</span></button>

<script>
const WA = "923231926873";
const PRODS = [{",\n".join('{n:"'+p[0]+'",p:"'+p[3]+'",g:"'+p[1]+'",s:"'+p[2]+'"}' for p in b["prods"])}];
let IQ=[];
function addIq(i){{ const p=PRODS[i]; if(!IQ.includes(p)) IQ.push(p); renderIq(); openIq(); }}
function renderIq(){{ const box=document.getElementById("iqItems"); document.getElementById("fabCnt").textContent=IQ.length;
box.innerHTML = IQ.length ? IQ.map((p,i)=>`<div class="iq-item"><div><div class="nm">${{p.n}}</div><div class="pr">${{p.p}} · ${{p.g}} · ${{p.s}}</div></div><button class="iq-rm" onclick="IQ.splice(${{i}},1);renderIq()">×</button></div>`).join("")
: `<div class="iq-empty">Your inquiry list is empty.</div>`;
const tot = IQ.reduce((s,p)=>s+parseInt(p.p.replace(/[^0-9]/g,"")),0);
document.getElementById("iqTotal").textContent="$"+tot.toLocaleString(); }}
function openIq(){{ renderIq(); document.getElementById("iq").classList.add("open"); document.getElementById("iqOv").classList.add("open"); }}
function closeIq(){{ document.getElementById("iq").classList.remove("open"); document.getElementById("iqOv").classList.remove("open"); }}
function sendIq(){{ if(!IQ.length) return alert("Add a bundle first.");
const lines=IQ.map((p,i)=>`${{i+1}}. ${{p.n}} — ${{p.p}} (${{p.g}}, ${{p.s}})`).join("\\n");
window.open("https://wa.me/"+WA+"?text="+encodeURIComponent("Assalam-o-Alaikum! Quote please for {name} vintage:\\n\\n"+lines)," _blank"); }}
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add("on");io.unobserve(e.target);}}}}),{{threshold:.12}});
document.querySelectorAll(".rv").forEach(el=>io.observe(el));
/* Central CMS: admin panel publishes to data/products.json + data/categories.json */
(function(){{
  const BRAND="{name}";
  fetch("data/products.json").then(r=>{{if(!r.ok)throw 0;return r.json();}}).then(all=>{{
    const list=all.filter(p=>p.type==="wholesale"&&p.brand===BRAND);
    if(!list.length)return;
    document.getElementById("bpListings").innerHTML=list.map(p=>`
    <article class="pcard"><div class="pcard-img"><img src="${{p.img}}" alt="${{p.name}}" loading="lazy">
      <span class="grade-badge${{p.grade&&p.grade!=="A"?" gb-b":""}}">Grade ${{p.grade||"A"}}</span>
      <div class="pcard-quick"><button class="add-btn" style="width:100%;padding:13px" onclick="addIqB('${{p.id}}')">+ Add to Inquiry</button></div></div>
      <div class="pcard-body"><div class="pcard-cat">${{BRAND}} · Wholesale bundle</div><h3>${{p.name}}</h3>
      <div class="pcard-spec">${{p.pcs?p.pcs+" pcs · ":""}}${{p.sizes||""}} ${{p.desc?"· "+p.desc:""}}</div>
      <div class="pcard-foot"><div class="price">$${{p.price}}<small> / bundle</small></div>
      <button class="add-btn" onclick="addIqB('${{p.id}}')">Add +</button></div></div></article>`).join("");
    PRODS.length=0;
    list.forEach(p=>PRODS.push({{n:p.name,p:"$"+p.price,g:"Grade "+(p.grade||"A"),s:((p.pcs?p.pcs+" pcs ":"")+(p.sizes||"")).trim(),_id:p.id}}));
  }}).catch(()=>{{}});
  window.addIqB=function(id){{
    const p=PRODS.find(x=>x._id===id);
    if(p&&!IQ.includes(p))IQ.push(p); renderIq(); openIq();
  }};
}})();
</script>
<a class=\"wa-float\" href=\"https://wa.me/923231926873?text=Assalam-o-Alaikum%21%20I%20have%20a%20question%20about%20Sigma%20Vintage%20Wear.\" target=\"_blank\" rel=\"noopener\" aria-label=\"Chat on WhatsApp\"><svg viewBox=\"0 0 32 32\"><path d=\"M16 3C9.4 3 4 8.4 4 15c0 2.4.7 4.6 2 6.5L4 29l7.7-2c1.8 1 3.9 1.6 6.1 1.6h.1c6.6 0 12-5.4 12-12S22.6 3 16 3zm0 21.8c-1.9 0-3.7-.5-5.3-1.5l-.4-.2-4.6 1.2 1.2-4.4-.3-.4c-1-1.6-1.6-3.5-1.6-5.5 0-5.4 4.4-9.8 9.9-9.8s9.9 4.4 9.9 9.8-4.5 9.8-9.8 9.8zm5.4-7.3c-.3-.2-1.8-.9-2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.2-.7-1.7-1-2.4-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.2-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.2-.6-.4z\"/></svg></a>
</body>
</html>"""

for b in BRANDS:
    out = os.path.join(BASE, f"brand-{b['slug']}.html")
    open(out, "w").write(page(b))
    print("wrote", out, len(open(out).read())//1024, "KB")
