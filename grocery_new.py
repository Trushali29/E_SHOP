import customtkinter
from customtkinter import StringVar,IntVar
from tkcalendar import DateEntry
import sqlite3  as db
from PIL import Image,ImageTk
import tkinter
from CTkMessagebox import CTkMessagebox
import random
import subprocess

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

master = customtkinter.CTk()
master.geometry("1520x820")
master.title("Grocery Management System")
master.resizable(False,False)

def establishconnect():
    connectobject = db.connect("GroceryManagement.db")
    c = connectobject.cursor()
    product_table = '''
    create table if not exists products (
        pid string,
        date string,
        product string,
        price number,
        quantity number
        )
    '''

    c.execute(product_table)
    
    connectobject.commit()   

establishconnect()

# SET THE BACKGROUND IMAGE
Main_frame = customtkinter.CTkFrame(master, width=1920 , height = 1080)
Main_Image = customtkinter.CTkImage(Image.open("img.jpg"),size=(1920, 1080))
Main_Label = customtkinter.CTkLabel(master,text="",image=Main_Image)
Main_Label.place(relx = 0.5 ,rely = 0.5,anchor=customtkinter.CENTER)

# SET THE TABS VIEW FOR STOCK AND SELL
tabview = customtkinter.CTkTabview(master,height = 800, width = 800,fg_color = "SandyBrown",border_color = "SandyBrown")
tabview.grid(row = 0, column = 1,padx = 650,pady = 13)
    
stockview = tabview.add("Stock")  # add tab at the end
sellview = tabview.add("Sell")  # add tab at the end
stockview = tabview.set("Stock")  # set currently visible tab


# SET THE STOCK TAB VIEW FOR ADD UPDATE AND DELETE OF PRODUCTS
# SET THE LABLES FOR THE STOCK 
dateL=customtkinter.CTkLabel(tabview.tab("Stock"),text="Date",width=12,font=('arial',18,'bold'))
dateL.grid(row=1,column=1,padx=15, pady=15)

product_label=customtkinter.CTkLabel(tabview.tab("Stock"), text="Product",font=('arial',18,'bold'),width=12)
product_label.grid(row=2,column=1,padx=15, pady=15)

price_label=customtkinter.CTkLabel(tabview.tab("Stock"), text="Price",font=('arial',18,'bold'),width=12)
price_label.grid(row=3,column=1,padx=15, pady=15)

quantity_label=customtkinter.CTkLabel(tabview.tab("Stock"), text="Quantity",font=('arial',18,'bold'),width=12)
quantity_label.grid(row=4,column=1, padx=15, pady=15)

# SET THE ENTER FOR THE STOCK
name=StringVar()
price=StringVar()
quantity=StringVar()

dateE2=DateEntry(tabview.tab("Stock"),width=12,font=('arial',15,'bold'))
dateE2.grid(row=1,column=2, padx=15, pady=15)

Name=customtkinter.CTkEntry(tabview.tab("Stock"),textvariable=name,font=('arial',18,'bold'),width=155)
Name.grid(row=2,column=2, padx=15, pady=15)

Price=customtkinter.CTkEntry(tabview.tab("Stock"),textvariable=price,font=('arial',18,'bold'),width=155)
Price.grid(row=3,column=2, padx=15, pady=15)

Quantity=customtkinter.CTkEntry(tabview.tab("Stock"),textvariable=quantity,font=('arial',18,'bold'),width=155)
Quantity.grid(row=4,column=2, padx=15, pady=15)

product_names = list()
def add_stock():
    if len(dateE2.get()) == 0 or quantity.get() == " " or name.get() == " " or price.get() == " ":
        CTkMessagebox(title="Warning Message!", message="All fields are required!!",icon="warning")
    else:

        product_id = random.randint(111, 999)

        connectobject = db.connect("GroceryManagement.db")
        c = connectobject.cursor()

        sql = '''INSERT INTO products VALUES(?, ?, ?, ?,?)'''

        c.execute(sql,("P"+str(product_id),dateE2.get(),name.get(),int(price.get()),int(quantity.get())))
        connectobject.commit()

        CTkMessagebox(title="Info", message="product added successfully")

        update_options_products()

def update_options_products():
    # to update the combox product list
    result = subprocess.run(['node', 'product_sell.js'], capture_output=True)
    global product_names
    # TO REMOVE EMPTY SPACE AND NEW LINES THEN ADD THE PRODUCTS IN COMBO BOX
    product_names = result.stdout.decode('utf-8').strip().split("\n")
    #print(product_names)
    # to update every time the new product comes
    combobox.configure(values = product_names)
    

