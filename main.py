import os
import re
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# ================= CONFIG =================

TOKEN = os.getenv("8927671568:AAEIs-A6sS3H2KljAHpQ3hBvwYyYhnobPUo")

# ================= DATABASE =================

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS antilink(chat_id TEXT PRIMARY KEY)")
cur.execute("CREATE TABLE IF NOT EXISTS warnings(user_id TEXT PRIMARY KEY, count INTEGER)")
conn.commit()

# ================= ADMIN =================

async def is_admin(update: Update):
    admins = await update.effective_chat.get_administrators()
    return any(admin.user.id == update.effective_user.id for admin in admins)

# ================= UI PANEL =================

def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛡 AntiLink ON", callback_data="on"),
         InlineKeyboardButton("❌ AntiLink OFF", callback_data="off")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")]
    ])

# ================= COMMANDS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 BOT ONLINE - FINAL VERSION")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text("❌ Admin only")
    await update.message.reply_text("⚙️ CONTROL PANEL", reply_markup=panel())

# ================= BUTTON =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    chat_id = str(q.message.chat.id)

    if q.data == "on":
        cur.execute("INSERT OR IGNORE INTO antilink VALUES (?)", (chat_id,))
        conn.commit()
        await q.answer("🛡 AntiLink ON")

    elif q.data == "off":
        cur.execute("DELETE FROM antilink WHERE chat_id=?", (chat_id,))
        conn.commit()
        await q.answer("❌ AntiLink OFF")

    elif q.data == "stats":
        cur.execute("SELECT COUNT(*) FROM warnings")
        total = cur.fetchone()[0]
        await q.message.reply_text(f"📊 Total warned users: {total}")

# ================= MUTE =================

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        return

    user_id = update.message.reply_to_message.from_user.id

    await update.effective_chat.restrict_member(
        user_id,
        permissions=ChatPermissions(can_send_messages=False)
    )

    await update.message.reply_text("🔇 Muted")

# ================= BAN =================

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        return

    user_id = update.message.reply_to_message.from_user.id

    await update.effective_chat.ban_member(user_id)
    await update.message.reply_text("🚫 Banned")

# ================= ANTI LINK =================

LINK_REGEX = r"(https?://|www\.|t\.me|discord\.gg|\.com|\.net|\.org)"

async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat_id = str(update.effective_chat.id)

    cur.execute("SELECT * FROM antilink WHERE chat_id=?", (chat_id,))
    if not cur.fetchone():
        return

    text = update.message.text
    if not text:
        return

    if re.search(LINK_REGEX, text, re.IGNORECASE):

        admins = await update.effective_chat.get_administrators()
        if any(admin.user.id == update.message.from_user.id for admin in admins):
            return

        try:
            await update.message.delete()
        except:
            pass

        user_id = str(update.message.from_user.id)

        cur.execute("SELECT count FROM warnings WHERE user_id=?", (user_id,))
        row = cur.fetchone()

        if row:
            count = row[0] + 1
            cur.execute("UPDATE warnings SET count=? WHERE user_id=?", (count, user_id))
        else:
            count = 1
            cur.execute("INSERT INTO warnings VALUES (?,?)", (user_id, count))

        conn.commit()

        if count >= 3:
            try:
                await update.effective_chat.ban_member(int(user_id))
            except:
                pass
        else:
            await update.message.reply_text(f"⚠️ Warning {count}/3")

# ================= RUN =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("ban", ban))

app.add_handler(CallbackQueryHandler(buttons))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, anti_link)
)

print("🚀 BOT FINAL RUNNING")

app.run_polling()
