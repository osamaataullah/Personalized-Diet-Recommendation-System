from pyrebase import pyrebase
import pandas as pd
from flask import Flask, flash, redirect, render_template,json, request, session, abort, url_for, current_app as curr_app
from flask_session import Session
import random
import os
from collections import defaultdict

app = Flask(__name__)   
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# config = {
#   'apiKey': "AIzaSyAeviXJXuLFRf74WG6stRXKxFDPj4rLAUc",
#   'authDomain': "mealrecommendations.firebaseapp.com",
#   'databaseURL': "https://mealrecommendations-default-rtdb.firebaseio.com",
#   'projectId': "mealrecommendations",
#   'storageBucket': "mealrecommendations.appspot.com",
#   'messagingSenderId': "736279978024",
#   'appId': "1:736279978024:web:b2ea7700c1331187d1151d"
# }
# filename = os.path.join(app.static_folder,'data','Final_File_1.json')
# with open(filename) as test_file:
#     data = json.load(test_file)

# # print(data)
# merged_df = pd.io.json.json_normalize(data, 'data')
# # print(df)
# merged_df.set_axis(["url", "img_url", "ingredients","region","recipe_id","recipe_title","calories"],
#                     axis=1,inplace=True)
# print(df)
# merged_df=pd.read_json(app.static_folder+'/data'+'/Final_File.json', orient ='split', compression = 'infer')
# print(merged_df)



config ={
    'apiKey': "AIzaSyCpmBU-uDvjohUBYLc8yH0g20uCeA7c0iI",
    'authDomain': "mealplanner-6d132.firebaseapp.com",
    'databaseURL': "https://mealplanner-6d132-default-rtdb.firebaseio.com/",
    'projectId': "mealplanner-6d132",
    'storageBucket': "mealplanner-6d132.appspot.com",
    'messagingSenderId': "675310218180",
    'appId': "1:675310218180:web:2427a4790d96925504d291",
    'measurementId': "G-BDFBYNFC0H"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
userInfo ={"height":"", "weight":"","cuisine":"", "activity_level":"", "allergies":""}

def take_input():
  cuisuine_name = userInfo["cuisine"]
  ref = db.child('users').get(person["uid"])
#   age  = int(ref["age"])
  age= 20
  height = int(userInfo["height"])
  weight = int(userInfo["weight"])
#   gender = ref["gender"]
  gender = "Male"
#   print('Enter Activity Level:\n')
#   print('1. Sedentary\n2.Lightly active\n3. Moderately Active\n4.Very Active\n5.Extra Active\n')
  activity_level = userInfo["activity_level"]

#   print('Enter any allergy with food ingredient:\n')
  allergy = []
  allergy.append(userInfo["allergies"])

  calorie=0
  if(gender == 'male'):
      bmr = 66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age)
  else:
      bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
  if(activity_level=="Sedentary"):
      calorie=bmr*1.2
  elif(activity_level=="Lightly active"):
      calorie=bmr*1.375
  elif(activity_level=="Moderately Active"):
      calorie=bmr*1.55
  elif(activity_level=="Very Active"):
      calorie=bmr*1.725
  else:
      calorie=bmr*1.9

  if(userInfo["breakfast"]== "Light"):
    breakfast=0
  else:
    breakfast=1    


  if(userInfo["lunch"]== "Light"):
        lunch=0
  else:
        lunch=1

  
  if(userInfo["dinner"]== "Light"):
        dinner=0
  else:
        dinner=1

  breakfast_cal=0
  lunch_cal=0
  dinner_cal=0
  target=calorie

  if((breakfast==1 and lunch ==1 and dinner ==1) or (breakfast==0 and lunch==0 and dinner==0)):#if all three are equal
    breakfast_cal=int(target/3)
    lunch_cal=int(target/3)
    dinner_cal=int(target/3)
  elif(breakfast==0 and lunch==0):#if breakfast and lunch are light
    breakfast_cal=int(target*0.25)
    lunch_cal=int(target*0.25)
    dinner_cal=int(target*0.5)
  elif(breakfast==0 and dinner==0):#if breakfast and dinner are light
    breakfast_cal=int(target*0.25)
    lunch_cal=int(target*0.5)
    dinner_cal=int(target*0.25)
  elif(lunch==0 and dinner==0):#if lunch and dinner are light
    breakfast_cal=int(target*0.5)
    lunch_cal=int(target*0.25)
    dinner_cal=int(target*0.25)
  elif(breakfast==1 and lunch==1):#if breakfast and lunch are heavy
    breakfast_cal=int(target*0.4)
    lunch_cal=int(target*0.4)
    dinner_cal=int(target*0.2)
  elif(breakfast==1 and dinner==1):#if breakfast and dinner are heavy
    breakfast_cal=int(target*0.4)
    lunch_cal=int(target*0.2)
    dinner_cal=int(target*0.4)
  elif(lunch==1 and dinner==1):
    breakfast_cal=int(target*0.2)#if lunch and dinner are heavy
    lunch_cal=int(target*0.4)
    dinner_cal=int(target*0.4)
  
  return cuisuine_name,breakfast_cal,lunch_cal,dinner_cal,allergy


