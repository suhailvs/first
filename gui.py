from tkinter import *
from tkinter.ttk import *
import sql
from guiwidgets.calendar import ttkCalendar
from guiwidgets.listview import MultiListbox
from blackbox import _init_toolbar
from datetime import datetime #to understand currentdate

                        #####################
                        #FormMenu class     #
                        #####################
def label_entry(frmlblent,txtlbl,txtlbl2=None):
    label=Label(frmlblent,text=txtlbl)
    label.pack(side=LEFT)
    frmlblent._entry=Entry(frmlblent)
    frmlblent._entry.pack(side=LEFT)
    if txtlbl2:
        label2=Label(frmlblent,text=txtlbl2)
        label2.pack(side=LEFT)
        frmlblent._entry2=Entry(frmlblent)
        frmlblent._entry2.pack(side=LEFT)
    
class FormMenu:
    """This is the main form that shows after user login.
    Contains
    =========
    --> Label shows login Company name.
    --> Three Buttons
        --> Products:   OnClick Shows FormProducts,
        --> Invoices:   OnClick Shows FormInvoices,
        --> Customers:  OnClick shows FormCustomers
    --> A background Image
    """
    def __init__(self,master):
        self.master=master
        #self.master.title="Shop Pro using Python & Tkinter by Suhail"
        self.frm_invoices=None
        self.frm_calendar=None

    def _init_widgets(self):
        #initiate toolbar
        self.toolbar = Frame(self.master)
        lbl0=Label(self.toolbar,text='Name of you Company').pack(side=LEFT)
        butcalc=Button(self.toolbar,text='Calc',command=self.calc_click).pack(side=LEFT)
        butcalendar=Button(self.toolbar,text='Calander',command=self.calendar_click).pack(side=LEFT)
        self.toolbar.pack(side='top',fill='x')
        
        style = Style()
        style.configure("BW.TLabel", foreground="white", background="black")


        #buttons frame
        #--------------------------------------------
        self.buttons = Frame(self.master, style="BW.TLabel")
        #button products
        self.btnproducts = Button(self.buttons,command=self.products_click)
        self.imgprdt=PhotoImage(file="img/products.gif")#self.btnproducts['font']=("Helvetica", 16)
        self.btnproducts['image']=self.imgprdt
        self.btnproducts.pack(side='top')#, fill='x')
        lbl1=Label(self.buttons,text="Products...", style="BW.TLabel").pack()
        #button invoices
        self.btninvoices = Button(self.buttons, text='Invoices...', command=self.invoices_click)
        self.imginv=PhotoImage(file="img/invoices.gif")
        self.btninvoices['image']=self.imginv
        self.btninvoices.pack(side='top')
        lbl2=Label(self.buttons,text="Invoices...", style="BW.TLabel").pack()
        #button customers
        self.btncustomers = Button(self.buttons, text='Customers...', command=self.customers_click)
        self.imgcust=PhotoImage(file="img/customers.gif")
        self.btncustomers['image']=self.imgcust
        self.btncustomers.pack(side='top')
        lbl3=Label(self.buttons,text="Customers...", style="BW.TLabel").pack()
        self.buttons.pack(side='left',padx=10)

        #background label
        #-------------------------------------------
        self.imgback=PhotoImage(file="img/back.gif")
        self.lblbackground= Label(self.master, style="BW.TLabel",borderwidth=0)
        self.lblbackground.pack(side='top')
        self.lblbackground['image'] = self.imgback

    def calc_click(self):
        import os
        os.startfile('calc.exe')

    #calendar-------    
    def calendar_click(self):
        if self.frm_calendar==None:
            self.frm_calendar=ttkCalendar(master=self.master)
        elif self.frm_calendar.flag: #frm_products currently opened
            print ('already a window exists')
            return 0
        else:
            self.frm_calendar=ttkCalendar(master=self.master)
            
        print ('called wait window')
        self.master.wait_window(self.frm_calendar.top)
        print ('exited from wait window')
        print (self.frm_calendar.datepicked)
        
    def products_click(self):
        print ("products")
        self.btnproducts['state']=  DISABLED
        self.btninvoices['state']=DISABLED
        self.btncustomers['state']=DISABLED
        self.frm_products=FormProducts()
        self.master.wait_window(self.frm_products.frame)
        self.btnproducts['state']=  NORMAL
        self.btninvoices['state']=NORMAL
        self.btncustomers['state']=NORMAL
        
        
        '''if self.frm_products==None:
            self.frm_products=FormProducts()
        elif self.frm_products.flag: #frm_products currently opened
            print ('already a window exists')
        else:
            self.frm_products=FormProducts()'''

    def invoices_click(self):
        print ("invoices")
        self.btnproducts['state']=  DISABLED
        self.btninvoices['state']=DISABLED
        self.btncustomers['state']=DISABLED
        self.frm_invoices=FormInvoices()
        self.master.wait_window(self.frm_invoices.frame)
        self.btnproducts['state']=  NORMAL
        self.btninvoices['state']=NORMAL
        self.btncustomers['state']=NORMAL

    def customers_click(self):
        self.btnproducts['state']=  DISABLED
        self.btninvoices['state']=DISABLED
        print ("customers")
        
