

from tic_tac_toe import game as g0
import random

import time
class main_class():


    def main(self):
        game = g0()
        tt = 0
        

        action_dimension = game.action_dimension
        state_dimension =game.state_dimension

        td_on = 0 # mc
        # td_on = 1 # td

        device = torch.device('cpu')
        if( torch.cuda.is_available()   ):
            device = torch.device('cuda')
            
        device = torch.device('cpu')    

        while(1):
            game.render_on = 1
            if(tt>=3):
                game.render_on = 0
            tt+=1

            
            state ,flag = game.reset()
            while(1):
                action  = random.randint(0,game.action_dimension-1)
                

                state,flag,t,w = game.step(action)
                if(t):
                    break
                pass

            print('w',w)
                


        return
    def __init__(self):
        self.main()

    
if __name__ == '__main__':
    b_class()