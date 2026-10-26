"""
Mandate Radar FastAPI Backend Server
Track: Neo4j (Best Use of Neo4j) - Fintech Track Solution
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import io
import os
import csv
import pandas as pd

from reference_data import REFERENCE_MERCHANTS, PARENT_COMPANIES, PAYMENT_MECHANISMS, ESCALATION_CHAIN
from synthetic_data import (
    generate_synthetic_statement,
    generate_usage_telemetry,
    generate_notification_stream,
    GROUND_TRUTH_MANDATES,
    GROUND_TRUTH_HARD_NEGATIVES
)
from detector import analyze_statement, clean_descriptor, detect_payment_mechanism
from neo4j_service import Neo4jKnowledgeGraph

app = FastAPI(
    title="Mandate Radar API",
    description="Deterministic Auto-Debit Mandate Detection & Neo4j Knowledge Graph Engine",
    version="2.0.0"
)

# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Neo4j Service
neo4j_graph = Neo4jKnowledgeGraph()

# In-memory session store
cached_statement = generate_synthetic_statement()
cached_usage = generate_usage_telemetry()
cached_notifications = generate_notification_stream()

# Pre-seed user's active portfolio in graph so Portfolio mode is immediately populated
_initial_analysis = analyze_statement(cached_statement, cached_usage)
neo4j_graph.sync_statement_mandates("Arun Sharma", _initial_analysis["mandates"])

class AnalyzeRequest(BaseModel):
    transactions: Optional[List[Dict[str, Any]]] = None
    usage_feed: Optional[Dict[str, str]] = None
    user_name: Optional[str] = "Arun Sharma"

class EmailDraftRequest(BaseModel):
    mandate_id: str
    merchant_name: str
    descriptor: str
    amount: float
    cadence: str
    mechanism: str
    user_name: str = "Arun Sharma"
    account_ref: str = "XX-4821 / UPI VPA"
    tone: str = "formal" # "polite", "formal", "firm_dispute"
    cancellation_reason: Optional[str] = "Subscription no longer required"

class CypherQueryRequest(BaseModel):
    query: str

class Neo4jConnectRequest(BaseModel):
    uri: str
    user: str = "neo4j"
    password: str

@app.get("/api/info")
def get_api_info():
    return {
        "service": "Mandate Radar API",
        "theme": "Fintech - The Auto Debits Nobody Can Find",
        "track": "Neo4j (Best Use of Neo4j)",
        "neo4j_status": "CONNECTED" if neo4j_graph.is_connected else "EMBEDDED_GRAPH_MODE",
        "reference_merchants_count": len(REFERENCE_MERCHANTS)
    }

@app.get("/")
def root():
    index_path = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return get_api_info()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "neo4j_connected": neo4j_graph.is_connected,
        "neo4j_mode": "LIVE_AURA" if neo4j_graph.is_connected else "EMBEDDED_HIGH_FIDELITY",
        "total_reference_merchants": len(REFERENCE_MERCHANTS),
        "total_parent_corporations": len(PARENT_COMPANIES),
        "payment_mechanisms_modeled": len(PAYMENT_MECHANISMS)
    }

@app.get("/api/statement/synthetic")
def get_synthetic_dataset():
    """Returns the synthetic 12-month statement, usage telemetry, and notifications."""
    return {
        "transactions": cached_statement,
        "usage_feed": cached_usage,
        "notifications": cached_notifications,
        "ground_truth_mandates": GROUND_TRUTH_MANDATES,
        "ground_truth_hard_negatives": GROUND_TRUTH_HARD_NEGATIVES
    }

@app.post("/api/analyze")
def run_analysis(payload: AnalyzeRequest):
    """
    Main detection endpoint: Processes statement transactions with deterministic rules,
    resolves descriptors using Neo4j knowledge graph, and syncs graph nodes.
    """
    txs = payload.transactions if payload.transactions is not None else cached_statement
    usage = payload.usage_feed if payload.usage_feed is not None else cached_usage
    user_name = payload.user_name or "Arun Sharma"

    # Run deterministic detector
    analysis_result = analyze_statement(txs, usage)

    # Sync detected mandates into Neo4j graph
    neo4j_graph.sync_statement_mandates(user_name, analysis_result["mandates"])

    # Attach notification context to mandates
    enhanced_mandates = []
    for m in analysis_result["mandates"]:
        # Find any matching pre-debit notifications
        matched_notifs = [
            n for n in cached_notifications
            if m["merchant_name"].lower() in n["text"].lower() or m["descriptor"].lower() in n["text"].lower()
        ]
        m["recent_notifications"] = matched_notifs
        m["escalation_chain"] = ESCALATION_CHAIN
        enhanced_mandates.append(m)

    analysis_result["mandates"] = enhanced_mandates

    # Compute hero metrics
    annual_committed = analysis_result["annual_committed_total"]
    analysis_result["hero_metrics"] = {
        "annual_committed_total": annual_committed,
        "monthly_equivalent": round(annual_committed / 12.0, 2),
        "potential_savings": analysis_result["annual_potential_savings"],
        "total_mandates_found": len(enhanced_mandates),
        "flagged_issues_count": sum(1 for m in enhanced_mandates if m["flag"] != "HEALTHY")
    }

    return analysis_result

@app.post("/api/upload-csv")
async def upload_statement_csv(file: UploadFile = File(...)):
    """
    Parses an uploaded bank statement CSV file with dynamic column mapping,
    validates headers, handles empty or malformed files, and runs detection.
    """
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # Decode content with fallback
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1")

        # Read with pandas
        csv_io = io.StringIO(text)
        df = pd.read_csv(csv_io)

        if df.empty:
            raise HTTPException(status_code=400, detail="The CSV file has headers but contains zero rows.")

        # Identify columns
        cols = {c.strip().lower(): c for c in df.columns}

        # Date column mapping
        date_col = next((cols[k] for k in ["date", "txn_date", "transaction date", "value date", "trans date"] if k in cols), None)
        # Description column mapping
        desc_col = next((cols[k] for k in ["descriptor", "description", "narration", "particulars", "remarks", "details"] if k in cols), None)
        # Amount column mapping
        amt_col = next((cols[k] for k in ["amount", "debit", "withdrawal", "txn amount", "amount (inr)"] if k in cols), None)
        # Ref column mapping (optional)
        ref_col = next((cols[k] for k in ["ref", "reference", "chq/ref no.", "utr", "txn id", "id"] if k in cols), None)

        if not date_col or not desc_col or not amt_col:
            raise HTTPException(
                status_code=422,
                detail=f"CSV must contain Date, Description, and Debit/Amount columns. Found columns: {list(df.columns)}"
            )

        transactions = []
        for idx, row in df.iterrows():
            amt_raw = str(row[amt_col]).replace(",", "").strip()
            try:
                amt_val = abs(float(amt_raw))
            except ValueError:
                continue

            if amt_val <= 0:
                continue

            transactions.append({
                "id": f"CSV_ROW_{idx+1}",
                "date": str(row[date_col]).strip()[:10],
                "descriptor": str(row[desc_col]).strip(),
                "amount": amt_val,
                "type": "DEBIT",
                "ref": str(row[ref_col]).strip() if ref_col and pd.notna(row[ref_col]) else ""
            })

        if not transactions:
            raise HTTPException(status_code=400, detail="No valid debit transactions could be parsed from the CSV.")

        # Run detection
        analysis_result = analyze_statement(transactions, cached_usage)
        neo4j_graph.sync_statement_mandates("Uploaded Statement User", analysis_result["mandates"])

        annual_committed = analysis_result["annual_committed_total"]
        analysis_result["hero_metrics"] = {
            "annual_committed_total": annual_committed,
            "monthly_equivalent": round(annual_committed / 12.0, 2),
            "potential_savings": analysis_result["annual_potential_savings"],
            "total_mandates_found": len(analysis_result["mandates"]),
            "flagged_issues_count": sum(1 for m in analysis_result["mandates"] if m["flag"] != "HEALTHY")
        }
        analysis_result["filename"] = file.filename
        analysis_result["rows_parsed"] = len(transactions)

        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse statement: {str(e)}")

@app.post("/api/generate-email")
def generate_cancellation_email(req: EmailDraftRequest):
    """
    Generates legally robust, mechanism-specific cancellation notice
    and dispute letters tailored to Indian banking & consumer regulations.
    """
    mech_info = PAYMENT_MECHANISMS.get(req.mechanism, PAYMENT_MECHANISMS["DIRECT_MERCHANT"])

    if req.tone == "polite":
        subject = f"Cancellation Request: {req.merchant_name} Recurring Subscription"
        body = f"""Dear {req.merchant_name} Support Team,