#-------------------------------------------end of FormMenu class--------


                        #####################
                        #FormProducts class #
                        #####################       
class FormProducts:
    '''The Products window with toolbar and a datagrid of products'''
    def __init__(self):
        self.frame=Toplevel()
        _init_toolbar(self)
        self._init_gridbox()
        self.frm_addproduct=None
        self.frm_editproduct=None
        self.addproductflag=False # frmaddproduct doesn't exist
        
    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',3),('Product', 25), ('Description', 25), ('Price', 10)))
        tbproducts=sql.session._query("select * from products")
        self.update_mlb(tbproducts)
        self.mlb.pack(expand=YES,fill=BOTH)
            
    #form product add button clicked()        
    def btn_add_click(self):
        if self.addproductflag: return 0
        print ('not exist')
        self.addproductflag=True
        self.frm_addproduct=FormAddProduct()
        self.frame.wait_window(self.frm_addproduct.frame)
        if self.frm_addproduct._okbtn_clicked==1:
            tbproducts=sql.session._query("select * from products")
            self.update_mlb(tbproducts)
        self.addproductflag=False
            
    def btn_edit_click(self):
        print ('edit')
        
    def btn_del_click(self):
        if self.mlb.item_selected==None: return 'please select first'
        print (self.mlb.item_selected[1])
        sql.session._delete_product(int(self.mlb.item_selected[1]))
        self.mlb.delete(self.mlb.item_selected[0])
        self.mlb.item_selected=None
        
    def btn_find_click(self):
        fnd=self.entryfind.get()

        tbproducts=sql.session._find_products(fnd)
        self.update_mlb(tbproducts)
    def update_mlb(self,tb):
        self.mlb.delete(0,END)
        #tbproducts=sql.session._query(q)
        for row in tb:
            self.mlb.insert(END, (int(row[0]),
                                  row[1],
                                  row[2],
                                  int(row[3])))
           
#-------------------------------------------end of FormProducts class--------


                        ######################
                        #FormAddProduct class#
                        ######################   

