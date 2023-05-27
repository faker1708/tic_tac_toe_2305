

from tic_tac_toe import game as g0
import random

# import time

import DQN


import torch

class main_class():

    def fm(self,mode,n_episode):

        game = self.game

        if(mode=='train'):
            epsilon = 0.9
        else:
            epsilon = 1

        # while(1):
        for i in range(n_episode):
            game.render_on = 1
            if(tt>=3):
                game.render_on = 0
            tt+=1

            exp_list = list()
            state ,flag = game.reset()
            while(1):
                if(flag ==1):
                    action = self.dqn(state,epsilon)        
                else:                 
                    action  = random.randint(0,game.action_dimension-1)

                state,flag,t,w = game.step(action)
                exp = [state,action,0]
                exp_list.append(exp)
                if(t):
                    break
                pass

            for _,exp in enumerate(exp_list):
                if(w == 1):
                    exp[2] =1
                self.dqn.store(exp)

            self.dqn.learn
            print('w',w)

                



    def main(self):
        game = g0()
        self.game = game
        tt = 0
        

        state_dimension =game.state_dimension
        action_dimension = game.action_dimension

        td_on = 0 # mc
        # td_on = 1 # td

        device = torch.device('cpu')
        # if( torch.cuda.is_available()   ):
        #     device = torch.device('cuda')
            

        self.dqn = DQN.DQN(state_dimension,action_dimension,device,td_on) # init 
        # self.dqn = dqn
        while(1):
            self.fm('train',2**5)


        return
    def __init__(self):
        self.main()

    
if __name__ == '__main__':
    b_class()