import telebot
import os
from telebot import types
import dbcon as db
from flask import Flask, request


TOKEN = '1251792713:AAH9ysrTdhNnT4mJVqoBbgvUXQ0TJaSPr6A'

bot = telebot.TeleBot(TOKEN)
table = {}

def dialog_volume(curent):
  table.update({curent.pop(0):curent})

def create_kbord():
  keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
  key_yes = types.InlineKeyboardButton(text='create exp card', callback_data='expp') 
  keyboard.add(key_yes) 
  key_no= types.InlineKeyboardButton(text='balanse', callback_data='bal')
  keyboard.add(key_no)
  return keyboard

@bot.message_handler(commands=['start' ,'relogin'])
def start_message(message):
  dialog_volume([message.from_user.id,0,0])
  bot.send_message(message.chat.id, "sand login:")


    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  try:
    
    if table.get(message.from_user.id)[0] == 0:
      dialog_volume([message.from_user.id,1,db.getLogin(str(message.text))])
      bot.send_message(message.from_user.id, "send password")
      return 0 
    
    elif table.get(message.from_user.id)[0] == 1:
      a = db.getPass(table.get(message.from_user.id)[1], str(message.text))

      if a != None:
        dialog_volume([message.from_user.id,2,a])
        question = 'u login succes '
        bot.send_message(message.from_user.id, text=question, reply_markup=create_kbord())
      else :
        dialog_volume([message.from_user.id,0])
        bot.send_message(message.from_user.id, "not user with this credential send LOGIN")
    
    
    elif table.get(message.from_user.id)[0] == 2:
      balanse =  db.getBalance(table.get(message.from_user.id)[1],message.text)
      keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
      key_yes = types.InlineKeyboardButton(text='back to menu', callback_data='back') #кнопка «Да»
      keyboard.add(key_yes)
      bot.send_message(message.from_user.id, text=balanse, reply_markup=keyboard)
    
    elif table.get(message.from_user.id)[0] == 3:
      bot.send_message(message.from_user.id, text='u login succes ', reply_markup=create_kbord());
    
    elif table.get(message.from_user.id)[0] == 4 :
       dialog_volume([message.from_user.id,5,table.get(message.from_user.id)[1],message.text])
       bot.send_message(message.chat.id, "enter date:" )
    
    elif table.get(message.from_user.id)[0] == 5 :
      dialog_volume([message.from_user.id,6,table.get(message.from_user.id)[1],table.get(message.from_user.id)[2],message.text])
      bot.send_message(message.chat.id, "enter description:" )
    
    elif table.get(message.from_user.id)[0] == 6 :
      dialog_volume([message.from_user.id,6,table.get(message.from_user.id)[1],table.get(message.from_user.id)[2],table.get(message.from_user.id)[3],message.text])
      controlChek = "amount:"+str(table.get(message.from_user.id)[2])+" date: "+table.get(message.from_user.id)[3]+" decrp: "+str(table.get(message.from_user.id)[4])
      keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
      key_yes = types.InlineKeyboardButton(text='recreate expense', callback_data='reset') #кнопка «Да»
      keyboard.add(key_yes)
      key_yes = types.InlineKeyboardButton(text='create', callback_data='create')
      keyboard.add(key_yes)
      bot.send_message(message.from_user.id, text=controlChek, reply_markup=keyboard)
 
  except TypeError :
       bot.send_message(message.from_user.id, "u not login enter command /start")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
  try:
    if call.data == "expp":
      dialog_volume([call.message.chat.id,4,table.get(call.message.chat.id)[1]])
      bot.send_message(call.message.chat.id, 'enter amount:');
    elif call.data == "bal":
      dialog_volume([call.message.chat.id,2,table.get(call.message.chat.id)[1]])
      bot.send_message(call.message.chat.id, 'enter date in format YYYY-MM-DD');
    elif call.data == "back":
      dialog_volume([call.message.chat.id,3,table.get(call.message.chat.id)[1]])
      print(call.message.chat.id)
      question = 'u login succes '
      bot.send_message(call.message.chat.id, text=question, reply_markup=create_kbord())
    elif call.data =="reset":
      dialog_volume([call.message.chat.id,4,table.get(call.message.chat.id)[1]])
      bot.send_message(call.message.chat.id, 'enter amount:');
    elif call.data == "create":
      data = table.get(call.message.chat.id)
      getIdMonExp =db.getIdMonthexp(data[1],data[3])
      response = db.cteateExpCard(data[1], data[2],data[4],data[3],getIdMonExp)
      if response != 'exp':
        dialog_volume([call.message.chat.id,3,table.get(call.message.chat.id)[1]])
        bot.send_message(call.message.chat.id, text='u login succes ', reply_markup=create_kbord());
      else :
        dialog_volume([call.message.chat.id,3,table.get(call.message.chat.id)[1]])
        bot.send_message(call.message.chat.id, text='u send uncorect data, try again', reply_markup=create_kbord()); 
  except TypeError:
    bot.send_message(call.message.chat.id, "u not login enter command /start")    

if "HEROKU" in list(os.environ.keys()):
  server = Flask(__name__)
  @server.route('/' + TOKEN, methods=['POST'])
  def getMessage():
      bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
      return "!", 200


  @server.route("/")
  def webhook():
      bot.remove_webhook()
      bot.set_webhook(url='https://intense-badlands-19799.herokuapp.com/' + TOKEN)
      return "!", 200


  if __name__ == "__main__":
      server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

else:
  bot.remove_webhook()
  bot.polling(none_stop=True, interval=0)



