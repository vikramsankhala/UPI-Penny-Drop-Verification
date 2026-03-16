"""
UPI Penny Drop Verification Application
Full verification flow: QR scan → payment → verify via Razorpay (RazorpayX)
Supports both Bank Account and UPI/VPA verification.
"""
import os
import uuid
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Razorpay credentials (from env - never commit these)
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
RAZORPAY_SOURCE_ACCOUNT = os.getenv("RAZORPAY_SOURCE_ACCOUNT")  # RazorpayX account for penny drop
USE_MOCK = not (RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and RAZORPAY_SOURCE_ACCOUNT)


def mock_penny_drop_verification(account_number: str, ifsc: str, beneficiary_name: str):
    """Simulate penny drop flow when Razorpay credentials are not configured."""
    # Simulate API latency
    import time
    time.sleep(2)
    
    # Mock response - in production this comes from Razorpay
    return {
        "id": f"fav_{uuid.uuid4().hex[:14]}",
        "entity": "fund_account.validation",
        "status": "completed",
        "utr": "".join([str((hash(account_number + ifsc) % 10)) for _ in range(12)]),
        "validation_results": {
            "account_status": "active",
            "registered_name": "JOHN DOE",  # Bank-registered name from transaction
            "name_match_score": 85,  # 0-100, how well beneficiary_name matches
            "details": {
                "bank_name": "HDFC Bank",
                "branch": "Mumbai Main"
            }
        },
        "status_details": {
            "description": "Account verified successfully",
            "source": "penny_drop",
            "reason": "validation_completed"
        },
        "fund_account": {
            "id": f"fa_{uuid.uuid4().hex[:14]}",
            "bank_account": {
                "account_number": account_number[-4:].rjust(len(account_number), "*"),
                "ifsc": ifsc,
                "bank_name": "HDFC Bank",
                "name": "JOHN DOE"
            }
        },
        "_mock": True
    }


