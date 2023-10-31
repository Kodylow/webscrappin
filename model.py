class P2PDataRow:
    def __init__(
        self,
        page_type,
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
        self.page_type = page_type  # "buy" or "sell"
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
            "page_type": self.page_type,
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


class Header:
    def __init__(self, name, last_seen, joined_on):
        self.name = name
        self.last_seen = last_seen
        self.joined_on = joined_on

    def to_dict(self):
        return {
            "name": self.name,
            "last_seen": self.last_seen,
            "joined_on": self.joined_on,
        }


class Feedback:
    def __init__(self, positive_feedback, total_feedback, positive, negative):
        self.positive_feedback = positive_feedback
        self.total_feedback = total_feedback
        self.positive = positive
        self.negative = negative

    def to_dict(self):
        return {
            "positive_feedback": self.positive_feedback,
            "total_feedback": self.total_feedback,
            "positive": self.positive,
            "negative": self.negative,
        }


class Stats:
    def __init__(
        self,
        all_trades,
        buy_sell_ratio,
        buy,
        sell,
        _30d_trades,
        _30d_completion_rate,
        avg_release_time,
        avg_pay_time,
    ):
        self.all_trades = all_trades
        self.buy_sell_ratio = buy_sell_ratio
        self.buy = buy
        self.sell = sell
        self._30d_trades = _30d_trades
        self._30d_completion_rate = _30d_completion_rate
        self.avg_release_time = avg_release_time
        self.avg_pay_time = avg_pay_time

    def to_dict(self):
        return {
            "all_trades": self.all_trades,
            "buy_sell_ratio": self.buy_sell_ratio,
            "buy": self.buy,
            "sell": self.sell,
            "30d_trades": self._30d_trades,
            "30d_completion_rate": self._30d_completion_rate,
            "avg_release_time": self.avg_release_time,
            "avg_pay_time": self.avg_pay_time,
        }


class UnifiedDataRow(P2PDataRow, Header, Feedback, Stats):
    def __init__(
        self,
        advertiser,
        page_type,
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
        name,
        last_seen,
        joined_on,
        positive_feedback,
        total_feedback,
        positive,
        negative,
        all_trades,
        buy_sell_ratio,
        buy,
        sell,
        _30d_trades,
        _30d_completion_rate,
        avg_release_time,
        avg_pay_time,
    ):
        P2PDataRow.__init__(
            self,
            advertiser,
            page_type,
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
        )
        Header.__init__(self, name, last_seen, joined_on)
        Feedback.__init__(self, positive_feedback, total_feedback, positive, negative)
        Stats.__init__(
            self,
            all_trades,
            buy_sell_ratio,
            buy,
            sell,
            _30d_trades,
            _30d_completion_rate,
            avg_release_time,
            avg_pay_time,
        )

    def to_dict(self):
        result = P2PDataRow.to_dict(self)
        result.update(Header.to_dict(self))
        result.update(Feedback.to_dict(self))
        result.update(Stats.to_dict(self))
        return result


fieldnames = [
    "advertiser",
    "page_type",
    "trade_partner_info",
    "merchant_badge",
    "shield_badge",
    "price",
    "currency",
    "orders",
    "completion",
    "available",
    "limit",
    "payment",
    "name",
    "last_seen",
    "joined_on",
    "positive_feedback",
    "total_feedback",
    "positive",
    "negative",
    "all_trades",
    "buy_sell_ratio",
    "buy",
    "sell",
    "30d_trades",
    "30d_completion_rate",
    "avg_release_time",
    "avg_pay_time",
]
