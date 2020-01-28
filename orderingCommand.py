#Ryan Dalton - Week 5 - Command Pattern - Pizza Ordering System

"""
Idea is to create a customer object that creates an order object (contains details of order, pizza objects, cost etc.)
Once the order is sent, command object is created which uses a execute command for multiple objects.  Each object has its own
execute method.  Also added the ability for command objects to be created in other objects functions when a logical next step occurs.

Store receives the execute and ticket - which is then passed to cook object who proceeds to make the order and then the cashier who
receives the order and notifies the customer.
"""

#from pizzaFactory import * - wont require pizza factory until final project
from random import randrange

class Person:
    def __init__(self, name, location):
        self.name = name
        self.location = location
            
class Customer(Person):
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.order = None
    
    #create a generic order (tuple w/ strings - in final project it will be series of objects
    def createOrder(self, *items):
        self.order = Order(items)
        self.order.status = "Order Created"
        return self.order
    
    def requestUpdate(self):
        return self.order.status
    
    #return order list
    def getOrder(self):
        return self.order
    
    #customer creates command w/ order token which is sent to store designated
    def sendOrder(self, pizzaStore, order):
        newCommand = Commander()
        newCommand.assign(pizzaStore, order)
        newCommand.execute()
        
class Cook(Person):
    def __init__(self, name, location):
        self.name = name
        self.location = location #should be pizza store object
    
    #when Cook receives execute command, creates items in orders
    def execute(self, order):
        order.status = "Order being prepared by cook..."
        order.sendUpdate()
        for item in order.items:
            self.create(item)
        order.status = "Order Prepared"
        order.sendUpdate()
        newCommand = Commander()
        newCommand.assign(self.location.cashier, order)
        newCommand.execute()

    def create(self, item): #At this point order will be processed by cook
        ##Connect pizza factory here based on order information
        pass

class Cashier(Person):
    def __init__(self, name, location):
        self.name = name
        self.location = location #This should be the pizza store object
    
    def execute(self, order):
        self.generateReceipt()
        self.location.orderqueue.remove(order)
        self.location.ordersReady.append(order)
        order.status = "Order is ready for pickup"
        order.sendUpdate()
    
    def generateReceipt(self):
        #More to come on this
        #As it will generate a price and format for customer
        pass

class PizzaStore:
    def __init__(self, locationNum):
        self.locationNum = locationNum
        self.orderqueue = []
        self.cookList = []
        self.ordersReady = []
        self.cashier = None
    
    #when store gets command to execute
    def execute(self, order):
        order.status = "Order received by store"
        order.sendUpdate()
        self.orderqueue.append(order)
        nextCook = self.cookList.pop()
        self.cookList.append(nextCook)
        nextCook.execute(order)
        
    def addCook(self, cookObj):
        self.cookList.append(cookObj)
        
    def assignCashier(self, cashier):
        self.cashier = cashier
        

class Commander:
    def __init__(self):
        self.target = None
        self.token = None
        
    def assign(self, target, token):
        self.target = target
        self.token = token
    
    def execute(self):
        return self.target.execute(self.token)
    
class Order:
    def __init__(self, *items):
        self.items = list(items)
        self.status = None #this will be updated as the order is sent to different objects
        #generates a random 7 digit account number upon creation of object
        self.orderNumber = randrange(1000000, 9999999)
        
    def __str__(self):
        print("Order",self.orderNumber)
        return str(self.items)
    
    def sendUpdate(self):
        return print(self.status)

#might be interesting to always have a singleton commander available globally that
#queues up and procesess requests and targets as it receives them
#globalCommand = Commander()

def main():
    #Idea behind this is that the sendUpdate function provides customer an SMS
    print("Testing command pattern...\n")
    customer = Customer("Bob", "Suburbia")
    pizzaStore = PizzaStore("OldTown")
    charlie = Cook("Charlie", pizzaStore)
    becky = Cashier("Deb", pizzaStore)
    pizzaStore.addCook(charlie)
    pizzaStore.assignCashier(becky)
    #create a mock order
    order1 = customer.createOrder("Pepperoni Pizza", "Pepsi", "Breadsticks")
    print(order1)
    print(order1.status)
    customer.sendOrder(pizzaStore, order1)
    #Aboev creates a chain of executes - first order to store, then store to cook
    #followed by cook to cashie -  customer sees SMS updates as to where the order is at in its lifecycle
    print("\n")
    #create another customer w/ different order
    customer2 = Customer("Ryan", "Suburbia")
    order2 = customer2.createOrder("Stuffed Calzone", "Wings")
    print(order2)
    print(customer2.requestUpdate())
    customer2.sendOrder(pizzaStore, order2)
    
    
main()
