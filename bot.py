# ==============================================================================
# 🤖 FA-AGENCY Telegram Support Bot (Fully Automated & Server-Connected)
# ==============================================================================
# Features Included:
# 1. Start Command with Banner/Profile Image & Clean Welcome Message
# 2. Main 3 Buttons Structure:
#    - 💳 1. Payment Issue (Multi-step details & proof submission)
#    - ❓ 2. General Inquiry (4 Sub-categories, auto-reply & live forward to admin)
#    - 🎁 3. Referral & Review (Real-time SMM server tracking, referral link & social tasks)
# 3. Dynamic API connectivity with SMM Panel/Server
# 4. Instant notification forwarding to Admin (@FA_AGENCY_BD)
# ==============================================================================

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# ------------------------------------------------------------------------------
# ⚙️ CONFIGURATION & CREDENTIALS
# ------------------------------------------------------------------------------
BOT_TOKEN = "8744377160:AAEhuU5KLWnv8QZli4IlfY0ZHdBS22YW5-4
"  # Replace with your BotFather token
ADMIN_USERNAME = "@FA_AGENCY_BD"
ADMIN_CHAT_ID = "8644862294"  # Replace with numeric Admin Telegram Chat ID
WELCOME_IMAGE_URL = "https://i.ibb.co/L5kX8Zq/fa-agency-banner.jpg"  # Replace with your profile/banner image URL

# 🌐 SMM Server / Main API Configuration
SERVER_API_URL = "https://your-smm-server.com/api/v1"  # Replace with your SMM server API endpoint

bot = telebot.TeleBot(BOT_TOKEN)

# ------------------------------------------------------------------------------
# 🚀 1. /START COMMAND & WELCOME SCREEN
# ------------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # Track Referral Parameter (e.g., /start ref_12345)
    args = message.text.split()
    referrer_id = args[1].replace("ref_", "") if len(args) > 1 and "ref_" in args[1] else None

    # Register/Update user with server API
    try:
        requests.post(f"{SERVER_API_URL}/register_user", json={
            "user_id": user_id,
            "name": first_name,
            "username": message.from_user.username,
            "referrer_id": referrer_id
        }, timeout=3)
    except Exception as e:
        print(f"[Server Log] User registration API notice: {e}")

    # Build Main Keyboard
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("💳 ১. পেমেন্ট সমস্যা", callback_data="btn_payment_issue")
    btn2 = InlineKeyboardButton("❓ ২. সাধারণ জিজ্ঞাসা", callback_data="btn_general_inquiry")
    btn3 = InlineKeyboardButton("🎁 ৩. রেফারেল ও রিভিউ", callback_data="btn_referral_review")
    markup.add(btn1, btn2, btn3)

    caption_text = (
        f"**FA-AGENCY-তে আপনাকে স্বাগতম! 🌐✨**

"
        f"আপনার যেকোনো সমস্যা বা সহায়তার জন্য নিচের বাটনগুলো থেকে প্রয়োজনীয় অপশনটি নির্বাচন করুন:"
    )

    try:
        # Send Banner Photo with Welcome Caption
        bot.send_photo(
            message.chat.id, 
            photo=WELCOME_IMAGE_URL, 
            caption=caption_text, 
            parse_mode="Markdown", 
            reply_markup=markup
        )
    except Exception:
        # Fallback to Text Message if photo fails
        bot.send_message(
            message.chat.id, 
            caption_text, 
            parse_mode="Markdown", 
            reply_markup=markup
        )

