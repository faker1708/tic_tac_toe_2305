

from tic_tac_toe import tic_tac_toe
import random

class b_class():


    def main(self):
        game = tic_tac_toe()

        while(1):
            game.render_on = 1
            state ,flag = game.reset()
            # print(state,flag)
            while(1):
                action  = random.randint(0,game.action_dimension-1)
                # state,flag,t,w =game.step(action)

                xxx = game.step(action)
                print(xxx[1])
                # print(state,flag,t,w)
                if(xxx[2]):
                    break
                pass
                


        return
    def __init__(self):
        self.main()

    
if __name__ == '__main__':
    b_class()