def create_dictionary(merged_df,cuisuine_name):
  merged_df=merged_df.loc[merged_df['region'] == cuisuine_name]
  data_dict = defaultdict(list)
  for index, row in merged_df.iterrows():
    data_dict[row['calories']].append(row['recipe_title'])
  calorie_list=merged_df['calories'].tolist()
  calorie_list=list(set(calorie_list))
  return calorie_list,data_dict,merged_df

def select_recipe(full_list1a,full_list2a,full_list3a,full_list4a):
  final_recommend=list()
  count=0
  if len(full_list1a) != 0:
    final_recommend.append(random.choice(full_list1a))
    count=count+1
  if len(full_list2a) != 0:
    final_recommend.append(random.choice(full_list2a))
    count=count+1
  if len(full_list3a) != 0:
    final_recommend.append(random.choice(full_list3a))
    count=count+1
  if len(full_list4a) !=0:
    final_recommend.append(random.choice(full_list4a))
    count=count+1
  
  while (count<4):
    big_list=full_list1a+full_list2a+full_list3a+full_list4a
    final_recommend.append(random.choice(big_list))
    count=count+1
  
  return final_recommend

# def display(list_of_lists,data_dict):
#   for list1 in list_of_lists:
#     for x in list1:
#       print(data_dict[x][0])
#     print('\n\n\n')

def recommend(arr,target):

  #list of two combinations
  list2=list()
  list3=list()
  list4=list()
  list5=list()

  for x in range(0,len(arr)):
      if(len(list2)>30):
        break
      for y in range(x,len(arr)):
        if(len(list2)>30):
          break
        if arr[x]+arr[y]==target and x!=y :
          temp=list()
          temp.append(arr[x])
          temp.append(arr[y])
          list2.append(temp)
  
  #combinations of three
  for x in range(0,len(arr)):
    if(len(list3)>30):
      break
    if(arr[x]>target):
      continue
    for y in range(x,len(arr)):
      if(len(list3)>30):
        break
      if(arr[x]+arr[y]>target):
        continue
      for z in range(y,len(arr)):
        if(len(list3)>30):
          break
        if(arr[x]+arr[y]+arr[z]>target):
          continue
        if arr[x]+arr[y]+arr[z]==target and x!=y and x!=z and y!=z :
          temp=list()
          temp.append(arr[x])
          temp.append(arr[y])
          temp.append(arr[z])
          x=x+1
          y=y+1
          z=z+1
          list3.append(temp)

  #combinations of four
  for x in range(0,len(arr)-3):
    if(len(list4)>30):
      break
    if(arr[x]>target):
      continue
    for y in range(x+1,len(arr)):
      if(len(list4)>30):
        break
      if(arr[x]+arr[y]>target):
        continue
      for z in range(y+1,len(arr)):
        if(len(list4)>30):
          break
        if(arr[x]+arr[y]+arr[z]>target):
          continue
        for a in range(z+1,len(arr)):
          if(len(list4)>30):
            break
          if(arr[x]+arr[y]+arr[z]+arr[a]>target):
            continue
          if arr[x]+arr[y]+arr[z]+arr[a]==target:
            temp=list()
            temp.append(arr[x])
            temp.append(arr[y])
            temp.append(arr[z])
            temp.append(arr[a])
            x=x+1
            y=y+1
            z=z+1
            a=a+1
            list4.append(temp)

  #combinations of five
  for x in range(0,len(arr)):
    if(len(list5)>30):
      break
    if(arr[x]>target):
      continue
    for y in range(x+1,len(arr)):
      if(len(list5)>30):
        break
      if(arr[x]+arr[y]>target):
        continue
      for z in range(y+1,len(arr)):
        if(len(list5)>30):
          break
        if(arr[x]+arr[y]+arr[z]>target):
          continue
        for a in range(z+1,len(arr)):
          if(len(list5)>30):
            break
          if(arr[x]+arr[y]+arr[z]+arr[a]>target):
            continue
          for b in range(a,len(arr)):
            if arr[x]+arr[y]+arr[z]+arr[a]+arr[b]==target:
              temp=list()
              temp.append(arr[x])
              temp.append(arr[y])
              temp.append(arr[z])
              temp.append(arr[a])
              temp.append(arr[b])
              x=x+1
              y=y+1
              z=z+1
              a=a+1
              b=b+1
              list5.append(temp)

  return list2,list3,list4,list5

