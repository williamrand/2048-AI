# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 01:08:24 2020

@author: willi
"""


import random
import time 
import math
import sys
import copy
from Grid import Grid
from Displayer  import Displayer

from BaseAI import BaseAI

class node:
    def __init__(self,grid):
        self.dgrid=grid
        self.data = None
        self.moves=[]
        self.nextval = []
        self.leaf=False
        self.complete=False
        self.alpha=-math.inf
        self.beta=math.inf
        self.cut=False
        self.chance=False
        self.cval=0
class IntelligentAgent(BaseAI):
    def getMove(self, grid):
    	# Selects a random move and returns it
        #if grid.getMaxTile()<8:
        #    if random.random()>.5:
        #        return 1
        #    else: 
        #        return 2
        move=self.search(grid)
        return move
    	#moveset = grid.getAvailableMoves()
    	#return random.choice(moveset)[0] if moveset else None
    def search(self,grid):
        start=time.process_time()
        depth=2
        top=self.createTree(grid,depth,start)
        found=self.minimax(top,0,-math.inf,math.inf,start)
        while(time.process_time()-start<.18) :
            
            #if(time.process_time()-start>.18):
            #    break
            depth+=1
            #self.createTreeHelp(top,0)
            top=self.createTree(grid,depth,start)
            if top==False:
                break
            hold=self.minimax(top,0,-math.inf,math.inf,start)
            if hold!=False:
                found=hold
            
            
            #top=self.createTreeHelp(top)
            #iterative depth first search
        
        
        bmove=found.moves[0]
        #print("depth:"+str(depth))
        #print("chosen value:"+ str(found.data))
        #for t in found.moves:
        #        print(t,end=" ")
        #print()
        return bmove
    def minimax(self,top,turn,alpha,beta,start):
        #will run minimax, ie go to bottom return values and prune so forth
        #print(top)
        if (time.process_time()-start>.185):
            return False
        if turn%2==0:
            nturn=1
            val=-math.inf
        else:
            nturn=0
            val=math.inf
        if top.chance==True:
            nturn=turn
            avg=0
        #alpha=-math.inf
        #beta=math.inf
        #fnode=top 
        if top.leaf==False:
            for point in top.nextval:
                #display=Displayer()
                #display.display(point.dgrid)
                #for t in point.moves:
                #    print(t,end=" ")
                #print()
                check=self.minimax(point,nturn,alpha,beta,start)
                #if check.data==None:
                #    check.data=self.evalfun2(check.dgrid)
                if check==False:
                    return False
                if top.chance==True:
                    if point.cval==2:
                        avg+=check.data*.9
                    else:
                         avg+=check.data*.1
                elif turn%2==0: #max it
                    
                    if check.data>val:
                        val=check.data
                        
                        fnode=check
                        top.data=check.data
                        if val>alpha:
                            alpha=check.data
                    if check.data>beta:
                        top.data="cut"#check.data
                        top.cut=True
                        top.leaf=True
                        break
                else: #min it
                    #print(check.data)
                    if check.data<val:
                        val=check.data
                        fnode=check
                        top.data=check.data
                        if check.data<beta:
                            beta=check.data
                    if check.data<alpha:
                        top.data="cut"#check.data
                        top.cut=True
                        top.leaf=True
                        break
            if top.chance==True:
                fnode=check
                fnode.data=avg
                return fnode
            if turn%2==0:
                
                return fnode
            else:
                
                return fnode
        else:
            
            return top #will want to return the whole node for the move paath
        return top    
    def evalfun2(self,grid):
        val=self.tiles(grid)+3*self.mono(grid)+self.smooth2(grid)
        if len(grid.getAvailableMoves())==0:
            val=0
        return val
    def tiles(self,grid):
        count=len(grid.getAvailableCells())
        val=count*11
        return val
    def smooth(self,grid):
        val=0
        for x in range(0,4):
            for y in range(0,4):
                if x!=0:
                    if grid.map[x][y]==grid.map[x-1][y]:
                        val+=x
                if y!=0:
                    if grid.map[x][y]==grid.map[x][y-1]:
                        val+=4-y
                
        return val
    
    def smooth2(self,grid):
        val=0
        for x in range(0,4):
            for y in range(0,4):
                if x!=3:
                    if grid.map[x][y]!=0 and grid.map[x+1][y]!=0:
                            val-=abs(math.log2(grid.map[x][y])-math.log2(grid.map[x+1][y]))
                    elif grid.map[x][y]!=0:
                        val-=math.log2(grid.map[x][y])
                    elif grid.map[x+1][y]!=0:
                        val-=math.log2(grid.map[x+1][y])
                if y!=3:
                    if grid.map[x][y]!=0 and grid.map[x][y+1]!=0:
                        val-=abs(math.log2(grid.map[x][y])-math.log2(grid.map[x][y+1]))
                    elif grid.map[x][y]!=0:
                        val-=math.log2(grid.map[x][y])
                    elif grid.map[x][y+1]!=0:
                        val-=math.log2(grid.map[x][y+1])
        return val           
    def mono(self,grid):
        val=0
        mx=5
        my=5
        for x in range(3,-1,-1):
            prev=0  
            for y in range(3,-1,-1): 
                if grid.map[x][y]==grid.getMaxTile():
                    mx=x
                    my=y
                    if mx ==3 and (my==0 or my==3):
                        val+=30*math.log2(grid.map[x][y])
        if grid.getMaxTile()>=2048:
            val+=60
        if my==0:
            for x in range(0,4):
                prev=0  
                for y in range(0,4):  
                    if y>0:
                        if grid.map[x][y]<=prev/2 and prev!=0:
                            val=val+(4- y)                 
                    prev=grid.map[x][y] 
            
            for y in range(0,4):
                prev=0
                for x in range(0,4):
                    if x>0:
                        if grid.map[x][y]>=prev*2 and prev!=0:
                            val=val+(x+1)
                         
                    prev=grid.map[x][y]
            
        else:
            for x in range(0,4):
                prev=0  
                for y in range(0,4):  
                    if y>0:
                        if grid.map[x][y]>=prev*2 and prev!=0:
                            val=val+(y)                 
                    prev=grid.map[x][y] 
            
            for y in range(0,4):
                prev=0
                for x in range(0,4):
                    if x>0:
                        if grid.map[x][y]>=prev*2 and prev!=0:
                            val=val+(x+1)
                         
                    prev=grid.map[x][y]
            
        return val
    
    
   
    def createTree(self,grid,depth,start): #TODO factor in the computer filling spots
        top=node(grid)
        
        queue=[]
        queue.append(top)
        for x in range(0,depth):
            nqueue=[]
            while len(queue)!=0:
                if time.process_time()-start>.185:
                    return False
                 # predict computer move
                parent=queue.pop(0)
                temp=parent.dgrid.getAvailableMoves()#list of tuples doubling deep copy on accident,
                if x%2==1 and len(parent.dgrid.getAvailableCells())<16:
                    temp=parent.dgrid.getAvailableCells()
                    if len(temp)==0:
                        if len(parent.dgrid.getAvailableMoves())==0:
                            parent.data=0
                            parent.leaf=True
                        elif x!=depth-1:
                            nqueue.append(parent)
                        else:
                            temp=parent.dgrid.getAvailableMoves()
                            for var in temp:
                                child=node(var[1])
                                parent.nextval.append(child)
                                child.moves=copy.deepcopy(parent.moves)
                                child.moves.append(var[0])
                                child.data=self.evalfun2(child.dgrid)
                                child.leaf=True
                                
                    
                    
                    parent.chance=True
                    
                    
                    
                    child1=node(parent.dgrid)
                    child1.cval=2
                    child2=node(parent.dgrid)
                    child2.cval=4
                    parent.nextval.append(child1)
                    parent.nextval.append(child2)
                    for z in parent.nextval:
                        temp=z.dgrid.getAvailableCells()
                        while (len(temp))!=0:
                            
                            mov=temp.pop()
                            ngrid=parent.dgrid.clone()
                           
                            ngrid.setCellValue(mov,z.cval)
                            child=node(ngrid)
                            z.nextval.append(child)
                            child.moves=copy.deepcopy(parent.moves)
                            #child.moves.append(mov[0])
                            if x==depth-1:
                                child.leaf=True
                                child.data=self.evalfun2(child.dgrid)
                                
                                #print(child.data)
                            else:
                                nqueue.append(child)
                else:
                    if len(temp)==0:
                        parent.leaf=True
                        parent.data=0 #self.evalfun2(parent.dgrid)
                    while (len(temp))!=0:
                        
                        mov=temp.pop()
                       
                        
                        child=node(mov[1])
                        parent.nextval.append(child)
                        child.moves=copy.deepcopy(parent.moves)
                        child.moves.append(mov[0])
                        if x==depth-1:
                            child.leaf=True
                            child.data=self.evalfun2(child.dgrid)
                            
                            #print(child.data)
                        else:
                            nqueue.append(child)
            queue=nqueue
        return top
    def createTreeHelp(self,top,turn): #will be good when we prune and only want to continue certain branches
        #destorying everything for some reason
        #display=Displayer()
        
        #display.display(top.dgrid)
        if top.leaf==True: #and top.cut==False:
            top.leaf=False
            if turn%2==0:
                temp=top.dgrid.getAvailableMoves()
                if len(temp)!=0:
                    for x in temp:
                        child=node(x[1])
                        #print(child)
                        
                        child.leaf=True
                        child.data=self.evalfun2(child.dgrid)
                        child.moves=copy.deepcopy(top.moves)
                        child.moves.append(x[0])
                else: 
                    top.leaf=True
                    top.data=0
            else:
                temp=top.dgrid.getAvailableCells()  
                if len(temp)!=0:
                    for x in temp:
                        
                        ngrid=top.dgrid.clone()
                        ngrid.setCellValue(x,2)
                        child=node(ngrid)
                        top.nextval.append(child)
                        child.moves=copy.deepcopy(top.moves)
                        child.leaf=True
                        child.data=self.evalfun2(child.dgrid)
                else:
                    temp=top.dgrid.getAvailableMoves()
                    if len(temp)==0:
                        top.data=0
                        top.leaf=True
                    else:
                        for x in temp:
                            child=node(x[1])
                            #print(child)
                            
                            child.leaf=True
                            child.data=self.evalfun2(child.dgrid)
                            child.moves=copy.deepcopy(top.moves)
                            child.moves.append(x[0])
            
        else: #top.cut==False:
            for y in top.nextval:              
                self.createTreeHelp(y,turn+1)
        
    def printTree(self,top):
        queue=[]
        layer=0
        display=Displayer()
        print(layer)
        display.display(top.dgrid)
        for y in top.nextval:
            queue.append(y)
        queue.append("!")    
        while len(queue)!=0:
            temp=queue.pop(0)
            if(temp=="!" and len(queue)!=0):
                queue.append("!")
                print("new layer")
            else:
                display.display(temp.dgrid)
                for x in temp.nextval:
                    queue.append(x)
                
            layer+=1
    def testTree(self):
        x=Grid()
        x.map[0][0]=16
        x.map[0][1]=8
        x.map[0][2]=2
        x.map[0][3]=16
        x.map[1][0]=2
        x.map[1][1]=256
        x.map[1][2]=64
        x.map[1][3]=2
        x.map[2][0]=512
        x.map[2][1]=32
        x.map[2][2]=8
        x.map[2][3]=0
        x.map[3][0]=1024
        x.map[3][1]=16
        x.map[3][2]=4
        x.map[3][3]=2
        top=self.createTree(x,6)
        found=self.minimax(top,0,-math.inf,math.inf)
        
        queue=[]
        layer=0
        display=Displayer()
        print(found.data)
        display.display(found.dgrid)
        print(layer)
        display.display(top.dgrid)
        for y in top.nextval:
            queue.append(y)
        queue.append("!")    
        while len(queue)!=0:
            temp=queue.pop(0)
            if(temp=="!" and len(queue)!=0):
                queue.append("!")
                print("new layer")
            elif temp=="break":
                print("break",end=" ")
            else:
                print(temp.data,end=" ")
                for x in temp.nextval:
                    queue.append(x)
                queue.append("break")
    def compmove(self,grid):
        temp=grid.getAvailableCells()
        spot=int(random.random()*len(temp))
        grid.map[temp[spot][0]][temp[spot][1]]=2
    def timeTest(self):
        x=Grid()
        x.map[0][0]=4
        x.map[0][1]=4
        x.map[0][2]=0
        x.map[0][3]=2
        start=time.process_time()
        
        node=self.createTree(x,4)
        print("Create Tree1:"+str(start-time.process_time()))
        y=2
        start=time.process_time()
        node=self.createTree(x,y)
        for y in range(3,6):
            self.createTreeHelp(node,0)
        print("Create TreeHelp:"+str(start-time.process_time()))    
        
    def testTree2(self):
        x=Grid()
        x.map[0][0]=4
        x.map[0][1]=4
        x.map[0][2]=0
        x.map[0][3]=2
        x.map[1][0]=16
        x.map[1][1]=128
        x.map[1][2]=32
        x.map[1][3]=2
        x.map[2][0]=512
        x.map[2][1]=256
        x.map[2][2]=512
        x.map[2][3]=32
        x.map[3][0]=1024
        x.map[3][1]=16
        x.map[3][2]=32
        x.map[3][3]=4
        display=Displayer()
        display.display(x)
        for y in range(0,15):
            top=self.createTree(x,6)
            
            found=self.minimax(top,0,-math.inf,math.inf)
            x.move(found.moves[0])
            print("goal")
            for t in found.moves:
                print(t,end=" ")
            
            #display.display(found.dgrid)
            print("Player turn: ")
            display.display(x)
            self.compmove(x)
            print("Comp turn: ")
            display.display(x)
        
        
               
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                