import json
import urllib.request

JSON_URL = "https://m3u-86e.pages.dev/jtv-mb.json"
OUTPUT_M3U = "playlist.m3u"

def convert_json_to_m3u():
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
        user_agent = ch.get("user_agent", "plaYtv/7.1.3 (Linux;Android 13) - @CloudPlay - ExoPlayerLib/824.0")
        license_url = ch.get("license_url", "")
        stream_url = ch.get("mpd_url") or ch.get("url") or ""
        
        headers = ch.get("headers", {}) if isinstance(ch.get("headers"), dict) else {}
        cookie = headers.get("cookie") or headers.get("Cookie") or ""
        referer = headers.get("referer") or headers.get("Referer") or "https://jiotv.com"
        origin = headers.get("origin") or headers.get("Origin") or "https://jiotv.com"
        
        if not stream_url:
            continue
        
        # 1. EXTINF channel info line
        m3u_lines.append(f'#EXTINF:-1 tvg-id="{ch_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{group}",{name}')
        
        # 2. ClearKey DRM key
        if license_url:
            m3u_lines.append("#KODPROP:inputstream.adaptive.license_type=clearkey")
            m3u_lines.append(f"#KODPROP:inputstream.adaptive.license_key={license_url}")
        
        # 3. VLCOPT Header directives
        if user_agent:
            m3u_lines.append(f"#EXTVLCOPT:http-user-agent={user_agent}")
        if cookie:
            m3u_lines.append(f"#EXTVLCOPT:http-cookie={cookie}")
        if referer:
            m3u_lines.append(f"#EXTVLCOPT:http-referrer={referer}")
        if origin:
            m3u_lines.append(f"#EXTVLCOPT:http-origin={origin}")
            
        # 4. Stream URL with Pipe (|) syntax for max compatibility in OTT Navigator
        pipe_headers = []
        if user_agent:
            pipe_headers.append(f"User-Agent={user_agent}")
        if referer:
            pipe_headers.append(f"Referer={referer}")
        if origin:
            pipe_headers.append(f"Origin={origin}")
        if cookie:
            pipe_headers.append(f"Cookie={cookie}")
            
        full_stream_url = f"{stream_url}|{'&'.join(pipe_headers)}" if pipe_headers else stream_url
        m3u_lines.append(f"{full_stream_url}\n")

    with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    
    print(f"Successfully generated {OUTPUT_M3U} with standard headers.")

if __name__ == "__main__":
    convert_json_to_m3u()
