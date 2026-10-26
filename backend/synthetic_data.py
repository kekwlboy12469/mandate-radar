"""
Mandate Radar Synthetic Data Generator
Generates clean 12-month transaction histories with planted ground truths,
usage telemetry feeds, notification streams, and explicit hard negatives.
No real financial data is ever touched.
"""

from datetime import datetime, timedelta
import random

GROUND_TRUTH_MANDATES = [
    {
        "merchant_id": "youtube_premium",
        "name": "YouTube Premium",
        "descriptor": "GOOGLE*YOUTUBE G.CO/HELPPAY",
        "mechanism": "PLAY_STORE",
        "cadence": "MONTHLY",
        "base_amount": 129.0,
        "is_mandate": True,
        "planted_issue": "PRICE_HIKE",
        "hike_from": 129.0,
        "hike_to": 149.0,
        "hike_month": 9, # September
        "last_usage_days_ago": 2,
        "explanation": "Silent price increase of +15.5% (₹129 to ₹149) detected starting in September. Adds ₹240/year in silent unbudgeted costs."
    },
    {
        "merchant_id": "amazon_prime",
        "name": "Amazon Prime India",
        "descriptor": "AMZN PRIME IN*849204",
        "mechanism": "UPI_AUTOPAY",
        "cadence": "ANNUAL",
        "base_amount": 1499.0,
        "is_mandate": True,
        "planted_issue": "NONE",
        "last_usage_days_ago": 1,
        "explanation": "Active annual commitment with regular streaming and delivery usage."
    },
    {
        "merchant_id": "netflix_india",
        "name": "Netflix India",
        "descriptor": "NETFLIX.COM NETFLIX ENTERTAINMENT",
        "mechanism": "CARD_SI",
        "cadence": "MONTHLY",
        "base_amount": 499.0,
        "is_mandate": True,
        "planted_issue": "NONE",
        "last_usage_days_ago": 3,
        "explanation": "Stable standard monthly plan billed via card standing instruction."
    },
    {
        "merchant_id": "spotify_india",
        "name": "Spotify Premium India",
        "descriptor": "SPOTIFY INDIA MUMBAI",
        "mechanism": "UPI_AUTOPAY",
        "cadence": "MONTHLY",
        "base_amount": 119.0,
        "is_mandate": True,
        "planted_issue": "TRIAL_CONVERSION",
        "trial_amount": 2.0,
        "last_usage_days_ago": 5,
        "explanation": "Trial conversion trap: Initiated with a ₹2 nominal trial verification charge in January, immediately followed by ₹119 recurring monthly auto-debits (59.5x increase)."
    },
    {
        "merchant_id": "cult_fit",
        "name": "Cult.fit (Cultpass)",
        "descriptor": "CUREFIT HEALTHCARE PVT LTD",
        "mechanism": "UPI_AUTOPAY",
        "cadence": "MONTHLY",
        "base_amount": 1450.0,
        "is_mandate": True,
        "planted_issue": "UNUSED_ZOMBIE",
        "last_usage_days_ago": 96, # > 75 days ago!
        "charges_since_last_use": 3,
        "explanation": "Zombie subscription: Zero gym check-ins or live class activity detected for 96 days, yet 3 monthly debits totaling ₹4,350 have cleared automatically."
    },
    {
        "merchant_id": "disney_hotstar",
        "name": "Disney+ Hotstar",
        "descriptor": "NOVI DIGITAL HOTSTAR",
        "mechanism": "UPI_AUTOPAY",
        "cadence": "QUARTERLY",
        "base_amount": 299.0,
        "is_mandate": True,
        "planted_issue": "NONE",
        "last_usage_days_ago": 4,
        "explanation": "Quarterly recurring subscription billed once every 90-92 days."
    },
    {
        "merchant_id": "canva_pro",
        "name": "Canva Pro",
        "descriptor": "CANVA PTY LTD SYDNEY",
        "mechanism": "CARD_SI",
        "cadence": "MONTHLY",
        "base_amount": 499.0,
        "is_mandate": True,
        "planted_issue": "NONE",
        "last_usage_days_ago": 6,
        "explanation": "Active monthly design tool commitment."
    },
    {
        "merchant_id": "truecaller_premium",
        "name": "Truecaller Premium",
        "descriptor": "TRUE SOFTWARE SCANDINAVIA AB",
        "mechanism": "UPI_AUTOPAY",
        "cadence": "MONTHLY",
        "base_amount": 79.0,
        "is_mandate": True,
        "planted_issue": "UNUSED_ZOMBIE",
        "last_usage_days_ago": 84,
        "charges_since_last_use": 2,
        "explanation": "Zombie charge: Zero caller lookup or app launches in 84 days, while ₹79 continues to be auto-debited monthly."
    },
    {
        "merchant_id": "chatgpt_plus",
        "name": "ChatGPT Plus (OpenAI)",
        "descriptor": "OPENAI *CHATGPT SUBSCRIPTION",
        "mechanism": "CARD_SI",
        "cadence": "MONTHLY",
        "base_amount": 1999.0,
        "is_mandate": True,
        "planted_issue": "NONE",
        "last_usage_days_ago": 0,
        "explanation": "Active AI tool subscription with daily usage."
    },
    {
        "merchant_id": "unrecognised_saas",
        "name": "Unrecognised Recurring Mandate",
        "descriptor": "ACME CLOUD RECURRING BILL SVCS #4928",
        "mechanism": "CARD_SI",
        "cadence": "MONTHLY",
        "base_amount": 450.0,
        "is_mandate": True,
        "planted_issue": "UNRECOGNISED_DESCRIPTOR",
        "last_usage_days_ago": 12,
        "explanation": "Genuine repeating mandate (₹450 on exact monthly cadence) with an unknown descriptor string not present in reference graph. Reported without guessing."
    }
]

