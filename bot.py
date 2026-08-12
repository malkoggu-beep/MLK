import os
from flask import Flask
from threading import Thread
import discord
import google.generativeai as genai

# إعداد خادم فلاسك عشان ريندر ما يقفل البوت #
app = Flask("")


@app.route("/")
def home():
  return "I am alive!"


def run():
  app.run(host="0.0.0.0", port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


# تعريف مفتاح قوقل جيمني #
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# تخزين محادثات الشات #
channel_histories = {}

SYSTEM_INSTRUCTION = """
;قواعد التعامل والردود:
- يرد على الأسئلة بمنها وبطريقة ذكية تعكس شخصيته.
- يكلم الأعضاء بصيغة تامة وكلهم خوياه.
- إذا ضحك أحد الأعضاء يعرف يرد.
- يثبت وجوده كخادم شقياري بروجه الطيبة وأخلاقه -

;الطباع والأسلوب:
- مرح، عارف دم، وذكي في طداقته وضحكته.
- مازح في أسلوبه ويعرف كيف يمون على الأعضاء.
- راقي في أسلوبه وما يحب اللف والدوران.
- كلامه مختصر ومفيد ولا يتعدى الحاجة -
- رده لا يزيد عن 60 حرف
"""

@bot.event
async def on_ready():
  print(f"البوت شغال ومتصل باسم {bot.user}")


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if bot.user.mentioned_in(message):
    try:
      user_text = message.content.replace(f"<@{bot.user.id}>", "").strip()
      print(f"رسالة سؤال: {user_text}")

      channel_id = message.channel.id

      if channel_id not in channel_histories:
        channel_histories[channel_id] = []

      channel_histories[channel_id].append({"role": "user", "content": user_text})

      if len(channel_histories[channel_id]) > 31:
        channel_histories[channel_id].pop(0)

      # إعداد نموذج جيمني وفلاش
      model = genai.GenerativeModel(
          model_name="gemini-1.5-flash",
          system_instruction=SYSTEM_INSTRUCTION,
      )

      # تنسيق سجل المحادثات ليتوافق مع مكتبة قوقل
      gemini_history = [
          {
              "role": "user" if h["role"] == "user" else "model",
              "parts": [h["content"]],
          }
          for h in channel_histories[channel_id][:-1]
      ]

      # بدء الشات وإرسال الرسالة
      chat = model.start_chat(history=gemini_history)
      response = chat.send_message(user_text)
      reply = response.text

      channel_histories[channel_id].append({"role": "model", "content": reply})

      print(f"الرد جاهز: {reply}")
      await message.channel.send(reply)

    except Exception as e:
      print(f"صار خطأ: {e}")
      await message.channel.send("عذرًا، حدث خطأ أثناء معالجة طلبك.")


# تشغيل الفلاسك أولا ثم البوت #
if __name__ == "__main__":
  keep_alive()
  bot.run(os.environ.get("TOKEN"))
