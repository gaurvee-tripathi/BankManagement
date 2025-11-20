from pathlib import Path
import json
import random
import string
class Bank:
    database='database.json'
    data=[]
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())    #to load not change
        else:
            print("sorry we are facing errorr")

    except Exception as err:
        print(f"error occured as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(cls.data))    #update (dumps)

    @staticmethod    #other can't access
    def __accountno():        
        alpha =random.choices(string.ascii_letters,k=5)
        digits =random.choices(string.digits,k=4)
        id =alpha +digits
        random.shuffle(id)
        return"".join(id)        #to convert any list to string
    def createaccount(self):
        d={
            "name":input("please tell your name:"),
            "email":input("please tell your email:0"),
            "phoneNo.":input("please tell your phoneno.:-"),  
            "pin":int(input("please tell your  4 digit pin:")),
            "Accountno.":Bank.__accountno(),   
            "balance":0
        }
        print(f"please note down your acc no :{d['Accountno.']}")
        if len(str(d['pin'])) != 4:    
            print("please review your pin")
         
        elif len(str(d['phoneNo.'])) != 10:   
            print("please review your account")
        else:
            Bank.data.append(d)
            Bank.__update()
            print(Bank.data)
            
    def deposite_money(self):
        accNo = input("enter your acc no ")
        pin =int(input("enter your pin"))
        user_data =[i for i in Bank.data if i['Accountno.']==accNo and i['pin']==pin]
        print(user)
        if not user_data:
            print("user not found")
        else:
            amount = int(input("enter amount to be deposited"))
            if amount <=0:
                print ("invalid amount")
            elif amount >10000:
                print("greater than 10000")
            else:
                user_data[0]['balance'] +=amount
                Bank.__update()
                print("Amount deposited")
    
    def withdraw_money(self):
        accNo = input("enter your acc no ")
        pin =int(input("enter your pin"))
        user_data =[i for i in Bank.data if i['Accountno.']==accNo and i['pin']==pin]
        if not user_data:
            print("user not found")
        else:
            amount = int(input("enter amount to be withdrawn:"))
            if amount <=0:
                print ("invalid amount")
            elif amount >10000:
                print("greater than 10000")
            else:
                if user_data[0]['balance'] <amount:
                    print("insufficient amount")
                else:
                    user_data[0]['balance'] -=amount
                    Bank.__update()
                    print("Amount credited")
    def show_details(self):
        accNo = input("enter your acc no ")
        pin =int(input("enter your pin"))
        user_data =[i for i in Bank.data if i['Accountno.']==accNo and i['pin']==pin]
        if not user_data:
            print("user not found")
        else:
            for i in user_data[0]:
                print(i,user_data[0][i])

        
    
    def update_details(self):
        accNo = input("enter your acc no ")
        pin =int(input("enter your pin"))
        user_data =[i for i in Bank.data if i['Accountno.']==accNo and i['pin']==pin]
    
        if not user_data:
            print("user not found")
        else:
            print("you cannot change acc no.\n now update your details")
            new_data={
                "name":input("enter your new name:"),
                "email":input("enter new email:"),
                "phoneNo.":input("enter your new phoneno.:-"),  
                "pin":input("please tell your new  4 digit pin:"),
            }
            # the skipped values
            for i in new_data:
                if new_data[i]=="":
                    new_data[i] =user_data[0][i]
            new_data['Accountno.'] = user_data[0]['Accountno.']
            new_data['balance']=user_data[0]['balance']

        
            #we have to update new data to database
            for i in user_data[0]:
                if user_data[0][i] ==new_data[i]:
                    continue
                else:
                    if new_data[i].isnumeric():
                        user_data[0][i] =int(new_data[i])
                    else:
                        user_data[0][i]=new_data[i]

            Bank.__update()
            print("data updated")
            print(user_data)

    def delete_account(self):
        accNo = input("enter your acc no ")
        pin =int(input("enter your pin"))
        user_data =[i for i in Bank.data if i['Accountno.']==accNo and i['pin']==pin]
        if not user_data:
            print("user not found")
        else:
            for i in Bank.data:
                if i['Accountno.']==accNo and i['pin']==pin:
                    Bank.data.remove(i)
            Bank.__update()
            print("data deleted")

    
       
    
user=Bank()                    #instance or object of class
print("press 1 for creating an account")
print("press 2 to deposit money")
print("press 3 for withdraw money")
print("press 4 for details") 
print("press 5 for updating the details")
print("press 6 for deleting an account")

check=int(input("tell your choice:-"))

if check==1:
    user.createaccount ()  #call the object user


if check==2:
    user.deposite_money()


if check ==3:
    user.withdraw_money()


if check==4:
    user.show_details()
   

if check ==5:
    user.update_details()

if check ==6:
    user.delete_account()



    