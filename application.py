from tkinter import *
from tools import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

root =Tk()
root.geometry('800x600+1+1')
root.config(background="#30D5C8")
title=Label(root, text="Employee Table", bg="#30D5C8", font=("bold",16), fg="black")
title.pack()







#-----------------------------------variables------------------------------------

emp_id_var=IntVar()
emp_name_var=StringVar()
Add_var=StringVar()
Sal_var=IntVar()


#-------------------------------------Donnees------------------------------------
employee_id=Label(root, text="employee ID", font=("bold",14), fg='blue',bg="#30D5C8",  )
employee_id.place(x=350, y=50)
entry1=Entry(root, justify='center', bd=2, bg='white', textvariable=emp_id_var)
entry1.place(x=350, y=80, width=200, height=30)

employee_name=Label(root, text="employee name", font=("bold",14), fg='blue', bg="#30D5C8", )
employee_name.place(x=350, y=110)
entry2=Entry(root, justify='center', bd=2, bg='white',textvariable=emp_name_var )
entry2.place(x=350, y=140, width=200, height=30)

Address=Label(root, text="Address", font=("bold",14),  fg="blue", bg="#30D5C8", )
Address.place(x=350, y=170)
entry3=Entry(root, justify='center', bd=2, bg='white', textvariable=Add_var)
entry3.place(x=350, y=200, width=200, height=30)

Salary=Label(root, text="Salary", font=("bold",14), bg="#30D5C8",fg="blue", )
Salary.place(x=350, y=230)
entry4=Entry(root, justify='center', bd=2, bg='white' , textvariable=Sal_var)
entry4.place(x=350, y=260, width=200, height=30)



#-------------------------------------functions--------------------------------------


def connection():
    try:
        conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'salary_database',
        )
        return conn
    except:
        print("erreur")
conn=connection()
mycur=conn.cursor()
#mycur.execute("CREATE DATABASE salary_database")
#mycur.execute("CREATE TABLE SALARIES (employee_id int primary key, employee_name VARCHAR(50), address VARCHAR(100) , Salary VARCHAR(100) )")

def create():

    child=Toplevel(root)
    child.geometry('700x700')
    child.config(background="#30D5C8",  )
    ss=Frame(child,bg='#30D5C8')
    ss.place(x=1, y=1, width=700,height=700)
    
    conn=connection()
    mycur=conn.cursor()
    mycur.execute("SELECT * FROM SALARIES")
    rows=mycur.fetchall()
    scroll_x=Scrollbar(ss, orient= HORIZONTAL)
    scroll_y=Scrollbar(ss, orient=VERTICAL)

    salary_table=ttk.Treeview(ss, columns=('id_employee','employee_name','Adress','Salary'))
    
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side= LEFT, fill= Y)
    salary_table.place(x=100,y=150,width=500,height=500)
    
    salary_table['show']='headings'
    salary_table.heading('id_employee', text="id_employeer")
    salary_table.heading('employee_name', text="employee_name")
    salary_table.heading('Adress', text="Adress")
    salary_table.heading('Salary', text="Salary")

    salary_table.column('id_employee', width=30)
    salary_table.column('employee_name',width=60)
    salary_table.column('Adress', width=60)
    salary_table.column('Salary', width=60)
    for row in rows:
        salary_table.insert("", END, values = row)
            
        conn.commit()
    def choisir():
        for x in salary_table.get_children():
            salary_table.delete(x)
        conn=connection()
        mycur = conn.cursor()
        mycur.execute(" SELECT * from  SALARIES where employee_name like '"+str(choicir_var.get())+"' ")
        tt=mycur.fetchall()
        for row in tt:
           salary_table.insert("", END, values = row)
           print(row)
           conn.commit()
    def sortbyname():
        for x in salary_table.get_children():
          salary_table.delete(x)
        conn=connection()
        mycur = conn.cursor()
        mycur.execute("select * from SALARIES order by employee_name asc")
        tt = mycur.fetchall()
        conn.commit()
        for row in tt:
          salary_table.insert("", END, values = row)
    conn.close()
    
    title=Label(ss, text="Employee Table", bg="#30D5C8", font=("bold",16), fg="black")
    title.pack()
    add_btn=Button(ss, text='chercher',  font=("bold",12), fg="black", bg='silver', bd=2, command=choisir)
    add_btn.pack()
    choicir_var=StringVar()
    entry_chercher=Entry(ss, justify='center', bd=2, bg='white', textvariable=choicir_var)
    entry_chercher.pack()
    sortByName_btn=Button(ss, text='sortByName',  font=("bold",12), bg='silver', bd=2, command=sortbyname)
    sortByName_btn.pack()
    

    conn.close()

