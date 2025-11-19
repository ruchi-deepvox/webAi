# 🔧 Troubleshooting Network Connection Issues

## Problem: "Failed to connect or fetch from other device"

This means the firewall is blocking incoming connections to port 8000.

---

## ✅ SOLUTION (Choose One Method):

### **Method 1: Using PowerShell Script (Easiest)**

1. **Right-click PowerShell** → Select **"Run as Administrator"**

2. Navigate to project folder:
```powershell
cd E:\deepvox\python\pythonAgentWeb
```

3. Run the firewall script:
```powershell
.\add_firewall_rule.ps1
```

4. If you get execution policy error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\add_firewall_rule.ps1
```

---

### **Method 2: Using Command Line (Quick)**

**Run PowerShell as Administrator** and execute:

```powershell
netsh advfirewall firewall add rule name="Python API Server" dir=in action=allow protocol=TCP localport=8000
```

You should see: `Ok.`

---

### **Method 3: Using Windows GUI (Visual)**

1. Press `Win + R`, type: `wf.msc`, press Enter
2. Click **"Inbound Rules"** (left panel)
3. Click **"New Rule..."** (right panel)
4. Select **"Port"** → Click Next
5. Select **"TCP"** and enter **"8000"** in Specific local ports → Next
6. Select **"Allow the connection"** → Next
7. Check all boxes (Domain, Private, Public) → Next
8. Name: **"Python API Server"** → Finish

---

## 🧪 TESTING

### Test from Server Machine (192.168.0.102):

Open PowerShell and run:
```powershell
# Test localhost
curl http://localhost:8000/api/health

# Test network IP
curl http://192.168.0.102:8000/api/health
```

Both should return JSON with `"success": true`

### Test from Other Device:

**Option 1: Use the Test Page**
1. Copy `test_from_other_device.html` to the other device
2. Open it in a browser
3. Click "Run All Tests"
4. All tests should show ✅

**Option 2: Use curl (if available)**
```bash
# On Mac/Linux/Windows PowerShell
curl http://192.168.0.102:8000/api/health
```

**Option 3: Use browser**
Open: `http://192.168.0.102:8000/api/health`

Should see:
```json
{
  "success": true,
  "status": "healthy",
  "services": {...}
}
```

---

## 🚨 Still Not Working? Check These:

### 1. Verify Both Services Are Running
```powershell
# Terminal 1
cd E:\deepvox\python\pythonAgentWeb
$env:PYTHONIOENCODING='utf-8'
uv run python src/agent.py dev

# Terminal 2
cd E:\deepvox\python\pythonAgentWeb
uv run python unified_api.py
```

### 2. Check if Port is Listening
```powershell
netstat -ano | findstr :8000
```
Should show: `TCP    0.0.0.0:8000 ... LISTENING`

### 3. Verify IP Address
```powershell
ipconfig | findstr IPv4
```
Should show: `IPv4 Address. . . . . . : 192.168.0.102`

### 4. Check Firewall Rule
```powershell
netsh advfirewall firewall show rule name="Python API Server"
```
Should show rule details (not "No rules match")

### 5. Temporarily Disable Firewall (Testing Only!)
```powershell
# As Administrator
netsh advfirewall set allprofiles state off
```

Test connection. If it works, the firewall was blocking it.

**Don't forget to turn it back on:**
```powershell
netsh advfirewall set allprofiles state on
```

Then add the proper firewall rule using Method 1, 2, or 3 above.

### 6. Check Antivirus
Some antivirus software has its own firewall:
- **Windows Defender**: Settings → Firewall → Allow an app
- **Third-party AV**: Check its firewall settings

### 7. Verify Same Network
On both devices:
- **Server:** `ipconfig` → Should show `192.168.0.xxx`
- **Client:** Check WiFi/network settings → Should be `192.168.0.yyy`

Both must be on the same subnet (192.168.0.x)!

### 8. Check Router Settings
Some routers block device-to-device communication:
- Look for "AP Isolation" or "Client Isolation" in router settings
- Disable it if enabled

---

## 📱 Device-Specific Notes

### Android/iOS:
- Make sure phone is on WiFi (not mobile data)
- Use Chrome or Safari (best WebRTC support)
- Grant microphone permission when prompted

### Mac:
```bash
curl http://192.168.0.102:8000/api/health
```

### Linux:
```bash
curl http://192.168.0.102:8000/api/health
```

### Other Windows PC:
Use `test_from_other_device.html` or PowerShell:
```powershell
Invoke-RestMethod -Uri http://192.168.0.102:8000/api/health
```

---

## ✅ Success Checklist

- [ ] Firewall rule added for port 8000
- [ ] Agent service running (`uv run python src/agent.py dev`)
- [ ] API server running (`uv run python unified_api.py`)
- [ ] Port 8000 is listening on `0.0.0.0`
- [ ] Both devices on same network (192.168.0.x)
- [ ] Health check returns JSON from other device
- [ ] `test_from_other_device.html` shows all tests passing

---

## 🎉 Once Working:

Open `portable_voice_ui.html` on the other device and:
1. Set Server URL to: `http://192.168.0.102:8000/api/connect`
2. Enter custom instructions
3. Click "Connect & Talk"
4. Start speaking!

---

## 💡 Pro Tips

**For permanent setup:**
- Assign static IP to server (192.168.0.102)
- Add firewall rule (done!)
- Create desktop shortcuts for starting services

**For mobile testing:**
- Connect phone to WiFi first
- Use Chrome for best compatibility
- Keep screen on during conversation

**For production:**
- Use a proper domain with SSL
- Deploy to cloud server
- Add authentication

---

Need more help? Check the logs:
```powershell
# Agent logs
# Shows in Terminal 1 where agent is running

# API logs
# Shows in Terminal 2 where API server is running
```

