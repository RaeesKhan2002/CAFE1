from typing import List
import uuid

# Observer Pattern used for Order

class OrderObserver:
    def update(self, order: "Order"):
        pass


class OrderLogger(OrderObserver):
    def update(self, order: "Order"):
        print(f"[Observer] Order {order.orderId} updated. Items in basket: {len(order.orderItems)}")


# Inheritance used

class MenuItem:  # Base class
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def getDetails(self) -> str:
        raise NotImplementedError("Must be implemented in subclass.")

    def getPrice(self) -> float:
        return self.price


class FoodItem(MenuItem):
    def __init__(self, name: str, price: float, cuisineType: str):
        super().__init__(name, price)

    def getDetails(self) -> str:
        return f"Food: {self.name} - £{self.price:.2f}"


class DrinkItem(MenuItem):
    def __init__(self, name: str, price: float, size: str):
        super().__init__(name, price)
        self.size = size

    def getDetails(self) -> str:
        return f"Drink: {self.name} ({self.size}) - £{self.price:.2f}"


# Factory Pattern

class MenuItemFactory:
    @staticmethod
    def create_item(item_type: str, *args) -> MenuItem:
        if item_type == "food":
            return FoodItem(*args)
        elif item_type == "drink":
            return DrinkItem(*args)
        else:
            raise ValueError("Invalid menu item type")


# Main Entities

class Customer:
    customer_counter = 0  

    # Class variable to generate ID numbers

    def __init__(self, name: str):
        self.name = name
        Customer.customer_counter += 1
        self.customerId = f"{Customer.customer_counter:03d}"  # ID Number 001, etc

    def placeOrder(self, order: "Order"):
        print(f"\nWelcome {self.name}! (Customer ID: {self.customerId})")
        print(f"Your Order ID is {order.orderId}\n")


class Order:
    def __init__(self, orderId: str, customer: Customer):
        self.orderId = orderId
        self.customer = customer
        self.orderItems: List[MenuItem] = []
        self.observers: List[OrderObserver] = []

    # Observer pattern used 

    def attach(self, observer: OrderObserver):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)

    def addItem(self, item: MenuItem):
        self.orderItems.append(item)
        print(f"\nAdded {item.name} to your basket.")
        self.notify()
        self.printBasket()

    def removeItem(self, index: int):
        if 0 <= index < len(self.orderItems):
            removed = self.orderItems.pop(index)
            print(f"\nRemoved {removed.name} from your basket.")
            self.notify()
        else:
            print("\nInvalid index. No item removed.")
        self.printBasket()

    def calculateTotal(self) -> float:
        return sum(item.getPrice() for item in self.orderItems)

    def generateBill(self) -> "Bill":
        total = self.calculateTotal()
        return Bill(billId=f"{uuid.uuid4().hex[:6].upper()}", order=self, totalAmount=total, tax=0.1)

    def printBasket(self):
        if not self.orderItems:
            print("\nYour basket is currently empty.\n")
        else:
            print("\n--- Your Basket ---")
            for i, item in enumerate(self.orderItems, start=1):
                print(f"{i}. {item.getDetails()}")
            print(f"Total so far: £{self.calculateTotal():.2f}\n")

     # Final reciept - Contains Order ID, Bill ID, Customer Name, items and total


class Bill:
    def __init__(self, billId: str, order: Order, totalAmount: float, tax: float):
        self.billId = billId
        self.order = order
        self.totalAmount = totalAmount
        self.tax = tax

    def calculateFinalAmount(self) -> float:
        return self.totalAmount * (1 + self.tax)

    def printBill(self):
        print("\n Cafe Bill ")
        print(f"Bill ID: {self.billId}")
        print(f"Order ID: {self.order.orderId}")
        print(f"Customer: {self.order.customer.name} (Customer ID: {self.order.customer.customerId})\n")
        print("Items:")
        for i, item in enumerate(self.order.orderItems, start=1):
            print(f"{i}. {item.getDetails()}")
        print(f"\nSubtotal: £{self.order.calculateTotal():.2f}")
        print(f"Tax: {self.tax*100:.1f}%")
        print(f"Total: £{self.calculateFinalAmount():.2f}")
        print("---------------------\n")
        print(f"Thank you {self.order.customer.name}! Please do come again!\n")


