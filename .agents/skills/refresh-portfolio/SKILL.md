---
name: refresh-portfolio
description: Refresh the portfolio's blog posts (Medium, Dev.to) and GitHub repositories by running the ingestion tool. Dynamic usernames are extracted from the `.env` file.
---
To refresh the portfolio content (blogs from Medium and Dev.to, and GitHub repositories), use this skill.

This skill runs the helper script at `.agents/skills/refresh-portfolio/scripts/refresh.py`, which parses the `.env` file to extract Medium/Dev.to profiles, infers the correct usernames, and executes `uv run python -m app.tools.ingest`.

Since the GitHub username should not be hardcoded in public repository files, it must be provided as a command-line argument when executing the script.

### Execution
You can execute this sync in simulation mode (dry run) or run it for real.

**Run in simulation mode (recommended first step to verify usernames and connections):**
```bash
uv run python .agents/skills/refresh-portfolio/scripts/refresh.py --github-user <github_user> --simulate
```

**Run real ingestion:**
```bash
uv run python .agents/skills/refresh-portfolio/scripts/refresh.py --github-user <github_user>
```

### Reporting Back
After running the script, you MUST parse the output of the ingestion tool to report the sync status back to the user:
1. Extract and display the inferred/parsed usernames (GitHub, Medium, Dev.to).
2. Report any errors (e.g. rate limits on GitHub or connectivity issues).
3. Display the **Ingestion Summary** showing:
   - For each platform (MEDIUM, DEVTO, GITHUB):
     - New items created.
     - Items updated or patched.
     - AI Enriched items.
     - Skipped (existing) items.
