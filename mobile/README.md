# Mobile Access - Clawpack V2 on Your Phone

Clawpack runs on your PC but you can control it from any phone or tablet.

## Quick Start (Android)

### 1. Start Clawpack on your PC
`ash
python a2a_server.py
2. Find your PC's IP address
Windows: Open PowerShell, type ipconfig, look for IPv4 Address (e.g., 192.168.1.100)
Mac: System Settings > Network > Wi-Fi > IP Address
Linux: ip addr show | grep inet

3. Open on your phone
Open Chrome on your Android phone. Go to:

text
http://[YOUR-PC-IP]:8766/health
You should see a JSON response. The server is reachable.

4. Serve the mobile interface
On your PC:

bash
python -m http.server 8080 --directory mobile
5. Connect
On your phone, go to:

text
http://[YOUR-PC-IP]:8080
Tap the status dot (top right) and set the server URL to:

text
http://[YOUR-PC-IP]:8766
6. Use it
Select an agent from the dropdown

Type commands or tap the M button to speak

Responses appear in the chat

Install as an app (optional)
In Chrome, tap the three-dot menu > "Add to Home Screen." Clawpack installs like a native app with its own icon.

iPhone/iPad
Same steps as Android. Use Safari instead of Chrome. "Add to Home Screen" works from the Share menu.

What Works on Mobile
FeatureStatus
Text inputYes
Voice input (mic button)Yes (Chrome/Safari Web Speech API)
Agent selectionYes (dynamic from /v1/agents)
Server health indicatorYes (green dot)
Offline shellYes (service worker)
TTS audio outputNo (text responses only)
Wake wordsNo (requires PC microphone)
HotkeysNo (mobile has no keyboard shortcuts)
Troubleshooting
Can't connect? Make sure:

PC and phone are on the same Wi-Fi network

Windows Firewall allows Python on port 8766 (approve the popup on first launch)

The A2A server is running (python a2a_server.py)

You're using your PC's IP, not 127.0.0.1

Voice input not working? Chrome on Android supports Web Speech API. Ensure microphone permission is granted. iPhone Safari also supports it.

Server not found? Try http://[IP]:8766/health in your phone's browser first. If that works, the server is reachable and the issue is with the PWA serving.
