

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
            epsilon = 0.5
        else:
            epsilon = 1
        # epsilon = 0.5
        # epsilon = 0.1
        
        if(mode=='show'):
            game.render_on = 1
        else:
            game.render_on = 0


        sum = 0
        sum_2 =0

        # while(1):
        for i in range(n_episode):

            exp_list = list()
            state ,flag = game.reset()
            while(1):
                if(flag ==1):
                    _,ql = self.dqn.take_action(state,epsilon)  
                    

                    # print(action)
                    if(ql): 
                        pass
                        # print('action',action,ql)      
                        # for i,ele in enumerate(ql):
                        #     if(i%6 == 6-1):
                        #         enddd = '\n'
                        #     else:
                        #         enddd = ' '
                        #     print(ele,end=enddd)
                        # print(']',action,'\n\n')

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
                    # exp[2] = 0
                    pass
                # print('exp',exp)
                self.dqn.store(exp)

            self.dqn.learn
            # print('w',i,w)
            if(w==1):
                sum+=1
            elif(w==2):
                sum_2 +=1


        if(mode == 'train'):
            print('avg',sum/n_episode,sum)
        # print('avg',sum_2/n_episode)
                



    def main(self):
        game = g0()
        self.game = game
        tt = 0
        

        state_dimension =game.state_dimension
        action_dimension = game.action_dimension -1

        td_on = 0 # mc
        # td_on = 1 # td

        device = torch.device('cpu')
        # if( torch.cuda.is_available()   ):
        #     device = torch.device('cuda')
            

        self.dqn = DQN.DQN(state_dimension,action_dimension,device,td_on) # init 
        # self.dqn = dqn
        while(1):
            self.fm('train',2**10)
            self.fm('show',2**0)


        return
    def __init__(self):
        self.main()

    
if __name__ == '__main__':
    b_class()