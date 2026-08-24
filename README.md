# 🤖 API Bomber Telegram Bot

A powerful Telegram bot with 900+ working APIs for SMS/Call/WhatsApp bombing with credit system, premium membership, and admin panel.

## ✨ Features

### Main Bot Features:
- 💰 **Credit System** - 1 credit = 20 minutes of continuous API bombing
- 📱 **900+ Working APIs** - Calls, WhatsApp, and SMS
- ⏱️ **Live Statistics** - Real-time success/fail tracking with timer
- 🛑 **Stop Button** - Cancel bombing anytime
- 🔗 **Referral System** - Earn 1 credit per referral
- 👑 **Premium Membership** - Daily 20 credits auto-added
- 📊 **User Dashboard** - Track credits, stats, and premium status

### Admin Bot Features:
- 🔐 **Full Admin Panel** - Complete bot control
- 👥 **User Management** - Add/set credits, block/unblock users
- 👑 **Premium Management** - Add premium memberships
- 🚀 **API Control** - Enable/disable individual APIs
- 💰 **Price Management** - Set credit prices dynamically
- 📢 **Broadcast** - Send messages to all users
- 📊 **Statistics** - Real-time bot analytics

## 💳 Default Pricing

**Credits:**
- ₹25 → 2 Credits
- ₹50 → 5 Credits
- ₹100 → 12 Credits
- ₹200 → 25 Credits

**Premium:**
- ₹999 → 1 Month Premium (20 credits daily)

## 🚀 Railway Deployment

### Step 1: Create GitHub Repository
1. Create new repository on GitHub
2. Upload these files:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `README.md`

### Step 2: Deploy on Railway
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect and deploy

### Step 3: Configure
1. Go to your Railway project
2. Click on your service
3. Go to "Settings" → "Environment Variables"
4. Add any custom configurations (optional)

### Step 4: Start
- Bot will start automatically!
- Check logs to confirm both bots are running

## 📋 Bot Configuration

### Tokens (Already Set):
- Main Bot: `7883509707:AAGnaQFs07hXjX6-1MrU8IRaDZXQSb-Gd-w`
- Admin Bot: `8353268447:AAEFfkkubAfWldYfUdOSE7sHrK2taZl_YXs`

### Owner ID:
- `8458169644`

### Channel Settings:
- Update in `bot.py` or use admin commands to modify

## 🎮 How to Use

### For Users:
1. Start bot: `/start`
2. Join required channels
3. Send 10-digit phone number
4. Bot will bomb for 20 minutes
5. View live statistics

### For Admins:
1. Start admin bot: `/start`
2. Use admin commands:
   - `/on` - Turn bot on
   - `/off` - Turn bot off
   - `/stats` - View statistics
   - `/add uid credits` - Add credits
   - `/addpremium uid days` - Add premium
   - `/listapis` - View all APIs
   - `/toggleapi id` - Enable/disable API
   - `/setprice amount credits` - Set price
   - `/broadcast message` - Send to all

## 🔧 Admin Commands

### Bot Control:
- `/on` - Activate bot
- `/off` - Maintenance mode
- `/stats` - Bot statistics

### User Management:
- `/add uid credits` - Add credits to user
- `/set uid credits` - Set user credits
- `/check uid` - Check user info
- `/block uid` - Block user
- `/unblock uid` - Unblock user
- `/addpremium uid days` - Add premium membership

### API Management:
- `/listapis` - List all APIs
- `/toggleapi id` - Toggle API on/off
- `/apicount` - Count active APIs

### Price Management:
- `/setprice amount credits` - Set credit price
- `/setpremium price days daily_credits` - Set premium config
- `/showprices` - Show current prices

### Broadcast:
- `/broadcast message` - Send message to all users

## 📊 Features Breakdown

### Credit System:
- New users get 2 credits free
- 1 credit = 20 minutes API bombing
- Referrals earn 1 credit
- Admin can add/set credits

### Premium System:
- Daily credit auto-add (default: 20)
- Configurable by admin
- Expiry tracking
- Automatic renewal notifications

### API System:
- 900+ working APIs included
- Individual API toggle
- Success/fail tracking
- Real-time statistics

### Security:
- Channel join verification
- User blocking system
- Admin-only controls
- Rate limiting built-in

## 🔄 Auto Features

1. **Daily Credit Reset** - Premium users get credits at midnight
2. **Premium Expiry Check** - Automatic expiry tracking
3. **Auto Restart** - Bot auto-restarts on errors
4. **Data Persistence** - JSON file storage

## 📁 File Structure

```
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── Procfile           # Railway process file
├── runtime.txt        # Python version
├── README.md          # This file
├── users.json         # User data (auto-created)
├── settings.json      # Bot settings (auto-created)
├── admins.json        # Admin list (auto-created)
├── apis.json          # API database (auto-created)
└── blocked.json       # Blocked users (auto-created)
```

## ⚠️ Important Notes

1. **API Success Rate**: Not all APIs work 100% of the time
2. **Rate Limiting**: Built-in delays to prevent IP bans
3. **SSL Verification**: Disabled for maximum API compatibility
4. **Concurrent Limits**: No limit on concurrent connections
5. **Error Handling**: Automatic retry and error logging

## 🛠️ Customization

### Change Channel:
Edit in `bot.py`:
```python
CHANNELS = {"channel": "@yourChannel"}
CHANNEL_LINKS = {"channel": "https://t.me/yourChannel"}
```

### Modify Start Credits:
```python
START_CREDITS = 2  # Change this value
```

### Update Referral Rewards:
```python
REF_CREDITS = 1  # Change this value
```

### Add More Admins:
Use admin bot command:
```
/addadmin user_id
```

## 📞 Support

- Owner: @TGxTHOMASx
- Bot Issues: Contact via bot
- Admin Help: Use admin bot commands

## 🎯 Success Tips

1. **Set Competitive Prices** - Use `/setprice` to adjust
2. **Monitor APIs** - Disable non-working APIs with `/toggleapi`
3. **Promote Bot** - Share referral links
4. **Engage Users** - Use broadcast for updates
5. **Premium Push** - Encourage premium subscriptions

## 📈 Growth Strategy

1. Offer initial free credits
2. Promote referral system
3. Run premium promotions
4. Regular API updates
5. Active user support

## 🔒 Security Features

- User blocking system
- Admin-only commands
- Channel verification
- Anti-spam protection
- Secure token storage

## 🚦 Status Indicators

- 🟢 Bot Active
- 🔴 Maintenance Mode
- ✅ Premium Active
- ❌ Premium Inactive
- 🔥 Bombing in Progress
- ✅ Success
- ❌ Failed

## 📝 License

Private use only. Not for resale or redistribution.

---

**Made with ❤️ for Telegram Bot Community**

**Deploy Now and Start Earning! 🚀**