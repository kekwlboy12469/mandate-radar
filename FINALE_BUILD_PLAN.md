# STEP ZERO: PRODUCT AUDIT AND FINALE BUILD PLAN

**Product:** Mandate Radar: The Auto Debits Nobody Can Find  
**Theme:** Fintech  
**Track:** Neo4j (Best Use of Neo4j)  
**Submission Due:** 4:00 PM, 21 November 2026  
**Finale Evaluation Target:** 12:00 PM, 22 November 2026  
**Repository:** [https://github.com/kekwlboy12469/mandate-radar](https://github.com/kekwlboy12469/mandate-radar)  

---

## 1. Where We Are (Current Prototype Status)

### What Works Today
- **Deterministic Detection Engine (`backend/detector.py`):**
  - **Cadence Inference:** Maps median charge intervals to monthly (24–36d), quarterly (80–100d), and annual (350–380d) bands with tolerance to absorb date drift and weekend clearing shifts.
  - **Silent Price Increase Detection:** Detects single step increases (>3%) in stable recurring series (e.g., YouTube Premium creeping from ₹129 to ₹149/mo in September, computing an extra ₹240/yr annualized leakage).
  - **Trial Conversion Traps:** Detects nominal initiation charges (₹2) escalating by ≥10x into recurring plans (Spotify 59.5x jump).
  - **Zombie / Dormant Charges:** Cross-references charges with service telemetry to flag mandates with **≥75 days of zero usage** and 2+ cleared debits (Cult.fit 96d idle; Truecaller 84d idle).
  - **Hard Negative Filtering (0% False Alarm Rate):** Deterministically rejects weekly groceries (Zepto: 6.5d median gap), fluctuating utility bills (BESCOM electricity: metered consumption variance >3%), and ad-hoc food delivery orders (Swiggy: chaotic distribution).
  - **Zero-Guessing Unrecognised Mandates:** Identifies regular recurring intervals for unknown descriptors (ACME Cloud) and reports them as "Unrecognised Merchant" without hallucination.
- **Reference Knowledge Graph (`backend/reference_data.py`, `backend/neo4j_service.py`):**
  - Hand-assembled reference catalog of **76 verified Indian and global merchants**, 21 corporate parent conglomerates (Alphabet, Amazon, Microsoft, Apple, Disney, Tata, Reliance, Swiggy, Zomato), 6 payment rails, and direct cancellation policies.
  - Generates a full 428-line declarative Cypher DDL seed script (`.cql`) with schema constraints and indexes.
  - Dual graph engine: connects to live Neo4j Aura clusters via the official Bolt driver, with a high-fidelity embedded in-memory graph engine for instant offline execution.
- **Frontend Dashboard (`frontend/src/App.tsx`, `components/GraphCanvas.tsx`):**
  - **Behavioral Hero View:** Bold headline metric showing **₹65,623 / year, committed** (₹5,469/mo baseline run-rate across 10 mandates).
  - **Interactive Staging Simulator:** Dynamically recalculates annual savings upon toggling mandates, with an automated "Stage All 4 Anomalies" action.
  - **Dual View Modes:** Grid card layout with brand visual avatars and dense tabular ledger view.
  - **Concentric Graph Canvas:** Solves the 270-node hairball problem by defaulting to an orbital active portfolio subgraph (31 nodes: Person ➔ Mandates ➔ Merchants ➔ Parents/Rails) with physical collision clearance and 1-click cluster filters (`Alphabet`, `Amazon`, `Streaming`, `Full Catalog`).
  - **Cancellation & Dispute Dossier:** Mechanism-specific cancellation instructions (Google Play, UPI AutoPay, Card SI, NACH), 4-tier statutory RBI/CCPA escalation chain (Merchant 48h SLA ➔ Bank SI Revocation ➔ RBI CMS ➔ NCH 1915), and a copyable legal notice drafting studio with tone switcher.
  - **CSV Statement Ingestion (`/api/upload-csv`):** Uploads raw CSV bank statements with auto-column resolution (Date, Descriptor, Debit/Amount, Reference) and malformed file validation.
- **Verification Scorecard (`/api/benchmark`):**
  - 100% recall on planted ground truth mandates (10/10).
  - 100% detection of planted price hikes, trial traps, and zombie charges.
  - 0.0% false positive rate on planted hard negatives.

### What is Mocked, Hardcoded, or Missing
- **Usage Telemetry Feed:** Synthetic dictionary in `synthetic_data.py`; not yet connected to live app-activity logs or screen-time feeds.
- **Notification Stream:** Pre-debit alerts are synthetic samples; not yet connected to an automated Android SMS listener or notification hook.
- **Live Neo4j Default State:** The app defaults to the embedded graph emulator; live Neo4j Aura requires pasting credentials in the UI modal rather than auto-connecting via pre-configured environment secrets.
- **Edge-Case Mandate Types:** Loans/EMIs with scheduled maturation end dates, variable postpaid mobile plans with fixed base commitments, and mid-cycle plan upgrades are not yet represented in the dataset.
- **Dispute Letter Generation:** Templates use deterministic regex slot-filling; dynamic contextual adaptation with an LLM is not yet connected.

---

## 2. Where We Will Be (By 12:00 PM, 22 November)

By the finale deadline, Mandate Radar will have the following working features, flows, and integrations:

1. **Live Neo4j Aura by Default:** Pre-wire and auto-connect to a live Neo4j AuraDB instance with pre-seeded constraints, indexes, and full 76-merchant reference topology on startup, with automated fallback.
2. **Deep Cypher Traversal Queries in the UI:**
   - **Corporate Conglomerate Aggregator:** 1-click query traversing `(Parent)<-[:OWNED_BY]-(Merchant)<-[:FOR]-(Mandate)` to roll up total household exposure across corporate umbrellas (e.g., total spend with Alphabet across YouTube, Google One, and Workspace).
   - **Mechanism Vulnerability Index:** Cypher traversal calculating what percentage of a user's committed outflow is on high-friction rails (NACH, Card SI) versus instant-revocation rails (UPI AutoPay).
   - **Multi-Account / Household Graph:** Model `(:Person)-[:OWNS_ACCOUNT]->(:Account)-[:HAS_MANDATE]->(:Mandate)` to allow multi-card/family audit traversals.
3. **Messy Statement & Multi-Bank Parser:**
   - Ingestion support for exported statement CSVs from major Indian banks (HDFC, SBI, ICICI, Axis) with auto-detection of inverted debit/credit columns, varied date formats (`DD/MM/YYYY`, `DD-Mon-YYYY`), and multi-line narrations.
4. **Expanded Synthetic Edge-Case Dataset:**
   - **Consumer EMIs with End Dates:** Differentiating loan/EMI auto-debits (which must not be cancelled to avoid CIBIL damage) from discretionary recurring subscriptions.
   - **Postpaid Telecom Base Mandates:** Disentangling fixed base line rental commitments from variable international roaming/data add-on charges.
5. **Contextual LLM Notice Drafting:**
   - Integration of an LLM drafting pipeline to tailor the cancellation email and statutory dispute letter with exact customer particulars, bank transaction reference numbers, and specific RBI Ombudsman grievance filing instructions.
6. **One-Click Dossier Export:**
   - Exporting the complete Mandate Revocation Dossier (evidence timeline, descriptor resolution, bank dispute letter) as a clean printable PDF / text package for bank dispute submission.

---

## 3. User Segments

### Primary Segment: The Over-Subscribed Digital Professional
- **Profile:** Urban salaried professionals, tech workers, and digital natives (ages 22–40) holding 2–4 credit cards and multiple UPI apps (GPay, PhonePe, Paytm).
- **Pain Point:** Subscribed to 10–20 digital services (OTT platforms, quick commerce VIP passes, fitness memberships, cloud storage, productivity SaaS) over multiple years. They lose ₹15,000–₹35,000 annually to forgotten free trials that silently converted, sneaky price hikes of ₹20–₹50/month that escape notice, and gym or app passes they stopped using months ago.
- **Value Delivered:** The single aggregate metric (**₹X/year, committed**) forces behavioral awareness, while the instant savings simulator and rail-specific cancellation wizard eliminate the friction of figuring out how to cancel.

### Additional Segment 1: Family Financial Stewards & Caregivers
- **Profile:** Individuals managing or auditing personal finances for non-tech-savvy family members (elderly parents, spouses, or teenage dependents).
- **Pain Point:** Senior citizens frequently fall prey to deceptive mobile VAS subscriptions, accidental annual auto-debits, or dark-pattern renewals on co-signed cards that they do not know how to dispute or revoke.
- **Value Delivered:** Allows the steward to upload a parent's bank statement, immediately surface every hidden mandate in plain language with parent company attribution, and generate formal bank-side cancellation notices quoting RBI circulars.

### Additional Segment 2: Freelancers, Solo Founders & Micro-SMBs
- **Profile:** Independent consultants, developers, agency owners, and bootstrap founders operating on personal or small-business accounts.
- **Pain Point:** Recurring SaaS tools (Figma, GitHub, Notion, OpenAI API, AWS, Zoom, Google Workspace) charge cards automatically. Abandoned project tools and unused seats continue to debit silently, bleeding operational runway.
- **Value Delivered:** Traverses corporate SaaS footprints, highlights price increases and dormant tool charges, and provides direct admin-level cancellation routes to protect operating cash flow.

---

## 4. Partner Tech Choice: Neo4j (Deepening Our Core Track)

### Why Neo4j?
Auto-debit detection and cancellation routing is fundamentally a **graph relationship problem, not a key-value or relational lookup problem**. 

A flat table requires complex, brittle multi-table JOINs and fails when billing rails diverge:
- `GOOGLE*YOUTUBE G.CO/HELPPAY` billed via `PLAY_STORE` requires cancelling in Google Play Subscriptions on Android, whereas the same merchant billed via `CARD_SI` requires logging into Google Payments and instructing the issuing bank.
- Flat schemas cannot dynamically traverse corporate conglomerates: when Amazon bills through Prime Video, Audible India, and AWS, only a graph traversal effortlessly surfaces the aggregate corporate footprint.

### Core Graph Schema
```cypher
(:Descriptor)-[:RESOLVES_TO]->(:Merchant)-[:OWNED_BY]->(:Parent)
(:Merchant)-[:BILLED_VIA]->(:Mechanism)-[:CANCELLED_BY]->(:CancellationPath)
(:CancellationPath)-[:ESCALATES_TO]->(:EscalationStep)
(:Person)-[:HAS_MANDATE]->(:Mandate)-[:FOR]->(:Merchant)
(:Mandate)-[:VIA_MECHANISM]->(:Mechanism)
(:Mandate)-[:HAD_CHARGE]->(:Charge)
```

### How We Will Deepen Neo4j for the Finale
1. **Live AuraDB Production Connection:** Transition from the embedded fallback engine to an active cloud-hosted Neo4j Aura instance with pre-warmed schema constraints, unique node indexes, and production Bolt driver pooling.
2. **Advanced Multi-Hop Cypher Traversal Algorithms:**
   - Multi-merchant parent footprint aggregation (`MATCH (p:Parent)<-[:OWNED_BY]-(m:Merchant)<-[:FOR]-(mand:Mandate) ...`).
   - Dynamic path discovery linking raw statement strings directly to statutory escalation steps:
     ```cypher
     MATCH path = (d:Descriptor {pattern: $desc})-[:RESOLVES_TO]->(m:Merchant)
                  -[:BILLED_VIA]->(mech:Mechanism)-[:CANCELLED_BY]->(c:CancellationPath)
                  -[:ESCALATES_TO]->(e:EscalationStep)
     RETURN path;
     ```
3. **Graph-Driven Vulnerability & Risk Scoring:** Using Cypher graph queries to compute a "Friction Score" based on the distribution of cancellation mechanisms (e.g., scoring NACH and Card SI as high-friction vs. UPI AutoPay as low-friction).
4. **Interactive Graph UI Filtering:** Expanding the frontend concentric canvas with live Cypher querying, allowing users to run custom Cypher statements directly from the web interface.

---

## 5. Definition of Done

> **"A complete end-to-end financial audit system where a user uploads any bank statement and receives an instant, verified annual commitment figure, zero-hallucination descriptor resolution to merchants and parents via Neo4j, deterministic flags for silent price hikes, trial traps, and zombie debits with 0% false alarms on hard negatives, and an actionable, rail-specific cancellation dossier with statutory RBI/CCPA escalation routes."**
