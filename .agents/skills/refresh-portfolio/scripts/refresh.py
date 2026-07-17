"""
Description: Helper script to parse .env for usernames and run the portfolio ingestion tool.
Why: Automates refreshing Medium, Dev.to, and GitHub sources by dynamically extracting usernames.
How: Parses .env, extracts/infers usernames, and executes the app.tools.ingest module using subprocess.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def parse_env(env_path: Path) -> dict[str, str]:
    """
    Simple parser for env files that handles exports and quotes.
    """
    vars_dict = {}
    if not env_path.exists():
        return vars_dict

    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Remove optional 'export ' prefix
            if line.startswith("export "):
                line = line[7:]
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            # Strip quotes
            if (val.startswith('"') and val.endswith('"')) or (
                val.startswith("'") and val.endswith("'")
            ):
                val = val[1:-1]
            vars_dict[key] = val
    return vars_dict


def main():
    # Parse CLI arguments first to extract github-user and other options
    parser = argparse.ArgumentParser(description="Refresh portfolio data.")
    parser.add_argument(
        "--github-user",
        required=True,
        help="GitHub username (required, not hardcoded for security)",
    )

    # We use parse_known_args to collect any other args (like --simulate) and pass them down
    args, unknown_args = parser.parse_known_args()
    github_user = args.github_user

    # Find .env in the current directory or parent directories
    current_dir = Path.cwd()
    env_file = current_dir / ".env"

    # Fallback to walk up to find .env if not in current directory
    for parent in [current_dir, *current_dir.parents]:
        if (parent / ".env").exists():
            env_file = parent / ".env"
            break

    env_vars = parse_env(env_file)

    # 1. Parse Medium username from MEDIUM_PROFILE
    medium_profile = env_vars.get("MEDIUM_PROFILE", "")
    medium_user = None
    if medium_profile:
        # Match e.g. https://medium.com/@username
        match = re.search(r"medium\.com/(@[a-zA-Z0-9_.-]+)", medium_profile)
        if match:
            medium_user = match.group(1)
        else:
            # Fallback to last URL path component
            medium_user = medium_profile.rstrip("/").split("/")[-1]

    # 2. Parse Dev.to username from DEVTO_PROFILE
    devto_profile = env_vars.get("DEVTO_PROFILE", "")
    devto_user = None
    if devto_profile:
        # Get last path segment
        devto_user = devto_profile.rstrip("/").split("/")[-1]

    print("Parsed/Inferred usernames:")
    print(f"  GitHub: {github_user}")
    print(f"  Medium: {medium_user}")
    print(f"  Dev.to: {devto_user}")

    # Build command
    cmd = [
        "uv",
        "run",
        "python",
        "-m",
        "app.tools.ingest",
        "--github-user",
        github_user,
    ]
    if medium_user:
        cmd.extend(["--medium-user", medium_user])
    if devto_user:
        cmd.extend(["--devto-user", devto_user])

    # Pass along any extra arguments (like --simulate)
    cmd.extend(unknown_args)

    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