def viewingStock():
    update_options_products()
    # delete all text inside textbox
    view_stock.delete("0.0", "end")
    
    connectobject = db.connect("GroceryManagement.db")
    c = connectobject.cursor()  

    sql = 'Select * from products'
    c.execute(sql)

    rows=c.fetchall()
    for i in rows:
        allrows="" 
        for j in i:
            allrows+=str(j)+'\t  '
        allrows+='\n'
        view_stock.insert("0.0",allrows)
    view_stock.insert("0.0", f"ProductID\t   Date\t  Product\t  Price\t  Quantity\t \n")

   
# SET CRUD BUTTONS
view_stock_btn=customtkinter.CTkButton(tabview.tab("Stock"),text="View Stock",
font=('arial',18,'bold'),width=20,command = viewingStock)
view_stock_btn.grid(row=6,column=2,padx=15,pady=15)

add_product=customtkinter.CTkButton(tabview.tab("Stock"),text="Add product",font=('arial',18,'bold'),width=20,command = add_stock)
add_product.grid(row=6,column=3,padx=15,pady=15)

view_stock=customtkinter.CTkTextbox(tabview.tab("Stock"),font=('arial',14),width = 400 ,height = 400)
view_stock.grid(row=7,column=2)


# SET THE SELLING TABVIEW
product_label=customtkinter.CTkLabel(tabview.tab("Sell"), text="Product",font=('arial',18,'bold'),width=12)
product_label.grid(row=2,column=1,padx=15, pady=15)


def set_price(name):
    result = subprocess.run(['node', 'price_sell.js', name], capture_output=True)
    value = result.stdout.decode('utf-8').strip()
    # CLEAR THE PRICE THEN INSERT NEW PRICE
    Price.delete(0,customtkinter.END)
    Price.insert(0,str(value))

def add_sell():
     if Price.get() == "" or combobox.get() == "" or Quantity.get() == "" or cust_name.get() == "":
         CTkMessagebox(title="Warning Message!", message="All fields are required!!",icon="warning")
     else:
        result = subprocess.run(['node', 'add_sell.js', combobox.get(),Price.get(),Quantity.get(),cust_name.get()], capture_output=True)
        print(result.stdout.decode('utf-8').strip())
        CTkMessagebox(title="Info", message="product added successfully")

def view_sell():
    # delete all text inside textbox
    view_sell.delete("0.0", "end")
    
    connectobject = db.connect("GroceryManagement.db")
    c = connectobject.cursor()
    product_table = '''
    create table if not exists sell (
        id string,
        customer string,
        date string,
        product string,
        price number,
        quantity number
        )
    '''
    c.execute(product_table)

    result = subprocess.run(['node', 'view_sell.js'], capture_output=True)
    sell_id,customer,date,product,price,quantity = result.stdout.decode('utf-8').strip().split("\n")
    sell_id = sell_id.split(",")
    customer = customer.split(",")
    date = date.split(",")
    product = product.split(",")
    price = price.split(",")
    quantity = quantity.split(",")
    view_sell.insert("0.0", f"Sell_ID\t  Customer\t   Date\t    Product\t   Price\t  Quantity\t \n")
    for i in range(len(sell_id)):
        view_sell.insert("end",sell_id[i]+"\t  "+customer[i]+"\t   "+date[i]+"\t  "+product[i]+"\t   "+price[i]+"\t  "+quantity[i]+"\t \n")


def show_bill():
    new_window = customtkinter.CTkToplevel(master)
    new_window.geometry("300x180")
    new_window.title("search bill")
    new_window.resizable(False,False)

    global cust_name_new_win, dateE2_new_win
      
    cust_name_new_win_label=customtkinter.CTkLabel(new_window, text="Customer name",font=('arial',12,'bold'),width=12)
    cust_name_new_win_label.grid(row=0,column=1,padx=15, pady=15)

    cust_name_new_win=customtkinter.CTkEntry(new_window, textvariable="",font=('arial',12,'bold'),width=150)
    cust_name_new_win.grid(row=0,column=2, padx=15, pady=15)

    dateL_new_win=customtkinter.CTkLabel(new_window,text="Date",width=12,font=('arial',12,'bold'))
    dateL_new_win.grid(row=1,column=1)
    
    dateE2_new_win=DateEntry(new_window,width=12,font=('arial',12,'bold'))
    dateE2_new_win.grid(row=1,column=2)
    
    search_product_btn=customtkinter.CTkButton(new_window,text="search",font=('arial',12,'bold'),width=90,command = billing)
    search_product_btn.place(relx=0.5, rely=0.6,anchor=tkinter.CENTER)

