import unittest
from Cafe import FoodItem, DrinkItem, Order, Customer, Bill

class TestCafeSystem(unittest.TestCase):

    # Defines the test class which groups all the test cases for the system

    def test_menu_item_creation(self):
        item = FoodItem("Sandwich", 5.00, "Carbs")
        self.assertEqual(item.getPrice(), 5.00)

        # Creates the customers orders/drinks

    def test_order_add_item(self):
        customer = Customer("Thawhid")
        order = Order("1", customer)
        item = DrinkItem("Latte", 3.50, "Large")
        order.addItem(item)
        self.assertEqual(len(order.orderItems), 1)

        #adds multiple items to the order and calculates the prices

    def test_order_total_calculation(self):
        customer = Customer("Arshad")
        order = Order("2", customer)
        order.addItem(FoodItem("Salad", 3.90, "Healthy"))
        order.addItem(DrinkItem("Tea", 1.80, "Medium"))
        self.assertAlmostEqual(order.calculateTotal(), 5.70)

        # Generates a bill for the customer, also confirms the total amount of the order after tax

    def test_bill_calculation(self):
        customer = Customer("Jawad")
        order = Order("3", customer)
        order.addItem(DrinkItem("Coffee", 2.00, "Small"))
        bill = order.generateBill()
        self.assertAlmostEqual(bill.calculateFinalAmount(), 2.20)

if __name__ == "__main__":
    unittest.main()
