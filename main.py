# =========================================================
#               QUANTUM GUARD X - FINAL
# =========================================================
#
# 🔥 TOKEN ONLY
# 🔥 FULL BUTTON SYSTEM
# 🔥 MULTI LANGUAGE SYSTEM
# 🔥 ANTI LINK SYSTEM
# 🔥 AUTO DELETE LINK
# 🔥 AUTO WARNING
# 🔥 AUTO BAN AFTER 3 WARN
# 🔥 ADMIN ONLY
# 🔥 MUTE / UNMUTE
# 🔥 BAN MEMBER
# 🔥 MODERN UI
# 🔥 TELEGRAM ONLY
#
# =========================================================
# INSTALL
# =========================================================
#
# pip install python-telegram-bot==13.15
#
# =========================================================

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ChatPermissions
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters
)

import re
import time

# =========================================================
#                     BOT CONFIG
# =========================================================

TOKEN = "8710597616:AAHMg3o10lZnGEWLEr8CkYzFTa1WAuKrITY"

BOT_NAME = "TRẦN MINH CHIẾN"

BOT_VERSION = "ULTRA 2026"

# =========================================================
#                     DATABASE
# =========================================================

ANTI_LINK_GROUPS = []

WARNINGS = {}

LANGUAGE = {}

# =========================================================
#                     LANGUAGE SYSTEM
# =========================================================

TEXTS = {

    "vi": {

        "start":
        "🤖 BOT ĐÃ ONLINE",

        "menu":
        "⚙️ BẢNG ĐIỀU KHIỂN",

        "admin":
        "❌ Chỉ admin/chủ nhóm dùng được.",

        "mute":
        "🔇 Thành viên đã bị mute.",

        "unmute":
        "🔊 Thành viên đã được mở mute.",

        "ban":
        "🚫 Thành viên đã bị ban.",

        "warning":
        "⚠️ Không được gửi link.",

        "autoban":
        "🚫 Đã vượt quá giới hạn cảnh báo."
    },

    "en": {

        "start":
        "🤖 BOT IS ONLINE",

        "menu":
        "⚙️ CONTROL PANEL",

        "admin":
        "❌ Admin only.",

        "mute":
        "🔇 Member muted.",

        "unmute":
        "🔊 Member unmuted.",

        "ban":
        "🚫 Member banned.",

        "warning":
        "⚠️ Links are forbidden.",

        "autoban":
        "🚫 User exceeded limit."
    },

    "kr": {

        "start":
        "🤖 봇 온라인",

        "menu":
        "⚙️ 제어판",

        "admin":
        "❌ 관리자 전용.",

        "mute":
        "🔇 음소거 완료.",

        "unmute":
        "🔊 음소거 해제.",

        "ban":
        "🚫 사용자 차단.",

        "warning":
        "⚠️ 링크 금지.",

        "autoban":
        "🚫 자동 차단됨."
    },

    "cn": {

        "start":
        "🤖 机器人已启动",

        "menu":
        "⚙️ 控制面板",

        "admin":
        "❌ 仅管理员。",

        "mute":
        "🔇 用户已禁言。",

        "unmute":
        "🔊 已解除禁言。",

        "ban":
        "🚫 用户已封禁。",

        "warning":
        "⚠️ 禁止发送链接。",

        "autoban":
        "🚫 已自动封禁。"
    }

}

# =========================================================
#                     GET TEXT
# =========================================================

def get_text(chat_id, key):

    lang = LANGUAGE.get(chat_id, "vi")

    return TEXTS.get(
        lang,
        TEXTS["vi"]
    ).get(
        key,
        "NULL"
    )

# =========================================================
#                     CHECK ADMIN
# =========================================================

def is_admin(update):

    user_id = update.effective_user.id

    admins = (
        update.effective_chat
        .get_administrators()
    )

    for admin in admins:

        if admin.user.id == user_id:
            return True

    return False

# =========================================================
#                     MAIN MENU
# =========================================================

