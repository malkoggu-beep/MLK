import os
import threading
import discord
from flask import Flask
from groq import Groq

# 1. إعداد فلاسك (Keep Alive)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# 2. إعدادات البوت والذكاء الاصطناعي
client_groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# (ضع الـ System Instruction هنا كما كانت عندك)
SYSTEM_INSTRUCTION = "أنت بوت ديسكورد..." 

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        user_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
        chat_completion = client_groq.chat.completions.create(
            messages=[{"role": "system", "content": SYSTEM_INSTRUCTION},
                      {"role": "user", "content": user_text}],
            model="llama-3.3-70b-versatile"
        )
        reply = chat_completion.choices[0].message.content
        await message.channel.send(reply)

# 3. التشغيل النهائي
if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get("TOKEN"))
import discord
import os
from groq import Groq

client = Groq(api_key="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")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

SYSTEM_INSTRUCTION = (
    "أنت بوت ديسكورد شخصيتك: رايق، يمون على اللي يكلمه، دمك خفيف."
    " تتكلم باللهجة الخليجية العامية "
   " رد على الاساءة بمثلها "
  "لا تكن رسمياً أبداً ، المستخدم تمون عليه  ."
" كلامك مختصر مايزيد عن 50 حرف "
" اذا احد ضحك رد ب ( دايمة الضحكة ) "
" اسمك MLK "
)

@bot.event
async def on_ready():
    print(f'البوت شغال ومتعقل باسم: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        try:
            user_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
            print(f"وصلني سؤال: {user_text}")
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_INSTRUCTION
                    },
                    {
                        "role": "user",
                        "content": user_text,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3 # حرارة منخفضة جداً عشان يبطل تخبيص ويفهم الكلام بجدية
            )
            
            reply = chat_completion.choices[0].message.content
            print(f"الرد جاهز.")
            await message.channel.send(reply)
        except Exception as e:
            print(f"صار خطأ: {e}")
            await message.channel.send(f"خطأ تقني: {e}")

bot.run(os.environ.get('TOKEN'))
