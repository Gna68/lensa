"""
WorldGuessr - Location Tracker
 
"""

import asyncio
import json
import re
import os
from playwright.async_api import async_playwright

last_coords = None

COUNTRY_CODES = {
    'ID': 'Indonesia',
    'US': 'United States',
    'GB': 'United Kingdom',
    'CA': 'Canada',
    'AU': 'Australia',
    'DE': 'Germany',
    'FR': 'France',
    'IT': 'Italy',
    'ES': 'Spain',
    'JP': 'Japan',
    'CN': 'China',
    'IN': 'India',
    'BR': 'Brazil',
    'RU': 'Russia',
    'ZA': 'South Africa',
    'EG': 'Egypt',
    'NG': 'Nigeria',
    'KE': 'Kenya',
    'MX': 'Mexico',
    'AR': 'Argentina',
    'CL': 'Chile',
    'CO': 'Colombia',
    'PE': 'Peru',
    'VE': 'Venezuela',
    'MY': 'Malaysia',
    'SG': 'Singapore',
    'PH': 'Philippines',
    'TH': 'Thailand',
    'VN': 'Vietnam',
    'KR': 'South Korea',
    'TW': 'Taiwan',
    'HK': 'Hong Kong',
    'NZ': 'New Zealand',
    'NL': 'Netherlands',
    'BE': 'Belgium',
    'CH': 'Switzerland',
    'AT': 'Austria',
    'SE': 'Sweden',
    'NO': 'Norway',
    'DK': 'Denmark',
    'FI': 'Finland',
    'PL': 'Poland',
    'CZ': 'Czech Republic',
    'HU': 'Hungary',
    'GR': 'Greece',
    'PT': 'Portugal',
    'IE': 'Ireland',
    'IL': 'Israel',
    'SA': 'Saudi Arabia',
    'AE': 'United Arab Emirates',
    'TR': 'Turkey',
    'PK': 'Pakistan',
    'BD': 'Bangladesh',
    'MM': 'Myanmar',
    'KH': 'Cambodia',
    'LA': 'Laos',
    'MN': 'Mongolia',
    'NP': 'Nepal',
    'LK': 'Sri Lanka',
    'AF': 'Afghanistan',
    'IQ': 'Iraq',
    'IR': 'Iran',
    'SY': 'Syria',
    'JO': 'Jordan',
    'LB': 'Lebanon',
    'KW': 'Kuwait',
    'QA': 'Qatar',
    'OM': 'Oman',
    'YE': 'Yemen',
    'MA': 'Morocco',
    'DZ': 'Algeria',
    'TN': 'Tunisia',
    'LY': 'Libya',
    'SD': 'Sudan',
    'ET': 'Ethiopia',
    'TZ': 'Tanzania',
    'UG': 'Uganda',
    'GH': 'Ghana',
    'CI': 'Ivory Coast',
    'CM': 'Cameroon',
    'ZW': 'Zimbabwe',
    'ZM': 'Zambia',
    'MW': 'Malawi',
    'MZ': 'Mozambique',
    'AO': 'Angola',
    'NA': 'Namibia',
    'BW': 'Botswana',
    'MG': 'Madagascar',
    'MU': 'Mauritius',
    'SC': 'Seychelles',
    'FJ': 'Fiji',
    'PG': 'Papua New Guinea',
    'SB': 'Solomon Islands',
    'VU': 'Vanuatu',
    'WS': 'Samoa',
    'TO': 'Tonga',
    'KI': 'Kiribati',
    'TV': 'Tuvalu',
    'MH': 'Marshall Islands',
    'PW': 'Palau',
    'FM': 'Micronesia',
    'NR': 'Nauru',
}


