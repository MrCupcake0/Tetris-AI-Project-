import random 



class Random_Agent:
    def __init__(self,env):
        self.env = env
    
        
    def get_Action(self, events = None, state = None):
        actions, __ = self.env.get_legal_actions(state)
        idx = random.randrange(len(actions))
        return actions[idx],0

        # return random.randint(0,4), None