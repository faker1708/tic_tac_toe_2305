

import pygame
import time
import os

class game():

    def __init__(self):
        self.__main()
        return 
    
    def reset(self):
        plate_len = self.wide* self.height
        plate = list()
        for _ in range(plate_len):
            plate.append(0)
        
        flag = 1

        self.__render_reset()
        self.__terminate = 0


        self.__record = list()
        self.plate = plate
        self.flag= flag
        return [plate,flag]

    def step(self,action):
        # flag = self.flag
        plate = self.plate

        pos_1d =self.__action_to_pos(action)
        if(pos_1d>=0):
            if(plate[pos_1d]==0):
                plate[pos_1d] = self.flag
            else:
                pos_1d = -1 # 判为弃手
        else:
            pos_1d = -1

        self.__record.append(pos_1d)
        
        terminate,winner = self.__is_terminate()
        # if(terminate==1):

        # if(self.render_on):
        self.__render()

        # print(self.flag)
        self.flag = 3-self.flag

        return [plate,self.flag,terminate,winner]
    
    def __main(self):
        
        self.render_on = 0

        self.wide = 3
        self.height = 3
        
        self.action_dimension = self.wide*self.height+1  # 多一个是弃手
        self.state_dimension = self.wide*self.height

    def __pos_legal(self,pos_2d):
        x = pos_2d[0]
        y = pos_2d[1]
        # matrix = self.matrix
        min_x = 0
        max_x = self.wide-1

        min_y = 0
        max_y = self.height-1

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
            if(flag==0):continue    # 0 是空地不能算啊。。
            pos_2d = self.__decode_pos(pos_1d)

            for direction in range(2+1):      # 选择一个检查方向 0 1 2
                # print('direction',direction)
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
                    
                    ok = 1
                    for _,peer_1d in enumerate(peer_list):
                        p_flag = plate[peer_1d]
                        # print('p f',p_flag,flag)
                        if(p_flag != flag ):
                            ok = 0
                            break
                    if(ok):
                        # print('terminate 连珠了',flag)
                        terminate = 1
                        terminater = flag
                        # return [terminate,terminater]
                        break
                    else:

                        terminate = 0
                        terminater = 0
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
                #
                # print(' 再检查 是否双方同时弃手')
                record = self.__record
                # print('record ',record)
                if(len(record)>=2):
                    if(record[-1]==-1 and record[-2]==-1):
                        # print('双方同时弃手了')
                        terminate = 1
                        terminater = 0
                        # 平局


            # if(terminate):
            #     print('terminate','没有连珠的')

        self.__terminate = terminate
        return [terminate,terminater]
    
    def __action_to_pos(self,action):
        pos_1d =-1

        # state = plate.append(flag)
        # state = np.array(state)
        # state = self.get_state(flag,plate)
        # print('__action_to_pos action_dimension',self.action_dimension)
        if(action == self.action_dimension-1): # 表示 弃手
            pos_1d= -1
            # print('弃手')
        else:
            pos_1d = action
        return pos_1d
    
    def __encode_pos(self,pos_2d):
        # matrix = self.matrix
        x = pos_2d[0]
        y = pos_2d[1]
        mx = self.wide # 矩阵的列数

        pos_1d = y*mx+x
        return pos_1d

    def __decode_pos(self,pos_1d):
        mx = self.wide # 矩阵的列数 一行能放几个子
        go_y = pos_1d // mx
        go_x = pos_1d % mx
        pos_2d = [go_x,go_y]
        return pos_2d
    
    def __render_reset(self):
        
        if(self.render_on):
            kv = 0.7
            self.screen_x = 1080*kv
            self.screen_y = 1080*kv
            table_color = (255,255,64)


            bgc = (255,255,255)
            # bgc = (0,0,0)
            fgc = (255-bgc[0],255-bgc[1],255-bgc[2])

        

            #使用pygame之前必须初始化
            pygame.init()
            #设置主屏窗口 ；设置全屏格式：flags=pygame.FULLSCREEN
            self.screen = pygame.display.set_mode((self.screen_x,self.screen_y))
            #设置窗口标题
            pygame.display.set_caption('dva_tic_tac_toe')

    def __render(self):
        
        if(self.render_on):
            road_width = self.screen_x/(self.wide+1)
            road_height = self.screen_y/(self.height+1)

            table_color = 'white'
            flag_color = [0,'deeppink','blue']
            self.screen.fill(table_color)

            plate = self.plate

            font = pygame.font.Font(None, 20)
            matrix = [self.wide,self.height]
            fgc = 'black'
            # 画轴
            for j in range(0,2):
                for i in range(matrix[j]):
                    
                    # 轴号
                    text = font.render(str(i), True, 'black')
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
                    end_pos = (road_width*self.wide,road_height*(i+1))
                    if(j==1):
                        start_pos = (road_width*(i+1),road_height)
                        end_pos = (road_width*(i+1),road_height*matrix[j])
                        pass
                    pygame.draw.line(self.screen, fgc, start_pos,end_pos, 1)

            # 画棋子
            for kk ,ele in enumerate(plate):
                
                # 棋子在棋盘上的坐标
                go_y = kk//self.wide
                go_x = kk%  (self.wide)

                # 在画布上的坐标
                pos = (go_x*road_width+road_width,go_y*road_height+road_height)

                go_radius = (road_width+road_height)/2/3  # 半径   # 棋子 视觉 大小


                if(plate[kk]==1):
                    # print(go_x,go_y,plate[kk])

                    pygame.draw.circle(self.screen, flag_color[1], pos, go_radius, width=0)


                if(plate[kk]==2):
                    # print(go_x,go_y,plate[kk])

                    # pos = (go_x*road_width+road_width,go_y*road_height+road_height)
                    # radius = (road_width+road_height)/2/4  # 半径   # 棋子 视觉 大小
                    pygame.draw.circle(self.screen, flag_color[2], pos, go_radius, width=0)
                    # pygame.draw.circle(self.screen, fgc, pos, go_radius, width=3)
            
            pygame.display.flip() #更新屏幕内容
            if( self.__terminate == 1):
                print(self.__record)
                time.sleep(2)
                # os.system('cls')

        return 