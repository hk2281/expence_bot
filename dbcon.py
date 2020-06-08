import os
import psycopg2
from datetime import date, datetime 
import calendar
import time

DATABASE_URL = os.environ.get('DATABASE_URL')


print("HOME:", DATABASE_URL) 
def tesst():
   cur.execute("INSERT INTO salesforce.Contact (name, lastname) VALUES (%s, %s);",("kaff","fo",))

def getLogin(name):
   cur.execute("SELECT email FROM salesforce.Contact WHERE email = %s;",(name,))
   a = cur.fetchone()
   print(a)
   return a 
def getPass(login , pas):
   cur.execute("SELECT sfid FROM salesforce.Contact WHERE email = %s AND password__c = %s ;",(login,pas,))
   a = cur.fetchone()
   print(a)
   return a 
def getd(strdate):
   date = datetime.strptime(strdate, '%Y-%m-%d')
   first_day = date.replace(day = 1)
   last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
   return first_day.date().strftime('%Y-%m-%d'), last_day.date().strftime('%Y-%m-%d')

def getBalance(keeper , date):
   try:
      range_d  = getd(date)
      cur.execute("""SELECT balance__c FROM salesforce.Monthly_Expense__c WHERE keeper__c = %s 
                     AND month_date__c > %s AND month_date__c < %s;""",(keeper,range_d[0],range_d[1],))
      a = cur.fetchone()
      print('balanse',a)
      if a == None:
         a = '0'
      return a
   except BaseException:
      return 'uncorect date, try again'  


def createMonExp(keeper_x, date_x):
   try:
      cur.execute("""INSERT INTO salesforce.Monthly_Expense__c (keeper__c, month_date__c ,balance__c)
                     VALUES (%s, %s, %s) RETURNING id;""",
                     (keeper_x,date_x,"0",))
      conn.commit()
      return cur.fetchone()[0]
   except BaseException:
      return  'uncorect date, try again'  

def getIdMonthexp(keeper, date):
   try:
      range_d  = getd(date)
      print(range_d)
      cur.execute("""SELECT id FROM salesforce.Monthly_Expense__c WHERE keeper__c = %s
                     AND month_date__c > %s
                     AND month_date__c < %s;""",
                     (keeper,range_d[0],range_d[1],))
      a = cur.fetchone()
      if a == None:
         a = (createMonExp(keeper,date))
      time.sleep(6)    
      return a
   except BaseException:
      return 'uncorect date, try again'

def cteateExpCard(cardkeeper,amount,decrp,date,mon_id):
   try:
      cur.execute("SELECT sfid FROM salesforce.monthly_expense__c WHERE id = %s;",(mon_id,))
      fullid = cur.fetchone()[0]
      print(fullid)
      cur.execute("""INSERT INTO salesforce.expense_card__c 
                     (card_keeper__c,amount__c,description__c,card_date__c ,monthly_expense__c)
                     VALUES (%s, %s, %s, %s,%s);""",
                     (cardkeeper,amount,decrp,date,fullid,))
      conn.commit()
      return 'ok'
   except BaseException:
      return 'exp' 
def te(did):
   cur.execute("""SELECT name FROM salesforce.expense_card__c 
                  WHERE monthly_expense__c = (SELECT sfid FROM salesforce.monthly_expense__c WHERE id = %s);""",
                  (did,))
   print(cur.fetchone())

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()





# a = getLogin ("1@f.c")
# if getPass(a, "1234")==None:
#    print('fi')


 
#conn.commit()



