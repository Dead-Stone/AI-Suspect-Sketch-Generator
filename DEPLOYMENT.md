# 🚀 AI Suspect Sketch Generator - Deployment Guide

## ⚠️ Important Notes Before Deployment

**Resource Requirements:**
- **Memory:** 8GB+ RAM recommended (AI model is memory-intensive)
- **Storage:** 10GB+ (model downloads ~4GB on first run)
- **GPU:** Optional but highly recommended for performance

**Model Download:**
- The app downloads Stable Diffusion model on first run
- This may take 5-10 minutes depending on internet speed
- Model is cached for subsequent runs

## 🎯 Deployment Options (Ranked by Recommendation)

### 1. 🏆 **Streamlit Community Cloud** (FREE - BEST OPTION)

**Perfect for:** Demo, portfolio, sharing with team

**Steps:**
1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `AI-Suspect-Sketch-Generator`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **URL:** You'll get a URL like `https://yourname-ai-suspect-sketch-generator.streamlit.app`

**Limitations:**
- 1GB RAM limit (may cause memory issues with large models)
- CPU only (slower generation)
- Public repositories only

### 2. 🔥 **Hugging Face Spaces** (FREE - GREAT FOR AI)

**Perfect for:** AI/ML community, better GPU access

**Steps:**
1. **Create Space:**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Streamlit" SDK
   - Name: `ai-suspect-sketch-generator`

2. **Upload Files:**
   - Upload all your project files
   - Ensure `app.py` is in root
   - Make sure `requirements.txt` is included

3. **Configuration:**
   - Space will build automatically
   - First run will download the model (takes time)

**Advantages:**
- Better hardware options
- GPU available on paid tiers
- Great for AI community

### 3. 🚄 **Railway** (PAID - BEST PERFORMANCE)

**Perfect for:** Production use, custom domain, scaling

**Steps:**
1. **Setup Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"

2. **Configure:**
   - Select your repository
   - Railway will auto-detect Streamlit app
   - Set environment variables if needed

3. **Custom Domain:**
   - Go to Settings → Domains
   - Add custom domain or use railway.app subdomain

**Cost:** ~$5-20/month depending on usage

### 4. 🐳 **Docker Deployment** (FLEXIBLE)

**Perfect for:** Self-hosting, cloud providers, full control

**Steps:**
1. **Build Image:**
   ```bash
   docker build -t ai-suspect-sketch .
   ```

2. **Run Container:**
   ```bash
   docker run -p 8501:8501 ai-suspect-sketch
   ```

3. **Deploy to Cloud:**
   - **Google Cloud Run**
   - **AWS ECS**
   - **Azure Container Instances**
   - **DigitalOcean App Platform**

## 🔧 Pre-Deployment Checklist

### Files Created for You:
- ✅ `runtime.txt` - Python version specification
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `Dockerfile` - Container configuration
- ✅ `DEPLOYMENT.md` - This guide

### Existing Files:
- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `generator.py` - AI model handler
- ✅ `style.css` - Custom styling

## 🚨 Deployment Considerations

### 1. **Model Access Token**
If you get authentication errors:
```bash
# Install huggingface-hub
pip install huggingface-hub

# Login with your token
huggingface-cli login
```

### 2. **Environment Variables** (Optional)
Create `.env` file for sensitive data:
```
HUGGINGFACE_TOKEN=your_token_here
CASE_DATA_PATH=/secure/path/
```

### 3. **Memory Optimization**
For limited memory environments, add to your app:
```python
# Add this to app.py if needed
torch.cuda.empty_cache()  # Clear GPU memory
```

### 4. **Security Considerations**
- Remove sensitive data from git history
- Use environment variables for secrets
- Consider authentication for production use

## 🎯 Recommended Deployment Path

**For Demo/Portfolio:** Streamlit Community Cloud
**For Production:** Railway or Hugging Face Spaces (paid tier)
**For Enterprise:** Docker on cloud provider

## 🆘 Troubleshooting

**Common Issues:**
1. **Memory Error:** Use smaller model or upgrade hosting tier
2. **Model Download Fails:** Check internet connection and Hugging Face access
3. **Audio Not Working:** Some hosting platforms don't support audio recording
4. **Slow Performance:** Use GPU-enabled hosting or optimize model settings

## 📞 Support
If you encounter issues, check the hosting platform's documentation or create an issue in the repository.

---
**Ready to Deploy?** Start with Streamlit Community Cloud for the easiest setup! 