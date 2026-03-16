# Add Razorpay Credentials to GitHub

Add these as **Repository Secrets** so workflows and deployments can use them.

## Steps

1. Go to **[github.com/vikramsankhala/UPI-Penny-Drop-Verification](https://github.com/vikramsankhala/UPI-Penny-Drop-Verification)**
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each:

| Secret Name | Value |
|-------------|-------|
| `RAZORPAY_KEY_ID` | `rzp_test_SRrvT3hLoMLgU3` |
| `RAZORPAY_KEY_SECRET` | `4Vv3m3ETgEH8d2WdMsWMFwZQ` |
| `RAZORPAY_SOURCE_ACCOUNT` | *(add when you have RazorpayX Lite)* |

## For GitHub Environments (e.g. Production)

If using Environments (Settings → Environments):

1. Create environment (e.g. `production`)
2. Add the same secrets under that environment

## Note

These are **Test** keys. Account validation (penny drop) requires **Live** keys and RazorpayX Lite. Test keys will keep the app in demo/mock mode until you switch to live credentials.
