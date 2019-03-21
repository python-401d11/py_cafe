from src.models import Manager, Customer, Employee, Order, OrderItems, Item
from src.models_reports import CustomerOrders

class TestReportModels():
    """ Tests for Reports """
    def test_create_model(self):
        assert CustomerOrders
    def test_created_model(self):
        assert CustomerOrders(0)
    def test_sales_report(self,customer,items,order):
        res = CustomerOrders(0)
        assert res.item_totals(1)[0][0] == 'Biscuits and Gravy'
        assert res.item_totals(1)[0][1] == 1
        assert res.item_totals(1)[1][0] == 'Cheeseburger'
        assert res.item_totals(1)[1][1] == 1
        
    def test_customer_totals_report(self,customer,items,order):
        res = CustomerOrders(0)
        #testing for Biscuits and Gravy
        assert res.customer_totals(1)[0][0] == 'Milo'
        assert res.customer_totals(1)[0][1] == 1
        #testing for Cheeseburger
        assert res.customer_totals(2)[0][0] == 'Milo' 
        assert res.customer_totals(2)[0][1] == 1
        