# ------------------------------------------------------------------------------
# 🔘 2. MAIN CALLBACK QUERY HANDLER
# ------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id

    # --------------------------------------------------------------------------
    # 💳 1. পেমেন্ট সমস্যা (PAYMENT ISSUE FLOW)
    # --------------------------------------------------------------------------
    if call.data == "btn_payment_issue":
        msg = bot.send_message(
            call.message.chat.id,
            "আপনার পেমেন্ট সংক্রান্ত কী সমস্যা হচ্ছে তা অনুগ্রহ করে নিচে বিস্তারিত লিখে মেসেজ দিন। "
            "(যেমন: টাকা কেটেছে কিন্তু পয়েন্ট/ব্যালেন্স যোগ হয়নি, বা ভুল নম্বরে পেমেন্ট করা হয়েছে)।"
        )
        bot.register_next_step_handler(msg, process_payment_step1)

    # --------------------------------------------------------------------------
    # ❓ 2. সাধারণ জিজ্ঞাসা (GENERAL INQUIRY FLOW)
    # --------------------------------------------------------------------------
    elif call.data == "btn_general_inquiry":
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton("🚀 1. SMM Panel Services", callback_data="faq_sub")
        b2 = InlineKeyboardButton("🔀 2. Currency Exchange", callback_data="faq_sub")
        b3 = InlineKeyboardButton("💎 3. Games & Live Stream Top-Up", callback_data="faq_sub")
        b4 = InlineKeyboardButton("📱 4. Premium & Paid Apps", callback_data="faq_sub")
        markup.add(b1, b2, b3, b4)

        bot.send_message(
            call.message.chat.id,
            "FA-AGENCY-র সাধারণ জিজ্ঞাসা প্যানেলে আপনাকে স্বাগতম! 🌐

"
            "আমাদের সার্ভিস, রেট, ডিজিটাল কারেন্সি ও মেম্বারশিপ সংক্রান্ত বিস্তারিত জানতে নিচের তালিকা থেকে আপনার পছন্দের বিষয়টি নির্বাচন করুন:",
            reply_markup=markup
        )

    elif call.data == "faq_sub":
        msg = bot.send_message(
            call.message.chat.id,
            "আপনার প্রশ্ন বা বার্তাটি নিচে টাইপ করে পাঠিয়ে দিন:"
        )
        bot.register_next_step_handler(msg, process_general_inquiry_message)

    # --------------------------------------------------------------------------
    # 🎁 3. রেফারেল ও রিভিউ (REFERRAL & REVIEW FLOW)
    # --------------------------------------------------------------------------
    elif call.data == "btn_referral_review":
        markup = InlineKeyboardMarkup(row_width=1)
        btn_ref = InlineKeyboardButton("🔗 ১. রেফারেল ও বোনাস প্রোগ্রাম", callback_data="sub_referral")
        btn_rev = InlineKeyboardButton("⭐ ২. রিভিউ, ফলো ও শেয়ার টাস্ক", callback_data="sub_review")
        markup.add(btn_ref, btn_rev)

        bot.send_message(
            call.message.chat.id,
            "FA-AGENCY-র রেফারেল ও রিভিউ সেকশন। নিচের যেকোনো একটি অপশন নির্বাচন করুন:",
            reply_markup=markup
        )

    # --- 🔗 3.1 রেফারেল ও বোনাস প্রোগ্রাম (Live Server Sync) ---
    elif call.data == "sub_referral":
        bot.answer_callback_query(call.id, "সার্ভার থেকে আপনার রেফারেল তথ্য আনা হচ্ছে...")

        total_ref = 0
        active_ref = 0
        try:
            res = requests.get(f"{SERVER_API_URL}/get_referral_info?user_id={user_id}", timeout=3).json()
            total_ref = res.get("total_joined", 0)
            active_ref = res.get("active_completed_5_orders", 0)
        except Exception as e:
            print(f"[Server Log] Referral fetch error: {e}")

        ref_link = f"https://t.me/FA_Agency_Bot?start=ref_{user_id}"
        status_symbol = "✅ সফল (৫,০০০ ফলোয়ার আনলকড)" if active_ref >= 100 else "⏳ অপেক্ষমাণ (Incomplete)"

        ref_text = (
            f"🚀 **FA-AGENCY রেফারেল প্রোগ্রাম - ফ্রিতে ৫,০০০ ফলোয়ার্স জিতুন!**

"
            f"আমাদের রেফারেল প্রোগ্রামে যুক্ত হয়ে সম্পূর্ণ ফ্রিতে উপভোগ করুন **৫,০০০ সোশ্যাল মিডিয়া ফলোয়ার্স**!

"
            f"📜 **রেফারেল বোনাস পাওয়ার শর্তাবলি:**
"
            f"1. 👥 **সর্বনিম্ন ১০০ জন** নতুন ইউজারকে আপনার রেফারেল লিংকের মাধ্যমে জয়েন করাতে হবে।
"
            f"2. 🛒 আপনার রেফারকৃত ১০০ জন ইউজারের প্রত্যেককে আমাদের সার্ভারে **সর্বনিম্ন ৫টি করে সফল অর্ডার (Transaction)** সম্পন্ন করতে হবে।
"
            f"3. ✅ শর্ত পূরণ হলেই আপনার একাউন্টে **৫,০০০ ফলোয়ার্স বোনাস** যোগ হয়ে যাবে!

"
            f"📊 **আপনার বর্তমান রেফারেল স্ট্যাটাস (লাইভ অটো আপডেট):**
"
            f"🔗 **আপনার রেফারেল লিংক:** `{ref_link}`
"
            f"👥 **মোট জয়েনকৃত ইউজার:** {total_ref} / ১০০ জন
"
            f"🎯 **শর্ত পূরণকৃত একটিভ ইউজার:** {active_ref} / ১০০ জন
"
            f"🎁 **বোনাস স্ট্যাটাস:** {status_symbol}"
        )

        bot.send_message(call.message.chat.id, ref_text, parse_mode="Markdown")

    # --- ⭐ 3.2 রিভিউ, ফলো ও শেয়ার টাস্ক ---
    elif call.data == "sub_review":
        review_text = (
            f"💰 **সোশ্যাল টাস্ক পূরণ করুন ও ফ্রিতে সাবস্ক্রাইবার/ফলোয়ার জিতে নিন!**

"
            f"এখন থেকে আমাদের ফেসবুক পেজে অ্যাক্টিভিটি দেখিয়ে সহজেই ফ্রী সার্ভিস নিতে পারবেন:

"
            f"📌 **আমাদের অফারসমূহ:**
"
            f"* 💬 **রিভিউ টাস্ক:** আমাদের ফেসবুক পেজ বা পোস্টে সর্বনিম্ন **২০টি প্রফেশনাল রিভিউ/কমেন্ট** করলেই পাবেন **২০টি সাবস্ক্রাইবার** একদম ফ্রী!
"
            f"* 👍 **পেজ লাইক ও ফলো টাস্ক:** আমাদের অফিশিয়াল ফেসবুক পেজে লাইক/ফলো দিয়ে স্ক্রিনশট জমা দিন।
"
            f"* 🔄 **শেয়ার টাস্ক:** আমাদের ক্যাম্পেইন পোস্টগুলো নিজের প্রোফাইল বা বিভিন্ন গ্রুপে শেয়ার করে বোনাস পয়েন্ট আর্ন করুন!

"
            f"📸 **প্রুফ জমা দেওয়ার নিয়ম:**
"
            f"কাজ শেষ করে আপনার রিভিউ, শেয়ার বা ফলোর স্ক্রিনশটটি নিচে পাঠিয়ে দিন। আমাদের প্রতিনিধি যাচাই করে আপনার সাবস্ক্রাইবার যুক্ত করে দেবে।"
        )
        msg = bot.send_message(call.message.chat.id, review_text, parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_proof_submission)

