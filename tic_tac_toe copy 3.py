

import pygame


class tic_tac_toe():




    def __init__(self,render = 1):
        self.__main(render)

        return 
    


    def reset(self):
        plate_len = self.wide* self.hight
        plate = list()
        for _ in range(plate_len):
            plate.append(0)
        
        flag = 1

        self.__record = list()
        self.plate = plate
        self.flag= flag
        return [plate,flag]


    def step(self,action):
        flag = self.flag
        plate = self.plate

        pos_1d =self.__action_to_pos(action)
        if(plate[pos_1d]==0):
            plate[pos_1d]=flag
        
        self.__is_terminate()


        flag = 3-flag

        self.flag = flag

        return [plate,flag]
    
    def __pos_legal(self,pos_2d):
        x = pos_2d[0]
        y = pos_2d[1]
        # matrix = self.matrix
        min_x = 0
        max_x = self.wide-1

        min_y = 0
        max_y = self.hieght-1

        legal = 0
        if(x>=min_x and x<= max_x):
            if(y>=min_y and y<= max_y):
                legal = 1
        return legal
    
    def __get_peer(self,pos_2d,i:int,direction:int):
        peer = list()
        x = pos_2d[0]
        y = pos_2d[1]
        if(direction==0):   # right
            px = x+i
            py = y
        elif(direction == 1):   # right_down
            px = x+i
            py = y+i
        elif(direction == 2):#'down')
            px = x
            py = y+i
        else:
            raise(BaseException('direction illegal ,example 0 1 2'))

        # peer.append(px)
        # peer.append(py)
        peer = [px,py]
        return peer

    def __is_terminate(self):
        
        #　 首先检查是否有子连成串
        # 然后检查棋盘是否已经满了，满了就判平局
        # 然后检查是否双方都弃手，都弃手也判断结束，且是平局

        flag = self.flag
        plate = self.plate

        target = 3  # 连成三子即可，也就是三子棋

        # 遍历每个子
        # 选择一个检查方向
        # 获取该方向上的连续几个子的位置
        # 如果位置合法。则判断是否同色。

        terminate = 0
        terminater = 0  # 赢家

        for pos_1d,flag in enumerate(plate): # 遍历每个子
            # right 向右检查
            pos_2d = self.__decode_pos(pos_1d)

            for direction in range(2):      # 选择一个检查方向
                peer_list = list()  #包含自己
                br = 0
                for i in range(target): #取三个子的位置来，包含自己 # 获取该方向上的连续几个子的位置
                    peer = self.__get_peer(pos_2d,i,direction)
                    # peer = [peer_x,perr_y]
                    if(self.__pos_legal(peer)):
                        peer_1d = self.__encode_pos(peer)
                        peer_list.append(peer_1d)
                    else:
                        br = 1
                        break
                if(br ==0):
                    # 检查是否同色  # 如果位置合法。则判断是否同色。
                    for _,peer_1d in enumerate(peer_list):
                        p_flag = plate[peer_1d]
                        if(p_flag == flag ):
                            terminate = 1
                            terminater = flag
                            break
            if(terminate == 1):
                break
            
        if(terminate ==0):
            # 如果尚未结局，则检查棋盘是否满了，井字栱是有平局的
            tt = 1
            for pos_1d,flag in enumerate(plate):
                if(plate[pos_1d] ==0):
                    tt = 0  #存在某处无子
                    break
            if(tt==1):
                # 全都有子了
                terminate = 1
                terminater = 0
                # 平局
            else:
                # 再检查 是否双方同时弃手
                record = self.__record
                if(len(record)>=2):
                    if(record[-1]==-1 and record[-2]==-1):
                        terminate = 1
                        terminater = 0
                        # 平局
        
        return [terminate,terminater]
    
    def __main(self,render):
        
        self.render = render

        self.wide = 3
        self.hight = 3
        
        self.action_dimension = self.wide*self.hight+1  # 多一个是弃手

    def __action_to_pos(self,action):
        pos_1d =-1

        # state = plate.append(flag)
        # state = np.array(state)
        # state = self.get_state(flag,plate)
        if(action == self.action_dimension-1): # 表示 弃手
            pos_1d= -1
        else:
            pos_1d = action
        return pos_1d
    

    def __encode_pos(self,pos_2d):
        matrix = self.matrix
        x = pos_2d[0]
        y = pos_2d[1]
        mx = self.matrix[0] # 矩阵的列数

        pos_1d = y*mx+x
        return pos_1d

    def __decode_pos(self,pos_1d):
        mx = self.matrix[0] # 矩阵的列数 一行能放几个子
        go_y = pos_1d // mx
        go_x = pos_1d % mx
        pos_2d = [go_x,go_y]
        return pos_2d
    


    def render(self):



        return 