def billing():
    if (cust_name_new_win.get() == "" or len(dateE2_new_win.get()) == 0):
        CTkMessagebox(title="Warning Message!", message="All fields are required!!",icon="warning")
    else:
        result = subprocess.run(['node', 'generate_bill.js', cust_name_new_win.get(),dateE2_new_win.get()], capture_output=True)
        product,price,quantity = result.stdout.decode('utf-8').strip().split("\n")
        product = product.split(",")
        price = price.split(",")
        tot_cost = 0
        quantity = quantity.split(",")
        generate_bill.delete("0.0", "end")
        generate_bill.insert("0.0","\n\t\t K2 Grocery Shop ")
        generate_bill.insert("end","\n\t Senapati Bapat Marg, Lower Parel")
        generate_bill.insert("end","\n\t\tPhone No. 9873022093 ")
        generate_bill.insert("end","\n\n\tCustomer :  "+cust_name_new_win.get())
        generate_bill.insert("end","\t\tBill date:  "+dateE2_new_win.get())
        generate_bill.insert("end",f"\n\n\t Product\t   Price\t  Quantity\t \n")
        for i in range(len(product)):
            tot_cost += int(price[i])
            generate_bill.insert("end",f"\n\t "+product[i]+"\t   "+price[i]+"\t  "+quantity[i]+"\t ")
        
        generate_bill.insert("end","\n\t"+str("-")*50)
        generate_bill.insert("end","\n\t Total Cost :- "+str(tot_cost))

   
combobox = customtkinter.CTkOptionMenu(tabview.tab("Sell"),values = ["Choose option"],command = set_price)
combobox.grid(row=2,column=2,padx=15, pady=15)
combobox.set("Choose product")
update_options_products()

price_label=customtkinter.CTkLabel(tabview.tab("Sell"), text="Price",font=('arial',18,'bold'),width=12)
price_label.grid(row=3,column=1,padx=15, pady=15)
 
Price=customtkinter.CTkEntry(tabview.tab("Sell"),textvariable = "",font=('arial',18,'bold'),width=155)
Price.grid(row=3,column=2, padx=15, pady=15)

quantity_label=customtkinter.CTkLabel(tabview.tab("Sell"), text="Quantity",font=('arial',18,'bold'),width=12)
quantity_label.grid(row=4,column=1,padx=15, pady=15)

Quantity=customtkinter.CTkEntry(tabview.tab("Sell"),textvariable="",font=('arial',18,'bold'),width=155)
Quantity.grid(row=4,column=2, padx=15, pady=15)

cust_name_label=customtkinter.CTkLabel(tabview.tab("Sell"), text="Customer name",font=('arial',18,'bold'),width=12)
cust_name_label.grid(row=3,column=3,padx=15, pady=5)

cust_name=customtkinter.CTkEntry(tabview.tab("Sell"),textvariable="",font=('arial',18,'bold'),width=155)
cust_name.grid(row=3,column=4, padx=15)

# ADDING THE SOLD PRODUCT IN THE DATABASE
view_sell_btn=customtkinter.CTkButton(tabview.tab("Sell"),text="View sell",font=('arial',19,'bold'),width=20,command = view_sell)
view_sell_btn.grid(row=6,column=1,padx=15,pady=15)

add_product=customtkinter.CTkButton(tabview.tab("Sell"),text="Add product",font=('arial',18,'bold'),width=20,command = add_sell)
add_product.grid(row=6,column=2,padx=15,pady=15)

print_bill=customtkinter.CTkButton(tabview.tab("Sell"),text="Billing",font=('arial',18,'bold'),width=20,command = show_bill)
print_bill.grid(row=6,column=3,padx=15,pady=15)
# to show sell database
view_sell=customtkinter.CTkTextbox(tabview.tab("Sell"),font=('arial',12),width = 380 ,height = 400)
view_sell.grid(row=7,column=0,columnspan=3,padx=15,pady=15)
#to show bill of particular customer
generate_bill=customtkinter.CTkTextbox(tabview.tab("Sell"),font=('arial',14),width = 380 ,height = 400)
generate_bill.grid(row=7,column=3,columnspan=3,padx=15,pady=15)
master.mainloop()