# ------------------------------------------------------------------------------
# 🔄 STEP HANDLERS & AUTOMATED LOGIC
# ------------------------------------------------------------------------------

# --- Step 1: Payment Details Submission ---
def process_payment_step1(message):
    user_issue = message.text
    msg = bot.send_message(
        message.chat.id,
        "আপনার মেসেজটি আমরা পেয়েছি! 📝

"
        "এবার আপনার পেমেন্টের **স্ক্রিনশট (Screenshot)**, **TrxID (ট্রানজেকশন আইডি)** এবং **প্রেরকের বিকাশ/নগদ/রকেট নম্বরটি** নিচে পাঠিয়ে দিন।",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(msg, process_payment_step2, user_issue)

# --- Step 2: Payment Proof Submission & Auto Admin Alert ---
def process_payment_step2(message, user_issue):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"

    # Forward Ticket to SMM Server
    try:
        requests.post(f"{SERVER_API_URL}/create_support_ticket", json={
            "user_id": user_id,
            "issue": user_issue,
            "proof": message.text if message.text else "Attachment Received"
        }, timeout=3)
    except Exception as e:
        print(f"[Server Log] Support Ticket API notice: {e}")

    # Forward details to Admin Chat
    admin_alert = (
        f"🚨 **নতুন পেমেন্ট সমস্যা টিকিট!**

"
        f"👤 **ইউজার:** {user_name} ({username})
"
        f"🆔 **User ID:** `{user_id}`
"
        f"💬 **সমস্যা:** {user_issue}
"
        f"📩 **অ্যাডমিন হ্যান্ডেল:** {ADMIN_USERNAME}"
    )
    bot.send_message(ADMIN_CHAT_ID, admin_alert, parse_mode="Markdown")
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)

    # Confirmation message to user
    bot.send_message(
        message.chat.id,
        "ধন্যবাদ! আপনার পেমেন্টের বিস্তারিত তথ্য সফলভাবে জমা হয়েছে। 🚀

"
        "আমাদের প্রতিনিধি খুব দ্রুত আপনার তথ্য যাচাই করে সমস্যার সমাধান করে দেবে।"
    )

