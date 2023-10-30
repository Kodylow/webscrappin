class P2PDataRow:
    def __init__(
        self,
        advertiser,
        trade_partner_info,
        merchant_badge,
        shield_badge,
        price,
        currency,
        orders,
        completion,
        available,
        limit,
        payment,
    ):
        self.advertiser = advertiser
        self.trade_partner_info = trade_partner_info
        self.merchant_badge = merchant_badge
        self.shield_badge = shield_badge
        self.price = price
        self.currency = currency
        self.orders = orders
        self.completion = completion
        self.available = available
        self.limit = limit
        self.payment = payment

    def to_dict(self):
        return {
            "advertiser": self.advertiser,
            "trade_partner_info": self.trade_partner_info,
            "merchant_badge": self.merchant_badge,
            "shield_badge": self.shield_badge,
            "price": self.price,
            "currency": self.currency,
            "orders": self.orders,
            "completion": self.completion,
            "available": self.available,
            "limit": self.limit,
            "payment": self.payment,
        }
