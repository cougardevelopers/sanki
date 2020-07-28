import kivy
kivy.require("1.9.1") 
import re
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget 
from datetime import datetime
from kivy.uix.button import Button 
kivy.require('1.9.0')
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from random import seed
from random import randint
from random import sample
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pathlib
import os
import json
from kivy.clock import Clock


Config.set('graphics','resizeable', True)
def get_sank():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_name='test-4814ee794374.json'

    fname=os.path.join(dir_path,json_name)
    scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(fname, scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    
    sheet = client.open("Sankitest").sheet1
    # Extract and print all of the values
    sank = sheet.get_all_records()
    sank_len=len(sank)
    lst_quo=list()
    lst_date=list()
    lst_final=list()
    d_quo=dict()
    d_date=dict()
    for dic in sank:
        k=dic.get('Number')
        val=dic.get('Quote')
        date=dic.get('Date')
        # print(k)
        d_quo[k]=val
        d_date[k]=date
    # print(d_quo)
    for num,quote in d_quo.items():
        lst_quo.append(quote)
    for num,date in d_date.items():
        lst_date.append(date)
    for i in range(0,len(lst_quo)):
        tup=(lst_date[i],lst_quo[i])
        lst_final.append(tup)
    return lst_quo,lst_date,lst_final,sank_len,sheet

class MainWindow(Screen):
    def set_text(self):    
        _,_,lst_final,sank_len,_=get_sank()
        lst_gen=lst_final
        sank_gen=sank_len
        value=randint(1,sank_gen)
        for date, quo in lst_gen[value-1:value]:
            my_label=quo
            my_date=date
        # print(len(lst))
        my_label=self.ids.my_label
        my_label.text=quo
        my_label2=self.ids.my_label2
        my_label2.text=""
        my_date=self.ids.my_date
        my_date.text=date
    def set_story(self):
        lst_quo,_,_,sank_len,_=get_sank()
        lst_sto=lst_quo
        sank_sto=sank_len
        value1, value2, value3= random.sample(range(1,sank_sto),3)
        # print(value1,value2,value3)
        d_var=dict()
        d_var[1]=value1
        d_var[2]=value2
        d_var[3]=value3
        d_s=dict()
        i=1
        x=(1,2,3)
        for i in x:
            for quo in lst_sto[:d_var[i]]:            
                d_s[i]=quo
        # print(d_s)
        story1=self.ids.my_label
        story1.text=str(d_s.get(1))
        story2=self.ids.my_label2
        story2.text=str(d_s.get(2))
        my_date=self.ids.my_date
        my_date.text=str(d_s.get(3))
    
class Contribute(Screen):
    uquote=ObjectProperty(None)
    udate=ObjectProperty(None)
    # num=ObjectProperty(None)
    def set_submit(self):
        _,_,lst_final,sank_len,sheet=get_sank()
        lst_sub=lst_final
        self.sank_sub=sank_len
        self.sheet_sub=sheet
        self.index=self.sank_sub+2
        num_quo=self.ids.num
        num_quo.text=str(self.sank_sub)
        # #User to enter values in the sheet
        self.squote=self.uquote.text
        self.sdate=self.udate.text
        for date,quo in lst_sub:
            if self.squote==quo:
                self.squote=""
                self.sdate=""
            else:
                continue
        self.callback='Thankyou!'
        self.popup=Popup(title='',
                    content=Label(text=self.callback),
                    size_hint=(None,None), size=(400,400),auto_dismiss=False)
        self.popup.open()
        self.event=Clock.schedule_once(self.sub_popup,2)
        self.event=Clock.schedule_once(self.popup.dismiss,10)
        self.uquote.text=""
    def sub_popup(self,dt):
        self.popup.content=Label(text=self.callback)
        
        if self.squote!="":
            for i in range(50):
                row=[self.sank_sub+i+1,self.sdate,self.squote]
                # print(row)
                self.sheet_sub.insert_row(row, self.index)
                self.popup.content=Label(text="Added!")
                # correct=True
                # print("submitted")
                i=i+1
                break
        else:
            # print("Already exists")
            self.popup.content=Label(text="Someone added before\nTry adding another quote")            
            # correct=False        

class ManagerWindow(ScreenManager):
    pass

kv = Builder.load_file("test.kv")

sm = ManagerWindow()
screens = [MainWindow(name="main"), Contribute(name="contribute")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

class Sankiquotes(App):
    
   def build(self):
        return sm
#    pass
 
if __name__=="__main__":
    Sankiquotes().run()
