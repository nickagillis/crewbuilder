# CrewBuilder Deployment Architecture

## Overview

CrewBuilder has two deployment layers:
1. **Platform Layer**: The CrewBuilder system itself (10 agents, web UI)
2. **Customer Layer**: Generated AI agent systems for each user

## Deployment Options

### Option 1: Fully Managed (Recommended)
```
Railway (Your Account)
├── crewbuilder-platform/          # Main CrewBuilder app
│   ├── Frontend (Next.js)
│   ├── Backend (FastAPI)
│   └── Costs: ~$20-50/month
│
├── customer-001-blog-agents/      # Isolated project
│   ├── Generated CrewAI system
│   ├── Customer's API keys (encrypted)
│   └── Costs: ~$5-20/month (bill customer $49/month)
│
├── customer-002-sales-agents/     # Isolated project
│   └── ... (same structure)
│
└── customer-003-data-agents/      # Isolated project
    └── ... (same structure)
```

**Pros:**
- Full control over deployments
- Consolidated billing
- Easy monitoring and support
- Recurring revenue model

**Cons:**
- You pay Railway bills upfront
- Need to manage scaling
- Responsible for uptime

### Option 2: Deploy to Customer's Railway
```
Your Railway:
└── crewbuilder-platform/

Customer's Railway:
└── their-generated-system/
```

**Implementation:**
```python
# In railway_deployer.py
def deploy_to_customer_railway(customer_railway_token, generated_code):
    # Use customer's token instead of yours
    deployer = RailwayDeployer(railway_token=customer_railway_token)
    return deployer.deploy_crewai_system(...)
```

**Pros:**
- Customer pays Railway directly
- No infrastructure costs for you
- Unlimited scaling

**Cons:**
- Less control
- Harder to support
- One-time revenue only

### Option 3: Hybrid Approach
- Start with managed hosting
- Offer "bring your own Railway" for enterprise
- Charge more for managed vs self-hosted

## Implementation Details

### For Managed Hosting:
1. **Project Naming Convention**:
   ```
   crewbuilder-{user_id}-{project_name}-{timestamp}
   ```

2. **Resource Isolation**:
   - Each deployment is a separate Railway project
   - No shared resources between customers
   - Independent scaling and billing

3. **Cost Tracking**:
   ```python
   # Track costs per customer
   customer_costs = {
       "user_001": {
           "project_id": "prj_xxx",
           "monthly_cost": 15.32,
           "api_calls": 1523
       }
   }
   ```

4. **Security**:
   - Customer API keys encrypted at rest
   - Environment variables isolated per project
   - No cross-project access

### For Customer Railway:
1. **Onboarding Flow**:
   - Customer provides Railway token
   - We deploy to their account
   - They manage their own billing

2. **Support Model**:
   - Provide deployment package
   - Customer handles infrastructure
   - We support the code only

## Recommended First Step

Start with **Option 1 (Fully Managed)** because:
- Simpler to implement
- Better user experience
- Recurring revenue
- You can add Option 2 later

## Billing Models

### Managed Hosting Pricing:
- **Starter**: $49/month (1 system, $5-10 Railway cost)
- **Pro**: $149/month (5 systems, $25-50 Railway cost)
- **Enterprise**: $499/month (unlimited, custom)

### Self-Hosted Pricing:
- **One-time**: $299 deployment fee
- **With support**: $99/month maintenance

## Next Steps

1. Deploy CrewBuilder platform to Railway first
2. Test managed customer deployments
3. Track actual costs for 1 week
4. Finalize pricing based on real data
5. Add customer Railway option later