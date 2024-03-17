import mysql.connector

mycon=mysql.connector.connect(host="localhost",user="root",password="sql123",database="bank")

from datetime import *

d=date.today()

from tabulate import tabulate

#Admin function to open account
def open_account():
    global ac
    name=input("enter name")
    ac = input("Enter account number")
    db=input("enter dob")
    add=input("enter address")
    phone=input("enter phone number")
    ob=float(input("enter opening balance"))
    pwd=input("enter password")
    cur=mycon.cursor()
    cur.execute(f'insert into account values("{name}","{ac}","{db}","{add}","{phone}",{ob},"{pwd}")')
    mycon.commit()
    print("account created succesfully")
    if ob>=1000:#minimum opening balance should be 1000
        cur.execute(f'insert into amount values({1},"{ac}","2022/11/03","D",{ob},{ob})')
   

    else:
        print("Insufficient opening balance")
mycon.commit()

    
    

#User function to deposit amount
def depo_amount():
    global ac
    cur=mycon.cursor()
    am=float(input("enter AMount:"))
    cur.execute(f'select max(t_no) from amount where account_number="{ac}"')
    max_tno=cur.fetchall()
    new_tno=max_tno[0][0]+1
    a=max_tno[0][0]
    cur.execute(f'select balance from amount where account_number="{ac}" and t_no ={a}')
    result=cur.fetchall()
    total=result[0][0]+am
    cur.execute(f"insert into amount values({new_tno},'{ac}','{d}','D',{am},{total})")
    mycon.commit()
    print("amount deposited")
    

#user function to withdraw amount from account
def withdrawl():
            global ac
            am=float(input("enter amount to be withdrawn"))
            cur=mycon.cursor()
            cur.execute(f"select max(t_no) from amount where account_number='{ac}'")
            max_tno=cur.fetchall()
            new_tno=max_tno[0][0]+1
            a=max_tno[0][0]
            cur.execute(f'select balance from amount where account_number="{ac}" and t_no ={a}')
            result=cur.fetchall()
            x=result[0][0]-am
            if x>1000:#minimum balance needs to be 1000
                cur.execute(f"insert into amount values({new_tno},'{ac}','{d}','W',{am},{x})")
                print("amount of",am, "withdrawn")
            else:
                print("insufficient balance")
            mycon.commit()


#user function to check account balance            
def balance():
    global ac    
    cur=mycon.cursor()
    cur.execute(f"select max(t_no) from amount where account_number='{ac}'")
    max_tno=cur.fetchall()
    a=max_tno[0][0]
    cur.execute(f'select balance from amount where account_number="{ac}" and t_no ={a}')
    result=cur.fetchall()
    h=["Balance"]
    print(tabulate(result,headers=h,tablefmt="psql"))


 #Admin function to display user details   
def display_details():                    
            cur=mycon.cursor()
            print("1.   All customers")
            print("2.   specific customer")
            ch=input("enter your choice")
            if ch=="1":
                cur.execute(f'select account_number,name,dob,address,phone_number from account')
                h=["account number","name","date of birth","phone number"]
                result=cur.fetchall()
                print(tabulate(result,headers=h,tablefmt="psql"))
            elif ch=="2":
                ac=input("enter account number")
                cur.execute(f'select account_number,name,dob,address,phone_number from account where account_number="{ac}"')
                h=["account number","name","date of birth","phone number"]
                result=cur.fetchall()
                r=cur.rowcount
                if r!=0:
                    print(tabulate(result,headers=h,tablefmt="psql"))
                elif r==0:
                    print("account number doesn't exist")
            else:
                print("invalid choice")
          
#Admin funciton to increase interest           
def interest():
    cur=mycon.cursor()
    cur.execute(f"select account_number,balance from amount")
    result=cur.fetchall()

    cur.execute(f"update amount set balance = balance + (balance * 2/100)")
    mycon.commit()
    print("Interest added")
    

#Admin function to close account
def close_account():
            global ac 
            cur=mycon.cursor()
            cur.execute(f'select * from account where account_number = "{ac}"')
            result=cur.fetchall()
            r=cur.rowcount
            if r!= 0:
                cur.execute(f'delete from amount where account_number = "{ac}"')
                cur.execute(f'delete from account where account_number= "{ac}"')
                mycon.commit()
                print("Account closed successfully")
            else:
                print("Account does not exist")
                

