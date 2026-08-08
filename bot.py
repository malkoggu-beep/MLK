import discord
from groq import Groq

TOKEN = "MTUzNTM5OTgzNTk3MTM1ODcyMA.G1IQLd.iIJZv99_sJD7i6Wm4D7UM-cJ6mpzfOOlcBcG-U"
client = Groq(api_key="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")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# تعليمات صارمة تمنع التخبيص وتخليه يرد بكلمات واضحة ومرتبة
SYSTEM_INSTRUCTION = (
    "أنت مساعد ذكي في ديسكورد. تحدث دائماً بلغة عربية سليمة وواضحة (أو إنجليزية صحيحة إذا تم مخاطبتك بالإنجليزية). "
    "ممنوع منعاً باتاً دمج اللغات بطريقة غريبة أو الهلوسة. "
    "إذا وجه لك أحد إساءة أو سبة، رد عليه برد مختصر، صارم، وقوي يوقفه عند حده فوراً وبدون أي استهبال."
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

bot.run(TOKEN)
