import numpy as np

from htsfi.constants import PD, ODR, SP, SPRAT_KEY, PD_KEY, PDMAP
from htsfi.rating import drivers as dv

class BaseModel:
    PD = PD
    ODR = ODR
    SP = SP
    PDMAP = PDMAP
    TV_BOUNDS = np.stack((np.arange(1,10,.5), np.arange(1,10,.5)+.5)).T

    def __init__(self, *args):
        if len(args) > len(self._args):
            txt = 'You provided too many arguments.'
            txt += f' Allowed arguments are: {", ".join(self._args)}'
            raise ValueError(txt)
        
        self.kwargs = {k:v for k,v in zip(self._args, args)}
 
    @property
    def drivers(self):
        NotImplementedError

    @property
    def betas(self):
        return self._betas

    @property
    def weights(self):
        return self._weights

    @property
    def drivers(self):
        if not hasattr(self, '_drivers'):
            drivers = []
            for drv_class in self._driver_classes:
                driver_args = [self.kwargs[arg] for arg in drv_class._args]
                driver = drv_class(*driver_args)
                drivers.append(driver)
        else:
            drivers = self._drivers

        return drivers

    @property
    def _args(self):
        return np.unique(np.array([arg for d in self._driver_classes for arg in d._args]))

    def drvkey(self):
        return {driver.shortname: driver for driver in self.drivers}
    
    def drvvals(self):
        return {driver.shortname: driver.value for driver in self.drivers}
    
    def transforms(self):
        transforms = np.zeros(len(self.drivers))
        for i in range(len(self.drivers)):
            transforms[i] = self.drivers[i].transformed
            
        return transforms
    
    def contribs(self):
        return self.transforms()*self.betas
    
    def score(self):
        return self.contribs().sum()

    def index(self):
        tv = self.score()
        idx = len(self.ODR) - 1
        for i in range(self.TV_BOUNDS.shape[0]):
            bounds = self.TV_BOUNDS[i]
            if tv >= bounds[0] and tv < bounds[1]:
                idx = i
                break
        
        return idx

    def pd(self):
        return self.PD[self.index()]
    
    def odr(self):
        return self.ODR[self.index()]
    
    def rating(self):
        return self.SP[self.index()]

    def display(self):
        # print (self.score())
        # print (self.drvvals())
        # print (self.transforms())
        print (self.pd(), self.odr(), self.rating())

class AllIndustries(BaseModel):
    _driver_classes = [
        dv.interest_cover,
        dv.opmarg, 
        dv.roc, 
        dv.ffo_to_debt, 
        dv.debt_to_cap, 
        dv.total_assets
    ]
    _betas = [.0827, .2427, .1154, .0195, .1838, .2326]
    _weights = [.094, .277, .132, .21, .022, .265]

class Wholesale(BaseModel):
    _driver_classes = [
        dv.interest_cover,
        dv.ebitda_marg, 
        dv.rev_yoy,
        dv.debt_to_cap, 
        dv.total_assets
    ]
    _betas = [.1004, .1760, .2235, .1743, .2312]
    _weights = [.111, .194, .247, .193, .255]
        
class Service(BaseModel):
    _driver_classes = [
        dv.interest_cover,
        dv.opmarg, 
        dv.roc,
        dv.arturn,
        dv.d_to_ebitda, 
        dv.total_assets
    ]
    _betas = [.092, .135, .131, .154, .154, .17]
    _weights = [.11, .161, .157, .185, .184, .203]

class Retail(BaseModel):
    _driver_classes = [
        dv.interest_cover,
        dv.ebitda_marg, 
        dv.rev_yoy,
        dv.debt_to_cap, 
        dv.total_assets
    ]
    _betas = [.0663, .1745, .2241, .2277, .219]
    _weights = [.073, .191, .246, .25, .24]

class Telco(BaseModel):
    _driver_classes = [
        dv.interest_cover,
        dv.ebitda_marg, 
        dv.rev_yoy,
        dv.ffo_to_debt, 
        dv.debt_to_cap,
        dv.total_assets
    ]
    _betas = [.159, .325, .144, .279, .093, .234]
    _weights = [.263, .129, .116, .226, .075, .19]

class CapGoods(BaseModel):
    _driver_classes = [
        dv.gm,
        dv.current, 
        dv.opmarg,
        dv.d_to_ebitda, 
        dv.debt_to_cap,
        dv.total_rev,
    ]
    _betas = [.11, .101, .103, .219, .077, .203, .187]
    _weights = [.263, .129, .116, .226, .075, .19]

class ConsumerGoods(BaseModel):
    _driver_classes = [
        dv.gm,
        dv.ebitda_marg, 
        dv.rev_yoy,
        dv.rev_to_ar, 
        dv.debt_to_cap,
        dv.total_rev,
    ]
    _betas = [.122, .143, .0678, .1523, .238, .1797]
    _weights = [.125, .16, .076, .171, .267, .201]

class Transportation(BaseModel):
    _driver_classes = [
        dv.ebitda_marg, 
        dv.current,
        dv.ffo_to_debt, 
        dv.debt_to_cap,
        dv.total_assets,
    ]
    _betas = [.3033, .1145, .0897, .2924, .1111]
    _weights = [.333, .126, .098, .321, .122]
