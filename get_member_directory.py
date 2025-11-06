# Single scrape call - login and get directory in one go

from firecrawl import Firecrawl
import json

API_KEY = "fc-d2612b97887e49fe9b9464a597b99ee6"
VISTAGE_EMAIL = 'tyler.smith@eosworldwide.com'
VISTAGE_PASSWORD = 'Rty1ers7!'

firecrawl = Firecrawl(api_key=API_KEY)

print("="*80)
print("VISTAGE MEMBER DIRECTORY SCRAPER")
print("="*80)
print("\n🔐 Logging in and navigating to member directory...")
print("(This will take about 20-30 seconds)")

# Do everything in ONE scrape call to avoid rate limits
result = firecrawl.scrape(
    url="https://myvistage.com/",
    formats=['links', 'markdown'],
    proxy='stealth',
    wait_for=10000,  # Wait 10s after actions complete
    actions=[
        # Login
        {"type": "wait", "milliseconds": 3000},
        {"type": "click", "selector": "input[type='text']"},
        {"type": "write", "text": VISTAGE_EMAIL},
        {"type": "wait", "milliseconds": 500},
        {"type": "click", "selector": "input[type='password']"},
        {"type": "write", "text": VISTAGE_PASSWORD},
        {"type": "wait", "milliseconds": 500},
        {"type": "press", "key": "Enter"},
        {"type": "wait", "milliseconds": 8000},
        
        # Navigate to member directory
        {"type": "executeJavascript", "script": "window.location.href = 'https://myvistage.com/people/?area=people&full_profile=&location_by=exact&distance=25&distance_units=miles&solr_fq%5B0%5D=roles:(member)'"},
        {"type": "wait", "milliseconds": 8000},
    ]
)

print(f"\n✅ Scrape complete!")
print(f"📄 Content length: {len(result.markdown) if result.markdown else 0} chars")
print(f"🔗 Total links: {len(result.links) if hasattr(result, 'links') else 0}")

# Save everything
with open('member_directory_page.txt', 'w') as f:
    f.write(result.markdown if result.markdown else "")
print(f"\n💾 Saved content to member_directory_page.txt")

if hasattr(result, 'links'):
    with open('all_directory_links.json', 'w') as f:
        json.dump(result.links, f, indent=2)
    print(f"💾 Saved {len(result.links)} links to all_directory_links.json")
    
    # Filter for actual member profiles
    member_profiles = [
        link for link in result.links 
        if '/people/' in link 
        and link.count('/') >= 4
        and not any(x in link for x in ['?', 'area=', 'es/', 'zh/', 'ar/', 'fr/'])
        and link != 'https://myvistage.com/people/'
    ]
    
    print(f"\n👥 Found {len(member_profiles)} member profile URLs:")
    for link in member_profiles[:20]:
        print(f"  - {link}")
    
    if len(member_profiles) > 20:
        print(f"  ... and {len(member_profiles) - 20} more")
    
    with open('member_profile_urls.json', 'w') as f:
        json.dump(member_profiles, f, indent=2)
    print(f"\n💾 Saved {len(member_profiles)} profile URLs to member_profile_urls.json")

print("\n" + "="*80)
print("NEXT STEPS:")
print("1. Check member_directory_page.txt to see what content was scraped")
print("2. Review member_profile_urls.json for the list of member URLs")
print("3. If we have profile URLs, we can scrape individual member details!")
print("="*80)
