from flask import Flask
from threading import Thread
import discord  # أو أي مكتبات ثانية عندك

app = Flask('')


@app.route('/')
def home():
  return "I'm alive!"


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


# تشغيل السيرفر الوهمي أولاً
keep_alive()

# هنا يبدأ كود بوت ديسكورد العادي حقك (مثل bot.run أو client.run)
import discord
import os
from groq import Groq

client = Groq(api_key="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")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

SYSTEM_INSTRUCTION = (
    "أنت بوت ديسكورد شخصيتك: رايق، يمون بقوة على اللي يكلمه، يحب يسولف ببرود أعصاب وراحة، وراعي طقطقة وتهبيل بس بدم خفيف وبدون نفسيات مفرطة."
    " تتكلم باللهجة الخليجية العامية (مثل: يالطيب، وشعليك، ههههههه، ياخي اصبر، وش تحس فيه، هديها). "
    "لا تكن رسمياً أبداً ولا تصير نفسية، عامل المستخدم كأنكم أصحاب من زمان وتمون عليه وتعرف سواياها."
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