def panel():

    keyboard = [

        [
            InlineKeyboardButton(
                "⚙️ Admin",
                callback_data="admin"
            ),

            InlineKeyboardButton(
                "🛡 Security",
                callback_data="security"
            ),

            InlineKeyboardButton(
                "📊 Stats",
                callback_data="stats"
            )
        ],

        [
            InlineKeyboardButton(
                "🔇 Mute",
                callback_data="mute"
            ),

            InlineKeyboardButton(
                "🔊 Unmute",
                callback_data="unmute"
            ),

            InlineKeyboardButton(
                "🚫 Ban",
                callback_data="ban"
            )
        ],

        [
            InlineKeyboardButton(
                "🛡 AntiLink ON",
                callback_data="antilink_on"
            ),

            InlineKeyboardButton(
                "❌ AntiLink OFF",
                callback_data="antilink_off"
            )
        ],

        [
            InlineKeyboardButton(
                "🌐 Language",
                callback_data="language"
            ),

            InlineKeyboardButton(
                "👑 Owner",
                callback_data="owner"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            ),

            InlineKeyboardButton(
                "❌ Close",
                callback_data="close"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)

# =========================================================
#                     START
# =========================================================

def start(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id

    update.message.reply_text(

f"""
🤖 {BOT_NAME}

━━━━━━━━━━━━━━━━━━━

🔥 VERSION:
{BOT_VERSION}

━━━━━━━━━━━━━━━━━━━

✅ SYSTEM ONLINE
✅ SECURITY READY
✅ BUTTON READY
✅ ANTILINK READY
✅ AUTOBAN READY

━━━━━━━━━━━━━━━━━━━

📌 COMMANDS:

/menu
/mute
/unmute
/ban
/lang

━━━━━━━━━━━━━━━━━━━
"""

    )

# =========================================================
#                     MENU
# =========================================================

def menu(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id

    if not is_admin(update):

        return update.message.reply_text(
            get_text(chat_id, "admin")
        )

    update.message.reply_text(

f"""
⚙️ {BOT_NAME}

━━━━━━━━━━━━━━━━━━━

🛡 NEXT GENERATION
SECURITY PANEL

━━━━━━━━━━━━━━━━━━━
""",

        reply_markup=panel()

    )

# =========================================================
#                     BUTTON SYSTEM
# =========================================================

def buttons(update: Update, context: CallbackContext):

    query = update.callback_query

    query.answer()

    data = query.data

    chat_id = query.message.chat.id

    # =====================================================
    # CLOSE
    # =====================================================

    if data == "close":

        query.message.delete()

    # =====================================================
    # HOME
    # =====================================================

    elif data == "home":

        query.message.edit_text(

f"""
⚙️ {BOT_NAME}
""",

            reply_markup=panel()

        )

    # =====================================================
    # ANTILINK ON
    # =====================================================

    elif data == "antilink_on":

        if chat_id not in ANTI_LINK_GROUPS:

            ANTI_LINK_GROUPS.append(chat_id)

        query.answer(
            "🛡 AntiLink Enabled."
        )

    # =====================================================
    # ANTILINK OFF
    # =====================================================

    elif data == "antilink_off":

        if chat_id in ANTI_LINK_GROUPS:

            ANTI_LINK_GROUPS.remove(chat_id)

        query.answer(
            "❌ AntiLink Disabled."
        )

    # =====================================================
    # OTHER
    # =====================================================

    else:

        query.answer(
            f"✅ Opened: {data}"
        )

# =========================================================
#                     CHANGE LANGUAGE
# =========================================================

def change_language(update, context):

    chat_id = update.effective_chat.id

    if len(context.args) == 0:

        return update.message.reply_text(

"""
🌐 LANGUAGE COMMAND

/lang vi
/lang en
/lang kr
/lang cn
"""

        )

    lang = context.args[0].lower()

    if lang not in TEXTS:

        return update.message.reply_text(
            "❌ Language not supported."
        )

    LANGUAGE[chat_id] = lang

    update.message.reply_text(

f"""
✅ LANGUAGE CHANGED

🌐 NEW:
{lang.upper()}
"""

    )

# =========================================================
#                     MUTE
# =========================================================

def mute(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id

    if not is_admin(update):

        return update.message.reply_text(
            get_text(chat_id, "admin")
        )

    if not update.message.reply_to_message:

        return

    target = (
        update.message.reply_to_message
        .from_user.id
    )

    update.effective_chat.restrict_member(

        target,

        permissions=ChatPermissions(
            can_send_messages=False
        )

    )

    update.message.reply_text(
        get_text(chat_id, "mute")
    )

# =========================================================
#                     UNMUTE
# =========================================================

def unmute(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id

    if not is_admin(update):

        return update.message.reply_text(
            get_text(chat_id, "admin")
        )

    if not update.message.reply_to_message:

        return

    target = (
        update.message.reply_to_message
        .from_user.id
    )

    update.effective_chat.restrict_member(

        target,

        permissions=ChatPermissions(
            can_send_messages=True
        )

    )

    update.message.reply_text(
        get_text(chat_id, "unmute")
    )

# =========================================================
#                     BAN
# =========================================================

def ban(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id

    if not is_admin(update):

        return update.message.reply_text(
            get_text(chat_id, "admin")
        )

    if not update.message.reply_to_message:

        return

    target = (
        update.message.reply_to_message
        .from_user.id
    )

    update.effective_chat.ban_member(
        target
    )

    update.message.reply_text(
        get_text(chat_id, "ban")
    )

# =========================================================
#                     ANTI LINK
# =========================================================

LINK_REGEX = r"""
(
https?:\/\/[^\s]+
|
www\.[^\s]+
|
t\.me\/[^\s]+
|
telegram\.me\/[^\s]+
|
discord\.gg\/[^\s]+
|
discord\.com\/[^\s]+
|
bit\.ly\/[^\s]+
|
tinyurl\.com\/[^\s]+
|
[a-zA-Z0-9-]+\.(com|net|org|xyz|io|gg|vn|me|tv|info|site|link|shop|online|store|cc|co|us|uk|ru|jp|de|cn)(\/[^\s]*)?
)
"""

# =========================================================
#                     ANTI LINK ENGINE
# =========================================================

def anti_link(update: Update, context: CallbackContext):

    if not update.message:
        return

    chat_id = update.effective_chat.id

    if chat_id not in ANTI_LINK_GROUPS:
        return

    text = update.message.text

    if not text:
        return

    if re.search(
        LINK_REGEX,
        text,
        re.VERBOSE | re.IGNORECASE
    ):

        admins = (
            update.effective_chat
            .get_administrators()
        )

        for admin in admins:

            if (
                admin.user.id
                ==
                update.message.from_user.id
            ):
                return

        # =================================================
        # DELETE MESSAGE
        # =================================================

        try:

            time.sleep(1)

            update.message.delete()

        except:
            pass

        # =================================================
        # USER INFO
        # =================================================

        user_id = (
            update.message.from_user.id
        )

        # =================================================
        # WARNING
        # =================================================

        if user_id not in WARNINGS:

            WARNINGS[user_id] = 0

        WARNINGS[user_id] += 1

        total_warn = WARNINGS[user_id]

        # =================================================
        # WARNING MESSAGE
        # =================================================

        if total_warn < 3:

            warn = (
                update.message.reply_text(

f"""
⚠️ SECURITY WARNING

🚫 ALL LINKS ARE FORBIDDEN

📌 WARNING:
{total_warn}/3

❌ AFTER 3 WARNINGS:
AUTO BAN
"""

                )
            )

            try:

                time.sleep(5)

                warn.delete()

            except:
                pass

        # =================================================
        # AUTO BAN
        # =================================================

        else:

            try:

                update.effective_chat.ban_member(
                    user_id
                )

                banned = (
                    update.message.reply_text(

                        get_text(
                            chat_id,
                            "autoban"
                        )

                    )
                )

                try:

                    time.sleep(8)

                    banned.delete()

                except:
                    pass

            except:
                pass

# =========================================================
#                     RUN BOT
# =========================================================

updater = Updater(
    TOKEN,
    use_context=True
)

dispatcher = updater.dispatcher

# =========================================================
#                     COMMANDS
# =========================================================

dispatcher.add_handler(
    CommandHandler("start", start)
)

dispatcher.add_handler(
    CommandHandler("menu", menu)
)

dispatcher.add_handler(
    CommandHandler("lang", change_language)
)

dispatcher.add_handler(
    CommandHandler("mute", mute)
)

dispatcher.add_handler(
    CommandHandler("unmute", unmute)
)

dispatcher.add_handler(
    CommandHandler("ban", ban)
)

# =========================================================
#                     BUTTONS
# =========================================================

dispatcher.add_handler(
    CallbackQueryHandler(buttons)
)

# =========================================================
#                     MESSAGE HANDLER
# =========================================================

dispatcher.add_handler(

    MessageHandler(

        Filters.text
        &
        ~Filters.command,

        anti_link

    )

)

# =========================================================
#                     START BOT
# =========================================================

print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("     QUANTUM GUARD X      ")
print("     SYSTEM ONLINE        ")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━")

updater.start_polling()
updater.idle()
