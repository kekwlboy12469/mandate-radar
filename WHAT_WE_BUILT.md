# ⚡ Mandate Radar: What We Have Built So Far

**Theme:** Fintech — The Auto Debits Nobody Can Find  
**Track:** Neo4j (Best Use of Neo4j Track Solution)  
**Data Policy:** 100% Synthetic & Anonymized (No real financial data or real PII used)  
**Repository:** [https://github.com/kekwlboy12469/mandate-radar](https://github.com/kekwlboy12469/mandate-radar)  
**Local App URL:** `http://127.0.0.1:8000` (Unified Runner: `python run.py`)

---

## 📌 1. Problem Statement & Core Mission

Every month, automated debits quietly withdraw money from consumer bank accounts for subscriptions and recurring services people forgot they agreed to. Bank interfaces fail to resolve this because:

1. **Cryptic Statement Narrations:** Bank slips display compressed, technical strings designed for clearing switches rather than humans (`GOOGLE*YOUTUBE G.CO/HELPPAY`, `AMZN PRIME IN*849204`, `NOVI DIGITAL HOTSTAR`, `ACH D ICICI LOMBARD GIC`).
2. **Cancellation Fragmented by Payment Rail:** Deleting an app or closing an account does **not** stop recurring debits. Cancellation varies fundamentally by payment rail:
   - **UPI AutoPay:** NPCI Central Switch PIN revocation inside payment applications.
   - **Card Standing Instructions (e-Mandates):** Merchant settings plus issuing bank e-Mandate portal revocation under RBI Master Directions (DPSS.CO.PD.No.S513/02.14.003/2021-22).
   - **Bank NACH / eNACH:** Unique Mandate Reference Number (UMRN) stop-mandate procedure.
   - **Google Play / Apple App Store:** Device OS subscription settings, preventing in-app dark patterns.
3. **Silent Price Increases:** Merchants introduce price creep inside existing active mandates without requiring user re-authentication.
4. **Trial Traps & Zombie Subscriptions:** Nominal ₹2 verification trials auto-escalate by 10x–60x into recurring plans; unused services debit continuously for months after zero account logins.

---

## 💡 2. The Solution Architecture

Mandate Radar reads statements and delivers four key pillars:

```
Bank Statement CSV / Synthetic Telemetry
                │
        Deterministic Engine (Pandas)
  [Interval Bands · Amount Stability · Trial Trap · Zombie]
                │                       │
      Neo4j Reference Graph    ◄─── Descriptor Resolution
 [76 Merchants · Parents · Rails]
                │
        FastAPI Backend (Python)
                │
        React 19 + Tailwind CSS Frontend
  - Hero Screen: ₹X a year, committed
  - Tick-To-Cancel Instant Savings Simulator
  - Interactive Concentric Neo4j Graph Canvas
  - Cypher Query Terminal & Seed CQL Generator
  - Cancellation Wizard & Draft Legal Notices
```

1. **Recurring Discovery:** Automatically extracts every recurring mandate, including those with irregular intervals or shifting calendar dates.
2. **Entity & Rail Resolution:** Normalizes raw descriptors into a verified merchant, corporate parent conglomerate, and underlying payment mechanism.
3. **Anomaly & Variance Flagging:** Detects silent price hikes, trial traps, and dormant/zombie debits.
4. **Actionable Revocation & Dispute Escalation:** Delivers rail-specific operational cancellation protocols, a 4-tier statutory RBI/CCPA escalation chain, and a customizable legal revocation notice studio.

The hero screen centers on one behavioral metric: **₹X a year, committed**, with an interactive **Revocation Staging & Savings Simulator**.

---

## 🕸️ 3. Why Neo4j is Central to the Solution

Merchant identity, corporate ownership, payment rails, and cancellation routes are **graph relationship problems, not flat lookup tables**. The same descriptor means different things depending on who bills it and through which mechanism.

### Cypher Graph Schema
```cypher
(:Descriptor)-[:RESOLVES_TO]->(:Merchant)-[:OWNED_BY]->(:Parent)
(:Merchant)-[:BILLED_VIA]->(:Mechanism)-[:CANCELLED_BY]->(:CancellationPath)
(:CancellationPath)-[:ESCALATES_TO]->(:EscalationStep)
(:Person)-[:HAS_MANDATE]->(:Mandate)-[:FOR]->(:Merchant)
(:Mandate)-[:VIA_MECHANISM]->(:Mechanism)
(:Mandate)-[:HAD_CHARGE]->(:Charge)
```

### Graph Capabilities vs. Flat SQL Tables

| Use Case | Flat Relational Table Approach | Neo4j Knowledge Graph Traversal |
|---|---|---|
| **Google Play / YouTube Premium Trap** | Hard-coded lookup directs the user to the YouTube app where cancellation does not exist. | Traversal `(Descriptor)-[:RESOLVES_TO]->(m:Merchant)-[:BILLED_VIA]->(mech:Mechanism)` resolves mechanism to `PLAY_STORE`, guiding the user: *"Cancel in Play Store Subscriptions, NOT inside the app"*. |
| **Multi-Subscription Conglomerate Footprint** | Requires multiple disjoint table queries across accounts to see corporate exposure. | One Cypher traversal `MATCH (p:Parent)<-[:OWNED_BY]-(m:Merchant)<-[:FOR]-(mand:Mandate) RETURN p.name, collect(m.name), sum(mand.annual_cost)` reveals total exposure across Google (YouTube + Google One + Workspace), Amazon (Prime + Audible + AWS), or Microsoft. |
| **Cross-Mechanism Cancellation & Escalation** | Rigid schema unable to handle differing legal authorities (NPCI vs RBI vs CCPA). | Payment mechanism is a first-class node. Traversal to `(:CancellationPath)` and `(:EscalationStep)` dynamically produces statutory SLAs, RBI circular citations, and dispute timelines. |
| **Catalog Extensibility** | Schema migrations and table updates needed for every new merchant. | Adding a new merchant takes 1 node and 3 relationships with zero schema downtime. |

---

## 📚 4. Reference Knowledge Base (76 Verified Merchants)

Unknown descriptors are **never hallucinated or guessed**. The reference graph includes **76 hand-built and verified merchants** and 21 corporate parents across OTT, SaaS, Cloud, Fitness, FinTech, and DTH:

- **Alphabet Inc.**: YouTube Premium, Google One, Google Workspace, Google Play Pass
- **Amazon.com Inc.**: Amazon Prime India, Audible India, AWS Cloud, Kindle Unlimited
- **Microsoft Corp.**: Microsoft 365, Xbox Game Pass, GitHub Copilot, LinkedIn Premium
- **Apple Inc.**: Apple One, Apple Music, iCloud+ Storage, Apple TV+
- **Entertainment & Streaming**: Netflix, Spotify, Disney+ Hotstar, Sony LIV, ZEE5, JioCinema Premium
- **Food & Quick-Commerce**: Swiggy One, Zomato Gold
- **Health & Fitness**: Cult.fit (Cultpass), Fittr Coach, Apollo 24/7 Circle, Tata 1mg, PharmEasy Plus
- **Productivity & SaaS**: OpenAI (ChatGPT Plus), Claude Pro, Perplexity AI, Canva, Notion, Zoom, Figma, Slack, Jira, Trello, Zoho One, Freshworks, ClearTax
- **Insurance & Loans**: ICICI Lombard, HDFC ERGO, Bajaj Finserv Consumer EMI

---

## ⚙️ 5. Deterministic Detection Logic & Hard Negatives

The detection engine (`backend/detector.py`) uses **deterministic Python / Pandas logic**, operating strictly on dates, descriptors, and amounts without relying on planted labels:

1. **Cadence Inference with Tolerance Bands**:
   - Monthly: 24 to 36 days (median gap ±5 days)
   - Quarterly: 80 to 100 days (median gap ±10 days)
   - Annual: 350 to 380 days (median gap ±15 days)
2. **Amount Stability & Silent Price Creep**:
   - Identifies step increases > 3% in an otherwise stable series.
   - Computes exact step % increase and annualized extra cost (e.g., YouTube Premium +15.5% hike, adding ₹240/yr).
3. **Trial Conversion Traps**:
   - Identifies nominal trial initiation charges (₹1 to ₹5) immediately auto-escalating by ≥ 10x to full subscription rates (Spotify ₹2 verification jumping 59.5x to ₹119/mo).
4. **Dormant / Zombie Subscriptions**:
   - Cross-referenced with service telemetry: Flags live mandates with **≥ 75 days of zero login/usage** where at least 2 recurring charges cleared (Cult.fit 96 days idle; Truecaller 84 days idle).
5. **Hard Negatives Successfully Eliminated (0% False Positives)**:
   - **Weekly Groceries** (*Zepto Delivery*): 5–7 day interval rejected as sub-monthly discretionary basket orders.
   - **Fluctuating Electricity Bills** (*BESCOM Bangalore*): Monthly schedule rejected due to >3% variable meter consumption swings across multiple cycles.
   - **Ad-hoc Food Orders** (*Swiggy Food*): Irregular random intervals rejected.
   - **Genuine Unrecognised Mandate** (*ACME Cloud*): Correctly detected on recurring schedule and reported as "Unrecognised Merchant" without guessing.

---

## ⚖️ 6. Mechanism-Specific Cancellation & Legal Escalation

Mandate Radar provides tailored, mechanism-specific walkthroughs:

- **UPI AutoPay**: Step-by-step revocation inside Google Pay / PhonePe / Paytm Mandates with UPI PIN authentication (instant NPCI switch execution).
- **Card Standing Instructions (e-Mandate)**: Cancellation on merchant site plus bank-side revocation via the Issuing Bank's e-Mandate portal under RBI Circular DPSS.CO.PD.No.S513/02.14.003/2021-22.
- **Bank NACH / eNACH**: Formal revocation request with Unique Mandate Reference Number (UMRN).
- **Play Store / App Store**: Device subscription settings cancellation preventing app-side dark patterns.

### 4-Tier Legal Escalation Chain (If Ignored or Obstructed)
1. **Tier 1 (48h SLA)**: Written Revocation Notice to Merchant Support & India Grievance Officer under Consumer Protection (E-Commerce) Rules 2020.
2. **Tier 2 (14 Days)**: Issuing Bank Chargeback & Standing Instruction Block under RBI Master Directions.
3. **Tier 3 (30 Days)**: Reserve Bank of India Integrated Ombudsman (CMS Portal: cms.rbi.org.in).
4. **Tier 4**: National Consumer Helpline (NCH 1915 / consumerhelpline.gov.in) for CCPA Dark Patterns (Forced Continuity).

---

## 🎨 7. Modern Luxury Fintech UI & User Experience

The web interface is styled with a **Midnight Obsidian & Cobalt Glassmorphism** aesthetic (`#07090e` base, satin card depth, clean hairline borders):

1. **Executive Hero Screen**:
   - Large aggregate figure: **`₹65,623 / year, committed.`**
   - Monthly equivalent: `₹5,469 / mo` automated outflow across 10 mandates.
   - Identifiable leakage: `₹14,280 / yr` across 4 stealth anomalies.
   - **Interactive Savings Simulator:** "Stage All 4 Anomalies to Save ₹14,280/yr" with live animated progress gauge.
2. **Dual View Modes**:
   - **Card Grid View:** Rich cards with brand visual avatars (YouTube, Netflix, Spotify, Amazon, Cult.fit, ChatGPT), anomaly pills, statement narration insets, and protocol pitfall notes.
   - **Dense Ledger Table View:** Commercial banking ledger view (modeled after Ramp & Stripe) with inline stage checkboxes, cadence, and latest debit amounts.
3. **Neo4j Graph Visualizer & Cluster Constellations (`GraphCanvas.tsx`)**:
   - **High-DPI Retina/4K Canvas**: Dynamically measures physical container dimensions with `window.devicePixelRatio` for 100% crisp circular nodes and zero stretch distortion.
   - **Concentric Orbital Engine (Portfolio Mode - Default)**: Renders the active user portfolio cleanly across 31 nodes with collision clearance physics (`Person` at center ➔ `Mandates` inner ring ➔ `Merchants` middle ring ➔ `Parents/Rails` outer ring).
   - **Clustered Constellation Engine (Full 270-Node Catalog)**: Solves the traditional graph "hairball" problem by partitioning nodes into 7 galactic clusters (Alphabet, Amazon, Streaming, Productivity, Telecom, Payment Rails, User Portfolio).
   - **Smart Edge Labeling**: Edge labels are hidden by default to prevent visual noise, rendering on-demand with contrast capsule badges only on hover/selection or deep zoom (>1.35x).
   - **Directional Relationship Arrows**: Smooth directed lines indicating exact multi-hop traversals (`-[:OWNED_BY]->`, `-[:BILLED_VIA]->`, `-[:CANCELLED_BY]->`).
   - **Interactive Node Inspector (Neo4j Bloom style)**: Click any node to inspect properties, labels, and an auto-generated Cypher query snippet with 1-click clipboard copy and direct execution.
   - **Instant Node Search & Taxonomy Filter**: Locate any merchant or parent instantaneously, or isolate by node type (Person, Mandate, Merchant, Parent, Payment Rail).
4. **Live Cypher Query Workbench**:
   - Integrated terminal with 1-click presets:
     * *Parent Spend Rollup* (`MATCH (p:Parent)<-[:OWNED_BY]-(m:Merchant)<-[:FOR]-(mand:Mandate) ...`)
     * *Mechanism Cancellation Routing* (`MATCH (mand:Mandate)-[:VIA_MECHANISM]->(mech:Mechanism)-[:CANCELLED_BY]->(c:CancellationPath) ...`)
     * *Anomaly Risk Filter Pattern* (`MATCH (mand:Mandate)-[:FOR]->(m:Merchant) WHERE mand.flag <> 'HEALTHY' ...`)
     * *Statutory Rail SLAs* (`MATCH (mech:Mechanism) RETURN mech.name, mech.authority, mech.turnaround ...`)
   - Executes against either live Neo4j Aura clusters or the embedded graph engine.
   - Cypher DDL Seed Script viewer & download (`.cql`).
5. **Revocation Dossier Drawer**:
   - Slide-over panel containing rail-specific instructions, 4-tier statutory escalation chain, and a **Notice Drafting Studio** with tone selectors (*Standard*, *Statutory*, *Dispute Warning*) and 1-click clipboard copy.
6. **Pre-Debit Alert Feed**:
   - Correlates bank SMS/Push pre-debit notifications received 24 hours prior to mandate execution.
7. **CSV Ingestion Studio**:
   - Upload custom bank statement CSVs with automatic column resolution.

---

## 📊 8. Ground Truth Benchmark Results

Run via the live endpoint `GET /api/benchmark`:

| Metric | Result | Ground Truth Status |
|---|---|---|
| **Planted Mandates Recall** | **100.0%** (10 of 10 detected) | **PASS** |
| **Silent Price Creep** | **1/1 Caught** (YouTube Premium: ₹129 ➔ ₹149 in Sept, +₹240/yr) | **PASS** |
| **Trial Trap Conversion** | **1/1 Caught** (Spotify: ₹2 trial verification ➔ ₹119 recurring, 59.5x jump) | **PASS** |
| **Zombie Subscriptions** | **2/2 Caught** (Cult.fit: 96d idle; Truecaller: 84d idle) | **PASS** |
| **Hard Negatives Filtered** | **3 of 3 correctly rejected** (0.0% False Positive Rate) | **PASS** |

---

## 📂 9. Project Directory & File Inventory

```
c:\web\hackfront\
├── backend/
│   ├── main.py              # FastAPI server, REST routes & static SPA mount
│   ├── detector.py          # Deterministic Pandas interval & anomaly detection engine
│   ├── reference_data.py    # Hand-built 76 merchant catalog, parent corporate trees & rails
│   ├── neo4j_service.py     # Neo4j driver + embedded graph engine + Cypher generator
│   ├── synthetic_data.py    # 12-month synthetic statement, usage feed & RBI notifications
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Hero Screen, Mandate cards, Cancellation wizard & tabs
│   │   ├── main.tsx         # React root
│   │   ├── style.css        # Tailwind CSS luxury fintech styling & animations
│   │   └── components/
│   │       └── GraphCanvas.tsx # Concentric Force-Directed Neo4j Graph Visualizer
│   ├── index.html           # HTML template
│   ├── package.json         # React 19, Lucide, Tailwind v4
│   ├── tsconfig.json        # TypeScript configuration
│   ├── vite.config.ts       # Vite build & proxy config
│   └── dist/                # Pre-compiled production web assets
├── .gitignore               # Clean git rules (ignoring node_modules, pycache, env)
├── LICENSE                  # MIT License
├── run.py                   # Root 1-command application runner
├── README.md                # Main repository documentation
└── WHAT_WE_BUILT.md         # Detailed architectural & feature summary
```

---

## 🚀 10. How to Run

```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Start the unified application
python run.py
```
Open **`http://127.0.0.1:8000`** in your browser.
