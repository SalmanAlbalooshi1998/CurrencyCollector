# 🔐 SECURITY TOKENS - Currency Collector

## **GENERATED SECURE TOKENS**

These tokens were generated using Python's `secrets` module with cryptographically secure random number generation.

### **Production Environment Variables**

```env
# Web Login Password (16 characters with special chars)
APP_PASSWORD=OwFuT*iQ%q3sYED@

# API Bearer Token (32 characters, URL-safe)
API_TOKEN=8shIm33PmVT5on1WjIq6X4qU6hseJYtV

# Session Cookie Secret (64 characters, URL-safe)
SESSION_SECRET=eTktz1Rl9uMxpu-teQTIHSXh8MIbGP3VIQILyDd-5qlFhA7NL8pPmMtQft0MNgme

# CSV Database Path
CSV_PATH=./sample_notes.csv

# CORS Origin (use your domain for production)
ALLOW_ORIGIN=*
```

## **SECURITY SPECIFICATIONS**

| Token Type | Length | Character Set | Security Level |
|------------|--------|---------------|----------------|
| **APP_PASSWORD** | 16 chars | Letters, digits, special chars | High |
| **API_TOKEN** | 32 chars | Letters, digits, hyphens, underscores | Very High |
| **SESSION_SECRET** | 64 chars | Letters, digits, hyphens, underscores | Very High |

## **BEST PRACTICES IMPLEMENTED**

✅ **Cryptographically Secure**: Uses `secrets.choice()` instead of `random.choice()`
✅ **URL-Safe Characters**: API tokens use URL-safe character set
✅ **Sufficient Length**: Session secret is 64 characters (exceeds 32-char minimum)
✅ **Mixed Character Sets**: Passwords include special characters
✅ **No Predictable Patterns**: Completely random generation
✅ **Production Ready**: Suitable for production deployment

## **DEPLOYMENT INSTRUCTIONS**

1. **Copy the tokens** to your `.env` file on PythonAnywhere
2. **Never commit** these tokens to version control
3. **Store securely** and limit access
4. **Rotate regularly** in production (recommended: every 90 days)
5. **Use different tokens** for each environment (dev/staging/prod)

## **SECURITY WARNINGS**

⚠️ **NEVER share these tokens publicly**
⚠️ **NEVER commit to version control**
⚠️ **NEVER use the same tokens across environments**
⚠️ **ALWAYS use HTTPS in production**
⚠️ **ROTATE tokens regularly**

## **TOKEN ROTATION**

To generate new tokens, run:
```bash
python generate_tokens.py
```

This will create new secure tokens that you can use to replace the current ones.

---

**🔒 These tokens are production-ready and follow security best practices.**
