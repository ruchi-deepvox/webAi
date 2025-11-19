# 🌐 Network Setup Guide - Use Voice Agent from Other Machines

## Your Server Information
- **Server IP:** `192.168.0.102`
- **API Port:** `8000`
- **API URL:** `http://192.168.0.102:8000/api/connect`

---

## 📋 Setup Steps

### 1. **On Server Machine (192.168.0.102):**

#### A. Make sure services are running:
```powershell
# Terminal 1: Run the agent
cd E:\deepvox\python\pythonAgentWeb
$env:PYTHONIOENCODING='utf-8'
uv run python src/agent.py dev

# Terminal 2: Run the API server
cd E:\deepvox\python\pythonAgentWeb
uv run python unified_api.py
```

#### B. Add Windows Firewall Rule (Run PowerShell as Administrator):
```powershell
netsh advfirewall firewall add rule name="Python API Server" dir=in action=allow protocol=TCP localport=8000
```

Or manually:
1. Open "Windows Defender Firewall with Advanced Security"
2. Click "Inbound Rules" → "New Rule"
3. Select "Port" → "TCP" → Specific local ports: **8000**
4. Select "Allow the connection"
5. Check all profiles (Domain, Private, Public)
6. Name: "Python API Server"

---

### 2. **On Client Machine (Any Device):**

#### Option 1: Use the HTML file directly
1. Copy `simple_voice_ui.html` to your client machine
2. Open it in a browser
3. It will automatically connect to `http://192.168.0.102:8000`

#### Option 2: Test with curl first
```bash
curl -X POST http://192.168.0.102:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"user_name": "John"}'
```

If you get a JSON response, it's working! ✅

---

## 🔧 Configuration

### Change API URL in HTML file:

Open `simple_voice_ui.html` and find line ~91:

```javascript
const API_URL = 'http://192.168.0.102:8000/api/connect';
```

Change the IP to:
- **Same machine:** `http://localhost:8000/api/connect`
- **Different machine on same network:** `http://192.168.0.102:8000/api/connect`
- **Public server:** `http://your-domain.com:8000/api/connect`

---

## 🧪 Testing

### Test 1: Check API health from client machine
```bash
curl http://192.168.0.102:8000/api/health
```

Expected response:
```json
{
  "success": true,
  "status": "healthy",
  "services": {...}
}
```

### Test 2: Get API documentation
Open browser on client machine: `http://192.168.0.102:8000/api`

### Test 3: Connect to agent
Open `simple_voice_ui.html` on client machine and click "Connect & Talk"

---

## ❓ Troubleshooting

### Problem: "Failed to fetch" error
**Solutions:**
1. Check if API server is running on server machine
2. Verify firewall rule is added (step 1B above)
3. Ping server from client: `ping 192.168.0.102`
4. Test with curl from client machine

### Problem: "Connection timeout"
**Solutions:**
1. Make sure both machines are on the same network
2. Check if antivirus is blocking the connection
3. Try disabling Windows Firewall temporarily to test

### Problem: Can't hear agent voice
**Solutions:**
1. Check browser console for errors (F12)
2. Make sure microphone permission is granted
3. Verify agent service is running (`uv run python src/agent.py dev`)
4. Check browser audio settings

---

## 🚀 Quick Start Commands

### Server Machine (192.168.0.102):
```powershell
# Terminal 1
cd E:\deepvox\python\pythonAgentWeb
$env:PYTHONIOENCODING='utf-8'
uv run python src/agent.py dev

# Terminal 2
cd E:\deepvox\python\pythonAgentWeb
uv run python unified_api.py
```

### Client Machine (Any Device):
Just open `simple_voice_ui.html` in a browser! 🎉

---

## 📱 Use on Mobile Devices

Yes! You can use it on mobile too:

1. Copy `simple_voice_ui.html` to your phone
2. Open it in **Chrome or Safari** (for microphone access)
3. Make sure your phone is on the same WiFi network
4. Grant microphone permission when prompted
5. Click "Connect & Talk" and start speaking!

---

## 🌍 Deploy to Production

For production use with HTTPS and public access, consider:

1. **Deploy to a cloud server** (AWS, Azure, GCP, DigitalOcean)
2. **Use a proper domain** with SSL certificate
3. **Add authentication** (API keys, JWT tokens)
4. **Use environment variables** for configuration
5. **Set up monitoring** and logging

For now, local network testing is perfect! ✅

