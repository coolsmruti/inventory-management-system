from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class catagoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        #variable
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #title

        lbl_title=Label(self.root,text="Manage Product Catagory",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_name=Label(self.root,text="Enter Catagory Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18),bg="lightyellow").place(x=50,y=170,width=300)

        btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="DELETE",command=self.delete,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)


        #catagory details
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.CatagoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.CatagoryTable.xview)
        scrolly.config(command=self.CatagoryTable.yview)
        
        self.CatagoryTable.heading("cid",text="C ID")
        self.CatagoryTable.heading("name",text="NAME")
        
        self.CatagoryTable["show"]="headings"

        self.CatagoryTable.column("cid",width=90)
        self.CatagoryTable.column("name",width=100)
        
        self.CatagoryTable.pack(fill=BOTH,expand=1)
        self.CatagoryTable.bind("<ButtonRelease-1>",self.get_data)

        #image
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((500,250),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)

        self.im2=Image.open("images/catagory.jpg")
        self.im2=self.im2.resize((500,250),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=580,y=220)

        self.show()
    #functions
    def add(self):
        con=sqlite3.connect(database=r'pp.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Catagory name should be required",parent=self.root)
            else:
                cur.execute("Select * from catagory where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Catagory already present, try different",parent=self.root)
                else:
                    cur.execute("Insert into catagory(name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Catagory Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def show(self):
        con=sqlite3.connect(database=r'pp.db')
        cur=con.cursor()
        try:
            cur.execute("select * from catagory")
            rows=cur.fetchall()
            self.CatagoryTable.delete(*self.CatagoryTable.get_children())
            for row in rows:
                self.CatagoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.CatagoryTable.focus()
        content=(self.CatagoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r'pp.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Please select catagory from the list",parent=self.root)
            else:
                cur.execute("Select * from catagory where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from catagory where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Catagory Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__=="__main__":
    root=Tk()
    obj=catagoryClass(root)
    root.mainloop()