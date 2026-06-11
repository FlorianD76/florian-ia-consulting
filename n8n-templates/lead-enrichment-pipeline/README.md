# Lead Enrichment Pipeline — n8n Template

## What This Workflow Does

Automatically enriches prospect data from multiple sources:
1. Takes a raw lead list (CSV or manual input)
2. Looks up company info (Hunter, Clearbit, LinkedIn)
3. Finds missing email addresses
4. Enriches with job title, company size, industry
5. Uploads enriched data back to your CRM (Salesforce, HubSpot)

## Why It Matters

Manual lead enrichment = 5 minutes per lead. This workflow = 10 seconds per lead.

**Example:** 100 leads × 5 minutes = 8+ hours. This saves you 8 hours per batch.

## How to Use This Template

1. **Download the workflow JSON** from this folder
2. **Import into your n8n instance** (Settings → Workflows → Import)
3. **Connect your sources:**
   - Input: Google Sheets, CSV upload, or form submission
   - Enrichment APIs: Hunter, Clearbit (free tier available)
   - Output: Salesforce, HubSpot, or Google Sheets
4. **Test with 5 leads first**, then scale to full lists
5. **Schedule it** (daily, weekly) to run automatically

## APIs You'll Need

- **Hunter.io** — Find work emails (free tier: 100/month)
- **Clearbit** — Company data (free tier: 50/month)
- **Your CRM** — API key to connect (Salesforce/HubSpot both free)

## Modifications for Your Business

- Change the fields (email, phone, job title, etc.)
- Add more enrichment sources (LinkedIn Sales Navigator, Apollo.io, etc.)
- Route to different CRM fields based on company size/industry
- Add filtering (only enrich if missing email, only B2B, etc.)

## Time to Set Up

- First time: 20 minutes (get API keys, connect apps)
- Template runs automatically after that

## Questions?

Email me: dierckx.florian@gmail.com

---

**Next Steps:**
1. Download the workflow.json file
2. Get API keys from Hunter & Clearbit (both have free tiers)
3. Follow the setup guide in the n8n UI
4. Start with 5 test leads
