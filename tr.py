# tr.py

import utils,pygame,random,g

rc=((2,4),(3,6),(4,8))
table=((0,1,2,3,4,5,6,7),\
       (1,2,3,0,5,6,7,4),\
       (2,3,0,1,6,7,4,5),\
       (3,0,1,2,7,4,5,6),\
       (4,7,6,5,0,3,2,1),\
       (5,4,7,6,1,0,3,2),\
       (6,5,4,7,2,1,0,3),\
       (7,6,5,4,3,2,1,0))

class piece:
    def __init__(self,img0,r,c,x,y):
        self.img0=img0; self.r=r; self.c=c; self.x=x; self.y=y

class Tr:
    
    def __init__(self,n): # 1,2,3 (level)
        self.nr,self.nc=rc[n-1]
        w=g.pic.get_width(); h=g.pic.get_height()
        dx=w/self.nc; dy=h/self.nr; self.dd=min(dx,dy)
        offset_x=(g.sy(32)-self.nc*self.dd)/2; offset_y=offset_x
        self.target_c=(g.sx(16),offset_y+h/2)
        self.pieces=[]
        y=0
        for r in range(self.nr):
            x=0
            for c in range(self.nc):
                img0=g.pic.subsurface(x,y,self.dd,self.dd)
                pce=piece(img0,r,c,x+g.offset+offset_x,y+offset_y)
                self.pieces.append(pce)
                x+=self.dd
            y+=self.dd
        d=g.sy(.25); x=g.offset+offset_x; y=offset_y
        w=self.nc*self.dd; h=self.nr*self.dd
        self.xywhd=x,y,w,h,d

    def setup(self):
        self.green=self.pieces[1]
        for pce in self.pieces:
            rnd=random.randint(1,7); pce.state=rnd
            self.transf(pce)
        pce=self.pieces[0]; pce.state=0; self.transf(pce)
        self.target=self.nr*self.nc-1
        for pce in self.pieces:
            if pce.state>4: self.target+=1
        self.target=int(self.target*1.4)
        self.finished=False; self.count=0; self.success=False

    def transf(self,pce):
        state=pce.state; img=pce.img0
        if state in (0,4): a=0
        elif state in (1,5): a=90
        elif state in (2,6): a=180
        elif state in (3,7): a=270
        if a!=0: img=pygame.transform.rotate(img,-a)
        if state>3: img=pygame.transform.flip(img,True,False)
        pce.img=img

    def draw(self):
        for pce in self.pieces:
            g.screen.blit(pce.img,(pce.x,pce.y))
        x,y,w,h,d=self.xywhd
        utils.obox(g.screen,utils.CREAM,x,y,w,h,d)
        if not self.complete():
            d=g.sy(.2); x=self.green.x; y=self.green.y; s=self.dd
            pygame.draw.rect(g.screen,utils.GREEN,(x,y,s,s),d)
        if self.count==0:
            utils.centre_blit(g.screen,g.target,self.target_c)
            self.number(self.target)
        else:
            s=str(self.count)+' / '+str(self.target)
            rect=utils.text_blit(g.screen,s,g.font2,g.score_c,utils.CREAM,False)
            if self.count>self.target:
                utils.text_blit1(g.screen,str(self.count),g.font2,\
                                 (rect.x,rect.y),utils.RED,False)
        if self.count>self.target:
            for pce in self.pieces:
                if pce.state!=0:
                    d=g.sy(.1); x=pce.x; y=pce.y; s=self.dd
                    pygame.draw.rect(g.screen,utils.RED,(x,y,s,s),d)
                    

    def button(self,bu):
        pce=self.green
        n=int(bu); current_state=pce.state
        pce.state=table[current_state][n]
        self.transf(pce)
        self.count+=1
        self.complete()
            
    def complete(self):
        if self.finished: return True
        for pce in self.pieces:
            if pce.state!=0: return False
        self.finished=True
        if self.count<=self.target: # success
            self.success=True
            if g.level>g.best[g.pic_n]: g.best[g.pic_n]=g.level
        return True
    
    def set_green(self,r,c):
        ind=self.nc*r+c
        self.green=self.pieces[ind]
        
    def click(self):
        first=True
        for pce in self.pieces:
            if not first:
                if utils.mouse_in(pce.x,pce.y,pce.x+self.dd,pce.y+self.dd):
                    self.green=pce; return True
            first=False
        return False
        
    def left(self):
        r=self.green.r; c=self.green.c
        c-=1
        if c<0: c=self.nc-1
        if r==0 and c==0: c=self.nc-1
        self.set_green(r,c)

    def right(self):
        r=self.green.r; c=self.green.c
        c+=1
        if c==self.nc: c=0
        if r==0 and c==0: c=1
        self.set_green(r,c)

    def up(self):
        r=self.green.r; c=self.green.c
        r-=1
        if r<0: r=self.nr-1
        if r==0 and c==0: r=self.nr-1
        self.set_green(r,c)

    def down(self):
        r=self.green.r; c=self.green.c
        r+=1
        if r==self.nr: r=0
        if r==0 and c==0: r=1
        self.set_green(r,c)

    def number(self,n):
        if n<10:
            utils.centre_blit(g.screen,g.digits[n],self.target_c)
        else:
            dx=g.sy(.6)
            n1=n/10; n2=n-n1*10; img1=g.digits[n1]; img2=g.digits[n2]
            x,y=self.target_c; y-=img1.get_height()/2
            xoffset=(img1.get_width()-img2.get_width())/2
            g.screen.blit(img1,(x-img1.get_width()+dx+xoffset,y))
            g.screen.blit(img2,(x-dx+xoffset,y))
            

                
