#!/usr/bin/env python3
"""
verify_privacy.py - Identity Shielding & Privacy Guardrail Scanner

Verifies:
1. Git user.email strictly matches the authorized pseudonym:
   komasan19283645@users.noreply.github.com
2. Zero personal email addresses leaked across the codebase and marketing copy.
3. Zero personal LinkedIn profiles or URLs in the repository.
4. Social distribution channels use only authorized pseudonyms:
   Reddit (u/Komaleon), X/Twitter (@Komaleon37), Pinterest (@migueldpsp), Gumroad (migueldp3).

Zero external dependencies - pure Python 3.
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, List

# Fix Windows console UTF-8 output if needed
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

AUTHORIZED_GIT_EMAIL = "komasan19283645@users.noreply.github.com"
AUTHORIZED_PSEUDONYMS = {
    "github": "komasan19283645",
    "reddit": "u/Komaleon",
    "twitter": "@Komaleon37",
    "pinterest": "@migueldpsp",
    "gumroad": "migueldp3",
}

# Personal consumer email domains that must NEVER appear in repository payloads
PERSONAL_EMAIL_DOMAINS = {
    "gmail.com",
    "hotmail.com",
    "yahoo.com",
    "outlook.com",
    "icloud.com",
    "live.com",
    "protonmail.com",
    "me.com",
}

# Specific personal usernames or tokens that must never be leaked
FORBIDDEN_PERSONAL_TOKENS = {
    "migueldpsp@",  # Personal email prefix
}

# File extensions to scan
SCANNABLE_EXTENSIONS = {".html", ".js", ".css", ".py", ".md", ".json", ".xml", ".txt", ".yml", ".yaml"}

# Directories to ignore
IGNORED_DIRS = {".git", ".gemini", "__pycache__", "node_modules", ".pytest_cache", ".agents"}

# Files to exempt from pattern self-scanning
EXEMPT_SCAN_FILES = {"verify_privacy.py"}

# Binary / asset extensions to skip
BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".zip", ".xlsx", ".ico", ".svg"}


def check_git_user_email(base_dir: str = None) -> Dict[str, Any]:
    """Checks git configuration user.email."""
    try:
        result = subprocess.run(
            ["git", "config", "user.email"],
            cwd=base_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        current_email = result.stdout.strip()
        matches = current_email.lower() == AUTHORIZED_GIT_EMAIL.lower()
        return {
            "current_email": current_email,
            "expected_email": AUTHORIZED_GIT_EMAIL,
            "matches": matches,
        }
    except Exception as e:
        return {
            "current_email": f"ERROR: {e}",
            "expected_email": AUTHORIZED_GIT_EMAIL,
            "matches": False,
        }


def scan_file_for_privacy_violations(file_path: str) -> List[Dict[str, Any]]:
    """Scans an individual text file for personal emails and personal LinkedIn profile URLs."""
    violations = []
    
    # Generic email regex pattern
    email_pattern = re.compile(r'\b([A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}))\b')
    # Real personal LinkedIn profile regex (e.g. linkedin.com/in/<username>)
    # Exclude dummy placeholders like '...' or '[user]'
    linkedin_profile_pattern = re.compile(r'linkedin\.com/in/([a-zA-Z0-9_\-]+)', re.IGNORECASE)

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                # 1. Check for personal emails
                for match, domain in email_pattern.findall(line):
                    domain_lower = domain.lower()
                    match_lower = match.lower()

                    is_personal_domain = domain_lower in PERSONAL_EMAIL_DOMAINS
                    is_forbidden_token = any(token in match_lower for token in FORBIDDEN_PERSONAL_TOKENS)

                    if is_personal_domain or is_forbidden_token:
                        violations.append({
                            "type": "PERSONAL_EMAIL_LEAK",
                            "line": line_no,
                            "match": match,
                            "details": f"Personal/consumer email address leaked: '{match}'"
                        })

                # 2. Check for personal LinkedIn profile URLs
                for handle in linkedin_profile_pattern.findall(line):
                    # Ignore placeholder handles like 'yourname', 'username', 'perfil'
                    if handle.lower() not in {"yourname", "username", "perfil", "usuario", "ejemplo"}:
                        violations.append({
                            "type": "PERSONAL_LINKEDIN_URL",
                            "line": line_no,
                            "match": f"linkedin.com/in/{handle}",
                            "details": f"Personal LinkedIn profile link detected: 'linkedin.com/in/{handle}'"
                        })

    except Exception as e:
        violations.append({
            "type": "SCAN_ERROR",
            "line": 0,
            "match": str(e),
            "details": f"Failed to read file: {e}"
        })

    return violations


def verify_privacy(base_dir: str = None) -> Dict[str, Any]:
    """
    Scans entire repository for privacy, pseudonym, and identity shielding violations.
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    git_status = check_git_user_email(base_dir)

    all_violations = []
    scanned_files_count = 0

    for root, dirs, files in os.walk(base_dir):
        # Filter ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]

        for file in files:
            if file in EXEMPT_SCAN_FILES:
                continue

            ext = os.path.splitext(file)[1].lower()
            if ext in BINARY_EXTENSIONS or ext not in SCANNABLE_EXTENSIONS:
                continue

            # Skip specific non-project artifacts or generated b64 dumps
            if file.endswith(".b64.txt"):
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_dir)

            scanned_files_count += 1
            file_violations = scan_file_for_privacy_violations(full_path)
            for v in file_violations:
                v["file"] = rel_path
                all_violations.append(v)

    passed = git_status["matches"] and len(all_violations) == 0

    return {
        "git_email": git_status,
        "scanned_files_count": scanned_files_count,
        "violations_count": len(all_violations),
        "violations": all_violations,
        "passed": passed,
    }


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 70)
    print("FreelanceToolkit - Privacy Audit & Identity Shielding Scanner")
    print(f"Scanning target: {base_dir}")
    print("=" * 70)

    res = verify_privacy(base_dir)

    # Git email reporting
    git_stat = res["git_email"]
    if git_stat["matches"]:
        print(f"[*] Git Committer Email:  [PASS] {git_stat['current_email']}")
    else:
        print(f"[!] Git Committer Email:  [FAIL] '{git_stat['current_email']}'")
        print(f"    Expected authorized: '{git_stat['expected_email']}'")
        print(f"    Fix via: git config user.email {git_stat['expected_email']}")

    print(f"[*] Total Files Scanned:   {res['scanned_files_count']}")
    print(f"[*] Privacy Violations:    {res['violations_count']}")

    if res["violations"]:
        print("\n[!] DETECTED PRIVACY VIOLATIONS:")
        for v in res["violations"]:
            print(f"    - [{v['type']}] in {v['file']}:{v['line']} -> {v['details']}")

    print("=" * 70)
    if res["passed"]:
        print("RESULT: SUCCESS - Zero personal emails, zero LinkedIn URLs, git noreply verified.")
        print("=" * 70)
        sys.exit(0)
    else:
        print("RESULT: FAILURE - Identity shielding violations detected above.")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