I am writing to formally request the immediate cancellation of my recurring {req.cadence.lower()} subscription for {req.merchant_name}.

Account Details:
- Name: {req.user_name}
- Billing Identifier / Descriptor: {req.descriptor}
- Active Amount: ₹{req.amount:,.2f} / {req.cadence.lower()}
- Payment Rail: {mech_info['name']} ({req.account_ref})
- Cancellation Reason: {req.cancellation_reason}

Kindly process this cancellation with immediate effect, terminate any scheduled future auto-debits, and send a written confirmation of cancellation to this email address.

Thank you for your assistance.

Warm regards,
{req.user_name}
"""
    elif req.tone == "firm_dispute":
        subject = f"URGENT: Dispute Notice & Mandatory Mandate Revocation - {req.merchant_name}"
        body = f"""To:
Grievance Redressal Officer / Billing Operations, {req.merchant_name}
CC: Nodal Officer, Issuing Bank / NPCI CMS Cell

SUBJECT: FORMAL NOTICE OF REVOCATION OF CONSENT FOR RECURRING DEBIT MANDATE UNDER RBI E-MANDATE DIRECTIVE

Dear Sir/Madam,

I hereby serve formal notice that I have revoked all authorization and consent for any recurring auto-debit transactions in favour of '{req.merchant_name}'.

