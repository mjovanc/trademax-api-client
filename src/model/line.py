class Line:
    """
    Represents a Line in a Purchase Order.
    """
    item_no = ''
    supplier_item_no = ''
    line_no = 0
    quantity = 0
    quantity_accepted = 0
    quantity_dispatched = 0
    quantity_recieved = 0
    units = ''
    gross_price = 0
    tax_percentage = 0
    gross_amount = 0
    tax_amount = 0
    total_amount = 0
    confirmed_delivery_from = ''
    confirmed_delivery_to = ''

    def __init__(self, item_no, supplier_item_no, line_no, quantity, quantity_accepted,
                 quantity_dispatched, quantity_recieved, units, gross_price, tax_percentage,
                 gross_amount, tax_amount, total_amount, confirmed_delivery_from,
                 confirmed_delivery_to):
        self.item_no = item_no
        self.supplier_item_no = supplier_item_no
        self.line_no = line_no
        self.quantity = quantity
        self.quantity_accepted = quantity_accepted
        self.quantity_dispatched = quantity_dispatched
        self.quantity_recieved = quantity_recieved
        self.units = units
        self.gross_price = gross_price
        self.tax_percentage = tax_percentage
        self.gross_amount = gross_amount
        self.tax_amount = tax_amount
        self.total_amount = total_amount
        self.confirmed_delivery_from = confirmed_delivery_from
        self.confirmed_delivery_to = confirmed_delivery_to

    def __iter__(self):
        """Iterates over all object attributes."""
        for attr, value in self.__dict__.items():
            yield attr, value