def razorpay_penny_drop_verification(account_number: str, ifsc: str, beneficiary_name: str,
                                     contact_name: str, contact_email: str, contact_phone: str):
    """Call Razorpay Composite Account Validation API for penny drop."""
    url = "https://api.razorpay.com/v1/fund_accounts/validations"
    auth = (RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
    
    payload = {
        "source_account_number": RAZORPAY_SOURCE_ACCOUNT,
        "validation_type": "pennydrop",  # Explicit penny drop
        "reference_id": str(uuid.uuid4())[:8],
        "fund_account": {
            "account_type": "bank_account",
            "bank_account": {
                "name": beneficiary_name,
                "ifsc": ifsc,
                "account_number": account_number
            },
            "contact": {
                "name": contact_name or beneficiary_name,
                "email": contact_email or "verify@example.com",
                "contact": contact_phone or "9999999999",
                "type": "employee"
            }
        }
    }
    
    response = requests.post(url, json=payload, auth=auth, timeout=30)
    data = response.json()
    
    if response.status_code != 200:
        return {
            "error": True,
            "status": "failed",
            "message": data.get("error", {}).get("description", "Verification failed"),
            "razorpay_error": data
        }
    
    return data


def mock_vpa_penny_drop_verification(vpa: str, beneficiary_name: str):
    """Simulate VPA/UPI penny drop when Razorpay credentials are not configured."""
    import time
    time.sleep(2)
    return {
        "id": f"fav_{uuid.uuid4().hex[:14]}",
        "entity": "fund_account.validation",
        "status": "completed",
        "utr": "".join([str(abs(hash(vpa + str(i))) % 10) for i in range(12)]),
        "validation_results": {
            "account_status": "active",
            "registered_name": "JOHN DOE",
            "name_match_score": 88,
            "details": {
                "bank_name": "HDFC Bank",
                "branch": "Mumbai Main"
            }
        },
        "status_details": {
            "description": "VPA verified successfully",
            "source": "penny_drop",
            "reason": "validation_completed"
        },
        "fund_account": {
            "id": f"fa_{uuid.uuid4().hex[:14]}",
            "account_type": "vpa",
            "vpa": {"address": vpa},
            "bank_account": None
        },
        "_mock": True
    }


def razorpay_vpa_penny_drop_verification(vpa: str, beneficiary_name: str,
                                        contact_email: str, contact_phone: str):
    """Call Razorpay VPA validation API for UPI penny drop."""
    url = "https://api.razorpay.com/v1/fund_accounts/validations"
    auth = (RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
    payload = {
        "source_account_number": RAZORPAY_SOURCE_ACCOUNT,
        "reference_id": str(uuid.uuid4())[:8],
        "fund_account": {
            "account_type": "vpa",
            "vpa": {"address": vpa},
            "contact": {
                "name": beneficiary_name,
                "email": contact_email or "verify@example.com",
                "contact": contact_phone or "9999999999",
                "type": "employee"
            }
        }
    }
    response = requests.post(url, json=payload, auth=auth, timeout=30)
    data = response.json()
    if response.status_code != 200:
        return {
            "error": True,
            "status": "failed",
            "message": data.get("error", {}).get("description", "Verification failed"),
            "razorpay_error": data
        }
    return data


@app.route("/")
def index():
    return render_template("index.html", use_mock=USE_MOCK)


@app.route("/api/verify", methods=["POST"])
def verify_account():
    """Penny drop verification endpoint."""
    data = request.get_json() or {}
    
    account_number = (data.get("account_number") or "").strip().replace(" ", "")
    ifsc = (data.get("ifsc") or "").strip().upper()
    beneficiary_name = (data.get("beneficiary_name") or "").strip()
    
    if not account_number or not ifsc or not beneficiary_name:
        return jsonify({
            "error": True,
            "message": "Account number, IFSC, and beneficiary name are required."
        }), 400
    
    if len(ifsc) != 11:
        return jsonify({
            "error": True,
            "message": "IFSC must be 11 characters (e.g., HDFC0000129)."
        }), 400
    
    try:
        if USE_MOCK:
            result = mock_penny_drop_verification(account_number, ifsc, beneficiary_name)
        else:
            result = razorpay_penny_drop_verification(
                account_number, ifsc, beneficiary_name,
                data.get("contact_name"),
                data.get("contact_email"),
                data.get("contact_phone")
            )
        
        if result.get("error"):
            return jsonify(result), 400
        
        # Normalize transaction response: bank, branch, bank-registered name
        # Razorpay returns these in validation_results and fund_account.bank_account
        vr = result.get("validation_results") or {}
        fa = result.get("fund_account") or {}
        ba = fa.get("bank_account") or {}
        details = vr.get("details") or {}
        
        result["transaction_response"] = {
            "bank": ba.get("bank_name") or details.get("bank_name"),
            "branch": details.get("branch") or ba.get("branch"),
            "bank_registered_name": vr.get("registered_name") or ba.get("name"),
        }
        
        return jsonify(result)
    
    except requests.RequestException as e:
        return jsonify({
            "error": True,
            "message": f"Payment provider error: {str(e)}"
        }), 502
    except Exception as e:
        return jsonify({
            "error": True,
            "message": str(e)
        }), 500


@app.route("/api/verify-vpa", methods=["POST"])
def verify_vpa():
    """UPI/VPA penny drop verification (from QR or manual entry)."""
    data = request.get_json() or {}
    vpa = (data.get("vpa") or "").strip().lower()
    beneficiary_name = (data.get("beneficiary_name") or "").strip()
    
    if not vpa or not beneficiary_name:
        return jsonify({
            "error": True,
            "message": "UPI ID (VPA) and beneficiary name are required."
        }), 400
    
    if "@" not in vpa:
        return jsonify({
            "error": True,
            "message": "Invalid UPI ID. Format: name@bank (e.g. merchant@paytm)"
        }), 400
    
    try:
        if USE_MOCK:
            result = mock_vpa_penny_drop_verification(vpa, beneficiary_name)
        else:
            result = razorpay_vpa_penny_drop_verification(
                vpa, beneficiary_name,
                data.get("contact_email"),
                data.get("contact_phone")
            )
        
        if result.get("error"):
            return jsonify(result), 400
        
        vr = result.get("validation_results") or {}
        fa = result.get("fund_account") or {}
        ba = fa.get("bank_account") or {}
        vpa_obj = fa.get("vpa") or {}
        details = vr.get("details") or {}
        
        result["transaction_response"] = {
            "bank": ba.get("bank_name") or details.get("bank_name"),
            "branch": details.get("branch") or ba.get("branch"),
            "bank_registered_name": vr.get("registered_name") or ba.get("name"),
            "vpa": vpa_obj.get("address") or vpa,
        }
        
        return jsonify(result)
    
    except requests.RequestException as e:
        return jsonify({
            "error": True,
            "message": f"Payment provider error: {str(e)}"
        }), 502
    except Exception as e:
        return jsonify({
            "error": True,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
