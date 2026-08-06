import json
import urllib.request

JSON_URL = "https://m3u-86e.pages.dev/jtv-mb.json"
OUTPUT_M3U = "playlist.m3u"

def convert_json_to_m3u():
    # Fetch the JSON content
    req = urllib.request.Request(JSON_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    channels = data.get("channels", data) if isinstance(data, dict) else data
    m3u_lines = ["#EXTM3U\n"]
    
    for ch in channels:
        if not isinstance(ch, dict):
            continue
        
        name = ch.get("name", "Unknown Channel")
        ch_id = ch.get("id", "")
        logo = ch.get("logo", "")
        group = ch.get("group", "")
        user_agent = ch.get("user_agent", "")
        license_url = ch.get("license_url", "")
        stream_url = ch.get("mpd_url") or ch.get("url") or ""
        
        headers = ch.get("headers", {})
        cookie = headers.get("cookie", "") if isinstance(headers, dict) else ""
        
        if not stream_url:
            continue
        
        # Form #EXTINF header
        m3u_lines.append(f'#EXTINF:-1 tvg-id="{ch_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{group}",{name}')
        
        # DRM Clearkey license tag
        if license_url:
            m3u_lines.append("#KODPROP:inputstream.adaptive.license_type=clearkey")
            m3u_lines.append(f"#KODPROP:inputstream.adaptive.license_key={license_url}")
        
        # User Agent & Cookies
        if user_agent:
            m3u_lines.append(f"#EXTVLCOPT:http-user-agent={user_agent}")
        if cookie:
            m3u_lines.append(f"#EXTVLCOPT:http-cookie={cookie}")
            
        m3u_lines.append(f"{stream_url}\n")

    with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    
    print(f"Successfully updated {OUTPUT_M3U}")

if __name__ == "__main__":
    convert_json_to_m3u()