GROUND_TRUTH_HARD_NEGATIVES = [
    {
        "id": "weekly_groceries",
        "name": "Weekly Quick Grocery Orders",
        "descriptor": "ZEPTO CONSUMER DELIVERY BLR",
        "category": "Weekly Groceries",
        "is_mandate": False,
        "expected_rejection_reason": "Interval is weekly (5-7 days) and amounts fluctuate between ₹280-₹650 with high variance (>35%)."
    },
    {
        "id": "variable_electricity",
        "name": "Bangalore Electricity (BESCOM)",
        "descriptor": "BESCOM BANGALORE ELECTRICITY",
        "category": "Fluctuating Utility",
        "is_mandate": False,
        "expected_rejection_reason": "Monthly recurrence present, but billed amounts fluctuate heavily based on meter readings (₹1,240 to ₹2,100). Rejected as variable utility bill."
    },
    {
        "id": "discretionary_food",
        "name": "Ad-Hoc Food Deliveries",
        "descriptor": "SWIGGY FOOD DELIVERY BENGALURU",
        "category": "Discretionary Food Deliveries",
        "is_mandate": False,
        "expected_rejection_reason": "Ad-hoc irregular gaps between 1 to 6 days apart and inconsistent amounts. Rejected as discretionary spend."
    }
]