class FormAddProduct:
    '''Add New product three labels and three textboxes and an OK button'''
    def __init__(self):
        
        self.frame=Toplevel()
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()
        
        
    def _init_widgets(self):
        self.label1=Label(self.frame,text="Product #")
        self.label1.grid(row=0,sticky=W)
        self.entry1=Entry(self.frame)
        self.entry1.grid(row=1,column=0)
        
        self.label2=Label(self.frame,text="Sales Price")
        self.label2.grid(row=0,column=1,sticky=W)
        self.entry2=Entry(self.frame)
        self.entry2.grid(row=1,column=1)

        self.label3=Label(self.frame,text="Description.")
        self.label3.grid(row=2,sticky=W,columnspan=2)
        self.entry3=Entry(self.frame)
        self.entry3.grid(row=3,sticky=W+E,columnspan=2)

        self.btn_ok=Button(self.frame,text="OK",width=7,command=self.btnok_click)
        self.btn_ok.grid(row=4,column=1,sticky=E)

    
        
    def btnok_click(self):
        items=(self.entry1.get(),self.entry3.get(),int(self.entry2.get()))
        if '' in items:
            print ('please fill all boxes')
            return 'break'
        sql.session._add_product(items)
        
        self._okbtn_clicked=1
        print ('user exits the screen by clicking ok butn')
        self.frame.destroy()
        
    def callback(self):
        
        self._okbtn_clicked=0
        print ('user exits the screen')
        self.frame.destroy()


#-------------------------------------------end of FormAddProduct class--------


                        #####################
                        # FormInvoices class#
                        #####################
class FormInvoices:
    def __init__(self):
        self.frame=Toplevel()
        _init_toolbar(self)
        self._init_gridbox()
        self.frm_addinvoice=None
        self.addinvoiceflag=False
        self.editinvoiceflag=False
        
    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',5),('Customer', 25), ('Date', 15), ('Grand Total', 15)))
        tbproducts=sql.session._query("select * from invoices")
        self.update_mlb(tbproducts)
        self.mlb.pack(expand=YES,fill=BOTH)
        

    def update_mlb(self,tb):
        self.mlb.delete(0,END)
        for row in tb:
            self.mlb.insert(END, (int(row[0]),
                                  row[1],
                                  row[2],
                                  int(row[3])))
        self.mlb.selection_set(0) #set first row selected
    
    def btn_add_click(self):
        print ('check addwindow exist or not. If not exist cmd will display not exist')
        if self.addinvoiceflag: return 0
        print ('not exist')
        self.addinvoiceflag=True
        self.frm_addinvoice=FormAddInvoice()
        self.frame.wait_window(self.frm_addinvoice.master)
        print ('form addinvoice doesnot exist. Add button will work')
        self.addinvoiceflag=False
        
    def btn_edit_click(self):
        if self.editinvoiceflag: return 0
        self.editinvoiceflag=True
        self.frm_editinvoice=FormEditInvoice()
        self.frm_editinvoice.init_entryboxes(self.mlb.item_selected[1:])#(id,customer,date,amount)
        tbinvitems=sql.session._show_invoice(self.mlb.item_selected[1])
        self.frm_editinvoice.update_mlbitems(tbinvitems)
        self.frame.wait_window(self.frm_editinvoice.master)
        self.editinvoiceflag=False
    

    def btn_del_click(self):
        if self.mlb.item_selected==None: return 'please select first'
        print (self.mlb.item_selected[1])
        sql.session._delete_invoice(int(self.mlb.item_selected[1]))
        self.mlb.delete(self.mlb.item_selected[0])
        self.mlb.item_selected=None
    def btn_find_click(self):
        print ('find')

#-------------------------------------------end of FormInvoices class--------


                        ########################
                        # FormAddInvoice class#
                        ########################