COUNTRY_CONTINENT = {
    # Asia
    'Indonesia': 'Asia',
    'Malaysia': 'Asia',
    'Singapore': 'Asia',
    'Philippines': 'Asia',
    'Thailand': 'Asia',
    'Vietnam': 'Asia',
    'Myanmar': 'Asia',
    'Cambodia': 'Asia',
    'Laos': 'Asia',
    'Mongolia': 'Asia',
    'Nepal': 'Asia',
    'Sri Lanka': 'Asia',
    'Afghanistan': 'Asia',
    'Iraq': 'Asia',
    'Iran': 'Asia',
    'Syria': 'Asia',
    'Jordan': 'Asia',
    'Lebanon': 'Asia',
    'Kuwait': 'Asia',
    'Qatar': 'Asia',
    'Oman': 'Asia',
    'Yemen': 'Asia',
    'Saudi Arabia': 'Asia',
    'United Arab Emirates': 'Asia',
    'Turkey': 'Asia',
    'Pakistan': 'Asia',
    'Bangladesh': 'Asia',
    'India': 'Asia',
    'China': 'Asia',
    'Japan': 'Asia',
    'South Korea': 'Asia',
    'Taiwan': 'Asia',
    'Hong Kong': 'Asia',
    'Israel': 'Asia',
    
    # Europe
    'United Kingdom': 'Europe',
    'Germany': 'Europe',
    'France': 'Europe',
    'Italy': 'Europe',
    'Spain': 'Europe',
    'Netherlands': 'Europe',
    'Belgium': 'Europe',
    'Switzerland': 'Europe',
    'Austria': 'Europe',
    'Sweden': 'Europe',
    'Norway': 'Europe',
    'Denmark': 'Europe',
    'Finland': 'Europe',
    'Poland': 'Europe',
    'Czech Republic': 'Europe',
    'Hungary': 'Europe',
    'Greece': 'Europe',
    'Portugal': 'Europe',
    'Ireland': 'Europe',
    'Russia': 'Europe',
    
    # North America
    'United States': 'North America',
    'Canada': 'North America',
    'Mexico': 'North America',
    
    # South America
    'Brazil': 'South America',
    'Argentina': 'South America',
    'Chile': 'South America',
    'Colombia': 'South America',
    'Peru': 'South America',
    'Venezuela': 'South America',
    
    # Africa
    'South Africa': 'Africa',
    'Egypt': 'Africa',
    'Nigeria': 'Africa',
    'Kenya': 'Africa',
    'Morocco': 'Africa',
    'Algeria': 'Africa',
    'Tunisia': 'Africa',
    'Libya': 'Africa',
    'Sudan': 'Africa',
    'Ethiopia': 'Africa',
    'Tanzania': 'Africa',
    'Uganda': 'Africa',
    'Ghana': 'Africa',
    'Ivory Coast': 'Africa',
    'Cameroon': 'Africa',
    'Zimbabwe': 'Africa',
    'Zambia': 'Africa',
    'Malawi': 'Africa',
    'Mozambique': 'Africa',
    'Angola': 'Africa',
    'Namibia': 'Africa',
    'Botswana': 'Africa',
    'Madagascar': 'Africa',
    'Mauritius': 'Africa',
    'Seychelles': 'Africa',
    
    # Oceania
    'Australia': 'Oceania',
    'New Zealand': 'Oceania',
    'Fiji': 'Oceania',
    'Papua New Guinea': 'Oceania',
    'Solomon Islands': 'Oceania',
    'Vanuatu': 'Oceania',
    'Samoa': 'Oceania',
    'Tonga': 'Oceania',
    'Kiribati': 'Oceania',
    'Tuvalu': 'Oceania',
    'Marshall Islands': 'Oceania',
    'Palau': 'Oceania',
    'Micronesia': 'Oceania',
    'Nauru': 'Oceania',
}

def get_continent(country_name):
    """Mendapatkan nama benua dari nama negara"""
    return COUNTRY_CONTINENT.get(country_name, 'Unknown')

def extract_json(text):
    text = text.strip()
    for prefix in [")]}'\n", ")]}'", ")]}'"]:
        if text.startswith(prefix):
            return text[len(prefix):].strip()
    match = re.search(r'\(\s*(\[.*)', text, re.DOTALL)
    if match:
        body = match.group(1).strip()
        if body.endswith(");"):
            body = body[:-2]
        elif body.endswith(")"):
            body = body[:-1]
        return body.strip()
    return text

def find_coords(obj, depth=0):
    if depth > 15:
        return None
    if isinstance(obj, list):
        if (len(obj) == 4 and obj[0] is None and obj[1] is None
                and isinstance(obj[2], float) and isinstance(obj[3], float)
                and -90 <= obj[2] <= 90 and -180 <= obj[3] <= 180):
            return obj[2], obj[3]
        for item in obj:
            r = find_coords(item, depth + 1)
            if r:
                return r
    return None

