from home import Home 
from order import Order
from service import DBService

db = DBService()
# query = "select firstname, lastname, address, date, time, contact, id from deliveree_user WHERE status = false ORDER BY id"
# allItems = db.fetchAll()
home = Home()
parameter = home.startListening()
order = Order()
flag = True
while(flag):
    order.loadDB(db.fetchAll())
    flag = order.startListening()
    