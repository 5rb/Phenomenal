import requests
from concurrent.futures import ThreadPoolExecutor
import os

class UltimateFootprintScanner:
    def __init__(self, username):
        self.username = username
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        # 51 Scaled High-Value Target Endpoints
        self.targets = {
            "GitHub": f"https://api.github.com/users/{username}",
            "Telegram": f"https://t.me/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Linktree": f"https://linktr.ee/{username}",
            "Pinterest": f"https://www.pinterest.com/{username}/",
            "Reddit": f"https://www.reddit.com/user/{username}/",
            "Twitch": f"https://www.twitch.fr/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
            "Vimeo": f"https://vimeo.com/{username}",
            "Behance": f"https://www.behance.net/{username}",
            "Dribbble": f"https://dribbble.com/{username}",
            "Medium": f"https://medium.com/@{username}",
            "About.me": f"https://about.me/{username}",
            "Flickr": f"https://www.flickr.com/people/{username}/",
            "Keybase": f"https://keybase.io/{username}",
            "Disqus": f"https://disqus.com/by/{username}/",
            "Imgur": f"https://imgur.com/user/{username}",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "Goodreads": f"https://www.goodreads.com/{username}",
            "Wattpad": f"https://www.wattpad.com/user/{username}",
            "Bandcamp": f"https://bandcamp.com/{username}",
            "DeviantArt": f"https://www.deviantart.com/{username}",
            "ProductHunt": f"https://www.producthunt.com/@{username}",
            "Letterboxd": f"https://letterboxd.com/{username}/",
            "PlayStation": f"https://psnprofiles.com/{username}",
            "XboxGamertag": f"https://xboxgamertag.com/search/{username}",
            "Smashcast": f"https://www.smashcast.tv/{username}",
            "SlideShare": f"https://www.slideshare.net/{username}",
            "Quora": f"https://www.quora.com/profile/{username}",
            "Tumblr": f"https://{username}.tumblr.com",
            "Blogger": f"https://{username}.blogspot.com",
            "WordPress": f"https://{username}.wordpress.com",
            "Scratch": f"https://scratch.mit.edu/users/{username}/",
            "Duolingo": f"https://www.duolingo.com/profile/{username}",
            "Patreon": f"https://www.patreon.com/{username}",
            "DockerHub": f"https://hub.docker.com/u/{username}",
            "Kaggle": f"https://www.kaggle.com/{username}",
            "Codechef": f"https://www.codechef.com/users/{username}",
            "Codewars": f"https://www.codewars.com/users/{username}",
            "Gumroad": f"https://gumroad.com/{username}",
            "BuyMeACoffee": f"https://www.buymeacoffee.com/{username}",
            "Substack": f"https://{username}.substack.com",
            "Unsplash": f"https://unsplash.com/@{username}",
            "TripAdvisor": f"https://www.tripadvisor.com/Profile/{username}",
            "Wikipedia": f"https://en.wikipedia.org/wiki/User:{username}",
            "HackTheBox": f"https://forum.hackthebox.eu/u/{username}",
            "TryHackMe": f"https://tryhackme.com/p/{username}",
            "Pastebin": f"https://pastebin.com/u/{username}",
            "Gist": f"https://gist.github.com/{username}",
            "Tellonym": f"https://tellonym.me/{username}"
        }
        self.hits = []

    def check_platform(self, platform, url):
        try:
            # Setting a reasonable timeout to prevent hanging on bad connections
            response = requests.get(url, headers=self.headers, timeout=5, allow_redirects=False)
            
            # API & Status Code Structural Validation Matrix
            if platform == "GitHub":
                is_found = (response.status_code == 200)
            elif platform in ["Tumblr", "Blogger", "WordPress", "Substack"]:
                is_found = (response.status_code == 200)
            else:
                is_found = (response.status_code == 200 and self.username.lower() in response.text.lower())

            if is_found:
                result = f"[+] FOUND on {platform}: {url}"
                print(result)
                self.hits.append(url)
            else:
                print(f"[-] NOT FOUND on {platform}")
                
        except requests.exceptions.RequestException:
            print(f"[!] Blocked/Timed out on {platform}")

    def execute_sweep(self):
        print(f"[*] Deploying High-Velocity OSINT Matrix for Target Vector: {self.username}")
        print(f"[*] Targets Loaded: {len(self.targets)} Endpoints.")
        print("=" * 70)
        
        # Parallel execution with 25 simultaneous workers for optimal speed
        with ThreadPoolExecutor(max_workers=25) as executor:
            executor.map(lambda p: self.check_platform(p, self.targets[p]), self.targets)
            
        print("=" * 70)
        print(f"[*] Analysis Finished. Total active footprints detected: {len(self.hits)}")
        
        if self.hits:
            report_name = f"target_{self.username}_intel_report.txt"
            with open(report_name, "w", encoding="utf-8") as report:
                report.write(f"OSINT MASS SWEEP REPORT FOR TARGET: {self.username}\n")
                report.write("="*60 + "\n")
                for hit in self.hits:
                    report.write(f"{hit}\n")
            print(f"[+] Operational log exported to: {report_name}")

if __name__ == "__main__":
    target_vector = input("Enter target identity vector (Username): ").strip()
    if target_vector:
        scanner = UltimateFootprintScanner(target_vector)
        scanner.execute_sweep()
