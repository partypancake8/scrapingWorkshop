# Test script to check if authentication is working

from firecrawl import Firecrawl
import json

API_KEY = "fc-d2612b97887e49fe9b9464a597b99ee6"
DIRECTORY_URL = "https://myvistage.com/people/?area=people&full_profile=&location_by=exact&distance=25&distance_units=miles&solr_fq%5B0%5D=roles:(member)&location_by=exact&distance=25&distance_units=miles"

# PASTE YOUR COOKIES HERE (from browser console: document.cookie)
VISTAGE_COOKIES = 'mv3Redirect=https%3A%2F%2Fmyvistage.com%2F; PHPSESSID=b088bb224d281ebc9aa3a0d9798497bf; _gid=GA1.2.2081867910.1762459165; googtrans=/en/en; _ga_359386664=GS2.1.s1762459165$o1$g1$t1762460635$j60$l0$h0; _ga_NJZTN8262H=GS2.1.s1762459253$o1$g1$t1762460635$j60$l0$h0; _ga=GA1.1.1341199934.1762459165'

print("="*80)
print("AUTHENTICATION TEST")
print("="*80)
print("\nInstructions:")
print("1. Log in to https://myvistage.com")
print("2. Navigate to the member directory")
print("3. Press F12 → Console")
print("4. Type: document.cookie")
print("5. Copy the ENTIRE output")
print("6. Paste it in this script where it says VISTAGE_COOKIES")
print("\nAlso get User-Agent:")
print("7. In Console, type: navigator.userAgent")
print("8. Copy that too (paste below)")
print("="*80)

# PASTE YOUR USER-AGENT HERE
USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36'

if VISTAGE_COOKIES == 'PASTE_HERE' or USER_AGENT == 'PASTE_HERE':
    print("\n❌ You need to set cookies and user-agent first!")
    exit(1)

firecrawl = Firecrawl(api_key=API_KEY)

print(f"\n🔍 Testing with:")
print(f"Cookies (first 50 chars): {VISTAGE_COOKIES[:50]}...")
print(f"User-Agent: {USER_AGENT}")

print("\n📡 Attempting to scrape...")

doc = firecrawl.scrape(
    url=DIRECTORY_URL,
    formats=['markdown'],
    headers={
        'Cookie': VISTAGE_COOKIES,
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://myvistage.com/',
    },
    proxy='stealth',
    wait_for=5000
)

print("\n📄 Page Content Analysis:")
print("-"*80)

content = doc.markdown[:1000] if doc.markdown else "No content"

# Check for login indicators
login_keywords = ['sign in', 'login', 'password', 'username', 'authentication']
is_login_page = any(keyword in content.lower() for keyword in login_keywords)

# Check for member indicators  
member_keywords = ['member', 'profile', 'contact', 'company', 'location']
has_member_content = any(keyword in content.lower() for keyword in member_keywords)

print(f"Content length: {len(doc.markdown) if doc.markdown else 0} chars")
print(f"Is login page? {'❌ YES - Auth failed' if is_login_page else '✅ NO - Looks good'}")
print(f"Has member content? {'✅ YES' if has_member_content else '❌ NO'}")

print(f"\nFirst 500 characters:")
print(content[:500])
print("-"*80)

if is_login_page:
    print("\n❌ AUTHENTICATION FAILED")
    print("\nPossible issues:")
    print("1. Cookies expired - get fresh ones")
    print("2. Session requires additional headers")
    print("3. Site uses JavaScript authentication (cookies alone won't work)")
    print("\n💡 Solution: Try using Firecrawl's 'actions' to log in instead")
else:
    print("\n✅ AUTHENTICATION WORKED!")
    print("Cookies are valid and working correctly")