# Managers

class MenuManager:
    def __init__(self):
        self.menuItems: List[MenuItem] = []

    def addMenuItem(self, item: MenuItem):
        self.menuItems.append(item)

    def getMenu(self) -> List[MenuItem]:
        return self.menuItems


class OrderManager:
    def __init__(self):
        self.activeOrders: List[Order] = []

    def createOrder(self, customer: Customer) -> Order:
        order = Order(orderId=str(len(self.activeOrders) + 1), customer=customer)
        order.attach(OrderLogger())
        self.activeOrders.append(order)
        return order


#Interface

def run_cli():
    print(" Welcome to the Café, What can we get you! \n")

    menu_manager = MenuManager()

    # Menu

    # Drinks

    menu_manager.addMenuItem(MenuItemFactory.create_item("drink", "Latte", 3.50, "Large"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("drink", "Espresso", 2.00, "Small"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("drink", "Cappuccino", 3.00, "Medium"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("drink", "Tea", 1.80, "Medium"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("drink", "Coke", 1.00, "330ml"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("drink", "Fanta", 1.00, "330ml"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("drink", "Sprite", 1.00, "330ml"))

    # Food

    menu_manager.addMenuItem(MenuItemFactory.create_item("food", "Chicken Sandwich", 5.00, "Carbs"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("food", "Turkey Sandwich", 8.00, "Carbs"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("food", "Fish Sandwich", 5.00, "Carbs"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("food", "Flafel Sandwich", 4.00, "Carbs"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("food", "Vegan Sandwich", 5.00, "Carbs"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("food", "Croissant", 2.75, "Breakfast"))
    menu_manager.addMenuItem(MenuItemFactory.create_item("food", "Salad", 3.90, "Healthy"))

    order_manager = OrderManager()

    while True:

        # Customer name input

        while True:
            name = input("\nEnter your first name: ").strip()
            if name:
                break

        customer = Customer(name)
        order = order_manager.createOrder(customer)
        customer.placeOrder(order)

        while True:
            print("\n1. Add item\n2. Remove item\n3. View basket\n4. Pay\n0. Back to main menu")
            choice = input("Choose: ").strip()

            if choice == "1":
                while True:
                    print("\n--- Menu ---")
                    for i, item in enumerate(menu_manager.getMenu(), start=1):
                        print(f"{i}. {item.getDetails()}")
                    print("0. Back to main options")
                    try:
                        idx = int(input("Item number to add: "))
                    except ValueError:
                        print("Enter a valid number.")
                        continue
                    if idx == 0:
                        break
                    elif 1 <= idx <= len(menu_manager.getMenu()):
                        order.addItem(menu_manager.getMenu()[idx - 1])
                    else:
                        print("Invalid choice. Try again.")


            elif choice == "2":
                while True:
                    order.printBasket()
                    if not order.orderItems:
                        break
                    print("0. Back to main options")
                    try:
                        idx = int(input("Item number to remove: "))
                    except ValueError:
                        print("Enter a valid number.")
                        continue
                    if idx == 0:
                        break
                    elif 1 <= idx <= len(order.orderItems):
                        order.removeItem(idx - 1)
                    else:
                        print("Invalid choice. Try again.")
                        

            elif choice == "3":
                order.printBasket()

            elif choice == "4":
                bill = order.generateBill()
                bill.printBill()
                break 

            # after the customer, it goes back to enter name for new customer (LOOP)

            elif choice == "0":
                print(f"Goodbye {customer.name}! Returning to main menu...\n")
                break


if __name__ == "__main__":
    run_cli()