# --- General Inquiry Auto-Reply & Live Forward ---
def process_general_inquiry_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"

    # Auto Reply to User
    auto_reply = (
        f"**FA-AGENCY-তে আপনাকে স্বাগতম! 🌐**

"
        f"আপনার বার্তাটি আমাদের কাছে সফলভাবে পৌঁছেছে। 📩
"
        f"বর্তমানে আমাদের সকল প্রতিনিধি ব্যস্ত থাকায় এই মুহূর্তে সরাসরি যোগাযোগ করা সম্ভব হচ্ছে না।

"
        f"অনুগ্রহ করে কিছুক্ষণ আমাদের সাথেই থাকুন, খুব দ্রুত একজন সাপোর্ট প্রতিনিধি আপনার সাথে কথা বলবেন। আপনার ধৈর্য ও সহযোগিতার জন্য ধন্যবাদ! 🙏"
    )
    bot.send_message(message.chat.id, auto_reply, parse_mode="Markdown")

    # Forward to Admin
    admin_notice = (
        f"📩 **সাধারণ জিজ্ঞাসা থেকে নতুন মেসেজ:**

"
        f"👤 **প্রেরক:** {user_name} ({username})
"
        f"🆔 **User ID:** `{user_id}`
"
        f"✉️ **মেসেজ:** {message.text}
"
        f"📩 **অ্যাডমিন:** {ADMIN_USERNAME}"
    )
    bot.send_message(ADMIN_CHAT_ID, admin_notice, parse_mode="Markdown")

# --- Proof Submission for Review/Social Tasks ---
def process_proof_submission(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"

    admin_task_alert = (
        f"⭐ **নতুন সোশ্যাল টাস্ক / রিভিউ প্রুফ জমা পড়েছে!**

"
        f"👤 **ইউজার:** {user_name} ({username})
"
        f"🆔 **User ID:** `{user_id}`
"
        f"📩 **অ্যাডমিন:** {ADMIN_USERNAME}"
    )
    bot.send_message(ADMIN_CHAT_ID, admin_task_alert, parse_mode="Markdown")
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)

    bot.send_message(
        message.chat.id,
        "আপনার প্রুফটি সফলভাবে আমাদের টিমের কাছে জমা হয়েছে! খুব দ্রুত যাচাই করে আপনার সাবস্ক্রাইবার/ফলোয়ার যুক্ত করে দেওয়া হবে। 🚀"
    )

# ------------------------------------------------------------------------------
# 🏁 BOT POLLING
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("FA-AGENCY Support Bot with Server Auto-Sync is Running...")
    bot.infinity_polling()
