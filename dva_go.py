

# import dva_go_rdqn


# 本地库
import uf_set


# 前端
import pygame
import time
import sys

import matplotlib.pyplot as plt

import sys


# 后端
import random
import math
import copy

# 人工智能
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import os

import pickle



class game():


    def encode_pos(self,pos_2d):
        matrix = self.matrix
        x = pos_2d[0]
        y = pos_2d[1]
        mx = self.matrix[0] # 矩阵的列数

        pos_1d = y*mx+x
        return pos_1d

    def decode_pos(self,pos_1d):
        mx = self.matrix[0] # 矩阵的列数 一行能放几个子
        go_y = pos_1d // mx
        go_x = pos_1d % mx
        pos_2d = [go_x,go_y]
        return pos_2d
    

    def get_area(self,pos,plate):
        # 返回 0 表示 在角 返回 1 表示在边 返回 2 表示在中部。这是狭义上的概念。

        # mx  有几列，x的范围是0 mx-1 

        matrix = self.matrix
        mx = matrix[0]
        my = matrix[1]

        pos_2d =self.decode_pos(pos)
        go_x= pos_2d[0]
        go_y = pos_2d[1]

        if(go_x == 0 or go_x == mx-1):
            # 不可能 是腹了
            if(go_y==0 or go_y==my-1):
                area = 0 # 角
            else:
                area = 1
        else:
            # 不可能是角了
            if(go_y==0 or go_y==my-1):
                area = 1 # 边
            else:
                area = 2


        return area


    def get_corner_neighbor(self,pos,plate):
        cn = set()
        pos_2d = self.decode_pos(pos)
        
        pos_x = pos_2d[0]
        pos_y = pos_2d[1]


        cc = [pos_x-1,pos_y-1]
        if(self.pos_legal(cc)):
            cn.add(self.encode_pos(cc))
            
        cc = [pos_x-1,pos_y+1]
        if(self.pos_legal(cc)):
            cn.add(self.encode_pos(cc))
        cc = [pos_x+1,pos_y-1]
        if(self.pos_legal(cc)):
            cn.add(self.encode_pos(cc))
        cc = [pos_x+1,pos_y+1]
        if(self.pos_legal(cc)):
            cn.add(self.encode_pos(cc))


        return cn



    def is_true_eye(self,pos,flag,plate):
        # 狭义真眼的定义
        out = 0
        if(self.is_eye(pos,flag,plate)):
            
            area = self.get_area(pos,plate)
            cn = self.get_corner_neighbor(pos,plate)    # 合法的角的坐标

            lcn = list(cn)
            tcn_count  =  self.count_territory_in_list(flag,lcn,plate)      # 自己占领的角的个数
            
            if(area == 2 and tcn_count>=3):
                out = 1
            elif(area ==1 and tcn_count ==2):
                out =1
            elif(area ==0 and tcn_count==1):
                out = 1

        return out


    def is_eye(self,pos,flag,plate):
        # 如果是腹，要求 同色的邻居为4 至少三个角是自己的领地
        # area = 2
        area = self.get_area(pos,plate)
        same_flag_neighbor_set = self.get_filter_neighbor(pos,flag,plate)
        same_flag_neighbor_set_count = len(same_flag_neighbor_set)
        

        out = 0
        if(area == 2):
            if(same_flag_neighbor_set_count==4):
                out = 1
        elif(area == 1):
            if(same_flag_neighbor_set_count==3):
                out = 1
        elif(area == 0):
            if(same_flag_neighbor_set_count==2):
                out = 1
        return out

    def get_neighbor_set(self,pos_1d):
        neighbor_set = set()
        # raise(BaseException('dont use'))
        
        
        pos_2d = self.decode_pos(pos_1d)
        pos_x = pos_2d[0]
        pos_y = pos_2d[1]
        up_pos_2d = [pos_x,pos_y-1]
        down_pos_2d = [pos_x,pos_y+1]
        left_pos_2d = [pos_x-1,pos_y]
        right_pos_2d = [pos_x+1,pos_y]
        
        neighbor_list_2d = list()   # 不一定在棋盘内
        neighbor_list_2d.append(   up_pos_2d )
        neighbor_list_2d.append(   down_pos_2d )
        neighbor_list_2d.append(   left_pos_2d )
        neighbor_list_2d.append(   right_pos_2d )

        # 遍历这个子的邻居
        for i,neighbor_2d in enumerate(neighbor_list_2d):
            if(self.pos_legal(neighbor_2d)):    # 如果这个位置在棋盘之内
                neighbor_1d = self.encode_pos(neighbor_2d)


                neighbor_set.add(neighbor_1d)


        return neighbor_set

    def get_filter_neighbor(self,pos_1d,target_flag,plate):
        filter_neighbor = set()

        neighbor_set = self.get_neighbor_set(pos_1d)


        for neighbor_1d in iter(neighbor_set):
            n_flag = plate[neighbor_1d]
            if(n_flag== target_flag):
                filter_neighbor.add(neighbor_1d)
        return filter_neighbor


    def update_block(self,plate):
        ufs = uf_set.uf_set(len(plate))
        for pos_1d,flag in enumerate(plate):
            if(self.bug):
                if(self.bug_pos==pos_1d):
                    print(plate)
                    print('updateblock flag',plate[pos_1d])
                # print('update_block',flag)

            if(flag):
                same_flag_neighbor_set = self.get_filter_neighbor(pos_1d,flag,plate)   # 选出同色的邻居

                if(self.bug and self.bug_pos==pos_1d ):
                    print('updateblock same_flag_neighbor_set',same_flag_neighbor_set ,self.decode_pos(pos_1d),flag)
                for n in iter(same_flag_neighbor_set):
                    # if(self.bug):
                    if(self.bug and self.bug_pos==pos_1d ):


                        # ufs.unite(pos_1d,n)
                        
                        ufs.debug = 1
                        print('将它两并在一个集合中',self.decode_pos(pos_1d),self.decode_pos(n))

                    else:
                        ufs.debug = 0
                    ufs.unite(pos_1d,n)

        if(self.bug):
            print('updateblock ufs print')
            ufs.print()



        return ufs

    def pos_legal(self,pos_2d):
        x = pos_2d[0]
        y = pos_2d[1]
        matrix = self.matrix
        min_x = 0
        max_x = matrix[0]-1

        min_y = 0
        max_y = matrix[1]-1

        legal = 0
        if(x>=min_x and x<= max_x):
            if(y>=min_y and y<= max_y):
                legal = 1
        return legal

    def pos_legal_1d(self,pos_1d):
        if(pos_1d>=0):
            pos_2d = self.decode_pos(pos_1d)
            out = self.pos_legal(pos_2d)
        else:
            out = 0
        return out

    
    def blank_neighbor_of_one_go(self,pos_1d,plate):
        # 获取一个棋子的所有空邻居
        blank_neighbor_set = set()


        flag = plate[pos_1d]
        if(flag):   # 当这个位置有子时
            pos_2d = self.decode_pos(pos_1d)
            pos_x = pos_2d[0]
            pos_y = pos_2d[1]
            up_pos_2d = [pos_x,pos_y-1]
            down_pos_2d = [pos_x,pos_y+1]
            left_pos_2d = [pos_x-1,pos_y]
            right_pos_2d = [pos_x+1,pos_y]
            
            neighbor_list_2d = list()
            neighbor_list_2d.append(   up_pos_2d )
            neighbor_list_2d.append(   down_pos_2d )
            neighbor_list_2d.append(   left_pos_2d )
            neighbor_list_2d.append(   right_pos_2d )

            # 遍历这个子的邻居
            for i,neighbor_2d in enumerate(neighbor_list_2d):
                if(self.pos_legal(neighbor_2d)):    # 如果这个位置在棋盘之内
                    neighbor_1d = self.encode_pos(neighbor_2d)

                    neighbor_flag = plate[neighbor_1d]
                    if(neighbor_flag ==0 ):
                        blank_neighbor_set.add(neighbor_1d)

        return blank_neighbor_set

    def pre_pick_up(self,new_go,new_go_flag,some_plate):
        # 仿真落子
        # 输出击杀信息
        dead_set = set()

        if(new_go_flag ==1 or new_go_flag==2):  # 围棋 只有两个 阵营

            bbn = list()    # block_blank_neighbor
            for pos_1d,flag in enumerate(some_plate):
                bbn.append(set())


            # 遍历每个块，把每块中的每个子的空邻居列在一个表里。
            plate = copy.deepcopy(some_plate)   # 虚拟棋盘
            plate[new_go] = new_go_flag# 仿真落子



            ufs = self.update_block(plate)
            if(self.bug):
                
                # print('3???????',new_go_flag)
                # for i in range(len(plate)):
                #     aa = plate[i]
                #     bb = somplate[i]
                #     if(aa!=bb)

                print(plate)
                print(some_plate)

                print(plate[new_go],'应该相等 ==',new_go_flag)
                print(some_plate[new_go])
                # time.sleep(1000)
                # print(new_go_flag)
            # print('棋子',new_go, new_go_flag)

            

            for pos_1d,flag in enumerate(plate):
                if(flag):#如果有子
                    # 获取这个 子的空邻居
                    blank_neighbor_set = self.blank_neighbor_of_one_go(pos_1d,plate)


                    # print('blank_neighbor_set',blank_neighbor_set)
                    block_head = ufs.find(pos_1d)    # 这个棋子 属于哪个块？
                    
                    bs = bbn[block_head]
                    bs = bs | blank_neighbor_set    # 并集
                    bbn[block_head] = bs
            
            kill_flag = set()


            protect_go = -1
            if(self.record):
                # protect_go = self.record[-1]
                protect_go = new_go

            if(protect_go>=0):
                protect_block = ufs.find(protect_go)   # 新落子的块标记为保护块。当击杀异阵营棋子时，触发保护条款。
                protect_flag = plate[protect_go]
            else:
                # 弃手应该直接 返回 空集合，谁也杀不掉。
                protect_block = -1
                protect_flag =-1

            for pos_1d,flag in enumerate(plate):
                if(flag):#如果有子
                    
                    block_head = ufs.find(pos_1d)

                    bs = bbn[block_head]    # 这个子所在块的所有空邻居


                    qi_count = len(bs)
                    if(qi_count==0):
                        kill_flag.add(flag)


            protect = 0 # 是否触发豁免

            if protect_flag in kill_flag:
                kill_flag.remove(protect_flag)

            if(kill_flag): # 击杀了其它阵营的玩家了
                # print('触发保护')
                protect = 1
            else:
                # print('不被保护')
                protect = 0

            # print('prepick protect',protect)
            # print('prepick protect_block',self.decode_pos(protect_block))

            for pos_1d,flag in enumerate(plate):
                if(flag):#如果有子
                    
                    block_head = ufs.find(pos_1d)

                    bs = bbn[block_head]    # 这个子所在块的所有空邻居


                    qi_count = len(bs)
                    if(qi_count==0):
                        
                        # 需要建立豁免棋块的概念。
                        
                        if(protect==1):
                            if(block_head==protect_block):
                                continue    #豁免


                        dead_set.add(pos_1d)


            if(dead_set):
                for pos in iter(dead_set):
                    # print(self.decode_pos(pos))
                    pass
        
        else:
            pass
            print('wrong')
            #raise(BaseException('error at pre_pick_up flag',new_go_flag)
        return dead_set

    def pick_b(self,pos_1d,flag,plate):
        # 真的要落子


        rec = -1

        # 如果有劫，要么 更新 ，要么清空


        dead_set = set()
        if(self.pos_legal_1d(pos_1d)):
            that_flag = plate[pos_1d]
            if(that_flag>=1):
                rec = -1    # 已经有子了，判 为弃手
            else:
                # 判断是否禁入，如果禁入，则也判为-1
                rec = pos_1d
                dead_set = self.pre_pick_up(pos_1d,flag,plate)
                # print('pick_b dead_set',dead_set)

                if(len(dead_set)==1):   # 新落子吃了一个子
                    # 先检查劫
                    jie_killer = self.jie[0]
                    jie_dead = self.jie[1]
                    if(self.pos_legal_1d(jie_killer) and self.pos_legal_1d(jie_dead)):
                        # 有劫存在
                        new_killer = pos_1d
                        # new_dead = list(dead_set)[0]
                        if(   jie_killer in dead_set):
                            # print('不可落子，触发 劫保护')
                            rec = -1
                            
                            dead_set = set() # 谁也不能击杀

                            # 清除劫
                            
                            self.jie[0] = -1
                            self.jie[1] = -1

                        else:
                            self.jie[0] = pos_1d
                            self.jie[1] = list(dead_set)[0]
                            rec = pos_1d
                    else:
                        # 没有劫
                        self.jie[0] = pos_1d
                        self.jie[1] = list(dead_set)[0]
                        rec = pos_1d

                else:
                    # 吃了0 个或2个或更多子
                    # 清除劫
                    self.jie[0] = -1
                    self.jie[1] = -1

                    

        else:
            # 落子位置 非法
            # 主动弃手


            pass
        

        # 真的落子了
        if(rec>=0):
            plate[rec]=flag

        # 记录
        self.record.append(rec)


        # 返回击杀集合
        return dead_set


    def pick_up(self,dead_set,plate):
        # 真的提子了

        for ele in iter(dead_set):
            plate[ele] = 0

        return 0

    def is_neutrality(self,pos,plate):
        out = 0
        if(self.is_territory(pos,plate,1) or self.is_territory(pos,plate,2)):
            # 不中立
            pass
        else:
            out = 1
        return out


    def neutrality_set(self,plate):
        ns = set()
        for pos,flag in enumerate(plate):
            if(flag ==0):
                if(self.is_territory(pos,plate,1) or self.is_territory(pos,plate,1)):
                    pass
                else:
                    ns.add(pos)
        return ns


    def random_pos(self,flag,plate):


        blank_pos_list = list()
        for pos,flag in enumerate(plate):
            if(flag==0):
                blank_pos_list.append(pos)
        
        bpc = len(blank_pos_list)
        
        patient = bpc
        while(1):
            rp = random.choice(blank_pos_list)
            if(self.is_neutrality(rp,plate)):
                pos_out = rp
                break
            else:
                patient-=1
                # print('random patient',patient)
                if(patient<=0):
                    pos_out= -1# 没地方落子，弃手
                    break
                else:
                    blank_pos_list.remove(rp)


        return pos_out

    def matrix_to_screen(self,m_pos):
        go_x = m_pos[0]
        go_y = m_pos[1]

        
        scx = self.screen_x
        scy = self.screen_y


        matrix = self.matrix
        mxo = matrix[0]+1
        myo = matrix[1]+1

        road_width = scx/mxo # 每条路的宽度
        road_height = scy/myo


        
        s_pos = (go_x*road_width+road_width,go_y*road_height+road_height)

        return s_pos

    def screen_to_matrix(self,s_pos):
        # 将画布坐标转成棋盘坐标
        sx = s_pos[0]
        sy = s_pos[1]

        scx = self.screen_x
        scy = self.screen_y

        # # 百分比
        # px = sx/
        # py = sy/self.screen_y

        matrix = self.matrix
        mxo = matrix[0]+1
        myo = matrix[1]+1

        rw = scx/mxo # 每条路的宽度
        rh = scy/myo

        sox = sx-rw # 偏移后的当前位置的屏幕坐标
        soy = sy-rw        

        kkx = sox/rw +0.5
        kx = math.floor(kkx)

        kky = soy/rh +0.5
        ky = math.floor(kky)

        # print('坐标',kx,ky)    # 矩阵坐标
        return [kx,ky]


    def is_terminal(self):

        out = 0

        if(len(self.record)>=2**12):
            out = 1
        else:

            if(len(self.record)>=2):
                aa = self.record[-1]
                bb = self.record[-2]

                if(aa==-1 and bb==-1): # 双方 都 弃手时
                    out = 1
                else:
                    out =0
            
        return out
    
    def battle_init(self):

        self.record = list()    # 记录对局情况  # 0 2 4 表示 玩家 1 的落子 -1 表示客观弃手。不记录主观的非法行为


        matrix = self.matrix
        plate = list()
        plate_len = matrix[0]*matrix[1]
        for i in range(plate_len):
            plate.append(0)

        self.flag_count =2  # 围棋 是两个阵营的博弈

        # self.ban_pos = [-1,-1]    # 这个设计不行。


        killer = -1
        dead = -1
        self.jie = [killer,dead]    
        # 对方如果能下在 dead位置 且判断发现 能击杀 killer ，则要判 对方 弃手。
        # 当有一方击杀单个棋子时，就读写这个列表 。
        
        return plate

    def is_single_self_kill_pos(self,pos,flag,plate):
        # 
        # print('计算单子自尽点')
        # 这个函数有问题
        out = 0

        if(flag==3):
            print('single flag ==',flag)
        dead_set = self.pre_pick_up(pos,flag,plate)
        
        ld = list(dead_set)
        



        if(len(ld)==1):# 如果杀了一个
            if(pos==ld[0]): # 死者的位置是自己的位置
                # 那就是单子自杀
                out = 1

        
        if(self.tpok):
            if(out==1):
                
                opponent = 3-flag
                if(self.is_eye(pos,opponent,plate)):
                    # print('debug self kill 眼',pos)
                    pass
                else:
                    # print('debug self kill',self.decode_pos(pos))
                    pass
        return out

    def is_territory(self,pos,plate,flag):
        out = 0

        opponent = 3-flag
        that_flag = plate[pos]


        if(that_flag == flag ):
            out = 1
        elif(that_flag==0):
            # 空地
            # 眼是领土的必要条件，但不充分
            if(self.is_single_self_kill_pos(pos,opponent,plate)):
                # print('空地 is_territory',pos,flag)
                out = 1
            else:
                out = 0
        else:
            # 既不是自己的棋子，也不是空地，直接就与自己无关了
            out =0
        return out 



    def count_territory_in_list(self,flag,list_a,plate):


        # print(' count_territory_in_list list_a',list_a)
        territory_count = 0
        for _,pos_1d in enumerate(list_a):
            # print('pos_1d',pos_1d)
            flag = plate[pos_1d]

            if(self.is_territory(pos_1d,plate,flag)):
                territory_count+=1
                


        return territory_count



    def count_territory(self,flag,plate):

        territory = 0
        for pos,_ in enumerate(plate):
            
            if(self.is_territory(pos,plate,flag)):
                territory+=1
                


        return territory



    def liquidate(self,compensate,plate):
        
        score_a = 0
        score_b = 0
        territory_plate = list()
        

        for pos,flag in enumerate(plate):
            tf = -1
            if(flag==1):
                score_a+=1
                tf =1
            elif(flag==2):
                score_b+=1
                tf = 2
            elif(flag==0):
                # 如果是空地

                if(self.is_territory(pos,plate,1)):
                    tf = 1
                elif(self.is_territory(pos,plate,2)):
                    tf =2
                else:
                    tf = 0

                if(tf>0):
                    if(self.get_area(pos,plate)==2):
                        gfn = self.get_filter_neighbor(pos,tf,plate)
                        if(len(gfn)<=3):
                            self.bug = 1
                            self.bug_pos = pos
                            
                            dead_set = self.pre_pick_up(pos,3-tf,plate)
                            self.bug = 0
                            print('bug',dead_set)

                            print('liq',self.decode_pos(pos),tf,end = ' ')
                            # print('nei',self.get_filter_neighbor(pos,tf,plate))
                            for pos in iter(gfn):
                                print(self.decode_pos(pos),end = ' ')
            
                            print(' ')
            territory_plate.append(tf)

        result = [score_a,score_b,territory_plate]
        
        return result


    def rect_pos(self,x,y,width):
        # 输入一个正方形形 的中心，与边长
        # 输出它的左上坐标，宽高


        d = width
        out = ((x-d/2,y-d/2),(d,d))
        return out

    def get_state(self,flag,plate):
        # plate.append(flag)
        # print('gets',state)

        state = list()
        for i,ele in enumerate(plate):
            state.append(ele)
        state.append(flag)
        np_state = np.array(state)
        return np_state

    def act_to_pos(self,action):
        pos_1d =-1

        # state = plate.append(flag)
        # state = np.array(state)
        # state = self.get_state(flag,plate)
        if(action == self.n_actions-1): # 表示 弃手
            pos_1d= -1
        else:
            pos_1d = action
        return pos_1d

    def fm(self,mode,num_episode,black_win_rate):
        # mode : train show

        # 取全局变量
        matrix = self.matrix
        tie_mu = self.tie_mu

        if(mode == 'show'):
            kv = 0.7
            self.screen_x = 1080*kv
            self.screen_y = 1080*kv
            table_color = (255,255,64)


            bgc = (255,255,255)
            # bgc = (0,0,0)
            fgc = (255-bgc[0],255-bgc[1],255-bgc[2])

            road_width = self.screen_x/(matrix[0]+1)
            road_height = self.screen_y/(matrix[1]+1)
        

            #使用pygame之前必须初始化
            pygame.init()
            #设置主屏窗口 ；设置全屏格式：flags=pygame.FULLSCREEN
            self.screen = pygame.display.set_mode((self.screen_x,self.screen_y))
            #设置窗口标题
            pygame.display.set_caption('dva_go')

        
            font = pygame.font.Font(None, 20)
            pre_go = [-2,-2]  # 预览棋子
        elif(mode == 'train'):
            pass

        battale_mode = 0 # 机机大战

        win_count = [-1,0,0]


        # 开启新的对局
        for i in range(num_episode):
            # print(i)
            record = list()
            winner = 0
            self.tpok = 0   # 0 没结束 1 结束了
            self.tp = list()
            mouse_leave = 0 # = 1时 智人离开对局，不认输，但永久连续弃手
            plate = self.battle_init()

            flag = 1    # 1号代表先行的玩家，黑子先行，这个不变
            
            # if(mode == 'train'):
            if(1):

                # 构造数据集，保存每个回合的状态数据
                transition_dict_1 = {
                    'states': [],
                    'actions': [],
                    'next_states': [],
                    'rewards': [],
                    'dones': [],
                    # 'flag':[]   # 标记玩家的阵营
                }
                transition_dict_2 = {
                    'states': [],
                    'actions': [],
                    'next_states': [],
                    'rewards': [],
                    'dones': [],
                    # 'flag':[]   # 标记玩家的阵营
                }
                transition_dict_list = list()
                transition_dict_list.append(0)
                transition_dict_list.append(transition_dict_1)
                transition_dict_list.append(transition_dict_2)


            while(1):   # 游戏中


                
                # next_state =   np.array([bx,by,vx,vy,px,py,pvx,pvy]) 


                if(mode == 'show'):
                    # time.sleep(0.1)

                    self.screen.fill(table_color)
                    
                    # 画轴
                    for j in range(0,2):
                        for i in range(matrix[j]):
                            
                            # 轴号
                            text = font.render(str(i), True, fgc)
                            text_x = i * road_width+ road_width
                            text_y = road_height/2
                            
                            if(j==1):
                                # txx = text_y
                                text_y = i * road_height+ road_height
                                text_x = road_width/2
                            
                            self.screen.blit(text, (text_x, text_y))


                        for i in range(matrix[1-j]):
                            # print(i)
                            start_pos = (road_width,road_height*(i+1))
                            end_pos = (road_width*matrix[0],road_height*(i+1))
                            if(j==1):
                                start_pos = (road_width*(i+1),road_height)
                                end_pos = (road_width*(i+1),road_height*matrix[j])
                                pass
                            pygame.draw.line(self.screen, fgc, start_pos,end_pos, 1)


                    for kk ,ele in enumerate(plate):# 画棋子
                        
                        # 棋子在棋盘上的坐标
                        go_y = kk//matrix[0]
                        go_x = kk%matrix[0]

                        # 在画布上的坐标
                        pos = (go_x*road_width+road_width,go_y*road_height+road_height)

                        go_radius = (road_width+road_height)/2/3  # 半径   # 棋子 视觉 大小


                        if(plate[kk]==1):# 黑子 实心圆
                            # print(go_x,go_y,plate[kk])

                            pygame.draw.circle(self.screen, fgc, pos, go_radius, width=0)


                        if(plate[kk]==2):# 白子 空心圆
                            # print(go_x,go_y,plate[kk])

                            # pos = (go_x*road_width+road_width,go_y*road_height+road_height)
                            # radius = (road_width+road_height)/2/4  # 半径   # 棋子 视觉 大小
                            pygame.draw.circle(self.screen, bgc, pos, go_radius, width=0)
                            pygame.draw.circle(self.screen, fgc, pos, go_radius, width=3)


                    if(battale_mode==1 or battale_mode==2 or battale_mode==3):
                        if(flag==1):

                            pre_go_color= 'black'
                        else:
                            pre_go_color = 'white'


                        s_pos = self.matrix_to_screen(pre_go)
                        pygame.draw.circle(self.screen, pre_go_color, s_pos, go_radius, width=0)
                        if(flag==2):
                            pygame.draw.circle(self.screen, 'black', s_pos, go_radius, width=3)
                        

                    for event in pygame.event.get():    
                        if event.type == pygame.QUIT:# 关闭游戏
                            pygame.quit()
                            sys.exit()

                        
                        if event.type == pygame.MOUSEMOTION:
                            pre_go = self.screen_to_matrix(event.pos)   # 预览坐标

                        
                        if event.type == pygame.MOUSEBUTTONUP:
                            e_pos = event.pos
                            put_go = self.screen_to_matrix(e_pos)
                            pos_1d_mouse = self.encode_pos(put_go)
                            button_up = 1

                            eb = event.button
                            mouse_out_put = eb
                            # print(eb)

                            if(eb==1):# 左键
                                pass
                            elif(eb==3):    # 右键

                                if(battale_mode==3):
                                    pass
                                else:
                                    pos_1d_mouse = -1   # 拦截，改成 -1 弃手
                            elif(eb==2):
                                if(battale_mode==1):    # 人机时，人可以永久放弃落子
                                    mouse_leave = 1

                    pygame.display.flip() #更新屏幕内容

                if(battale_mode==0):# 机机大战
                    # state = self.get_state(flag,plate)
                    # print(state)
                    np_plate = np.array(plate)
                    state = np_plate

                    
                    
                    # agent = component_list[flag]
                    
                    flag1x = random.randint(0,self.player_quantity-1)
                    agent = self.agent_list[flag][flag1x]
                    action,prob,wrong = agent.take_action(state)

                    kk = 0
                    rt =0
                    if(mode == 'show'): 
                        # if(random.randint(0,2**10-1)   <= 0.5*2**10    ):
                            if(flag==2):
                                rt = 0
                                kk = 0  # 随机合理落子

                    # el
                    # if(1):
                    if(mode == 'train'):
                        if(flag==1):
                            # rt = 0.1+ (1-black_win_rate)**3
                            if(black_win_rate==0):
                                rt = 0.7
                                # print(rt)
                        elif(flag==2):
                            # rt = 0.1+black_win_rate**3
                            if(black_win_rate==1):
                                rt = 0.7
                    # rt = 0
                    if(random.randint(0,2**10-1)   < rt*2**10    ):
                        
                        while(1):
                            action = random.randint(0,self.n_actions-2)
                            pos_1d = self.act_to_pos(action)
                            if(kk):
                                pos_1d = self.random_pos(flag,plate)
                                if(pos_1d==-1):
                                    action = self.n_actions-1
                                else:
                                    action = pos_1d
                                break
                            if(plate[pos_1d]==0):
                                break
                        # action = random.randint(0,22)


                    if(wrong==1):
                        return 0,1
                    pos_1d = self.act_to_pos(action)

                    rr = list()
                    rr .append(flag)
                    rr.append(pos_1d)
                    record.append(rr)

                if(battale_mode==3 and flag ==0 ):
                    # 打谱时清除棋子
                    plate[pos_1d] = 0
                    pass
                else:
                    # 常规对局
                    # 落子，修改棋盘
                    dead_set = self.pick_b(pos_1d,flag,plate)   # 击杀清单
                    # 提子 ，修改棋盘
                    self.pick_up(dead_set,plate)
                    # next_state = self.get_state(flag,plate)
                    next_state = np.array(plate)

                    # if(mode == 'train'):
                    if(1):

                        done = self.tpok
                        transition_dict_list[flag]['states'].append(state)
                        transition_dict_list[flag]['actions'].append(action)
                        transition_dict_list[flag]['next_states'].append(next_state)
                        transition_dict_list[flag]['rewards'].append(0)    # 对局结束前不给奖励
                        transition_dict_list[flag]['dones'].append(done)
                        # transition_dict_list[flag]['flag'].append(flag)

                    if(self.is_terminal()):
                        # print('对局结束，开始 清算')
                        # print('棋谱',self.record)
                        result = self.liquidate(tie_mu,plate)
                        
                        if(mode == 'show'):
                            # print('result',result)
                            pass
                        self.tp = result[2] # 领地分布
                        self.tpok = 1
                        sa = result[0]
                        sb = result[1]
                        if(sa-tie_mu>sb):
                            winner = 1
                        else:
                            winner = 2

                    else:# 对局尚未结束
                        state = next_state                        
                        if(battale_mode==3):

                            pass
                        else:
                            flag  = 3-flag      # 12 交替 黑白

                if(self.tpok):
                    if(mode == 'show'):
                        # tf_rect = ()
                        tf_rect_width = road_width/4
                        # print('t_plate,',self.tp)
                        # print('t_plate,',plate)
                        tcl = ['red','black','white']
                        for pos,tf in enumerate(self.tp):
                            if(tf<=0):
                            # if(plate[pos]>0):
                                continue
                            else:
                                kk= pos
                                bgcdd = tcl[tf]
                                
                                go_y = kk//matrix[0]
                                go_x = kk%matrix[0]

                                # 在画布上的坐标
                                pos = (go_x*road_width+road_width,go_y*road_height+road_height)
                                pygame.draw.circle(self.screen, bgcdd, pos, 8, width=0)
                                # bgcdd= 'weofjoweifjo'

                                # break
                        pygame.display.flip() #更新屏幕内容
                        # time.sleep(3)
                    break

            # if(mode == 'train'):
                
            if(1):
                # 一局游戏结束
                win_count[winner]+=1

                l_rewards = transition_dict_list[winner]['rewards']
                for ii ,ele in enumerate(l_rewards):
                    # if(l_flag[ii]==winner):  # 如果这样下能赢，就给1的奖励
                        l_rewards[ii]=1
                

                # 随机谁来学习
                flag1x = random.randint(0,self.player_quantity-1)
                flag2x = random.randint(0,self.player_quantity-1)
                component_list= list()  # 随机从两个阵营各选两个棋手
                component_list.append(0)
                component_list.append(self.agent_list[1][flag1x])
                component_list.append(self.agent_list[2][flag2x])

                for ia,agent in enumerate(component_list):
                    if(ia>=1):
                        if(not kk):
                            agent.learn(transition_dict_list[ia])
                #########

            
        return win_count[1]/num_episode,0


    def main(self):

        
        player_quantity = 2**2  # 每个阵营有几个军师

        plt_on = 0  # 是否显示图表

        if(plt_on ==1):
            plt.ion()
            plt.figure(1)
            t_list = list()
            black_win_rate_list = list()
        self.bug = 0
        # 全局常量

        # 游戏参数
        column = 9
        row = 9
        self.tie_mu = 0+0.5


        self.matrix = [column,row] # 列数，行数

        # 人工智能参数
        n_states = column* row +0 
        n_actions = column* row +1 # 多一个表弃手

        self.n_actions = n_actions
        
        # device = torch.device('cpu')
        # if(torch.cuda.is_available()):
        #     device = torch.device('cuda')

        device = torch.device('cuda') if torch.cuda.is_available() \
                                    else torch.device('cpu')


        self.player_quantity = player_quantity
        
        ie = 0        

        save_pace = 5
        folder_path = './model'
        while(1):
            # print("\n\n")
            if(plt_on ==1):
                t_list = list()
                black_win_rate_list = list()
                plt.close()
            files= os.listdir(folder_path)
            if(files):
                load = 1
                # print('files',files)
                max = -1
                ln = list()
                for _,ele in enumerate(files):
                    num = int(ele.split('.')[0])
                    ln.append(num)
                    # if(num>max):
                        # max = num
                ln.sort()
                # print(ln)
                if(1 <= len(files)):
                    ie = ln[-1]
                else:
                    ie = 0

            else:
                load= 0
                ie = 0
            if(load):
                    # print(int(num),'wefwef')
                # ie = 96
                # print('load',ie)
                with open('./model/'+str(ie)+'.pkl', "rb") as f:
                    self.agent_list = pickle.load(f)
            else:
                print('new')
                self.agent_list = list()
                self.agent_list.append(0)   # 0阵营是空的，不需要棋手

                for _ in range(0,2):
                    flag_x_player_list = list()
                    for j in range(0,player_quantity):
                        ax = RL_brain.PPO(n_states=n_states,  # 状态数
                            n_actions=n_actions,  # 动作数
                            actor_lr=1e-3,  # 策略网络学习率
                            critic_lr=1e-2,  # 价值网络学习率
                            lmbda = 0.95,  # 优势函数的缩放因子
                            epochs = 10,  # 一组序列训练的轮次
                            eps = 0.2,  # PPO中截断范围的参数
                            gamma=0.9,  # 折扣因子
                            device = device
                            )
                        flag_x_player_list.append(ax)
                    self.agent_list.append(flag_x_player_list)

                ie = 0        

            black_win_rate = 0.5
            while(1):
                ie = ie + 1
                # print(ie)
                black_win_rate,wrong = self.fm('train',2**4,black_win_rate)
                if(wrong):
                    save_pace -= 1                   
                    if(save_pace<=0):
                        files= os.listdir(folder_path)
                        # ln = list()
                        max = -1
                        for _,ele in enumerate(files):
                            num = int(ele.split('.')[0])
                            # ln.append(num)
                            if(num>max):
                                max = num
                        if(max>0):
                            last_file = folder_path+'/'+str(max)+'.pkl'
                            os.remove(last_file)
                            # print('remove',last_file)
                        save_pace = 5
                        break

                    # print('meet wrong',save_pace) 
                    
                    if(plt_on ==1):
                        t_list = list()
                        black_win_rate_list = list()
                        plt.close()

                    break


                # w,wr = self.fm('show',2**0,black_win_rate)
                # print('w',w)
                # if(w==1):
                #     print('1')
                # else:
                #     print('2')


                if(ie % 2**save_pace==0):
                    with open('./model/'+str(ie)+'.pkl', "wb") as f:
                            pickle.dump(self.agent_list, f)
                    # print('\n')
                    print('save',ie,black_win_rate)
                    # print('\n')
                    # print(ie,black_win_rate)
                    
                    if(plt_on ==1):
                        plt.close()
                        t_list = list()
                        black_win_rate_list = list()

                    # save_pace +=1
                    # if(save_pace>5):save_pace = 5
                    save_pace = 5
                
                # print('black_win_rate',black_win_rate)
                if(plt_on ==1):
                    t_list.append(ie)
                    black_win_rate_list.append(black_win_rate)
                    
                    if(black_win_rate==0 or black_win_rate==1):
                        print(ie,black_win_rate)
                    # print(t_list,black_win_rate_list)
                    # print(t_list[-1],black_win_rate_list[-1])
                    plt.plot(t_list,black_win_rate_list,c='blue')
                    plt.pause(0.001)

        return

    def __init__(self):

        
        # 游戏参数
        column = 9
        row = 9
        self.tie_mu = 0+0.5


        self.matrix = [column,row] # 列数，行数
        print('weoije')



        return
    