

from tic_tac_toe import game as g0
import random

import time
class main_class():


    def main(self):
        game = g0()
        tt = 0

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