class FormAddInvoice:
    '''Add New product three labels and three textboxes and an OK button'''
    def __init__(self):
        
        self.master=Toplevel()
        self.master.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()
        
        
    def _init_widgets(self):
        self.frame0=Frame(self.master)
        label_entry(self.frame0,'Invoice# :')
        rowid=sql.session._next_invoiceid()
        self.frame0._entry.insert(END,str(rowid))
        self.frame0._entry['state']=DISABLED
        self.frame0.pack(side=TOP)
        #frame1- lblinvoice, lbl_date, btn_date
        self.frame1=Frame(self.master)
        label_entry(self.frame1,'Customer:')
        self.lbl_date=Label(self.frame1,text='Date:'+str(datetime.today())[:10])
        self.lbl_date.pack(side=LEFT)
        self.btn_date=Button(self.frame1,text="PickDate",width=8,
                             command=self.btn_date_click)
        self.btn_date.pack(side=LEFT)
        self.frame1.pack(side=TOP)

        #frame2- lookuplist
        self.frame2=LookupList(self.master)
        self.frame2.ent.focus() #set_focus to entry product
        
        
        #frame3- quantity, ent_qty, btn_additem
        self.frame3=Frame(self.master)
        self.lbl3_1=Label(self.frame3,text="Quantity")
        self.lbl3_1.pack(side=LEFT)
        self.ent_qty=Entry(self.frame3)
        self.ent_qty.pack(side=LEFT)
        self.btn_additem=Button(self.frame3,text="AddItem",width=8,
                                command=self.btn_additem_click)
        self.btn_additem.pack(side=LEFT)
        self.frame3.pack(side=TOP)

        #frame4- mlbitems 
        self.frame4=Frame(self.master)
        self.mlbitems=MultiListbox(self.frame4, (('LN#',4),('ID#',6),
                ('Product', 15), ('Quantity',5),('Description', 20),
                ('UnitPrice', 10),('Total',10)))
        self.mlbitems.not_focus() #don't take_focus
        self.mlbitems.pack(expand=YES,fill=BOTH,side=TOP)
        self.frame4.pack(side=TOP)

        #frame5-netamount-stringvar, paid, balance
        self.frame5=Frame(self.master)
        self.lbl5_1=Label(self.frame5,text="Net:")
        self.lbl5_1.pack(side=LEFT)
        self.netamount=StringVar()
        self.netamount.set('0')
        self.lbl5_2=Label(self.frame5,textvariable=self.netamount, font=("Helvetica", 16))
        self.lbl5_2.pack(side=LEFT)
        self.lbl5_3=Label(self.frame5,text="paid:")
        self.lbl5_3.pack(side=LEFT)
        self.ent_paid=Entry(self.frame5)
        self.ent_paid.pack(side=LEFT)
        self.ent_paid.bind("<KeyRelease>",self.ent_paid_change)
        self.balanceamount=StringVar()
        self.lbl5_4=Label(self.frame5,text="Balance: ").pack(side=LEFT)
        #self.balanceamount.set('balance:')
        self.lblbal=Label(self.frame5,textvariable=self.balanceamount,
                          foreground='red',font=("Helvetica", 22)).pack(side=LEFT)
        
        self.frame5.pack(side=TOP)

        self.btn_ok=Button(self.master,text="OK",width=7,command=self.btnok_click)
        self.btn_ok.pack(side=TOP)
        
           
    def add_item(self):
        qty=self.ent_qty.get()
        if qty=='':
            print ('no quantity set')
            return 0
        qty=int(qty)
        LN=self.mlbitems.size()+1
        r,i_d,prdct,desc,price=self.frame2.mlb.item_selected
        self.mlbitems.insert(END, (LN,i_d,prdct,qty,desc,price,price*qty))
        net_amt=int(self.netamount.get())+(price*qty)
        self.netamount.set(str(net_amt))# stringvar: change liked to label
        self.frame2.ent.delete(0,END) #clear entry product
        self.ent_qty.delete(0,END)#clear entry quantity
        self.frame2.ent.focus()  #set_focus to entry product
        
    def btn_date_click(self):
        print('date')

    def ent_paid_change(self,event):
        paid=self.ent_paid.get()
        if paid=='':
            return 0
        bal=int(paid)-int(self.netamount.get())
        self.balanceamount.set(str(bal))
        
    def btn_additem_click(self):        
        self.add_item()
        
        #self.itemcounter+=1
        #LN=itemconter,product, qty, description,unitprice,total
        #print(self.frame2.mlb.item_selected)
        #print('add item')'''
        
    def btnok_click(self):
        no_of_items=self.mlbitems.size()
        if no_of_items==0:
            print('please select some products first')
            return '0'
        print('okbutton clicked')
        i_d=int(self.frame0._entry.get())#invoiceid
        tbinvitems_items=[]
        for item in range(no_of_items):
            temp1=self.mlbitems.get(item)
            tbinvitems_items.append((temp1[0],
                                i_d,temp1[1],temp1[3],))

        tbinv_item=(i_d,self.frame1._entry.get(),
                    str(datetime.today())[:10],int(self.netamount.get()))
        sql.session._add_invoice(tbinv_item,tbinvitems_items)
        self._okbtn_clicked=1
        print ('user exits the screen by clicking ok butn')
        self.master.destroy()
        
    def callback(self):
        
        self._okbtn_clicked=0
        print ('user exits the screen')
        self.master.destroy()

