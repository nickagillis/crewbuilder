# Railway Deployment Setup for CrewBuilder

## Prerequisites

1. **Railway Account**: Sign up at https://railway.app
2. **Railway CLI** (optional): `npm install -g @railway/cli`
3. **Railway API Token**: Get from https://railway.app/account/tokens

## Quick Setup

### 1. Set Railway Token

Add to your `.env` file:
```env
RAILWAY_TOKEN=your_railway_token_here
```

### 2. Test Deployment

1. Start backend: `py api_server.py`
2. Start frontend: `cd web && npm run dev`
3. Open http://localhost:3000
4. Generate a system
5. Click "Deploy to Railway"
6. Enter your OpenAI API key
7. Click "Deploy Now"

## What Gets Deployed

When you deploy a CrewAI system to Railway:

- **Python Application**: Your generated CrewAI agents
- **Environment Variables**: API keys securely stored
- **Auto-scaling**: Railway handles traffic automatically
- **Monitoring**: Built-in logs and metrics
- **HTTPS**: Automatic SSL certificates

## Cost Estimates

- **Hobby Plan**: $5/month (includes $5 of usage)
- **Typical CrewAI System**: ~$5-20/month depending on usage
- **Free Trial**: $5 credit for new accounts

## Deployment Architecture

```
Your Browser → CrewBuilder Frontend
                    ↓
              Generate System
                    ↓
              Deploy to Railway
                    ↓
        Live CrewAI System Running
        (https://your-system.up.railway.app)
```

## Manual Railway Deployment (Alternative)

If automatic deployment fails:

1. Download generated code from CrewBuilder
2. Create new Railway project
3. Connect GitHub repo or drag files
4. Set environment variables in Railway dashboard
5. Deploy!

## Troubleshooting

### "Railway token not found"
- Ensure RAILWAY_TOKEN is set in .env
- Restart the API server after setting token

### "Deployment failed"
- Check Railway dashboard for build logs
- Ensure all API keys are correct
- Verify Python version compatibility

### "System not accessible"
- Wait 2-3 minutes for deployment to complete
- Check Railway dashboard for deployment status
- Ensure PORT environment variable is set

## Advanced Configuration

### Custom Domains
1. Go to Railway project settings
2. Add custom domain
3. Update DNS records

### Persistent Storage
1. Add PostgreSQL database in Railway
2. Update generated code to use database
3. Redeploy

### Scheduled Tasks
1. Use Railway's cron job feature
2. Configure in railway.json
3. Set schedule in dashboard

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- CrewBuilder Issues: Create issue in this repo