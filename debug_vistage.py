# Debug script to see what Firecrawl is actually getting from the Vistage page

from firecrawl import Firecrawl
import json

API_KEY = "fc-d2612b97887e49fe9b9464a597b99ee6"
DIRECTORY_URL = "https://myvistage.com/people/?area=people&full_profile=&location_by=exact&distance=25&distance_units=miles&solr_fq%5B0%5D=roles:(member)&location_by=exact&distance=25&distance_units=miles"

# Paste your cookies here

VISTAGE_COOKIES = 'mv3Redirect=https%3A%2F%2Fmyvistage.com%2F; PHPSESSID=b088bb224d281ebc9aa3a0d9798497bf; _gid=GA1.2.2081867910.1762459165; googtrans=/en/en; _ga_359386664=GS2.1.s1762459165$o1$g1$t1762460635$j60$l0$h0; _gat_gtag_UA_397931_76=1; _ga_NJZTN8262H=GS2.1.s1762459253$o1$g1$t1762460635$j60$l0$h0; _ga=GA1.1.1341199934.1762459165'
firecrawl = Firecrawl(api_key=API_KEY)

print("Scraping Vistage directory page...")
print(f"URL: {DIRECTORY_URL}\n")

doc = firecrawl.scrape(
    url=DIRECTORY_URL,
    formats=['links', 'markdown'],
    headers={
        'Cookie': VISTAGE_COOKIES
    },
    proxy='stealth',
    wait_for=5000  # Wait 5 seconds for content to load
)

print("=" * 80)
print("RESULTS:")
print("=" * 80)

print(f"\n📊 Total links found: {len(doc.links)}")

print(f"\n🔗 All links ({len(doc.links)} total):")
for i, link in enumerate(doc.links[:50]):  # Show first 50
    print(f"  {i+1}. {link}")

if len(doc.links) > 50:
    print(f"\n... and {len(doc.links) - 50} more links")

print(f"\n📄 Page content (first 2000 characters):")
print("-" * 80)
if doc.markdown:
    print(doc.markdown[:2000])
else:
    print("No markdown content")
print("-" * 80)

print(f"\n📌 Page metadata:")
print(f"  Title: {doc.metadata.title if hasattr(doc.metadata, 'title') else 'N/A'}")
print(f"  URL: {doc.metadata.source_url if hasattr(doc.metadata, 'source_url') else 'N/A'}")
print(f"  Status: {doc.metadata.status_code if hasattr(doc.metadata, 'status_code') else 'N/A'}")

# Save full markdown to file for inspection
with open('debug_page_content.txt', 'w', encoding='utf-8') as f:
    f.write(doc.markdown if doc.markdown else "No content")

print(f"\n✅ Full page content saved to: debug_page_content.txt")

# Save all links to file
with open('debug_all_links.json', 'w') as f:
    json.dump(doc.links, f, indent=2)

print(f"✅ All links saved to: debug_all_links.json")

print("\n" + "=" * 80)
print("NEXT STEPS:")
print("=" * 80)
print("1. Check debug_page_content.txt - does it show member names or a login page?")
print("2. Check debug_all_links.json - are there any profile URLs?")
print("3. If you see 'Login' or 'Sign in', your cookies expired - get fresh ones")
print("4. If you see member content but no profile links, they might load via JavaScript")
