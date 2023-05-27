
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np




# 本地类
import Net



class DQN(object):
    def __init__(self,N_STATES,N_ACTIONS,device,td_on):


        # mlp_architecture 是一个列表，描述了要求的神经网络的结构 每层几个神经元
        # N_STATES 是输入层神经元的个数
        # N_ACTIONS 是输出层神经元的个数
        
        self.MEMORY_CAPACITY = 2000
        self.N_STATES = N_STATES
        self.N_ACTIONS = N_ACTIONS
        lr = 0.01

        self.device = device

        self.eval_net=Net.Net(N_STATES,N_ACTIONS,device).to(device)

        if(td_on):
            self.target_net = Net.Net(N_STATES,N_ACTIONS,device).to(device)
            self.learn = self.__learn_td
            print('class DQN 时序差分模式')
        else:
            self.learn = self.__learn_mc
            print('class DQN 蒙特卡洛模式')




        self.learn_step_counter = 0                                     # for target updating
        self.memory_counter = 0                                         # for storing memory
        self.memory = np.zeros((self.MEMORY_CAPACITY, self.N_STATES * 2 + 2))     # initialize memory
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr)
        self.loss_func = nn.MSELoss()


    def random_action(self):

        N_ACTIONS = self.N_ACTIONS
        action = np.random.randint(0, N_ACTIONS)
        return action
    

    def take_action(self, state,EPSILON):
        x = state
        x = torch.unsqueeze(torch.FloatTensor(x), 0)

        # EPSILON = self.epsilon
        ql = []

        if np.random.uniform() < EPSILON:   # greedy
            actions_value = self.eval_net.forward(x)
            actions_value = actions_value.to('cpu')
            
            # actions_value=torch.clamp(actions_value,0,1)

            ql = actions_value.tolist()[0]
            action = torch.max(actions_value, 1)[1].data.numpy()
            action = action[0] 
        else:   # random
            action = self.random_action()


        return action,ql

    # def store_transition(self, state, a, r, s_):
    def store(self, exp):

        state= exp[0]
        a = exp[1]
        r = exp[2]
        s_ = state
        MEMORY_CAPACITY=2000

        transition = np.hstack((state, [a, r], s_))
        # replace the old memory with new memory
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

        
    def __learn_mc(self):
        MEMORY_CAPACITY = 2000
        BATCH_SIZE = 32
        N_STATES = self.N_STATES

        device = self.device


        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)
        b_memory = self.memory[sample_index, :]
        b_s = torch.FloatTensor(b_memory[:, :N_STATES]).to(device)
        b_a = torch.LongTensor(b_memory[:, N_STATES:N_STATES+1].astype(int)).to(device)
        b_r = torch.FloatTensor(b_memory[:, N_STATES+1:N_STATES+2]).to(device)


        q_eval = self.eval_net(b_s).gather(1, b_a)
        q_target = b_r
        loss = self.loss_func(q_eval, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()