# Vistage Member Scraper - Cookie-Based Authentication
# pip install firecrawl-py

import json
import time
import os
from firecrawl import Firecrawl

# Configuration
API_KEY = "fc-d2612b97887e49fe9b9464a597b99ee6"
DIRECTORY_URL = "https://myvistage.com/people/?area=people&full_profile=&location_by=exact&distance=25&distance_units=miles&solr_fq%5B0%5D=roles:(member)&location_by=exact&distance=25&distance_units=miles"

# ============================================
# PASTE YOUR COOKIES HERE
# ============================================
# Instructions:
# 1. Log in to myvistage.com in your browser
# 2. Open DevTools (F12) → Application → Cookies → https://myvistage.com
# 3. Copy ALL cookies and paste them here in this format:
#    'cookie_name=value; another_cookie=value; etc'
# 
# Example:
# VISTAGE_COOKIES = 'sessionid=abc123; auth_token=xyz789; user_id=12345'

VISTAGE_COOKIES = 'mv3Redirect=https%3A%2F%2Fmyvistage.com%2F; PHPSESSID=b088bb224d281ebc9aa3a0d9798497bf; _gid=GA1.2.2081867910.1762459165; googtrans=/en/en; _ga_NJZTN8262H=GS2.1.s1762459253$o1$g1$t1762459630$j52$l0$h0; _ga=GA1.2.1341199934.1762459165; _ga_359386664=GS2.1.s1762459165$o1$g1$t1762459631$j51$l0$h0'

# ============================================

firecrawl = Firecrawl(api_key=API_KEY)

print("=" * 60)
print("VISTAGE MEMBER SCRAPER (Cookie-Based)")
print("=" * 60)

# Validate cookies are set
if VISTAGE_COOKIES == 'PASTE_YOUR_COOKIES_HERE' or not VISTAGE_COOKIES or len(VISTAGE_COOKIES) < 20:
    print("\n❌ ERROR: You need to set your cookies first!")
    print("\nFollow these steps:")
    print("1. Log in to https://myvistage.com")
    print("2. Press F12 to open DevTools")
    print("3. Go to Application tab → Cookies → https://myvistage.com")
    print("4. Copy all cookie values")
    print("5. Paste them in scrape_vistage.py where it says VISTAGE_COOKIES")
    print("\nSee GET_SESSION_COOKIE.md for detailed instructions")
    exit(1)

# Step 1: Get member profile URLs from the directory
print("\n[Step 1] Scraping member directory to find profile URLs...")
print(f"Using cookies: {VISTAGE_COOKIES[:50]}...")

try:
    # Scrape the directory page using your logged-in session
    directory_doc = firecrawl.scrape(
        url=DIRECTORY_URL,
        formats=['links', 'markdown'],
        headers={
            'Cookie': VISTAGE_COOKIES
        },
        proxy='stealth',
        wait_for=3000
    )
    
    print(f"\n📊 DEBUG INFO:")
    print(f"Total links found: {len(directory_doc.links)}")
    print(f"\nFirst 10 links:")
    for i, link in enumerate(directory_doc.links[:10]):
        print(f"  {i+1}. {link}")
    
    print(f"\nFirst 500 chars of markdown:")
    print(directory_doc.markdown[:500] if directory_doc.markdown else "No markdown content")
    
    # Filter for member profile URLs - try multiple patterns
    member_urls = []
    
    # Try different URL patterns
    for link in directory_doc.links:
        if any([
            '/people/' in link and '?' not in link,  # Individual profiles (no query params)
            '/profile/' in link,
            '/member/' in link,
            '/user/' in link
        ]) and link != DIRECTORY_URL:
            member_urls.append(link)
    
    # Remove duplicates
    member_urls = list(set(member_urls))
    
    print(f"\n✓ Found {len(member_urls)} unique member profiles")
    
    if len(member_urls) > 0:
        print(f"\nSample member URLs:")
        for url in member_urls[:5]:
            print(f"  - {url}")
    
    # Save URLs for reference
    with open('member_urls.json', 'w') as f:
        json.dump(member_urls, f, indent=2)
    
except Exception as e:
    print(f"✗ Error getting member URLs: {e}")
    import traceback
    traceback.print_exc()
    print("\nTroubleshooting:")
    print("1. Your session may have expired - log in again and get fresh cookies")
    print("2. Make sure you copied ALL cookies from DevTools")
    print("3. Check if the URL is accessible while logged in")
    exit(1)

# Step 2: Define member data schema
member_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'title': {'type': 'string'},
        'company': {'type': 'string'},
        'location': {'type': 'string'},
        'email': {'type': 'string'},
        'phone': {'type': 'string'},
        'linkedin': {'type': 'string'},
        'bio': {'type': 'string'},
        'industry': {'type': 'string'},
        'vistage_group': {'type': 'string'},
    }
}

# Step 3: Test with first 3 profiles
print(f"\n[Step 2] Testing scraper with first 3 profiles...")

TEST_LIMIT = 3
test_urls = member_urls[:TEST_LIMIT]

all_members = []

for i, url in enumerate(test_urls):
    print(f"\nScraping {i+1}/{len(test_urls)}: {url}")
    
    try:
        doc = firecrawl.scrape(
            url=url,
            formats=[
                {'type': 'json', 'schema': member_schema},
                'markdown'  # Also get markdown for verification
            ],
            headers={
                'Cookie': VISTAGE_COOKIES  # Use the same cookies
            },
            proxy='stealth',
            onlyMainContent=True,
            maxAge=86400000  # Cache for 24 hours
        )
        
        if doc.json:
            member_data = doc.json.copy()
            member_data['profile_url'] = url
            all_members.append(member_data)
            
            # Show what was extracted
            print(f"  ✓ Name: {member_data.get('name', 'N/A')}")
            print(f"  ✓ Company: {member_data.get('company', 'N/A')}")
        else:
            print(f"  ✗ No data extracted")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        continue
    
    # Delay between requests
    time.sleep(2)

# Save test results
with open('test_members.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total': len(all_members),
        'members': all_members
    }, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"TEST COMPLETE: Scraped {len(all_members)}/{TEST_LIMIT} profiles")
print(f"Results saved to: test_members.json")
print(f"{'='*60}")

# Step 4: Prompt to continue with full scrape
if len(all_members) > 0:
    print("\n✓ Test successful! Review test_members.json to verify data quality.")
    print(f"\nTo scrape all {len(member_urls)} profiles:")
    print("1. Change TEST_LIMIT = 3 to TEST_LIMIT = len(member_urls)")
    print("2. Re-run the script")
    print("\nNote: Your cookies will remain valid for this session.")
else:
    print("\n✗ Test failed. Common issues:")
    print("1. Session expired - get fresh cookies")
    print("2. Wrong URL pattern for member profiles")
    print("3. Schema doesn't match the page structure")
    print("\nNext steps:")
    print("1. Check member_urls.json to see what URLs were found")
    print("2. Manually visit one of those URLs while logged in")
    print("3. Verify what data is actually on the profile pages")
