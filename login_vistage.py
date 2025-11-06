# Login to Vistage using Firecrawl actions

from firecrawl import Firecrawl
import json

API_KEY = "fc-d2612b97887e49fe9b9464a597b99ee6"

# YOUR VISTAGE LOGIN CREDENTIALS
VISTAGE_EMAIL = 'tyler.smith@eosworldwide.com'
VISTAGE_PASSWORD = 'Rty1ers7!'

if VISTAGE_EMAIL == 'YOUR_EMAIL_HERE' or VISTAGE_PASSWORD == 'YOUR_PASSWORD_HERE':
    print("❌ Please set your Vistage email and password in this script first!")
    print("\nEdit lines 8-9:")
    print("  VISTAGE_EMAIL = 'your@email.com'")
    print("  VISTAGE_PASSWORD = 'yourpassword'")
    exit(1)

firecrawl = Firecrawl(api_key=API_KEY)

print("="*80)
print("VISTAGE LOGIN TEST")
print("="*80)
print(f"\n📧 Email: {VISTAGE_EMAIL}")
print("🔒 Password: " + "*" * len(VISTAGE_PASSWORD))
print("\n🔐 Attempting to log in...")

# Step 1: Log in using actions
login_result = firecrawl.scrape(
    url="https://myvistage.com/",
    formats=['markdown'],
    proxy='stealth',
    actions=[
        {"type": "wait", "milliseconds": 3000},
        {"type": "click", "selector": "input[type='text']"},
        {"type": "write", "text": VISTAGE_EMAIL},
        {"type": "wait", "milliseconds": 500},
        {"type": "click", "selector": "input[type='password']"},
        {"type": "write", "text": VISTAGE_PASSWORD},
        {"type": "wait", "milliseconds": 500},
        {"type": "press", "key": "Enter"},
        {"type": "wait", "milliseconds": 8000},
    ]
)

print("\n📄 After login:")
print("-"*80)

content = login_result.markdown[:1000] if login_result.markdown else "No content"

# Check if login succeeded
login_failed_keywords = ['sign in', 'login', 'password', 'username', 'incorrect']
login_succeeded = not any(keyword in content.lower() for keyword in login_failed_keywords)

print(f"Content length: {len(login_result.markdown) if login_result.markdown else 0} chars")
print(f"Login status: {'✅ SUCCESS' if login_succeeded else '❌ FAILED'}")

print(f"\nFirst 500 characters:")
print(content[:500])
print("-"*80)

if login_succeeded:
    print("\n✅ LOGIN SUCCESSFUL!")
    print("\nNow navigating to member directory in same session...")
    
    # Step 2: Navigate to member directory using JavaScript navigation
    member_dir = firecrawl.scrape(
        url="https://myvistage.com/",
        formats=['links', 'markdown'],
        proxy='stealth',
        actions=[
            {"type": "wait", "milliseconds": 3000},
            {"type": "click", "selector": "input[type='text']"},
            {"type": "write", "text": VISTAGE_EMAIL},
            {"type": "wait", "milliseconds": 500},
            {"type": "click", "selector": "input[type='password']"},
            {"type": "write", "text": VISTAGE_PASSWORD},
            {"type": "wait", "milliseconds": 500},
            {"type": "press", "key": "Enter"},
            {"type": "wait", "milliseconds": 8000},
            {"type": "executeJavascript", "script": "window.location.href = 'https://myvistage.com/people/?area=people&full_profile=&location_by=exact&distance=25&distance_units=miles&solr_fq%5B0%5D=roles:(member)'"},
            {"type": "wait", "milliseconds": 5000},
        ]
    )
    
    print(f"\n📋 Member Directory:")
    print(f"Content length: {len(member_dir.markdown) if member_dir.markdown else 0} chars")
    
    # Check for member profiles
    if hasattr(member_dir, 'links'):
        people_links = [link for link in member_dir.links if '/people/' in link and link.count('/') > 3]
        print(f"Found {len(people_links)} potential member profile links")
        
        # Save all links for inspection
        import json
        with open('all_directory_links.json', 'w') as f:
            json.dump(member_dir.links, f, indent=2)
        print(f"💾 Saved all {len(member_dir.links)} links to all_directory_links.json")
        
        # Save the full content too
        with open('member_directory_page.txt', 'w') as f:
            f.write(member_dir.markdown if member_dir.markdown else "")
        print(f"💾 Saved page content to member_directory_page.txt")
        
        if people_links:
            print("\n✅ Can access member directory!")
            print("\nSample member URLs:")
            for link in people_links[:5]:
                print(f"  - {link}")
        else:
            print("\n⚠️ No member profile links found")
            print("Content preview:")
            print(member_dir.markdown[:500] if member_dir.markdown else "No content")
else:
    print("\n❌ LOGIN FAILED")
    print("\nPossible issues:")
    print("1. Wrong username/password")
    print("2. Two-factor authentication enabled (needs additional code)")
    print("3. Site changed login form")
    print("\nCheck your credentials and try again.")
