# Graphytti

Graphytti is a proof-of-concept tool demonstrating the bypass of the Graphy E-Learning Platform's Digital Rights Management (DRM) system, enabling unauthorised download of course material.

### Dependencies
- Python3.x
    - requests
    - BeautifulSoup4
- NodeJS (23.1.0)
    - CryptoJS (^4.1.1)
- FFMPEG

### Overview

This vulnerability exists because the AES decryption key used to unlock protected media content is shared with the client over the internet. Although the key itself is encrypted using AES, it is decrypted client-side, allowing eventual access to the raw video files.

Efforts to obfuscate the key-decryption process can be bypassed by treating the obfuscated code as a "black box" where the decryption key can be extracted.

### Proof-of-Concept : Downloading Course Material on a self-published course.
1) In the `Main.py` file, replace the existing `SESSIONID` with your Graphy SessionID.

2) Update `FFMPEG_BIN` to the path of your FFMPEG installation.

3) Replace the placeholder `URL` with the URL of the course-owner to test.

4) Replace the existing `SELECTED_COURSE_ID` with the ID of the course you wish to test. The Course ID may be obtained from the URL of the course being tested.

5) Run the script using `python3 Main.py`.

The Video Files present in the course will be found at `./media/processed/<Name of Video>.mp4`

### Mitigation Strategies
Possible Strategies include:
- Using established DRM mechanisms that are designed for specific platforms, such as Google Widevine (Android/Chrome), Microsoft PlayReady (Windows), and Apple FairPlay (iOS/macOS).
- Implementing rate limiting to prevent bulk downloads that exceed normal human consumption rates.

# Responsible Disclosure
The findings have been timely reported to all concerned parties via email along with a video Proof-of-Concept.

This Proof-of-Concept is STRICTLY for informational purposes. The author does NOT support, encourage or condone Piracy in any way, shape or form. The author is NOT responsible for any actions performed with the tool.