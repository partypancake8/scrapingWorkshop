# How to Get Your Vistage Session Cookie

Since Vistage requires login, you need to provide your session cookie to the scraper.

## Steps:

1. **Open Chrome/Firefox and log in to Vistage**

   - Go to https://myvistage.com
   - Log in with your credentials
   - Navigate to the member directory

2. **Open Developer Tools**

   - Press `F12` (or `Cmd+Option+I` on Mac)
   - Click on the **Application** tab (Chrome) or **Storage** tab (Firefox)

3. **Find Cookies**

   - In the left sidebar, expand **Cookies**
   - Click on `https://myvistage.com`

4. **Copy Session Cookie**

   - Look for cookies named something like:

     - `session`
     - `sessionid`
     - `auth_token`
     - `PHPSESSID`
     - Or any cookie that looks like authentication

   - Copy the entire cookie string in this format:
     ```
     cookie_name=cookie_value; another_cookie=another_value
     ```

5. **Update the Script**

   - In `scrape_vistage.py`, find this line:

     ```python
     'Cookie': 'YOUR_SESSION_COOKIE'
     ```

   - Replace with your actual cookie:
     ```python
     'Cookie': 'sessionid=abc123xyz; auth_token=def456'
     ```

## Alternative: Use Actions for Login

Instead of cookies, you can let Firecrawl log in for you. The script already has login actions, but you may need to adjust the CSS selectors:

1. Inspect the login form elements
2. Update these lines in the script:

   ```python
   {'type': 'write', 'selector': 'input[type="email"]', 'text': VISTAGE_EMAIL},
   {'type': 'write', 'selector': 'input[type="password"]', 'text': VISTAGE_PASSWORD},
   {'type': 'click', 'selector': 'button[type="submit"]'},
   ```

3. Change the selectors to match Vistage's actual login form

## Testing

Run the script with:

```bash
source venv/bin/activate && python scrape_vistage.py
```

It will test with just 3 profiles first to verify everything works!
