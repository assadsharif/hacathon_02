# Render Deployment Guide - Backend with Built-in HTTPS

This guide walks you through deploying the FastAPI backend to Render with automatic HTTPS.

## 🌟 Why Render?

- ✅ **Automatic HTTPS** - Free SSL certificates, no configuration needed
- ✅ **Free Tier** - 750 hours/month for web services
- ✅ **Zero Config** - Deploy from GitHub in minutes
- ✅ **Built-in CI/CD** - Auto-deploy on git push
- ✅ **Environment Variables** - Secure secret management
- ✅ **Health Checks** - Automatic monitoring

---

## 📋 Prerequisites

1. **GitHub Repository** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at https://render.com (free)
3. **Database URL** - Your Neon PostgreSQL connection string
4. **JWT Secret** - Your JWT secret key

---

## 🚀 Deployment Steps

### Step 1: Sign Up / Log In to Render

1. Go to https://render.com
2. Click **"Get Started"** or **"Sign In"**
3. Sign up with GitHub (recommended for easy deployment)

### Step 2: Create New Web Service

1. From your Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if not already connected
   - Select your `Hackathon_02` repository
   - Click **"Connect"**

### Step 3: Configure Web Service

Fill in the following details:

**Basic Settings:**
- **Name:** `todo-chatbot-backend`
- **Region:** `Oregon (US West)` (or closest to you)
- **Branch:** `main`
- **Root Directory:** Leave empty (or set to `backend` if needed)
- **Runtime:** `Docker`

**Build Settings:**
- **Dockerfile Path:** `./backend/Dockerfile`
- **Docker Build Context Directory:** `./backend`

**Instance Type:**
- Select **"Free"** ($0/month, 750 hours included)

### Step 4: Add Environment Variables

Click **"Advanced"** and add the following environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | `postgresql://neondb_owner:***@ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require` | Your Neon connection string |
| `JWT_SECRET` | `your-jwt-secret-here` | Same as used in frontend |
| `CORS_ORIGINS` | `*` | Allow all origins (or specify Vercel domain) |
| `PORT` | `8000` | Render will inject this automatically |

**To get your secrets from Kubernetes:**

```bash
# Get DATABASE_URL
kubectl get secret todo-chatbot-secrets -n todo-chatbot -o jsonpath='{.data.database-url}' | base64 -d

# Get JWT_SECRET
kubectl get secret todo-chatbot-secrets -n todo-chatbot -o jsonpath='{.data.jwt-secret}' | base64 -d
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Build the Docker image
   - Deploy to a container
   - Provision HTTPS certificate
   - Assign a public URL

**Build Time:** ~2-5 minutes

### Step 6: Wait for Deployment

Monitor the build logs in real-time:
- ✅ **Building** - Docker image being built
- ✅ **Deploying** - Container starting
- ✅ **Live** - Service is running

You'll see logs like:
```
Building...
[build output]
Deploying...
==> Your service is live 🎉
https://todo-chatbot-backend-xxxx.onrender.com
```

---

## ✅ Verification

### 1. Check Service Status

In Render dashboard:
- Status should show **"Live"** with green indicator
- Health check should be passing

### 2. Test Health Endpoint

```bash
# Get your Render URL from the dashboard
RENDER_URL="https://todo-chatbot-backend-xxxx.onrender.com"

# Test health endpoint
curl $RENDER_URL/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "todo-api",
  "version": "1.0.0"
}
```

### 3. Test API Documentation

Open in browser:
```
https://todo-chatbot-backend-xxxx.onrender.com/docs
```

You should see the Swagger UI with all API endpoints.

### 4. Verify HTTPS Certificate

```bash
curl -v https://todo-chatbot-backend-xxxx.onrender.com/health 2>&1 | grep -E "subject:|issuer:"
```

**Expected Output:**
```
*  subject: CN=*.onrender.com
*  issuer: C=US; O=Let's Encrypt; CN=R10
```

✅ Certificate is valid and trusted!

---

## 🔄 Connect Vercel Frontend to Render Backend

### Option 1: Update NEXT_PUBLIC_API_URL

```bash
# Update Vercel environment variable
vercel env rm NEXT_PUBLIC_API_URL production --yes
vercel env add NEXT_PUBLIC_API_URL production

# When prompted, enter:
https://todo-chatbot-backend-xxxx.onrender.com

# Redeploy
cd frontend
vercel --prod --yes
```

### Option 2: Update BACKEND_URL (for rewrites)

```bash
vercel env rm BACKEND_URL production --yes
vercel env add BACKEND_URL production

# When prompted, enter:
https://todo-chatbot-backend-xxxx.onrender.com

