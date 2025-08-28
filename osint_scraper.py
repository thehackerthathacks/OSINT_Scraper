import requests
import argparse
import json
import sys
import hashlib
import re
import dns.resolver

def username_search(username):
    sources = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "Medium": f"https://medium.com/@{username}",
        "StackOverflow": f"https://stackoverflow.com/users/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "YouTube": f"https://www.youtube.com/c/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Keybase": f"https://keybase.io/{username}"
    }
    results = {}
    headers = {"User-Agent": "OSINT-Username-Checker"}
    for site, url in sources.items():
        try:
            resp = requests.get(url, timeout=5, headers=headers)
            results[site] = "Found" if resp.status_code == 200 else "Not Found"
        except requests.exceptions.RequestException:
            results[site] = "Error"
    return results

def check_gravatar(email):
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode()).hexdigest()
    try:
        resp = requests.get(gravatar_url + "?d=404", timeout=5)
        return "Found" if resp.status_code == 200 else "Not Found"
    except requests.exceptions.RequestException:
        return "Error"

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return "Valid" if re.match(pattern, email) else "Invalid"

def check_mx(email):
    domain = email.split("@")[-1]
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return "Exists" if answers else "Not Found"
    except Exception:
        return "Not Found"

def main():
    parser = argparse.ArgumentParser(description="OSINT Username/Email Scraper (No API Key Required)")
    parser.add_argument("--email", help="Email to check")
    parser.add_argument("--username", help="Username to search on popular platforms")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    results = {}

    if args.email:
        results['email'] = args.email
        results['validation'] = validate_email(args.email)
        results['gravatar'] = check_gravatar(args.email)
        results['mx_record'] = check_mx(args.email)
    
    if args.username:
        results['username'] = args.username
        results['accounts'] = username_search(args.username)

    if args.json:
        print(json.dumps(results, indent=4))
    else:
        if 'email' in results:
            print(f"\n[+] Email: {results['email']}")
            print(f"Validation: {results['validation']}")
            print(f"Gravatar: {results['gravatar']}")
            print(f"MX record: {results['mx_record']}")
        if 'username' in results:
            print(f"\n[+] Username: {results['username']}")
            for site, status in results['accounts'].items():
                print(f"- {site}: {status}")

if __name__ == "__main__":
    if not (len(sys.argv) > 1):
        print("Use --help for usage instructions.")
        sys.exit()
    main()