def filter_allergies(l1,l2,l3,l4,data_dict,allergy,merged_df):
  full_list1=list()
  full_list2=list()
  full_list3=list()
  full_list4=list()

  for x in l1:
    i1=merged_df.loc[merged_df['recipe_title'] == data_dict[x[0]][0], 'ingredients'].iloc[0]
    i2=merged_df.loc[merged_df['recipe_title'] == data_dict[x[1]][0], 'ingredients'].iloc[0]
    full_ingre=i1+i2
    counter=0
    for y in full_ingre:
      if y in allergy:
        counter=counter+1
    if(counter == 0):
      full_list1.append(x)

  for x in l2:
    i1=merged_df.loc[merged_df['recipe_title'] == data_dict[x[0]][0], 'ingredients'].iloc[0]
    i2=merged_df.loc[merged_df['recipe_title'] == data_dict[x[1]][0], 'ingredients'].iloc[0]
    i3=merged_df.loc[merged_df['recipe_title'] == data_dict[x[2]][0], 'ingredients'].iloc[0]
    full_ingre=i1+i2+i3
    counter=0
    for y in full_ingre:
      if y in allergy:
        counter=counter+1
    if(counter == 0):
      full_list2.append(x)

  for x in l3:
    i1=merged_df.loc[merged_df['recipe_title'] == data_dict[x[0]][0], 'ingredients'].iloc[0]
    i2=merged_df.loc[merged_df['recipe_title'] == data_dict[x[1]][0], 'ingredients'].iloc[0]
    i3=merged_df.loc[merged_df['recipe_title'] == data_dict[x[2]][0], 'ingredients'].iloc[0]
    i4=merged_df.loc[merged_df['recipe_title'] == data_dict[x[3]][0], 'ingredients'].iloc[0]
    full_ingre=i1+i2+i3+i4
    counter=0
    for y in full_ingre:
      if y in allergy:
        counter=counter+1
    if(counter == 0):
      full_list3.append(x)
  
  for x in l4:
    i1=merged_df.loc[merged_df['recipe_title'] == data_dict[x[0]][0], 'ingredients'].iloc[0]
    i2=merged_df.loc[merged_df['recipe_title'] == data_dict[x[1]][0], 'ingredients'].iloc[0]
    i3=merged_df.loc[merged_df['recipe_title'] == data_dict[x[2]][0], 'ingredients'].iloc[0]
    i4=merged_df.loc[merged_df['recipe_title'] == data_dict[x[3]][0], 'ingredients'].iloc[0]
    i5=merged_df.loc[merged_df['recipe_title'] == data_dict[x[4]][0], 'ingredients'].iloc[0]
    full_ingre=i1+i2+i3+i4+i5
    counter=0
    for y in full_ingre:
      if y in allergy:
        counter=counter+1
    if(counter == 0):
      full_list4.append(x)

  return full_list1,full_list2,full_list3,full_list4

def read_data():
    filename = os.path.join(app.static_folder,'data','Final_File_1.json')
    with open(filename) as test_file:
        data = json.load(test_file)
    # print(data)
    merged_df = pd.io.json.json_normalize(data, 'data')
    # print(df)
    merged_df.set_axis(["url", "img_url", "ingredients","region","recipe_id","recipe_title","calories"],axis=1,inplace=True)
    return merged_df


def main_function():
  merged_df=read_data()
  cuisuine_name,breakfast_cal,lunch_cal,dinner_cal,allergy=take_input()
  calorie_list,data_dict,merged_df=create_dictionary(merged_df,cuisuine_name)
  lista1,lista2,lista3,lista4 = recommend(calorie_list,breakfast_cal)
  listb1,listb2,listb3,listb4 = recommend(calorie_list,lunch_cal)
  listc1,listc2,listc3,listc4 = recommend(calorie_list,dinner_cal)
  full_list1a,full_list2a,full_list3a,full_list4a = filter_allergies(lista1,lista2,lista3,lista4,data_dict,allergy,merged_df)
  full_list1b,full_list2b,full_list3b,full_list4b = filter_allergies(listb1,listb2,listb3,listb4,data_dict,allergy,merged_df)
  full_list1c,full_list2c,full_list3c,full_list4c = filter_allergies(listc1,listc2,listc3,listc4,data_dict,allergy,merged_df)
  breakfast=select_recipe(full_list1a,full_list2a,full_list3a,full_list4a)
  lunch=select_recipe(full_list1b,full_list2b,full_list3b,full_list4b)
  dinner=select_recipe(full_list1c,full_list2c,full_list3c,full_list4c)