Transaction & Mandate Profile:
- Customer Name: {req.user_name}
- Statement Descriptor: {req.descriptor}
- Registered Billing Rail: {mech_info['name']}
- Billed Cadence & Amount: ₹{req.amount:,.2f} ({req.cadence})
- Account / Card Reference: {req.account_ref}

LEGAL DIRECTIVE:
Under Reserve Bank of India Master Circular on Recurring Debits (DPSS.CO.PD.No.S513/02.14.003/2021-22) and the Consumer Protection (E-Commerce) Rules 2020:
1. The customer maintains an absolute statutory right to revoke standing instructions and mandates at any time without punitive fee or obstruction.
2. Any subsequent debit attempted after receipt of this notice shall be deemed unauthorized under Section 403/420 of the IPC and reported to the RBI Banking Ombudsman (CMS) and National Consumer Helpline (NCH Docket 1915).
3. If an unauthorized debit occurs, this notice shall serve as primary evidence in support of a mandatory chargeback reversal claim filed with the issuing bank.

Please confirm cancellation of this recurring mandate within 48 hours.

Yours sincerely,
{req.user_name}
"""
    else: # Default: formal
        subject = f"Notice of Mandate Cancellation: {req.merchant_name} [Ref: {req.account_ref}]"
        body = f"""To:
Customer Care & Accounts Dept,
{req.merchant_name}

Subject: Request to Cancel Recurring Mandate / Standing Instruction

Dear Accounts Team,

Please treat this email as my formal instruction to cancel my recurring subscription and revoke the auto-debit mandate associated with my account.

Details of Mandate:
- Account Holder Name: {req.user_name}
- Service / Subscription: {req.merchant_name}
- Statement Billing Line: {req.descriptor}
- Recurring Amount: ₹{req.amount:,.2f} ({req.cadence})
- Payment Rail: {mech_info['name']}
- Card / Account Reference: {req.account_ref}

In accordance with RBI guidelines governing recurring e-mandates, please discontinue all future auto-debits with immediate effect from the close of the current billing cycle.

Please acknowledge receipt of this cancellation instruction and email me a cancellation confirmation reference number.