# Redeploy
vercel --prod --yes
```

---

## 📊 Monitoring & Logs

### View Logs

1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. See real-time application logs

### Health Checks

Render automatically monitors `/health` endpoint:
- **Interval:** 30 seconds
- **Timeout:** 10 seconds
- **Restarts:** Automatic if health check fails

### Metrics

Click **"Metrics"** tab to view:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🔧 Advanced Configuration

### Custom Domain

1. Go to service **"Settings"**
2. Scroll to **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain (e.g., `api.yourdomain.com`)
5. Add CNAME record to your DNS:
   ```
   CNAME api.yourdomain.com -> todo-chatbot-backend-xxxx.onrender.com
   ```
6. Wait for DNS propagation (~5 minutes)
7. Render automatically provisions SSL certificate

### Environment Variables Management

To update environment variables:
1. Go to service **"Environment"** tab
2. Edit or add variables
3. Click **"Save Changes"**
4. Service will automatically redeploy

### Auto-Deploy on Push

By default, Render auto-deploys when you push to `main` branch.

To disable:
1. Go to **"Settings"**
2. Scroll to **"Build & Deploy"**
3. Toggle **"Auto-Deploy"** off

### Manual Deploy

1. Go to **"Manual Deploy"** tab
2. Click **"Deploy latest commit"**
3. Or select a specific commit to deploy

---

## 🐛 Troubleshooting

### Build Fails

**Check build logs:**
1. Click on the failed build
2. Review error messages
3. Common issues:
   - Missing dependencies in `requirements.txt`
   - Dockerfile syntax errors
   - Build context path incorrect

**Solution:**
```bash
# Test Docker build locally
cd backend
docker build -t test-build .
```

### Service Won't Start

**Check logs for errors:**
- Database connection issues
- Missing environment variables
- Port binding errors

**Common fixes:**
```bash
# Verify DATABASE_URL is set correctly
# Check that PORT is not hardcoded (use $PORT from env)
```

### Health Check Failing

**Verify health endpoint:**
```bash
# SSH into Render shell (if available)
curl localhost:$PORT/health
```

**Fix:**
- Ensure `/health` endpoint returns 200 status
- Check health check path in Render settings

### Slow Cold Starts (Free Tier)

Free tier instances spin down after 15 minutes of inactivity.

**Workarounds:**
1. Upgrade to paid tier ($7/month) for always-on instances
2. Use a uptime monitoring service to ping every 10 minutes
3. Accept 30-60 second cold start delay

---

## 💰 Pricing

### Free Tier
- **750 hours/month** web service
- **Automatic HTTPS**
- **Sleep after 15 min inactivity**
- **Shared CPU**
- **512 MB RAM**

### Starter Plan ($7/month)
- **Always-on** instances
- **1 GB RAM**
- **No sleep**
- **Better performance**

**Recommendation:** Start with free tier, upgrade if needed.

---

## 🔐 Security Best Practices

1. **Secrets Management:**
   - Use Render environment variables (encrypted at rest)
   - Never commit secrets to git
   - Rotate JWT_SECRET periodically

2. **CORS Configuration:**
   - Set `CORS_ORIGINS` to specific domains in production
   - Example: `https://frontend-sigma-seven-25.vercel.app`

3. **Database:**
   - Always use SSL (`sslmode=require`)
   - Use connection pooling for efficiency

4. **HTTPS:**
   - Render handles HTTPS automatically
   - Certificates auto-renew
   - Force HTTPS redirects enabled by default

---

## 📚 Useful Resources

- [Render Documentation](https://render.com/docs)
- [Docker Deployment Guide](https://render.com/docs/docker)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Health Checks](https://render.com/docs/health-checks)
- [Custom Domains](https://render.com/docs/custom-domains)

---

## 🎯 Next Steps

After successful deployment:

1. ✅ Verify HTTPS certificate is working
2. ✅ Update Vercel frontend to use Render backend URL
3. ✅ Test full application flow (sign up, todos CRUD)
4. ✅ Set up monitoring/alerting (optional)
5. ✅ Consider upgrading to paid tier if needed

---

## 🆚 Comparison: Render vs AKS

| Feature | Render | AKS with cert-manager |
|---------|--------|----------------------|
| **Setup Time** | 5 minutes | 30+ minutes |
| **HTTPS** | Automatic | Manual setup |
| **Cost (Free)** | 750 hrs/month | Pay for infrastructure |
| **Scaling** | Click button | Configure HPA |
| **DevOps Knowledge** | None required | Kubernetes expertise |
| **Certificate Renewal** | Automatic | Automatic (cert-manager) |
| **Cold Starts** | Yes (free tier) | No |
| **Control** | Limited | Full control |

**Use Render if:** You want quick deployment with zero DevOps
**Use AKS if:** You need full control and already have K8s expertise

---

## ✅ Success Criteria

Your deployment is successful when:
- ✅ Render dashboard shows service as **"Live"**
- ✅ Health endpoint returns `{"status":"healthy"}`
- ✅ API docs accessible at `/docs`
- ✅ HTTPS certificate is valid (Let's Encrypt)
- ✅ Vercel frontend can connect to Render backend
- ✅ All CRUD operations work end-to-end

**Congratulations! You now have a backend deployed with built-in HTTPS! 🎉**