def find_country(obj, depth=0):
    """Mencari kode negara 2 huruf dan mengembalikan nama lengkap"""
    if depth > 15:
        return None
    if isinstance(obj, str) and len(obj) == 2 and obj.isupper():

        return COUNTRY_CODES.get(obj, obj)
    if isinstance(obj, list):
        for item in obj:
            r = find_country(item, depth + 1)
            if r:
                return r
    return None

def find_addresses(obj, depth=0):
    results = []
    if depth > 15:
        return results
    if (isinstance(obj, list) and len(obj) == 2
            and isinstance(obj[0], str) and isinstance(obj[1], str)
            and len(obj[1]) <= 3 and obj[0] not in ["", " "]):
        results.append(obj[0])
        return results
    if isinstance(obj, list):
        for item in obj:
            results.extend(find_addresses(item, depth + 1))
    return list(dict.fromkeys(results))

 
INIT_SCRIPT = """
(function() {
    function hookLeaflet(L) {
        if (!L || !L.Map) return false;
        if (L.__hunterHooked) return true;
        L.__hunterHooked = true;

       
        try {
            L.Map.addInitHook(function() {
                window.__leafletMap = this;
            });
        } catch(e) {}

        
        try {
            var origInit = L.Map.prototype.initialize;
            L.Map.prototype.initialize = function(id, options) {
                var r = origInit.call(this, id, options);
                window.__leafletMap = this;
                return r;
            };
        } catch(e) {}
        
        return true;
    }

  
    if (window.L) {
        hookLeaflet(window.L);
        return;
    }

     
    var _L = undefined;
    Object.defineProperty(window, 'L', {
        configurable: true,
        enumerable: true,
        get: function() { return _L; },
        set: function(val) {
            _L = val;
            hookLeaflet(val);
        }
    });
})();
"""

CLICK_JS = """
(function() {
    var lat = %s;
    var lng = %s;

    var map = window.__leafletMap;
    if (!map) return 'NO_MAP';

    var latlng = L.latLng(lat, lng);

    try {
        map.fire('click', {
            latlng: latlng,
            originalEvent: new MouseEvent('click', { bubbles: true })
        });
        return 'OK';
    } catch(e) {
        return 'FIRE_ERR: ' + e.message;
    }
})();
"""

async def inject_click(page, lat, lng):
    js = CLICK_JS % (lat, lng)
    try:
        result = await page.evaluate(js)
        if result == "OK":
            print(f"  ✅ sudah di klik!")
            return True
        print(f"  ⚠️  belum di klik: {result}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    return False

async def on_response(response, page):
    global last_coords
    if "GetMetadata" not in response.request.url:
        return
    try:
        text = await response.text()
        if not text.strip():
            return

        json_str = extract_json(text)
        data = json.loads(json_str)

        coords    = find_coords(data)
        country   = find_country(data) or "Unknown"
        addresses = find_addresses(data)

        if not coords:
            return
        if coords == last_coords:
            return
        last_coords = coords

        lat, lng = coords
        label = addresses[0] if addresses else f"{lat:.4f}, {lng:.4f}"
        continent = get_continent(country)

        print("\n" + "═" * 55)
        print("   LOCATION DETECTED")
        print("═" * 52)
        print(f"  Country    : {country}")
        print(f"  Continent  : {continent}")
        print(f"  Address    : {label}")
        print("═" * 55)

        await inject_click(page, lat, lng)

    except Exception:
        pass

async def main():
    print("""
╔══════════════════════════════════════════╗
║              WorldGuessr                 ║
║           Location Tracker               ║
╚══════════════════════════════════════════╝
by Skipper
To stop: Ctrl+C
""")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--start-maximized",
            ],
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
        )

         
        await context.add_init_script(INIT_SCRIPT)

        page = await context.new_page()
        page.on("response", lambda res: asyncio.ensure_future(on_response(res, page)))

        await page.goto("https://www.worldguessr.com", wait_until="domcontentloaded")
        print("Browser opened. Start the game...\n")

        try:
            await page.wait_for_event("close", timeout=0)
        except Exception:
            pass

        await browser.close()

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSuspended.")