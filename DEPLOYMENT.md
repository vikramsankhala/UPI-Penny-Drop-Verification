# Deploy to gopalsankhala.in

This guide covers deploying the UPI Penny Drop app to **gopalsankhala.in** with live Razorpay verification.

---

## Part A: Razorpay Live Mode Setup (You Must Complete)

These steps require your Razorpay account. **I cannot do these for you** — you must complete them in the Razorpay dashboard.

### Razorpay Checklist

| Step | Action | Where |
|------|--------|-------|
| 1 | Sign up / log in to Razorpay | [razorpay.com](https://razorpay.com) |
| 2 | Enable RazorpayX | Dashboard → Settings → Products |
| 3 | Complete KYC | Dashboard → Settings → Business details |
| 4 | Create RazorpayX Lite account | [x.razorpay.com](https://x.razorpay.com) |
| 5 | Add & validate source bank account | RazorpayX → + Add balance → + Add Account |
| 6 | Add funds to RazorpayX Lite | RazorpayX → Add balance (min ₹500 recommended) |
| 7 | Get RazorpayX account number | RazorpayX → Account / Settings → Banking |
| 8 | Generate Live API keys | [Dashboard → API Keys](https://dashboard.razorpay.com/app/keys) (Live mode) |
| 9 | Allowlist server IP | RazorpayX → Settings → IP Allowlist |

### After Completing Razorpay Setup

You will have:
- `RAZORPAY_KEY_ID` (rzp_live_...)
- `RAZORPAY_KEY_SECRET`
- `RAZORPAY_SOURCE_ACCOUNT` (your RazorpayX Lite account number)

---

## Part B: Server Deployment

### Option 1: Docker (Recommended)

**Prerequisites:** Docker installed on your server

```bash
# On your server (e.g. Ubuntu)
cd /var/www
git clone https://github.com/vikramsankhala/UPI-Penny-Drop-Verification.git penny-drop
cd penny-drop

# Create .env with your Razorpay credentials
nano .env
# Add:
# RAZORPAY_KEY_ID=rzp_live_xxxx
# RAZORPAY_KEY_SECRET=your_secret
# RAZORPAY_SOURCE_ACCOUNT=your_account_number

# Build and run
docker build -t penny-drop .
docker run -d --name penny-drop -p 5000:5000 --env-file .env --restart unless-stopped penny-drop
```

### Option 2: Python + Gunicorn (Direct)

**Prerequisites:** Python 3.10+, nginx

```bash
# On your server
cd /var/www
git clone https://github.com/vikramsankhala/UPI-Penny-Drop-Verification.git penny-drop
cd penny-drop

python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Create .env with Razorpay credentials
nano .env

# Test run
gunicorn --bind 127.0.0.1:5000 app:app
```

### Option 3: Systemd Service

```bash
# Copy service file
sudo cp penny-drop.service /etc/systemd/system/
sudo nano /etc/systemd/system/penny-drop.service
# Update paths if needed (WorkingDirectory, ExecStart)

sudo systemctl daemon-reload
sudo systemctl enable penny-drop
sudo systemctl start penny-drop
sudo systemctl status penny-drop
```

---

## Part C: Nginx Reverse Proxy

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/penny-drop
sudo ln -s /etc/nginx/sites-available/penny-drop /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d gopalsankhala.in -d www.gopalsankhala.in
```

Then uncomment the HTTPS block in `nginx.conf` and restart nginx.

---

## Part D: DNS for gopalsankhala.in

Ensure your domain points to your server:

| Type | Name | Value |
|------|------|-------|
| A | @ | Your server IP |
| A | www | Your server IP |

---

## Part E: Razorpay IP Allowlist

After deployment, add your **server's public IP** to Razorpay:

1. Go to [RazorpayX Dashboard](https://x.razorpay.com) → Settings → IP Allowlist
2. Add your server IP (e.g. from `curl ifconfig.me` on the server)

---

## Verification

1. Visit **https://gopalsankhala.in** (or http://)
2. You should see the app without "Demo mode" badge
3. Try a verification — it should call Razorpay live API

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Still shows Demo mode | Check .env is loaded, env vars are set |
| 401 from Razorpay | Verify API keys, no extra spaces in .env |
| IP not allowlisted | Add server IP in RazorpayX Settings |
| 502 Bad Gateway | Check gunicorn/docker is running on port 5000 |