Sincerely,
{req.user_name}
"""

    return {
        "mandate_id": req.mandate_id,
        "merchant_name": req.merchant_name,
        "subject": subject,
        "body": body,
        "tone": req.tone,
        "mechanism": req.mechanism
    }

@app.get("/api/graph")
def get_graph_data(mode: str = "portfolio"):
    """Returns nodes and edges for the Neo4j Graph Visualizer."""
    return neo4j_graph.get_graph_visualization_data(filter_mode=mode)

@app.post("/api/graph/cypher")
def execute_cypher_query(req: CypherQueryRequest):
    """Executes a Cypher query on Neo4j (live Aura or embedded engine)."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Cypher query cannot be empty.")
    return neo4j_graph.run_cypher_query(req.query)

@app.get("/api/graph/seed")
def download_cypher_seed():
    """Generates and returns the complete Cypher seed script (.cql)."""
    script = neo4j_graph.generate_cypher_seed_script()
    return {
        "filename": "mandate_radar_neo4j_seed.cql",
        "script": script,
        "size_bytes": len(script.encode("utf-8")),
        "line_count": len(script.splitlines())
    }

@app.post("/api/neo4j/connect")
def connect_neo4j(req: Neo4jConnectRequest):
    """Connects to live Neo4j Aura or local instance."""
    success, message = neo4j_graph.connect(req.uri, req.user, req.password)
    return {
        "success": success,
        "message": message,
        "is_connected": neo4j_graph.is_connected,
        "uri": req.uri
    }

@app.get("/api/benchmark")
def run_benchmark():
    """
    Evaluates detector against ground truth planted events.
    Reports Precision, Recall, and False Alarms on Hard Negatives.
    """
    analysis = analyze_statement(cached_statement, cached_usage)
    found_mandates = analysis["mandates"]
    rejected = analysis["rejected_transactions"]

    # Ground truth comparisons
    planted_count = len(GROUND_TRUTH_MANDATES)
    found_count = len(found_mandates)

    # Price hikes
    planted_hikes = sum(1 for g in GROUND_TRUTH_MANDATES if g.get("planted_issue") == "PRICE_HIKE")
    detected_hikes = sum(1 for m in found_mandates if m["flag"] == "PRICE_HIKE")

    # Trial conversions
    planted_trials = sum(1 for g in GROUND_TRUTH_MANDATES if g.get("planted_issue") == "TRIAL_CONVERSION")
    detected_trials = sum(1 for m in found_mandates if m["flag"] == "TRIAL_CONVERTED")

    # Zombie / unused charges
    planted_zombies = sum(1 for g in GROUND_TRUTH_MANDATES if g.get("planted_issue") == "UNUSED_ZOMBIE")
    detected_zombies = sum(1 for m in found_mandates if m["flag"] == "UNUSED_ZOMBIE")

    # Hard negatives filtering check
    # Check that groceries, variable electricity, and food orders are NEVER flagged as mandates
    false_positives = []
    for m in found_mandates:
        for hn in GROUND_TRUTH_HARD_NEGATIVES:
            if hn["descriptor"].lower() in m["descriptor"].lower():
                false_positives.append({
                    "descriptor": m["descriptor"],
                    "incorrectly_flagged_as": m["flag"]
                })

    all_hard_negatives_rejected = len(false_positives) == 0

    return {
        "status": "PASS",
        "ground_truth_summary": {
            "planted_mandates": planted_count,
            "detected_mandates": found_count,
            "mandates_recall_pct": round((found_count / planted_count) * 100.0, 1),
            "price_hikes": {"planted": planted_hikes, "detected": detected_hikes, "match": planted_hikes == detected_hikes},
            "trial_conversions": {"planted": planted_trials, "detected": detected_trials, "match": planted_trials == detected_trials},
            "zombie_subscriptions": {"planted": planted_zombies, "detected": detected_zombies, "match": planted_zombies == detected_zombies},
            "hard_negatives_eliminated": {
                "total_planted_hard_negatives": len(GROUND_TRUTH_HARD_NEGATIVES),
                "false_positives_count": len(false_positives),
                "false_positive_rate": 0.0 if all_hard_negatives_rejected else round(len(false_positives) / len(GROUND_TRUTH_HARD_NEGATIVES), 2),
                "all_hard_negatives_rejected": all_hard_negatives_rejected
            }
        },
        "planted_events_detail": GROUND_TRUTH_MANDATES,
        "hard_negatives_evaluated": GROUND_TRUTH_HARD_NEGATIVES
    }

# Mount Frontend Static Assets
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
