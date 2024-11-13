# %%
import requests
import json
from bs4 import BeautifulSoup
import re
import subprocess
from pathlib import Path

# %%
MEDIA_PATH = "./media"
FFMPEG_BIN = "./ffmpeg-darwin-arm64"
URL = "https://aathishsivasubrahmanian.graphy.com"
COOKIES = {
    "SESSIONID": ""
}
SELECTED_COURSE_ID = "6731ae22e5fa980e331decaf"
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json; charset=utf-8",
    "priority": "u=1, i",
    "referer": f"{URL}/s/mycourses?type=active&lsb",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
media_path = Path(MEDIA_PATH)
unprocessed_media_path = media_path/"unprocessed"
processed_media_path = media_path/"processed"


# %%
r = requests.get(f"{URL}/s/mycourses?type=active&lsb",cookies=COOKIES,headers=headers)
apkid = re.search(r'apkId = \"(.*)\", theme9',r.text).group(1)
apkid

# %%

r = requests.get(f"{URL}/s/courses/{SELECTED_COURSE_ID}/take",cookies=COOKIES,headers=headers)
hlsurl = re.search(r'https:\/\/.*hls.*.min.js',r.text).group(0)
soup = BeautifulSoup(r.content)
mydivs = soup.find_all("div", {"class": "courseSubItem"})
viddict = {}
for div in mydivs:
    viddict[div.attrs["data-title"]] = div.attrs['data-id']

print(json.dumps(viddict,indent=4))

# %%
r = requests.get(hlsurl,cookies=COOKIES,headers=headers)
with open("hls.min.js","w") as f:
    f.write(r.text)

# %%
for vid in viddict:
    r = requests.get(f"{URL}/s/courses/{SELECTED_COURSE_ID}/videos/{viddict[vid]}/get?_=1699857984568",cookies=COOKIES,headers=headers)
    print(r.text)
    viddict[vid] = r.json()
print(json.dumps(viddict,indent=4))

# %%
for vid in viddict:
    if not isinstance(viddict[vid],dict):
        continue 

    viddirpath = unprocessed_media_path/vid
    viddirpath.mkdir(exist_ok=True,parents=True)

    print(f"Starting Download : {vid}")
    url = viddict[vid]["spayee:resource"]["spayee:streamUrl"]
    r = requests.get(url,cookies=COOKIES,headers=headers)
    with open(viddirpath/"index.m3u8","wb") as f:
        f.write(r.content)
    NEEDS_SEPARATE_AUDIO = ("hls_audio_.m3u8" in r.text)
    
    r = requests.get(url[:-10]+"hls_500k_.m3u8",cookies=COOKIES,headers=headers)
    with open(viddirpath/"hls_500k_.m3u8","w") as f:
        f.write(r.content.decode("utf-8").replace("k/timestamp","key_video.bin"))
    
    with open(viddirpath/"hls_500k_.m3u8","r") as f:
        with open(viddirpath/"key_video.bin","wb") as f2:
            print(url)
            r = requests.get(url[:-10]+"k/timestamp",cookies=COOKIES,headers=headers)
            timestampreturn = list(bytearray(r.content))
            print(timestampreturn)
            bytestowrite = eval((subprocess.check_output(["node","decrypt_key.js", apkid, str(timestampreturn),r.url])).decode("utf-8").strip())
            print("bytes:",bytestowrite)
            f2.write(bytes(bytestowrite))
        for line in f.readlines():
            if line.startswith("hls_500k"):
                r = requests.get(url[:-10]+line.strip(),cookies=COOKIES,headers=headers)
                with open(viddirpath/line.strip(),"wb") as f2:
                    f2.write(r.content)

    if NEEDS_SEPARATE_AUDIO:
        r = requests.get(url[:-10]+"hls_audio_.m3u8",cookies=COOKIES,headers=headers)
        with open(viddirpath/"hls_audio_.m3u8","w") as f:
            f.write(r.content.decode("utf-8").replace("k/timestamp","key_audio.bin"))
        with open(viddirpath/"hls_audio_.m3u8","r") as f:
            with open(viddirpath/"key_audio.bin","wb") as f2:
                r = requests.get(url[:-10]+"k/timestamp",cookies=COOKIES,headers=headers)
                timestampreturn = list(bytearray(r.content))
                bytestowrite = eval((subprocess.check_output(["node","decrypt_key.js", apkid, str(timestampreturn),r.url])).decode("utf-8").strip())
                f2.write(bytes(bytestowrite))
            for line in f.readlines():
                if line.startswith("hls_audio"):
                    r = requests.get(url[:-10]+line.strip(),cookies=COOKIES)
                    with open(viddirpath/line.strip(),"wb") as f2:
                        f2.write(r.content)
    print(f"Finished : {vid}")
    # break


# %%
# List all folders in the directory
unprocessed_videos = [item for item in unprocessed_media_path.iterdir() if item.is_dir()]
processed_media_path.mkdir(parents=True,exist_ok=True)
for unprocessed_video in unprocessed_videos:
    subprocess.run([
        FFMPEG_BIN, 
        '-y', 
        '-allowed_extensions', 'ALL', 
        '-i', f"{unprocessed_video}/index.m3u8", 
        '-c', 'copy', 
        '-vcodec', 'copy', 
        f"{processed_media_path/unprocessed_video.name}.mp4"
    ])
    print(f"Complete! You may find a video at {processed_media_path/unprocessed_video.name}.mp4")




