money = "${:.2f}".format

class Bond:
    def __init__(self,**kwargs):
        for kv in kwargs.items(): setattr(self,*kv)

    @property
    def price(self):
        total = self.face / (1 + self.eff_yield) ** self.periods
        for period in range(self.periods):
            total += self.coupon / (1 + self.eff_yield) ** (1 + period)
        return total

print(money(
    Bond(
        face = 1000,
        periods = 23,
        coupon = 1000 * 0.058,
        eff_yield = 0.047,
    ).price))