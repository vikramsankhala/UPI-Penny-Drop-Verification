# UPI Penny Drop Verification

A web application that demonstrates the **full penny drop verification flow**: **Scan QR → Pay ₹1 → Verify** via [RazorpayX](https://razorpay.com/x/bank-account-verification).

## Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** — Purpose, applications, and detailed user guide

## Features

- **UPI QR Code** — Upload or scan a UPI QR to extract VPA and payee name
- **Bank Account** — Manual entry of account number, IFSC, and beneficiary name
- **Penny Drop** — ₹1 transfer to verify account exists and match bank-registered name
- **Transaction Response** — Returns bank, branch, and bank-registered name from the verification

## Verification Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. Scan QR /   │ ──► │  2. ₹1 transfer │ ──► │  3. Verify &    │
│  Enter details   │     │  (penny drop)    │     │  match name     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

### 3. Demo mode (no credentials)

Without Razorpay credentials, the app runs in **demo mode** and simulates the verification flow with mock responses. You can try the full UI, QR scan, and verification flow immediately.

### 4. Live verification (Razorpay)

To use real penny drop verification:

1. Sign up for [RazorpayX](https://razorpay.com/x) and enable **Bank Account Verification**
2. Create a RazorpayX Lite account (source account for the ₹1 transfer)
3. Copy `.env.example` to `.env` and add your credentials:

```env
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_secret_key
RAZORPAY_SOURCE_ACCOUNT=your_razorpayx_account_number
```

4. [Allowlist your IP](https://razorpay.com/docs/x/dashboard/allowlist-ip/) in the Razorpay dashboard (required for account validation)

> **Note:** Account validation is not available in Razorpay test mode. You need a RazorpayX Lite account in live mode.

## API

### `POST /api/verify-vpa` (UPI / QR)

Request body:

```json
{
  "vpa": "merchant@paytm",
  "beneficiary_name": "John Stores",
  "contact_email": "user@example.com",
  "contact_phone": "9123456789"
}
```

### `POST /api/verify` (Bank Account)

Request body:

```json
{
  "account_number": "765432123456789",
  "ifsc": "HDFC0000129",
  "beneficiary_name": "Gaurav Kumar",
  "contact_email": "user@example.com",
  "contact_phone": "9123456789"
}
```

Response (success) includes `transaction_response`:

```json
{
  "status": "completed",
  "transaction_response": {
    "bank": "HDFC Bank",
    "branch": "Mumbai Main",
    "bank_registered_name": "GAURAV KUMAR",
    "vpa": "merchant@paytm"
  },
  "validation_results": {
    "account_status": "active",
    "registered_name": "GAURAV KUMAR",
    "name_match_score": 95
  },
  "utr": "123456789012"
}
```

## UPI QR Format

The app parses standard UPI QR codes:

```
upi://pay?pa=merchant@paytm&pn=John%20Stores&am=1&cu=INR
```

- `pa` — Payee Address (UPI ID / VPA)
- `pn` — Payee Name
- `am` — Amount (optional, for dynamic QR)
- `cu` — Currency (INR)

## Project Structure

```
├── app.py              # Flask backend + Razorpay integration
├── templates/
│   └── index.html      # Frontend: QR scan, bank form, verification
├── requirements.txt
├── .env.example
└── README.md
```

## Payment Provider

This app uses **Razorpay** (RazorpayX) for penny drop. Other providers that offer similar APIs include:

- [Setu](https://docs.setu.co/) — Reverse penny drop via UPI
- [BulkPE](https://docs.bulkpe.in/)
- [Enkash](https://docs.enkash.com/)

## Deploy to gopalsankhala.in

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for:
- Razorpay live-mode checklist (KYC, bank validation, funds)
- Docker / systemd deployment
- Nginx + SSL setup
- DNS configuration

## License

MIT