def generate_synthetic_statement(base_year=2025):
    """
    Builds a realistic 12-month statement containing planted mandates,
    hard negatives, and background transactions.
    """
    transactions = []
    tx_id = 1001

    start_date = datetime(base_year, 1, 1)

    # 1. YouTube Premium (Monthly, price hike in Sept: 129 -> 149)
    for m in range(1, 13):
        dt = datetime(base_year, m, 12) + timedelta(days=random.choice([-1, 0, 1]))
        amt = 149.0 if m >= 9 else 129.0
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "GOOGLE*YOUTUBE G.CO/HELPPAY",
            "amount": amt,
            "type": "DEBIT",
            "balance": round(45000.0 - (m * 2000), 2),
            "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/GOOGLE/YOUTUBE"
        })
        tx_id += 1

    # 2. Amazon Prime (Annual, billed on Feb 18)
    dt_amzn = datetime(base_year, 2, 18)
    transactions.append({
        "id": f"TXN_{tx_id}",
        "date": dt_amzn.strftime("%Y-%m-%d"),
        "descriptor": "AMZN PRIME IN*849204",
        "amount": 1499.0,
        "type": "DEBIT",
        "balance": 48200.0,
        "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/AMAZON/PRIME"
    })
    tx_id += 1

    # 3. Netflix (Monthly, ₹499 on the 5th)
    for m in range(1, 13):
        dt = datetime(base_year, m, 5) + timedelta(days=random.choice([0, 1]))
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "NETFLIX.COM NETFLIX ENTERTAINMENT",
            "amount": 499.0,
            "type": "DEBIT",
            "balance": round(42000.0 - (m * 1500), 2),
            "ref": f"CARD-SI-VISA-4821-{m}"
        })
        tx_id += 1

    # 4. Spotify (Trial conversion: ₹2 in Jan, ₹119 from Feb-Dec)
    dt_jan_trial = datetime(base_year, 1, 8)
    transactions.append({
        "id": f"TXN_{tx_id}",
        "date": dt_jan_trial.strftime("%Y-%m-%d"),
        "descriptor": "SPOTIFY INDIA MUMBAI",
        "amount": 2.0,
        "type": "DEBIT",
        "balance": 52000.0,
        "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/SPOTIFY/VERIFY"
    })
    tx_id += 1
    for m in range(2, 13):
        dt = datetime(base_year, m, 8) + timedelta(days=random.choice([-1, 0, 1]))
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "SPOTIFY INDIA MUMBAI",
            "amount": 119.0,
            "type": "DEBIT",
            "balance": round(41000.0 - (m * 800), 2),
            "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/SPOTIFY/PREMIUM"
        })
        tx_id += 1

    # 5. Cult.fit (Monthly, ₹1450 on the 1st) - Zombie subscription
    for m in range(1, 13):
        dt = datetime(base_year, m, 1) + timedelta(days=random.choice([0, 1]))
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "CUREFIT HEALTHCARE PVT LTD",
            "amount": 1450.0,
            "type": "DEBIT",
            "balance": round(38000.0 - (m * 1200), 2),
            "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/CUREFIT/AUTOPAY"
        })
        tx_id += 1

    # 6. Disney+ Hotstar (Quarterly: Jan 15, Apr 15, Jul 15, Oct 15)
    for q_month in [1, 4, 7, 10]:
        dt = datetime(base_year, q_month, 15) + timedelta(days=random.choice([-1, 0, 1]))
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "NOVI DIGITAL HOTSTAR",
            "amount": 299.0,
            "type": "DEBIT",
            "balance": round(35000.0 - (q_month * 500), 2),
            "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/HOTSTAR/AUTOPAY"
        })
        tx_id += 1

    # 7. Canva Pro (Monthly, ₹499 on the 20th)
    for m in range(1, 13):
        dt = datetime(base_year, m, 20) + timedelta(days=random.choice([0, 1]))
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "CANVA PTY LTD SYDNEY",
            "amount": 499.0,
            "type": "DEBIT",
            "balance": round(46000.0 - (m * 600), 2),
            "ref": f"CARD-SI-MC-9012-{m}"
        })
        tx_id += 1

    # 8. Truecaller Premium (Monthly, ₹79 on the 25th) - Zombie subscription
    for m in range(1, 13):
        dt = datetime(base_year, m, 25) + timedelta(days=random.choice([-1, 0, 1]))
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "TRUE SOFTWARE SCANDINAVIA AB",
            "amount": 79.0,
            "type": "DEBIT",
            "balance": round(43000.0 - (m * 400), 2),
            "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/TRUECALLER/PREMIUM"
        })
        tx_id += 1

    # 9. ChatGPT Plus (Monthly, ₹1999 on the 28th)
    for m in range(1, 13):
        dt = datetime(base_year, m, 28)
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "OPENAI *CHATGPT SUBSCRIPTION",
            "amount": 1999.0,
            "type": "DEBIT",
            "balance": round(39000.0 - (m * 1000), 2),
            "ref": f"CARD-SI-VISA-4821-GPT-{m}"
        })
        tx_id += 1

    # 10. Unrecognised SaaS Mandate (Monthly, ₹450 on the 10th)
    for m in range(1, 13):
        dt = datetime(base_year, m, 10) + timedelta(days=random.choice([-1, 0]))
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "ACME CLOUD RECURRING BILL SVCS #4928",
            "amount": 450.0,
            "type": "DEBIT",
            "balance": round(36000.0 - (m * 450), 2),
            "ref": f"POS-DEBIT-ACME-{m}"
        })
        tx_id += 1

    # --- HARD NEGATIVES ---

    # HN 1: Weekly Groceries (Zepto, every 5-8 days, amounts 280-680)
    current_cur = datetime(base_year, 1, 3)
    end_date = datetime(base_year, 12, 28)
    while current_cur < end_date:
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": current_cur.strftime("%Y-%m-%d"),
            "descriptor": "ZEPTO CONSUMER DELIVERY BLR",
            "amount": float(random.choice([285, 340, 420, 515, 630, 310, 480])),
            "type": "DEBIT",
            "balance": 42000.0,
            "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/ZEPTO/QR"
        })
        tx_id += 1
        current_cur += timedelta(days=random.randint(5, 8))

    # HN 2: Fluctuating Electricity Utility (BESCOM, 14th of each month, fluctuating amounts)
    bescom_amounts = [1240.0, 1420.0, 1850.0, 2100.0, 1980.0, 1650.0, 1510.0, 1720.0, 1890.0, 1430.0, 1310.0, 1290.0]
    for m in range(1, 13):
        dt = datetime(base_year, m, 14)
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "BESCOM BANGALORE ELECTRICITY",
            "amount": bescom_amounts[m-1],
            "type": "DEBIT",
            "balance": 39000.0,
            "ref": f"BBPS/BILL/{random.randint(100000, 999999)}/BESCOM"
        })
        tx_id += 1

    # HN 3: Discretionary Food Orders (Swiggy food, 25 ad-hoc orders over the year)
    for _ in range(28):
        rand_day = random.randint(1, 350)
        dt = start_date + timedelta(days=rand_day)
        transactions.append({
            "id": f"TXN_{tx_id}",
            "date": dt.strftime("%Y-%m-%d"),
            "descriptor": "SWIGGY FOOD DELIVERY BENGALURU",
            "amount": float(random.choice([195, 260, 345, 410, 580, 220])),
            "type": "DEBIT",
            "balance": 37000.0,
            "ref": f"UPI/CR/{random.randint(10000000, 99999999)}/SWIGGY/FOOD"
        })
        tx_id += 1

    # Sort all transactions chronologically
    transactions.sort(key=lambda x: x["date"])
    return transactions