#   display(breakfast,data_dict)
#   display(lunch,data_dict)
#   display(dinner,data_dict)
  return breakfast, lunch, dinner,data_dict

@app.route("/")
def index():
    # return render_template("index.html")
    return render_template("tempLogin.html")

@app.route("/signup")
def signup():
    return render_template("signup2.html")

@app.route("/forgot_pass")
def forgot_pass():
    return render_template("forgot_pass.html")

@app.route("/index")
def login():
    return render_template("tempLogin.html")

# @app.route("/signup")
# def signup():
#     return render_template("signup.html")

@app.route("/meals")
def meals():
    return render_template("result.html")

@app.route("/add_details")
def add_details():
    return render_template("details.html")

@app.route("/add_details_page",methods=["POST","GET"])
def add_details_page():
    if request.method == "POST":
        try:
            result = request.form
            height = result["height"]
            weight = result["weight"]
            cs_pref = result["cs_pref"]
            allergies = result["allergies"]
            activity_level= result["activity_level"]
            global userInfo
            userInfo['height'] = height
            userInfo['weight'] = weight  
            userInfo['cuisine'] = cs_pref  
            userInfo['activity_level'] = activity_level
            userInfo['allergies']  = allergies
            return render_template("details_page.html") 
        except:
            return redirect(url_for('welcome'))

@app.route("/add_final",methods=["POST","GET"])
def add_final():
    if request.method == "POST":
        try:
            result = request.form
            breakfast = result["breakfast"]
            lunch=  result["lunch"]
            dinner= result["dinner"]
            global userInfo
            userInfo["breakfast"]= breakfast
            userInfo["lunch"]= lunch
            userInfo["dinner"] = dinner
            breakfast,lunch,dinner,data_dict = main_function()
            breakfast_name=list()
            lunch_name=list()
            dinner_name=list()

            for meal in breakfast:
              temp=""
              count=0
              for recipe in meal:
                if(count>0):
                  temp=temp+","+data_dict[recipe][0]
                else:
                  temp=temp+data_dict[recipe][0]
                count=count+1
              breakfast_name.append(temp)
            
            for meal in lunch:
              temp=""
              count=0
              for recipe in meal:
                if(count>0):
                  temp=temp+","+data_dict[recipe][0]
                else:
                  temp=temp+data_dict[recipe][0]
                count=count+1
              lunch_name.append(temp)

            for meal in dinner:
              temp=""
              count=0
              for recipe in meal:
                if(count>0):
                  temp=temp+","+data_dict[recipe][0]
                else:
                  temp=temp+data_dict[recipe][0]
                count=count+1
              dinner_name.append(temp)
              
            data =[]
            data.append(breakfast_name)
            data.append(lunch_name)
            data.append(dinner_name)

            return render_template("result.html", data=data)
        except:
            return redirect(url_for('welcome'))    

@app.route("/welcome")
def welcome():
    if (person["is_logged_in"] == True) or (session.get("name")):
        # return render_template("welcome.html", email = person["email"], name = person["name"])
        return render_template("homepage.html")
    else:
        return redirect('/')

@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        
        result = request.form          
        email = result["email"]
        password = result["pass"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            session["name"]= person["name"]
            return redirect(url_for('welcome'))
        except:
            return redirect('/')
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect('/')


@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":       
        result = request.form           
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        age = result["age"]
        gender= result["gender"]
        try:
           
            user = auth.create_user_with_email_and_password(email, password)
            user2 = auth.sign_in_with_email_and_password(email, password)
            
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            session["name"]= name
            data = {"name": name, "email": email, "age":age,"gender":gender}
            db.child("users").child(person["uid"]).set(data)
            auth.send_email_verification(user["idToken"])  

            if(person['uid'] != None) :
                return redirect(url_for('welcome'))
        
            #return redirect(url_for('welcome'))
        except:
            exist_msg = "This email already exists"
            return render_template("signup2.html",exist_message=exist_msg)

    else:
        if person["is_logged_in"] == True or session.get("name"):
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('signup'))

@app.route("/forgot_password", methods=["POST","GET"])
def forgot_password():  
    if request.method == "POST":
        try:
            email = request.form["email"]
            auth.send_password_reset_email(email)
            return redirect('/')
        except:
            print("Exception")
            return redirect('/')    


@app.route("/logout")
def logout():
    person.clear()
    session['name']= None
    return redirect('/')           

if __name__ == "__main__":
    app.run()

