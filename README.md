<div align="center">

# ⚡ Mandate Radar: The Auto Debits Nobody Can Find

**Fintech Track Solution · Best Use of Neo4j**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph_Database-008CC1?logo=neo4j&logoColor=white)](https://neo4j.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Money leaves bank accounts every month for recurring commitments people forgot they agreed to. Mandate Radar discovers them, resolves raw statement descriptors via a Neo4j knowledge graph, catches stealth price increases, and guides users through the correct mechanism-specific revocation path.*

</div>

---

## 📌 1. The Problem in One Paragraph

Money leaves every month for things people forgot they agreed to. Bank applications show mandates in one place, if at all. Statement descriptors are compressed strings designed for automated clearing systems rather than people (`GOOGLE*YOUTUBE G.CO/HELPPAY`, `AMZN PRIME IN*849204`, `ACH D ICICI LOMBARD GIC`). Cancellation differs fundamentally by payment mechanism, and merchants have zero incentive to explain the right route. A price increase inside an existing auto-debit is nearly invisible, which is precisely why it is done that way.

## 💡 2. The Solution

Mandate Radar reads bank statements and returns four things:

1. **Every recurring commitment**, including ones that are irregular in amount or interval (monthly, quarterly, annual, drifting billing dates).
2. **What each one really is**, resolved from raw descriptors to a verified merchant, its parent corporate conglomerate, and its payment mechanism.
3. **What is wrong with it**:
   - **Silent Price Creep**: Step increases inside stable series (e.g., YouTube Premium sneaking from ₹129 to ₹149 in Sept, +₹240/yr).
   - **Trial Conversion Traps**: Nominal verification charges (₹2) auto-escalating by ≥10x into recurring plans (Spotify 59.5x jump).
   - **Dormant / Zombie Charges**: Continuous debits for services unutilized for 75+ days (Cult.fit 96 days idle; Truecaller 84 days idle).
4. **How to stop it**: The exact operational cancellation route for that specific rail, an escalation path under RBI/CCPA regulations if the merchant ignores requests, and a customizable legal revocation notice.

The hero screen centers on one behavioral metric: **₹X a year, committed**, featuring an interactive **Tick-To-Cancel Savings Simulator**.

---

## 🕸️ 3. Why Neo4j is the Star of the Solution

Merchant identity, payment rails, corporate ownership, and cancellation routes are **graph relationship problems, not flat lookup problems**. The same descriptor means different things depending on who bills it and through which mechanism.

```
(:Descriptor)-[:RESOLVES_TO]->(:Merchant)-[:OWNED_BY]->(:Parent)
(:Merchant)-[:BILLED_VIA]->(:Mechanism)-[:CANCELLED_BY]->(:CancellationPath)
(:CancellationPath)-[:ESCALATES_TO]->(:EscalationStep)
(:Person)-[:HAS_MANDATE]->(:Mandate)-[:FOR]->(:Merchant)
(:Mandate)-[:VIA_MECHANISM]->(:Mechanism)
(:Mandate)-[:HAD_CHARGE]->(:Charge)
```

### What Neo4j Achieves That Flat Tables Cannot:

| Case | Flat SQL Table Approach | Neo4j Knowledge Graph Traversal |
|---|---|---|
| **Google Play / YouTube Premium Trap** | Hard-coded lookup fails when billing mechanism varies. Directs user to the YouTube app where cancellation does not exist. | Traversal `(Descriptor)-[:RESOLVES_TO]->(m:Merchant)-[:BILLED_VIA]->(mech:Mechanism)` resolves mechanism to `PLAY_STORE`, guiding the user: *"Cancel in Play Store Subscriptions, NOT inside the app"*. |
| **Multi-Subscription Conglomerate Footprint** | Requires multiple disjoint table queries across accounts to see corporate exposure. | One Cypher traversal `MATCH (p:Parent)<-[:OWNED_BY]-(m:Merchant)<-[:FOR]-(mand:Mandate) RETURN p.name, collect(m.name), sum(mand.annual_cost)` reveals total exposure across Google (YouTube + Google One + Workspace), Amazon (Prime + Audible + AWS), or Microsoft. |
| **Cross-Mechanism Cancellation & Escalation** | Rigid schema unable to handle differing legal authorities (NPCI vs RBI vs CCPA). | Payment mechanism is a first-class node. Traversal to `(:CancellationPath)` and `(:EscalationStep)` dynamically produces statutory SLAs, RBI circular citations, and dispute timelines. |
| **Catalog Extensibility** | Schema migrations and table updates needed for every new merchant. | Adding a new merchant takes 1 node and 3 relationships with zero schema downtime. |

---

## 📚 4. Hand-Built Reference Knowledge Base (76 Merchants)

Unknown descriptors are **never hallucinated or guessed**. The reference graph was assembled and reviewed covering **76 Indian & global merchants** across OTT, SaaS, Cloud, Fitness, FinTech, and DTH:

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

The detection engine uses **deterministic Python / Pandas logic**, operating strictly on dates, descriptors, and amounts without relying on planted labels:

1. **Interval Inference with Tolerance Bands**:
   - Monthly: 24 to 36 days (median gap ±5 days)
   - Quarterly: 80 to 100 days (median gap ±10 days)
   - Annual: 350 to 380 days (median gap ±15 days)
2. **Amount Stability & Silent Price Hike**:
   - Identifies step increases > 3% in an otherwise stable cadence.
   - Computes exact step % increase and annualized extra cost.
3. **Trial Conversion Traps**:
   - Identifies nominal trial initiation charges (₹1 to ₹5) immediately auto-escalating by ≥ 10x to full subscription rates.
4. **Dormant / Zombie Subscriptions**:
   - Cross-referenced with service telemetry: Flags live mandates with **≥ 75 days of zero login/usage** where at least 2 recurring charges cleared.
5. **Hard Negatives Successfully Eliminated (0% False Positives)**:
   - **Weekly Groceries** (*Zepto Delivery*): 5–7 day interval rejected as sub-monthly discretionary orders.
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

### 4-Tier Legal Escalation Chain if Merchant Does Not Respond:
1. **Tier 1 (48h SLA)**: Written Revocation Notice to Merchant Support & India Grievance Officer.
2. **Tier 2 (14 Days)**: Issuing Bank Chargeback & Standing Instruction Block under RBI Master Directions.
3. **Tier 3 (30 Days)**: RBI Integrated Ombudsman (CMS Portal - cms.rbi.org.in).
4. **Tier 4**: National Consumer Helpline (NCH 1915 / consumerhelpline.gov.in) for CCPA Dark Patterns (Forced Continuity).

---

## 📊 7. Ground Truth Benchmark Results

Run via the live endpoint `GET /api/benchmark`:

| Metric | Result | Ground Truth Status |
|---|---|---|
| **Planted Mandates Recall** | **100.0%** (10 of 10 detected) | **PASS** |
| **Silent Price Creep** | **100% Caught** (YouTube Premium: ₹129 ➔ ₹149 in Sept, +₹240/yr) | **PASS** |
| **Trial Trap Conversion** | **100% Caught** (Spotify: ₹2 trial verification ➔ ₹119 recurring, 59.5x jump) | **PASS** |
| **Zombie Subscriptions** | **100% Caught** (Cult.fit: 96d idle; Truecaller: 84d idle) | **PASS** |
| **Hard Negatives Filtered** | **3 of 3 correctly rejected** (0.0% False Positive Rate) | **PASS** |

---

## 🚀 8. Quick Start / Running the Project

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Node.js 18+ (Optional: only needed if building the frontend from source)

### Run with 1 Command:
```bash
# Clone the repository
git clone https://github.com/kekwlboy12469/mandate-radar.git
cd mandate-radar

# Install Python dependencies
pip install -r backend/requirements.txt

# Start the unified server
python run.py
```
Open **`http://127.0.0.1:8000`** in your browser!

### Running with Live Neo4j Aura (Optional):
Mandate Radar works out-of-the-box using its **Embedded High-Fidelity Graph Engine**. To connect to your live Neo4j Aura instance:
1. Click **"Neo4j Aura Config"** in the top navigation.
2. Enter your Bolt URI (`neo4j+s://...`), username, and password.
3. Click **"Test & Sync"**.

---

## 📁 9. Repository Structure

```
mandate-radar/
├── backend/
│   ├── main.py              # FastAPI server, REST routes & static SPA mount
│   ├── detector.py          # Deterministic Pandas interval & anomaly detection engine
│   ├── reference_data.py    # Hand-built 76 merchant reference knowledge base & parents
│   ├── neo4j_service.py     # Neo4j driver + embedded graph engine + Cypher generator
│   ├── synthetic_data.py    # 12-month synthetic statement, usage feed & RBI notifications
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Hero Screen, Mandate cards, Cancellation wizard & tabs
│   │   ├── main.tsx         # React root
│   │   ├── style.css        # Tailwind CSS imports & styles
│   │   └── components/
│   │       └── GraphCanvas.tsx # Concentric Force-Directed Neo4j Graph Visualizer
│   ├── index.html           # HTML template
│   ├── package.json         # React 19, Lucide, Tailwind v4
│   ├── tsconfig.json        # TypeScript configuration
│   ├── vite.config.ts       # Vite build & proxy config
│   └── dist/                # Pre-compiled production web assets
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── run.py                   # Root 1-command application runner
└── README.md                # Project documentation
```

---

## 📜 10. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
