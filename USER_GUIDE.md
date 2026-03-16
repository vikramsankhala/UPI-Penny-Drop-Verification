# UPI Penny Drop Verification — User Guide

## Table of Contents

1. [Purpose](#purpose)
2. [What is Penny Drop?](#what-is-penny-drop)
3. [Applications & Use Cases](#applications--use-cases)
4. [Getting Started](#getting-started)
5. [User Guide — UPI QR Code](#user-guide--upi-qr-code)
6. [User Guide — Bank Account](#user-guide--bank-account)
7. [Understanding the Results](#understanding-the-results)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)
10. [Security & Compliance](#security--compliance)

---

## Purpose

The **UPI Penny Drop Verification** application enables businesses and individuals to **verify bank account and UPI details** before making payments or disbursements. It reduces the risk of:

- **Failed transfers** — Incorrect account numbers or IFSC codes
- **Fraud** — Paying to the wrong beneficiary
- **Reversals** — Transfers to closed, frozen, or invalid accounts
- **Compliance gaps** — Unverified payee details in financial records

By sending a small amount (₹1) to the account and receiving the bank-registered name in the transaction response, you can confirm that the account exists, is active, and belongs to the intended recipient.

---

## What is Penny Drop?

**Penny drop** (also called *penny testing* or *account validation*) is a bank account verification method used widely in India:

1. **Transfer** — A small amount (typically ₹1) is transferred to the account to be verified
2. **Bank response** — The bank processes the transfer and returns the **account holder's name** as registered in their records
3. **Verification** — You compare the returned name with the name provided by your customer/vendor
4. **Result** — If the transfer succeeds, the account exists and is active; the name match confirms ownership

### Why ₹1?

The minimal amount keeps verification costs low while satisfying the technical requirement: the bank only returns account details when a real transaction is processed.

### UPI vs Bank Account

| Method | Input | Best for |
|--------|-------|----------|
| **UPI QR / VPA** | UPI ID (e.g. merchant@paytm), payee name | Merchants, individuals with UPI, QR-based payments |
| **Bank Account** | Account number, IFSC, beneficiary name | Payroll, vendor payments, loan disbursals |

---

## Applications & Use Cases

### 1. **Marketplaces & E-commerce**

- **Vendor onboarding** — Verify seller bank details before releasing payouts
- **Refund verification** — Confirm customer account before processing refunds
- **Commission payouts** — Validate affiliate or partner accounts

### 2. **Lending & Fintech**

- **Loan disbursal** — Verify borrower's bank account before transferring loan amount
- **EMI collection** — Validate mandate bank details
- **Co-lending** — Partner bank account verification

### 3. **Payroll & HR**

- **Employee onboarding** — Verify salary account details
- **Contractor payments** — Validate freelancer/vendor accounts
- **Reimbursements** — Confirm employee bank details for expense payouts

### 4. **Insurance**

- **Claim settlement** — Verify nominee or policyholder bank details
- **Premium refunds** — Validate account before processing refunds

### 5. **Brokerage & Investment**

- **Trading account linking** — Verify bank account for fund transfers
- **Dividend payouts** — Validate shareholder bank details

### 6. **Government & Pensions**

- **Beneficiary verification** — Confirm account for subsidy/scheme disbursals
- **Pension payouts** — Validate retiree bank details

### 7. **Small Business & Freelancers**

- **Client payments** — Verify client account before sending invoice payment details
- **UPI QR verification** — Confirm merchant QR details before paying at a new outlet

### 8. **Identity & KYC Companies**

- **Bank account verification** — Part of identity verification workflows
- **Document vs live verification** — Cross-check submitted bank details

---

## Getting Started

### Prerequisites

- Web browser (Chrome, Firefox, Safari, Edge)
- For **UPI QR**: Image of a UPI QR code (screenshot or photo)
- For **Bank Account**: Account number, IFSC code, beneficiary name

### Accessing the Application

- **Local**: Open `http://127.0.0.1:5000` after running `python app.py`
- **Deployed**: Open `https://gopalsankhala.in` (or your deployment URL)

### Demo vs Live Mode

| Mode | Badge | Behaviour |
|------|-------|-----------|
| **Demo** | "Demo mode — configure Razorpay for live verification" | Simulated responses; no real transfer |
| **Live** | No badge | Real ₹1 transfer via Razorpay; actual bank verification |

---

## User Guide — UPI QR Code

Use this flow when you have a **UPI QR code** (e.g. from a merchant, payment app, or invoice).

### Step 1: Open the UPI QR Code Tab

Click **"UPI QR Code"** (default tab).

### Step 2: Upload or Scan the QR

**Option A — Upload image**

1. Click the upload area or drag and drop an image
2. Supported formats: PNG, JPG, JPEG, GIF, WebP
3. The app decodes the QR and extracts:
   - **VPA** (UPI ID, e.g. `merchant@paytm`)
   - **Payee name** (from the QR)

**Option B — Manual entry**

1. If the QR fails to decode, or you have the UPI ID separately, type it in the **UPI ID (VPA)** field
2. Enter the **Payee / Beneficiary name** as you expect it to appear

### Step 3: Review Decoded Data

If the QR was decoded successfully, you'll see:

- **VPA**: The UPI ID
- **Payee**: The name embedded in the QR

These fields are auto-filled in the form. You can edit them if needed.

### Step 4: Optional — Add Contact Details

- **Contact email** — For records (optional)
- **Contact phone** — For records (optional)

### Step 5: Verify UPI

Click **"Verify UPI"**.

- The app sends a ₹1 penny drop to the UPI ID (in live mode)
- Wait a few seconds for the result

### Step 6: Review Results

See [Understanding the Results](#understanding-the-results) below.

---

## User Guide — Bank Account

Use this flow when you have **bank account details** (account number, IFSC, beneficiary name).

### Step 1: Open the Bank Account Tab

Click **"Bank Account"**.

### Step 2: Enter Bank Details

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| **Account number** | Yes | 9–18 digits, no spaces | `765432123456789` |
| **IFSC code** | Yes | 11 characters, alphanumeric | `HDFC0000129` |
| **Beneficiary name** | Yes | As per bank records | `Gaurav Kumar` |

### Step 3: Optional — Add Contact Details

- **Contact email** — For records
- **Contact phone** — For records

### Step 4: Verify Account

Click **"Verify account"**.

- The app sends a ₹1 penny drop to the bank account (in live mode)
- Wait a few seconds for the result

### Step 5: Review Results

See [Understanding the Results](#understanding-the-results) below.

---

## Understanding the Results

### Successful Verification

When verification succeeds, you'll see:

#### Transaction Response

| Field | Description |
|-------|-------------|
| **Bank** | Bank name from the transaction |
| **Branch** | Branch name |
| **Bank-registered name** | Account holder name as per bank records |
| **Account number** | Masked (e.g. `***********6789`) |
| **IFSC** | IFSC code |
| **UPI ID** | VPA (for UPI verification only) |

#### Validation Results

| Field | Description |
|-------|-------------|
| **Account status** | `active` or `invalid` |
| **Registered name** | Same as bank-registered name |
| **Name match score** | 0–100% — how well the name you provided matches the bank's name |

#### Transaction Metadata

| Field | Description |
|-------|-------------|
| **UTR** | Unique Transaction Reference (12-digit) |
| **Reference ID** | Your reference for the validation |
| **ID** | Razorpay validation ID |

### Failed Verification

If verification fails, you may see:

- **Invalid account** — Account number or IFSC incorrect
- **Account closed/frozen** — Account not operational
- **Name mismatch** — Beneficiary name doesn't match bank records
- **Provider error** — Temporary Razorpay or bank issue

### Name Match Score

- **High (80–100%)** — Strong match; likely correct beneficiary
- **Medium (50–79%)** — Partial match; review spelling/format
- **Low (0–49%)** — Poor match; verify details with the payee

---

## API Reference

For integration with other systems:

### UPI / VPA Verification

```
POST /api/verify-vpa
Content-Type: application/json

{
  "vpa": "merchant@paytm",
  "beneficiary_name": "John Stores",
  "contact_email": "user@example.com",
  "contact_phone": "9123456789"
}
```

### Bank Account Verification

```
POST /api/verify
Content-Type: application/json

{
  "account_number": "765432123456789",
  "ifsc": "HDFC0000129",
  "beneficiary_name": "Gaurav Kumar",
  "contact_email": "user@example.com",
  "contact_phone": "9123456789"
}
```

### Response (Success)

```json
{
  "status": "completed",
  "transaction_response": {
    "bank": "HDFC Bank",
    "branch": "Mumbai Main",
    "bank_registered_name": "GAURAV KUMAR",
    "account_number": "***********6789",
    "ifsc": "HDFC0000129",
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

---

## Troubleshooting

| Issue | Possible cause | Solution |
|-------|----------------|----------|
| "Demo mode" badge shown | Razorpay not configured | Add credentials to `.env`; see RAZORPAY_SETUP.md |
| QR not decoding | Blurry image, non-UPI QR | Use a clear image; ensure it's a UPI QR |
| "Invalid UPI ID" | Wrong format | Use `name@bank` (e.g. `merchant@paytm`) |
| "IFSC must be 11 characters" | Wrong IFSC length | Check IFSC (e.g. HDFC0000129) |
| Verification failed | Wrong details, closed account | Re-check account number, IFSC, name |
| 401 / Unauthorized | Invalid API keys | Verify Razorpay keys in `.env` |
| IP not allowlisted | Server IP not in Razorpay | Add IP in RazorpayX → Settings → IP Allowlist |

---

## Security & Compliance

### Data Handling

- **Account numbers** — Masked in responses (only last 4 digits visible)
- **API keys** — Stored in environment variables; never in code
- **No storage** — Verification results are not persisted by default

### Regulatory Context

- Penny drop is a standard practice for account verification in India
- Razorpay complies with RBI guidelines and NPCI requirements
- Use verification results in line with your data retention and privacy policies

### Best Practices

- Verify accounts before high-value disbursals
- Keep records of verification (UTR, reference ID) for audits
- Use HTTPS in production
- Restrict API access to authorised systems only

---

## Support

- **Razorpay documentation**: [razorpay.com/docs](https://razorpay.com/docs)
- **Bank Account Verification**: [razorpay.com/x/bank-account-verification](https://razorpay.com/x/bank-account-verification)
- **GitHub repository**: [github.com/vikramsankhala/UPI-Penny-Drop-Verification](https://github.com/vikramsankhala/UPI-Penny-Drop-Verification)
