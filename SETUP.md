# Repository Setup Guide

This document explains how to configure the required secrets and settings for this automated GitHub profile repository.

## Required GitHub Secrets

This repository requires **4 GitHub Secrets** to be configured. Go to **Settings > Secrets and variables > Actions** in your repository to add them.

### 1. WAKATIME_API_KEY

**Purpose:** Fetches your coding activity statistics from WakaTime

**How to obtain:**
1. Create a WakaTime account at https://wakatime.com
2. Install the WakaTime plugin for your IDE/editor
3. Go to https://wakatime.com/settings/api-key
4. Copy your API key (starts with `waka_`)

**Permissions needed:** Read access to your WakaTime coding statistics

**Used in workflows:**
- `.github/workflows/waka-readme.yml` (every 6 hours)
- `.github/workflows/wakatime-readme.yml` (daily at midnight UTC)

---

### 2. GOOGLE_API_KEY

**Purpose:** Generates natural language summaries of your coding activity using Google Gemini AI

**How to obtain:**
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key for Google Generative AI
3. Copy the API key (starts with `AIza`)

**Permissions needed:** Access to Google Generative AI (Gemini Pro model)

**Used in workflows:**
- `.github/workflows/wakatime-readme.yml` (daily at midnight UTC)

**Note:** The free tier should be sufficient for this use case (one request per day)

---

### 3. CLAUDE_CODE_OAUTH_TOKEN

**Purpose:** Enables Claude AI to perform code reviews and respond to @claude mentions

**How to obtain:**
1. Visit https://claude.ai/oauth (or check Anthropic's documentation for latest OAuth flow)
2. Generate an OAuth token for GitHub Actions
3. Grant necessary permissions for reading repositories and posting comments

**Permissions needed:**
- Read repository contents
- Post comments on issues and pull requests
- Read CI/CD results

**Used in workflows:**
- `.github/workflows/claude-code-review.yml` (on PR creation/updates)
- `.github/workflows/claude.yml` (when @claude is mentioned)

---

### 4. CLAUDE_CODE_OAUTH_TOKEN_SCHEDULER

**Purpose:** Separate OAuth token for scheduled Claude health checks

**How to obtain:**
Same process as `CLAUDE_CODE_OAUTH_TOKEN` (see above)

**Why separate token?**
- Allows independent token rotation
- Provides isolation between interactive and scheduled operations
- Enables separate rate limiting

**Used in workflows:**
- `.github/workflows/claude-scheduler.yml` (4 times daily at 0:00, 5:00, 10:00, 15:00 UTC)

**Note:** You can use the same token as `CLAUDE_CODE_OAUTH_TOKEN` if you prefer

---

## README.md Configuration

Your `README.md` must contain these marker comments for automated updates:

```markdown
<!-- WakaTime stats section -->
<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

<!-- AI-generated summary section -->
<!--START_SECTION:recentwaka-->
<!--END_SECTION:recentwaka-->
```

The workflows will automatically inject content between these markers.

---

## Workflow Schedule Summary

| Workflow | Frequency | Purpose |
|----------|-----------|---------|
| `waka-readme.yml` | Every 6 hours | Updates WakaTime coding stats |
| `wakatime-readme.yml` | Daily at midnight UTC | Generates AI summary of weekly activity |
| `update-readme.yml` | Every 30 minutes | Updates GitHub activity feed |
| `claude-code-review.yml` | On PR events | Automated code reviews |
| `claude.yml` | On @claude mentions | Interactive AI assistance |
| `claude-scheduler.yml` | 4 times daily | Repository health checks |

---

## Security Best Practices

### Secret Rotation

Rotate all API keys and OAuth tokens regularly:
- **WakaTime API Key:** Every 90 days
- **Google API Key:** Every 90 days
- **Claude OAuth Tokens:** Every 60 days

### Monitoring

Check workflow runs regularly:
```
Repository > Actions tab
```

Look for:
- ✅ Successful runs
- ❌ Failed runs (investigate immediately)
- ⚠️ Rate limit warnings

### Rate Limits

Be aware of API rate limits:
- **WakaTime:** Check https://wakatime.com/api#rate-limit
- **Google Generative AI:** Free tier limits apply
- **GitHub Actions:** 2,000 minutes/month for free accounts

---

## Troubleshooting

### "Invalid or missing WAKATIME_API_KEY"

**Cause:** API key is not set or doesn't start with `waka_`

**Solution:**
1. Verify secret is named exactly `WAKATIME_API_KEY`
2. Ensure the value starts with `waka_`
3. Generate a new key if needed

### "Invalid or missing GOOGLE_API_KEY"

**Cause:** API key is not set or doesn't start with `AIza`

**Solution:**
1. Verify secret is named exactly `GOOGLE_API_KEY`
2. Ensure the value starts with `AIza`
3. Enable the Generative AI API in Google Cloud Console

### "Markers not found in README.md"

**Cause:** Missing comment markers in README.md

**Solution:**
Add these lines to your README.md:
```markdown
<!--START_SECTION:recentwaka-->
<!--END_SECTION:recentwaka-->
```

### Workflow Failures

Check the Actions tab for detailed error logs:
```
Repository > Actions > [Failed Workflow] > View logs
```

---

## Testing Changes

Before committing workflow changes:

1. **Test Python scripts locally:**
   ```bash
   # Set environment variables
   export WAKATIME_API_KEY="your_key"
   export GOOGLE_API_KEY="your_key"

   # Install dependencies
   pip install -r requirements.txt

   # Test each script
   python fetch_wakatime.py
   python generate_summary.py
   python update_readme.py
   ```

2. **Validate workflow syntax:**
   ```bash
   # Use actionlint or GitHub's workflow validator
   actionlint .github/workflows/*.yml
   ```

3. **Test with workflow_dispatch:**
   Go to Actions tab and manually trigger workflows before relying on schedules

---

## Dependencies

Python packages (defined in `requirements.txt`):
- `requests==2.31.0` - HTTP requests for WakaTime API
- `google-generativeai==0.3.2` - Google Gemini AI integration

---

## Support

- **WakaTime Issues:** https://github.com/wakatime/wakatime/issues
- **Google AI Issues:** https://developers.google.com/generative-ai-sdk
- **Claude Code Issues:** https://github.com/anthropics/claude-code/issues
- **This Repository:** Open an issue for questions

---

## License

This setup is based on open-source GitHub Actions and public APIs. Refer to each service's terms of service:
- https://wakatime.com/terms
- https://ai.google.dev/terms
- https://www.anthropic.com/legal/terms

---

**Last Updated:** 2025-11-06