# LookupList class
# a mlb and a entry box for FormAddInvoice class
class LookupList:
    def __init__(self,master):
        self.frame=Frame(master)#,width=100,height=200)
        self.le_frame=Frame(self.frame)
        self.tblookup=sql.session
        lbl=Label(self.le_frame,text="product").pack(side=LEFT)
        self.ent=Entry(self.le_frame)
        self.ent.pack(side=LEFT)
        self.ent.bind("<KeyRelease>",self.txtchange)#<Key>",self.keypressed)
        self.le_frame.pack(side=TOP)
        self._init_gridbox()
        self.frame.pack(side=TOP,expand=NO)

    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',5),('Product', 20), ('Description', 30), ('UnitPrice', 15)))
        self.update_mlb('')
        self.mlb.not_focus()
        self.mlb.pack(expand=YES,fill=BOTH,side=TOP)
        
    def txtchange(self,event):
        txtent=self.ent.get()
        self.update_mlb(txtent)
        
                
    def update_mlb(self,val):
        x=self.tblookup._query("select * from products where name like '%"+val+"%' order by name")
        self.mlb.delete(0,END)
        for row in x:
            self.mlb.insert(END, (int(row[0]),
                                  row[1],
                                  row[2],
                                  int(row[3])))
        self.mlb.selection_set(0) #set first row selected
        
#-------------------------------------------end of FormAddInvoice class--------


                        ########################
                        #FormEditInvoice class #
                        ########################

class FormEditInvoice:
    def __init__(self):
        self.master=Toplevel()
        self.frame1=Frame(self.master)#,width=100,height=200)
        label_entry(self.frame1,'Invoice#:')
        self.frame1.pack(side=TOP)

        self.frame2=Frame(self.master)#,width=100,height=200)
        label_entry(self.frame2,'Customer:','Date:')
        self.frame2.pack(side=TOP)

        lblprod=Label(self.master,text='Items').pack(side=TOP)
        self.frame3=Frame(self.master)
        self.mlbitems=MultiListbox(self.frame3, (('LN#',5),
                ('Product', 15), ('Quantity',5),('Description', 20),
                ('UnitPrice', 10),('Total',10)))
        self.mlbitems.not_focus() #don't take_focus
        self.mlbitems.pack(expand=YES,fill=BOTH,side=TOP)
        self.frame3.pack(side=TOP)

        self.frame4=Frame(self.master)#,width=100,height=200)
        label_entry(self.frame4,'GrandTotal:')
        self.frame4.pack(side=TOP)

    def init_entryboxes(self,val):
        #val=(id,customer,date,amount)
        self.frame1._entry.insert(END,val[0])
        self.frame1._entry['state']=DISABLED
        
        self.frame2._entry.insert(END,val[1])
        self.frame2._entry2.insert(END,val[2])
        self.frame2._entry['state']=DISABLED
        self.frame2._entry2['state']=DISABLED
        
        self.frame4._entry.insert(END,val[3])
        self.frame4._entry['state']=DISABLED
        
        
    def update_mlbitems(self,invitems):
        self.mlbitems.delete(0,END)
        for row in invitems:
            self.mlbitems.insert(END,(row[0],row[1],row[2],row[3],row[4],row[5]))
        self.mlbitems.selection_set(0) #set first row selected
