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

This vulnerability exists due to Graphy sharing the AES decryption key required to decrypt the protected media content with the client over the internet.
The key itself is encrypted using AES and decrypted client-side before the video files are decrypted.

Evident efforts were taken to obfuscate the process of key decryption - however, these efforts can be circumvented by treating the obfuscated code as a black-box through which "arbitrary" data enters, and a media decryption key leaves.

### Proof-of-Concept : Downloading Course Material on a self-published course.
1) In the `Main.py` file, replace the existing `SESSIONID` with your Graphy SessionID.

2) Replace existing `FFMPEG_BIN` with the path to your installation of the FFMPEG tool.

3) Replace existing `URL` with the URL of the course you wish to test.

4) Replace the existing `SELECTED_COURSE_ID` with the ID of the course you wish to test. The Course ID may be obtained from the URL of the course being tested.

5) Run the script using `python3 Main.py`.

The Video Files present in the course will be found at `./media/processed/<Name of Video>.mp4`

### Mitigation Strategies
Possible Strategies include:
- Usage of tried and tested DRM mechanisms purpose built for specific platforms, such as Google Widevine for Android/Chrome, Microsoft Playready for Windows, and Apple FairPlay for iOS and MacOS devices.
- Addition of a rate limit to remove the ability to download course material at a faster rate is humanly possible to consume said course material.

# Responsible Disclosure
The findings have been timely reported to all concerned parties via email along with a video Proof-of-Concept.