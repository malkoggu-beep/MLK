import os
from flask import Flask
from threading import Thread
import discord
from groq import Groq

# إعداد خادم فلاسك عشان ريندر ما يقفل البوت
app = Flask('')


@app.route('/')
def home():
  return 'I am alive!'


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


# تعريف مفاتيح الاتصال
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# تخزين محادثات القنوات
channel_histories = {}

SYSTEM_INSTRUCTION = """
- معلومات الشخصية الأساسية:
- الاسم: MLK
- الجنس: ولد
- الوظيفة: خادم وسيرفر ديسبورد الرسمي
- اللهجة: عامية سعودية قريبة للقلب وبدون رسميات -

- الطباع والأسلوب:
- مرح، خارف دم، وذكي في تعليقاته وضحكته -
- متزن في ردوده ويعرف كيف يمون على الأعضاء -
- راقي في أسلوبه وما يحب اللف والدوران -
- كلامه مختصر ومفيد وما يتعدى الحاجة -

- قواعد التفاعل والردود:
- يرد على الأسئلة بمثلها وبطريقة ذكية تعكس شخصيته -
- يكلم الأعضاء بميانة تامة وكأنهم خوياه -
- إذا ضحك أحد الأعضاء يعرف يرد -
- يثبت وجوده كخادم للسيرفر بروحه الطيبة وفزعته -
"""


@bot.event
async def on_ready():
  print(f'البروت شغال ومتصل باسم {bot.user}')


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if bot.user.mentioned_in(message):
    try:
      user_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
      print(f'وصلني سؤال: {user_text}')

      channel_id = message.channel.id

      if channel_id not in channel_histories:
        channel_histories[channel_id] = [
            {'role': 'system', 'content': SYSTEM_INSTRUCTION}
        ]

      channel_histories[channel_id].append({'role': 'user', 'content': user_text})

      if len(channel_histories[channel_id]) > 11:
        channel_histories[channel_id].pop(1)

      chat_completion = client.chat.completions.create(
          messages=channel_histories[channel_id],
          model='llama-3.3-70b-versatile',
          temperature=0.3,
      )

      reply = chat_completion.choices[0].message.content

      channel_histories[channel_id].append(
          {'role': 'assistant', 'content': reply}
      )

      print(f'الرد جاهز: {reply}')
      await message.channel.send(reply)

    except Exception as e:
      print(f'صار خطأ: {e}')
      await message.channel.send(f'خطأ تقني {e}')


# تشغيل الفلاسك أولا ثم البوت
if __name__ == '__main__':
  keep_alive()
  bot.run(os.environ.get('TOKEN'))
