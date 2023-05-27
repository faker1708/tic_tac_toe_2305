import gym
import random
import time
import numpy as np

class TicTacToeEnv(gym.Env):
    def __init__(self):
        # self.state = np.zeros([3, 3])
        # self.winner = None
        WIDTH, HEIGHT = 300, 300 
        # self.viewer = rendering.Viewer(WIDTH, HEIGHT)

    def reset(self):
        self.state = np.zeros([3, 3])
        self.winner = None
        self.viewer.geoms.clear() # 清空画板中需要绘制的元素
        self.viewer.onetime_geoms.clear()

    def step(self, action):
        # 动作的格式：action = {'mark':'circle'/'cross', 'pos':(x,y)}# 产生状态
        x = action['pos'][0]
        y = action['pos'][1]
        if action['mark'] == 'blue':  
            self.state[x][y] = 1
        elif action['mark'] == 'red': 
            self.state[x][y] = -1
        # 奖励
        done = self.judgeEnd() 
        if done:
            if self.winner == 'blue': 
                reward = 1 
            else:
                reward = -1
        else: reward = 0
        # 报告
        info = {}
        return self.state, reward, done, info
    

    def judgeEnd(self):
        # 检查两对角
        check_diag_1 = self.state[0][0] + self.state[1][1] + self.state[2][2]
        check_diag_2 = self.state[2][0] + self.state[1][1] + self.state[0][2]
        if check_diag_1 == 3 or check_diag_2 == 3:
            self.winner = 'blue'
            return True
        elif check_diag_1 == -3 or check_diag_2 == -3:
            self.winner = 'red'
            return True
        # 检查三行三列
        state_T = self.state.T
        for i in range(3):
            check_row = sum(self.state[i]) # 检查行
            check_col = sum(state_T[i]) # 检查列
            if check_row == 3 or check_col == 3:
                self.winner = 'blue'
                return True
            elif check_row == -3 or check_col == -3:
                self.winner = 'red'
                return True
        # 检查整个棋盘是否还有空位
        empty = []
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0: empty.append((i,j))
        if empty == []: return True
        
        return False