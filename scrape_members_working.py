# Working Vistage member scraper with authentication

from firecrawl import Firecrawl
import json

API_KEY = "fc-d2612b97887e49fe9b9464a597b99ee6"
VISTAGE_EMAIL = 'tyler.smith@eosworldwide.com'
VISTAGE_PASSWORD = 'Rty1ers7!'

firecrawl = Firecrawl(api_key=API_KEY)

print("="*80)
print("VISTAGE MEMBER SCRAPER")
print("="*80)

# Step 1: Login and navigate to member directory
print("\n🔐 Logging in and accessing member directory...")

member_dir = firecrawl.scrape(
    url="https://myvistage.com/",
    formats=['links', 'markdown', 'html'],
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

print(f"✅ Loaded member directory ({len(member_dir.markdown)} chars)")

# Save full content for inspection
with open('member_directory_content.txt', 'w') as f:
    f.write(member_dir.markdown if member_dir.markdown else "")

print(f"📄 Saved full content to member_directory_content.txt")

# Save all links
all_links = member_dir.links if hasattr(member_dir, 'links') else []
with open('all_member_links.json', 'w') as f:
    json.dump(all_links, f, indent=2)

print(f"🔗 Found {len(all_links)} total links")
print(f"📄 Saved links to all_member_links.json")

# Filter for actual member profile links
# Pattern examples: /people/john-smith/, /people/jane-doe-12345/
member_profiles = [
    link for link in all_links 
    if '/people/' in link 
    and link.count('/') >= 4  # https://myvistage.com/people/name/
    and not any(x in link for x in ['?', '#', 'area=', 'es/', 'zh/', 'ar/'])
]

print(f"\n👥 Found {len(member_profiles)} potential member profiles:")
for link in member_profiles[:10]:
    print(f"  - {link}")

if len(member_profiles) > 10:
    print(f"  ... and {len(member_profiles) - 10} more")

# Save member profile URLs
with open('member_profile_urls.json', 'w') as f:
    json.dump(member_profiles, f, indent=2)

print(f"\n💾 Saved member URLs to member_profile_urls.json")
print(f"\nNext: Check member_directory_content.txt to see what the page looks like!")