'''
def get_cursor(ev):
    cursor_row=salary_table.focus()
    contents=salary_table.item(cursor_row)
    row=contents['values']
    employee_id.set(row[0])
    name_var.set(row[1])
    email_var.set(row[2])
    

salary_table.bind("<ButtonRelease-1>", get_cursor)'''





def clear():
    emp_id_var.set('')
    emp_name_var.set('')
    Add_var.set('')
    Sal_var.set(0)
    root.winfo_children()[2].focus() # curseur va se mettre automatiquement sur id apres clear



def add_employee():
    conn=connection()
    mycur=conn.cursor()
    mycur.execute("INSERT INTO SALARIES VALUES (%d, '%s', '%s', %d)" % ( emp_id_var.get(), emp_name_var.get(), Add_var.get(), Sal_var.get()))
    clear()
    conn.commit()
    conn.close()


def find_employee():
    conn=connection()
    mycur=conn.cursor()
        
    mycur.execute(" SELECT * from SALARIES where employee_id like '%"+str(emp_id_var.get())+"%' ")
    rows=(mycur.fetchall())[0]
    emp_id_var.set( rows[0] )
    emp_name_var.set(rows[1])
    Add_var.set(rows[2])
    Sal_var.set(rows[3])
    #clear()
    conn.commit()
    root.winfo_children()[11].config(state='disable()')
    conn.close()



def delete_employee():
    conn=connection()
    mycur=conn.cursor()
        
    mycur.execute(" DELETE from SALARIES where employee_id like '%"+str(emp_id_var.get())+"%' ")
    
    clear()
    conn.commit()
    conn.close()


def update_employee():
    conn=connection()
    mycur=conn.cursor()
        
    mycur.execute (" UPDATE SALARIES SET employee_name ='"+str(emp_name_var.get())+"', Address='"+str(Add_var.get())+"', Salary='"+str(Sal_var.get())+"' WHERE employee_id='"+str(emp_id_var.get())+"' ")
    
    clear()
    conn.commit()
    conn.close()


#----------------------------button----------------------------------
add_btn=Button(root, text='Add Employee',  font=("bold",12), fg="black", bg='silver', bd=2, command=add_employee )
add_btn.place(x=350,y=300, width=200, height=30)
find_btn=Button(root, text='Find Employee',  font=("bold",12), fg="black", bg='silver', bd=2, command= find_employee )
find_btn.place(x=350,y=340, width=200, height=30)
edit_btn=Button(root, text='Edit Employee',  font=("bold",12), fg="black", bg='silver', bd=2, command=update_employee)
edit_btn.place(x=350,y=380, width=200, height=30)
del_btn=Button(root, text='Delete Employee',  font=("bold",12), fg="black", bg='silver', bd=2, command=delete_employee )
del_btn.place(x=350,y=420, width=200, height=30)
clear_btn=Button(root, text='Clear Fields',  font=("bold",12), fg="black", bg='silver', bd=2, command=clear )
clear_btn.place(x=350,y=460, width=200, height=30)
EXIT_btn=Button(root, text='Exit',  font=("bold",12), fg="black", bg='silver', bd=2,command=root.quit )
EXIT_btn.place(x=350,y=500, width=200, height=30)
show_btn=Button(root, text='show',  font=("bold",12), fg="black", bg='silver', bd=2, command=create )
show_btn.place(x=350,y=540, width=200, height=30)



root.mainloop()