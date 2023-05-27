

from tic_tac_toe import tic_tac_toe
import random

import time
class main_class():


    def main(self):
        game = tic_tac_toe()

        while(1):
            game.render_on = 1
            state ,flag = game.reset()
            # print(state,flag)

            # r = [0,1,3,4,6,7]
            i = 0
            while(1):
                # if(i>=6):
                #     time.sleep(100)
                # action = r[i]
                i+=1
                action  = random.randint(0,game.action_dimension-1)
                
                # action = 9
                # state,flag,t,w =game.step(action)

                xxx = game.step(action)
                # print(xxx[1])
                print(xxx)
                # print(state,flag,t,w)
                if(xxx[2]):
                    print('结束')
                    import os
                    time.sleep(2)
                    os.system('cls')
                    break
                pass
                


        return
    def __init__(self):
        self.main()

    
if __name__ == '__main__':
    b_class()