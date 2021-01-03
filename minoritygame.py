from utils import *

class Strategy:
    def __init__(self):
        self.score = 0 # Strategy' initial score
        self.Responses = {} # Dict obj. for recording the action for each input (key)
    def init(self, state):
        self.Responses[state] = rand_pm() # rand_pm() generates randomly either -1 or 1
    def act(self, state): # act according to the current state (the global info)
        if not state in self.Responses: self.init(state)
        return self.Responses[state]
    def update(self, v=1):
        self.score += v #update the score by adding v to it

class User:
    def __init__(self, s=2):
        self.s = s # number of strategies a user can have
        self.Strategies = [Strategy() for i in range(self.s)] # the user's strategies
        self.action = None # for recording the user's latest action
        self.score = 0 #the user's score, i.e., cumulative number of wins
        self.acted = False # signal telling if the user has acted
 
    def act(self, state):
        self.state = state # recording the current global information 
        # respond using the best strategy
        self.strategy_id = max_idx([x.score for x in self.Strategies])
        self.action = self.Strategies[self.strategy_id].act(state) #from the current state get the action
        self.acted = True # signal that the user has acted
         
    def update(self,w):
        # update the scores of the strategies based on if the user loses or wins
        assert self.acted, 'act() first before update()'
        # update the score of the strategies
        for strategy in self.Strategies:
            ds = bool_pm(strategy.act(self.state) == w)
            strategy.update(ds)
        # update the score of the user
        self.score += ds
        self.acted = False # reset the signal

class System:
    def __init__(self, T = 1, N = 101, m=3, s=2):
        self.T = T # number of steps to run each time
        self.N = N # number of users
        self.m = m # memory length
        self.s = s # number of strategies for each user
        self.Users = [User(s=self.s) for i in range(self.N)] #initialize the users
        self.Prices = [0] # for storing the prices, initialize it with zero
        self.SuccessRates = [] # for storing the global success rates
        self.W = [rand_pm() for i in range(self.m)]# initialize global info (i.e. the winning actions)
        self.D = [] # net actions. sum_i a_i, where a_i is the i-th user's action +1 or -1
 
    @property
    def d(self): # current net action
        d = 0
        for u in self.Users:
            d += u.action
        return d
     
    def update(self):
        d = self.d
        self.D.append(d)
        self.W.append(minority(d))
        rate = (self.N-abs(d))/(2.0*self.N) # the success rate
        self.SuccessRates.append(rate)
        d = d/float(self.N) # normalize by N to get the price
        self.Prices.append(self.Prices[-1] + d) # update the price
             
    @property
    def state(self):
        return w2s(self.W[-self.m:]) # from memory to the strategy id
           
    def run(self):
        for t in range(self.T):
            state = self.state
            for u in self.Users:
                u.act(state)
            self.update()
            for u in self.Users:
                u.update(self.W[-1])