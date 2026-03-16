# Razorpay Live Verification Setup

This guide walks you through configuring Razorpay for **live** penny drop verification. Account validation is **not available in test mode** — you need a RazorpayX Lite account in **live mode**.

## Prerequisites

- Razorpay account (sign up at [razorpay.com](https://razorpay.com))
- Completed business KYC (required for RazorpayX Lite)
- Validated bank account to add funds to RazorpayX Lite

---

## Step 1: Enable RazorpayX & Bank Account Verification

1. Log in to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Go to **Settings** → **Products** and ensure **RazorpayX** is enabled
3. Sign up for [RazorpayX Bank Account Verification](https://razorpay.com/x/bank-account-verification) (contact Razorpay if not visible)

---

## Step 2: Create RazorpayX Lite Account

1. Go to [RazorpayX Dashboard](https://x.razorpay.com/)
2. Complete KYC if not already done (takes 2–3 business days)
3. Create a **RazorpayX Lite** account
4. Add and validate a source bank account:
   - Click **+ Add balance** → **+ Add Account**
   - Enter account holder name, account number, IFSC
   - Upload cancelled cheque or bank statement
   - Wait for validation (up to 3 days)
5. Add funds to RazorpayX Lite (minimum required for penny drops)

---

## Step 3: Get Your RazorpayX Account Number

The **source account number** is your RazorpayX Lite virtual account number (used to deduct the ₹1 for each penny drop).

1. Log in to [RazorpayX Dashboard](https://x.razorpay.com/)
2. Go to **Account** or **Settings** → **Banking**
3. Your RazorpayX account number is shown (e.g. `7878780080316316`)
4. If not visible, check **Transactions** or contact Razorpay support

---

## Step 4: Generate API Keys

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/) → **Settings** → **API Keys**
2. Switch to **Live mode** (toggle at top)
3. Click **Generate Key** if you don’t have live keys
4. Copy:
   - **Key ID** (e.g. `rzp_live_xxxxxxxxxxxx`)
   - **Key Secret** (shown once — save it securely)

---

## Step 5: Allowlist Your IP

Account validation requires IP allowlisting.

1. Go to [RazorpayX Dashboard](https://x.razorpay.com/) → **Settings**
2. Find **IP Allowlist** or **Security**
3. Add your server’s public IP address
4. For local development, add your current public IP ([whatismyip.com](https://whatismyip.com))

---

## Step 6: Configure the App

1. Copy the example env file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=your_live_secret_key
   RAZORPAY_SOURCE_ACCOUNT=your_razorpayx_account_number
   ```

3. Restart the app:
   ```bash
   python app.py
   ```

4. Confirm **Live mode** in the app (no "Demo mode" badge)

---

## Verification Checklist

| Item | Status |
|------|--------|
| RazorpayX enabled | ☐ |
| KYC completed | ☐ |
| RazorpayX Lite account created | ☐ |
| Source bank account validated | ☐ |
| Funds added to RazorpayX Lite | ☐ |
| Live API keys generated | ☐ |
| IP allowlisted | ☐ |
| `.env` configured | ☐ |

---

## Troubleshooting

**"Account validation not available"**  
- Ensure you’re using **live** keys, not test keys  
- RazorpayX Lite must be active and funded  

**"Invalid source account"**  
- Confirm `RAZORPAY_SOURCE_ACCOUNT` matches your RazorpayX Lite account number  
- Check the number in the RazorpayX dashboard  

**"IP not allowlisted"**  
- Add your current public IP in RazorpayX Settings → IP Allowlist  
- For dynamic IPs, consider a static IP or VPN  

**401 Unauthorized**  
- Verify `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`  
- Ensure no extra spaces in `.env`  

---

## Cost

- Each penny drop costs **₹1** (the transfer) plus Razorpay’s API fee
- Check [Razorpay pricing](https://razorpay.com/pricing/) for current fees