def generate_usage_telemetry():
    """
    Returns synthetic app / service usage logs (last activity timestamp).
    Used to detect Zombie subscriptions (debited despite 75+ days of zero activity).
    """
    now = datetime(2025, 12, 31)
    return {
        "youtube_premium": (now - timedelta(days=2)).strftime("%Y-%m-%d"),
        "amazon_prime": (now - timedelta(days=1)).strftime("%Y-%m-%d"),
        "netflix_india": (now - timedelta(days=3)).strftime("%Y-%m-%d"),
        "spotify_india": (now - timedelta(days=5)).strftime("%Y-%m-%d"),
        "cult_fit": (now - timedelta(days=96)).strftime("%Y-%m-%d"), # Zombie! 96 days ago
        "disney_hotstar": (now - timedelta(days=4)).strftime("%Y-%m-%d"),
        "canva_pro": (now - timedelta(days=6)).strftime("%Y-%m-%d"),
        "truecaller_premium": (now - timedelta(days=84)).strftime("%Y-%m-%d"), # Zombie! 84 days ago
        "chatgpt_plus": now.strftime("%Y-%m-%d"),
        "unrecognised_saas": (now - timedelta(days=12)).strftime("%Y-%m-%d")
    }

def generate_notification_stream():
    """
    Returns synthetic SMS / push notification alerts for pre-debit notifications
    mandated under RBI's 24-hour pre-debit notification requirement.
    """
    return [
        {
            "id": "NOTIF_01",
            "timestamp": "2025-12-11 10:15:00",
            "sender": "VM-HDFCBK",
            "channel": "SMS",
            "text": "Dear Customer, Mandate execution alert: Rs 149.00 will be debited towards GOOGLE*YOUTUBE on 12-DEC-2025. To manage or revoke, visit NetBanking.",
            "merchant_resolved": "YouTube Premium",
            "flag": "PRICE_HIKE_ALERT"
        },
        {
            "id": "NOTIF_02",
            "timestamp": "2025-12-04 18:30:00",
            "sender": "AX-ICICIB",
            "channel": "SMS",
            "text": "Standing instruction debit reminder: Rs 499.00 will be charged on your Card ending 4821 for NETFLIX ENTERTAINMENT on 05-DEC-2025.",
            "merchant_resolved": "Netflix India",
            "flag": "HEALTHY"
        },
        {
            "id": "NOTIF_03",
            "timestamp": "2025-12-07 14:02:00",
            "sender": "PHONEPE",
            "channel": "PUSH",
            "text": "UPI AutoPay Alert: ₹119.00 will be debited for SPOTIFY INDIA on 08-DEC-2025.",
            "merchant_resolved": "Spotify Premium India",
            "flag": "TRIAL_CONVERTED"
        },
        {
            "id": "NOTIF_04",
            "timestamp": "2025-11-30 09:45:00",
            "sender": "GPAY",
            "channel": "PUSH",
            "text": "AutoPay Reminder: ₹1,450.00 will be debited tomorrow for CUREFIT HEALTHCARE. Note: You have not visited a center in 95 days.",
            "merchant_resolved": "Cult.fit (Cultpass)",
            "flag": "ZOMBIE_SUBSCRIPTION"
        }
    ]