#User function to check their transaction history
def trans_history():
    global ac
    h=["Transaction number","Account number","Transaction date","Transaction type","Transaction amount","Balance"]
    cur=mycon.cursor()
    cur.execute(f'select * from amount where account_number = "{ac}"')
    result=cur.fetchall()
    r=cur.rowcount
    if r != 0:
        print(tabulate(result,headers=h,tablefmt="psql"))
        
    elif r ==0:
        
        print("No transaction history")  


#User function to reset their account password
def reset_password():
    global ac
    cur=mycon.cursor()
    old=input("enter current password")
    cur.execute(f'select pwd from account where account_number="{ac}" ')
    result=cur.fetchall()
    if result[0][0]==old:
        new=input("enter new password")
        new2=input("confirm password")
        if new==new2:
            cur.execute(f'update account set pwd = "{new}"   where account_number = "{ac}"')
            mycon.commit()  
            print("password updated successfully")
        else:
            print("Passwords do not match , please try again")
    else:
        print("Incorrect password, please try again")    


#User menu
def user():
    global ac
    while True:
        print( "=================USER LOGIN==================")        
        ac=input("enter account number")
        print("==============================================")
        cur=mycon.cursor()
        cur.execute(f'select * from account where account_number="{ac}"')
        rec=cur.fetchall()
        r=cur.rowcount
        if r == 0:
            print("invalid account number")
        else:
            pwd=input("enter password:")
            cur=mycon.cursor()
            cur.execute(f'select pwd from account where account_number="{ac}" ')
            result=cur.fetchall()
            if result[0][0]==pwd:
                print("login succesful")
                while True:
                    print("*=========================*")
                    print("******** ABC BANK *********")
                    print("*=========================*")
                    print("* 1. Deposit amount       *")
                    print("* 2. Withdraw amount      *")
                    print("* 3. Balance Enquiry      *")
                    print("* 4. Reset password       *")
                    print("* 5. Change details       *")
                    print("* 6. Transaction history  *")
                    print("* 7. Log out              *")
                    print("===========================")
                    ch = int(input("Enter choice"))
                    if ch == 1:
                        depo_amount()
                    elif ch==2:
                        withdrawl()
                    elif ch ==3:
                        balance()
                    elif ch == 4:
                        reset_password()

                    elif ch == 5:
                        change_details()

                    elif ch == 6:
                        trans_history()
                    elif ch== 7:
                        break                        
                    else:
                        print("Invalid choice , please enter again")
            else:
                print("invalid password")



#User function to change their details
def change_details():
    global ac
    
    cur=mycon.cursor()
    print("1.Change Phone number")
    print("2. Change address")
    ch = int(input("Enter choice"))
    if ch == 1:
        new=int(input("Enter new phone number"))
        cur.execute(f'update account set phone_number = {new} where account_number="{ac}"')
        mycon.commit()
    elif ch == 2:
        address=input("Enter new address")
        cur.execute (f'update account set address="{address}" where account_number = "{ac}"')
        mycon.commit()
        
#Admin menu
def admin():
    global ac
    print("   Admin login")
    Name=input("enter your name")
    pwd=input("enter password")
    cur=mycon.cursor()
    cur.execute(f'select pwd from admin where name="{Name}"')
    result=cur.fetchall()
    r=cur.rowcount
    if r!=0:
        if result[0][0]==pwd:
                    print("login succesful")
                    while True:
                        print("*===================================*")
                        print("*============ABC BANK===============*")
                        print("*    1.Open account                 *")
                        print("*    2.Close account                *")
                        print("*    3.Increase interest            *")
                        print("*    4.Display customer details     *")
                        print("*    5.Log out                      *")
                        print("*===================================*")
                        ch = int(input("Enter choice"))
                        if ch == 1:
                          open_account()  
                        elif ch==2:
                            ac=input("enter account number")
                            close_account()
                        elif ch ==3:
                            interest()
                        elif ch == 4:                            
                            display_details()
                        elif ch==5:
                            break                    
                        else:
                            print("Invalid choice , please enter again")
        else:
            print("invalid password")
    else:
        
        print("invalid username")

#main
def main():
    print("〖 Welcome to ABC Online Banking 〗")
    print("  Please select admin or user")
    while True:
    
        check=input(" A/U  : ")

        if check in "Aa":
            admin()
        elif check in"Uu":
            user()
        else:
            print("invalid choice")
main()
