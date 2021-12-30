import numpy as np

class BaseDriver:
    """
    Drivers are linearly transformed to scale between [1,10]
    """
    transformed_bounds = (10, 1)

    def __repr__(self):
        return f'{self.name}: {self.value} / {self.transformed}'

    @property
    def value(self):
        return self._value

    @property
    def alpha(self):
        return self.transformed_bounds[0]

    @property
    def omega(self):
        return self.transformed_bounds[1]

    @property
    def transformed(self):
        """
        Linear transform to scale between [1,10].
        
        Accounts for inverse drivers (a low value indicates a greater risk)

        1. Determine if driver is inverse
        2. assign min or max value as required if 'x' is outside the min/max bounds
        3. Rescaled according to this formula: https://stats.stackexchange.com/a/25897/314876
        """
        scaled_min, scaled_max = self.transformed_bounds
        x, min_, max_ = self.value, self.min, self.max
        
        if self.inverse:
            x = min_ if x > min_ else (max_ if x < max_ else x)
        else:
            x = min_ if x < min_ else (max_ if x > max_ else x)
        
        num = (scaled_max - scaled_min)*(x - min_)
        denom = max_ - min_
        
        return (num / denom) + scaled_min   

    @property
    def name(self):
        NotImplemented

    @property
    def definition(self):
        NotImplemented

    @property
    def defn(self):
        return self.definition

    def __call__(self):
        NotImplemented

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def inverse(self):
        return self.min > self.max


class interest_cover(BaseDriver):
    name = 'Interest Cover'
    shortname = 'intcov'
    _min = 0
    _max = 30
    _args = ['ebitda', 'interest']

    def __init__(self, ebitda, interest):
        self.ebitda = ebitda
        self.interest = interest
        self._value = ebitda / interest

class opmarg(BaseDriver):
    name = 'Operating Margin'
    shortname = 'opmarg'
    _min = 0
    _max = .84
    _args = ['rev', 'cogs', 'opex', 'amort', 'r_n_d', 'otherinc']
    
    def __init__(self, *args):
        self._value = self._calc(*args)

    def _calc(self, *args):
        rev, cogs, opex, amort, r_n_d, otherinc = list(args)
        num = rev - cogs + otherinc - opex + r_n_d + amort
        denom = rev

        return num / denom if rev != 0  else 0

class ebitda_marg(BaseDriver):
    name = 'EBITDA Margin'
    shortname = 'ebitda_marg'
    _min = -.0022
    _max = .2652
    _args = ['ebitda', 'rev']
    
    def __init__(self, *args):
        self._value = args[0] / args[1]

class rev_yoy(BaseDriver):
    name = 'Revenue Growth'
    shortname = 'rev_yoy'
    _min = -.2448
    _max = .4381
    _args = ['rev', 'rev_1']
    
    def __init__(self, *args):
        self._value = args[0] / args[1] - 1

class roc(BaseDriver):
    name = 'Return on Capital'
    shortname = 'roc'
    _min = 0
    _max = .2275
    _args = ['nibt', 'interest', 'capital', 'capleases']

    def __init__(self, *args):
        self._value = self._calc(*args)

    def _calc(self, *args):
        nibt, interest, cap, capleases = list(args)
        tax = 1 - .375
        num = (nibt + interest + (1/3)*capleases)*tax
        
        return num / cap

class ffo_to_debt(BaseDriver):
    name = 'FFO to Debt'
    shortname = 'ffo_to_debt'
    _min = 0
    _max = .675
    _args = ['ffo', 'debt']

    def __init__(self, *args):
        self._value = args[0] / args[1]

class debt_to_cap(BaseDriver):
    name = 'Debt to Capital'
    shortname = 'debt_to_cap'
    _min = .95
    _max = 0
    _args = ['debt', 'capital']

    def __init__(self, *args):
        self._value = args[0] / args[1]

class total_assets(BaseDriver):
    """
    Natural log of total assets
    """
    name = 'Total Assets'
    shortname = 'assets'
    _min = 0.67
    _max = 9.3
    _args = ['total_assets']

    def __init__(self, total_assets:float):
        """
        Params
        -------
        total_assets: float, in US$ MM
        """
        self._value = np.log(total_assets)

class arturn(BaseDriver):
    name = 'Accounts Receivable Turnover'
    shortname = 'ar_turn'
    _min = 0
    _max = 91.85
    _args = ['rev', 'ar']
    
    def __init__(self, *args):
        self._value = args[0] / args[1]

class d_to_ebitda(BaseDriver):
    name = 'Debt to EBITDA'
    shortname = 'd_to_ebitda'
    _min = 5.5
    _max = 0
    _args = ['debt', 'ebitda']
    
    def __init__(self, *args):
        self._value = args[0] / args[1]

class gm(BaseDriver):
    name = 'Gross Margin'
    shortname = 'gm'
    _min = .0822
    _max = .597
    _args = ['rev', 'cogs']
    
    def __init__(self, *args):
        self._value = 1 - args[1] / args[0]

class current(BaseDriver):
    name = 'Current Ratio'
    shortname = 'current'
    _min = .74
    _max = 4.52
    _args = ['current_assets', 'current_liabilities']
    
    def __init__(self, *args):
        self._value = 1 - args[1] / args[0]

class total_rev(BaseDriver):
    name = 'Total Revenue'
    shortname = 'total_rev'
    _min = 1.98
    _max = 10.6
    _args = ['rev']
    
    def __init__(self, *args):
        self._value = np.log(args[0])

class rev_to_ar(BaseDriver):
    name = 'Revenue to Accounts Receivable'
    shortname = 'rev_to_ar'
    _min = 3.5
    _max = 34.13
    _args = ['rev', 'ar']
    
    def __init__(self, *args):
        self._value = args[0] / args[1]
