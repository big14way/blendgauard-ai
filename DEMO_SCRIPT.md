# 🛡️ BlendGuard Demo Script

## Video Demo Flow (5-7 minutes)

### 📋 **Setup Checklist**
Before recording:
- [ ] Telegram bot running with token: `7837740210:AAHpN4ZdjBVfWU2OM0wm6_5bBdcrJ_Yt3kM`
- [ ] SafetyVault contract deployed: `CCHK4QGO6NODQ65PTKQPCWL7CDKKPMFVOXTN3SIR6KGDATETB6QUPY6G`
- [ ] Blend UI running on localhost
- [ ] Demo positions loaded with high-risk data
- [ ] Phone/Telegram ready for alert demo

---

## 🎬 **Demo Script**

### **Scene 1: Introduction (30 seconds)**
*Screen: Blend UI Dashboard*

**Narrator:** 
> "Welcome to BlendGuard - the first automated liquidation protection system for Blend Protocol. Today we'll show you how BlendGuard protects your DeFi positions from liquidation using SafetyVault smart contracts and real-time Telegram alerts."

**Actions:**
- Show Blend UI homepage
- Highlight BlendGuard SafetyVault button
- Quick overview of dashboard

---

### **Scene 2: High-Risk Position Discovery (45 seconds)**
*Screen: Dashboard showing positions*

**Narrator:** 
> "Let's look at a typical DeFi scenario. Here we have a position with 85% LTV - dangerously close to liquidation. The health factor is only 1.18, and the risk score is 85%."

**Actions:**
- Navigate to dashboard
- Show high-risk position details:
  - Asset: 1000 XLM
  - Debt: 850 XLM  
  - LTV: 85%
  - Risk Score: 85% (RED)
  - Health Factor: 1.18
- Highlight risk indicators

---

### **Scene 3: Telegram Alert Reception (30 seconds)**
*Screen: Split screen - Dashboard + Phone/Telegram*

**Narrator:** 
> "BlendGuard's monitoring system detects this high-risk position and immediately sends an alert to Telegram. The user receives a real-time notification with position details and one-click protection options."

**Actions:**
- Show Telegram notification arriving
- Display alert message:
  ```
  ⚠️ Liquidation Risk Alert
  
  🎯 Position: XLM
  📊 Risk Score: 85%
  💰 Amount: $1,000.00
  🔥 Health Factor: 1.18
  
  ⚡ Action Required - Your position is at risk!
  🛡️ SafetyVault: CCHK4QGO...
  ```
- Show inline buttons: "🛡️ Activate Protection" and "📊 View Details"

---

### **Scene 4: SafetyVault Protection Activation (60 seconds)**
*Screen: Telegram + Transaction processing*

**Narrator:** 
> "The user clicks 'Activate Protection' and BlendGuard's SafetyVault springs into action. The smart contract automatically executes protective measures to prevent liquidation."

**Actions:**
- Click "🛡️ Activate Protection" button
- Show loading/processing message
- Display transaction details:
  ```
  ✅ SafetyVault Protection Activated!
  
  🛡️ Contract: CCHK4QGO6NODQ65PTKQPCWL7CDKKPMFVOXTN3SIR6KGDATETB6QUPY6G
  📈 Your position is now protected from liquidation.
  
  🔗 Transaction: stellar_tx_high-risk_CCHK4QGO
  ℹ️ Status: SafetyVault 1.0 protection activated
  ```

---

### **Scene 5: Risk Reduction Verification (45 seconds)**
*Screen: Dashboard showing improved position*

**Narrator:** 
> "Let's verify the results. Back in the dashboard, we can see the SafetyVault has successfully reduced the risk score from 85% to just 15% - well below the danger threshold."

**Actions:**
- Return to Blend UI dashboard
- Show updated position:
  - Risk Score: 15% (GREEN)
  - Health Factor: Improved
  - Status: "🟢 Safe"
- Highlight the dramatic risk reduction
- Show "Protected by SafetyVault" indicator

---

### **Scene 6: Technical Overview (30 seconds)**
*Screen: Contract details + Architecture*

**Narrator:** 
> "Behind the scenes, BlendGuard uses Soroban smart contracts on Stellar, real-time risk monitoring, and Telegram integration to provide seamless protection. The SafetyVault contract can execute multiple protective actions automatically."

**Actions:**
- Show contract info command output
- Display technical stack:
  - Soroban/Stellar smart contracts
  - Python risk engine
  - Telegram Bot API
  - Real-time monitoring
- Show SafetyVault functions: execute_actions, get_info

---

### **Scene 7: Conclusion (30 seconds)**
*Screen: BlendGuard logo + Summary*

**Narrator:** 
> "BlendGuard revolutionizes DeFi safety by providing automated, intelligent protection against liquidation. Users can focus on their strategies while BlendGuard watches over their positions 24/7."

**Actions:**
- Show final summary:
  - ✅ Real-time risk monitoring
  - ✅ Instant Telegram alerts  
  - ✅ One-click protection
  - ✅ Automated SafetyVault execution
  - ✅ Risk reduced from 85% to 15%
- Display contact/GitHub information

---

## 🔧 **Technical Demo Commands**

### Start the demo environment:
```bash
# 1. Start the backend
cd backend
python alert_bot.py

# 2. Start the frontend
cd blend-ui
npm run dev

# 3. Deploy contract (if needed)
cd blend-contracts-v2
./deploy.sh
```

### Test Telegram bot:
```bash
# Send test alert
curl -X POST "https://api.telegram.org/bot7837740210:AAHpN4ZdjBVfWU2OM0wm6_5bBdcrJ_Yt3kM/sendMessage" \
  -d "chat_id=YOUR_CHAT_ID&text=🛡️ BlendGuard Test Alert"
```

---

## 📊 **Demo Data Points**

### Before Protection:
- **Position**: 1000 XLM
- **Debt**: 850 XLM
- **LTV**: 85%
- **Risk Score**: 85%
- **Health Factor**: 1.18
- **Status**: 🔴 High Risk

### After Protection:
- **Position**: Protected
- **Risk Score**: 15%
- **Health Factor**: Improved
- **Status**: 🟢 Safe
- **Protection**: ✅ SafetyVault Active

---

## 🎯 **Key Messages**

1. **Proactive Protection**: BlendGuard prevents liquidation before it happens
2. **User-Friendly**: Simple Telegram alerts with one-click protection
3. **Automated**: SafetyVault smart contracts handle complex protection logic
4. **Effective**: Risk reduction from 85% to 15% in seconds
5. **Reliable**: 24/7 monitoring and instant response

---

## 📱 **Demo Assets**

- **Contract ID**: `CCHK4QGO6NODQ65PTKQPCWL7CDKKPMFVOXTN3SIR6KGDATETB6QUPY6G`
- **Telegram Bot**: `7837740210:AAHpN4ZdjBVfWU2OM0wm6_5bBdcrJ_Yt3kM`
- **Network**: Stellar Testnet
- **Demo URL**: `http://localhost:3000`

**Ready to protect the DeFi ecosystem! 🛡️** 