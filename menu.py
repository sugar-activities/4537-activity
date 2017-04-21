# menu.py
import pygame,os,g,utils

class Item():
    def __init__(self,img,x,y,r,c,n):
        self.img=img; self.x=x; self.y=y; self.r=r; self.c=c; self.n=n

class Menu(): 
    def __init__(self,nr,nc,gutter_x,gutter_y,edge): # all measurements in pixels
        self.items=[]
        x0=g.offset+gutter_x; y0=gutter_x
        total_gutter=(nc+1)*gutter_x
        pic_w=(g.sy(32)-total_gutter)/nc
        y=y0; n=0
        for r in range(nr):
            x=x0
            for c in range(nc):
                img=pygame.image.load(os.path.join('data','pics',str(n)+'.jpg'))
                if n==0:
                    smooth=True
                    w=img.get_width(); h=img.get_height()
                    pic_h=h*pic_w/w
                    try:
                        tmp=pygame.transform.smoothscale(img,(pic_w,pic_h))
                    except:
                        smooth=False
                if smooth:
                    img=pygame.transform.smoothscale(img,(pic_w,pic_h))
                else:
                    img=pygame.transform.scale(img,(pic_w,pic_h))
                item=Item(img,x,y,r,c,n); self.items.append(item)
                x+=pic_w+gutter_x; n+=1
            y+=pic_h+gutter_y
        self.pic_w=pic_w; self.pic_h=pic_h; self.gutter_y=gutter_y
        self.edge=edge
        self.green=self.items[0]; self.green_set(); self.nr=nr; self.nc=nc
        

    def draw(self):
        ind=0
        for item in self.items:
            g.screen.blit(item.img,(item.x,item.y))
            xn,yn=item.x+self.pic_w/2,int(item.y+self.pic_h+self.gutter_y/2.5)
            if item==self.green:
                pygame.draw.rect(g.screen,utils.GREEN,\
                        (item.x,item.y,self.pic_w,self.pic_h),self.edge)
            if g.best[ind]==3:
                utils.centre_blit(g.screen,g.star,(xn,yn))
            utils.display_number(g.best[ind],(xn,yn),g.font1,(135,191,47))
            ind+=1

    def check_mouse(self):
        n=self.which()
        if n>-1: self.green=self.items[n]; return True
        return False
        
    def which(self):
        for item in self.items:
            x,y=item.x,item.y
            if utils.mouse_in(x,y,x+self.pic_w,y+self.pic_h):
                return item.n
        return -1
                
    def locn(self,r0,c0):
        ind=0
        for r in range(self.nr):
            for c in range(self.nc):
                if r==r0 and c==c0: return self.items[ind]
                ind+=1
        return None

    def green_set(self):
        if self.green==None: self.green=self.items[0]
        x=self.green.x+self.pic_w/2; y=self.green.y+self.pic_h/2
        pygame.mouse.set_pos((x,y)); g.pos=(x,y)
        
    def inc_r(self):
        if self.green==None: self.green=self.items[0]; return
        r=self.green.r; c=self.green.c
        r+=1
        if r==self.nr: r=0
        self.green=self.locn(r,c); self.green_set()
        
    def dec_r(self):
        if self.green==None: self.green=self.items[0]; return
        r=self.green.r; c=self.green.c
        r-=1
        if r<0: r=self.nr-1
        self.green=self.locn(r,c); self.green_set(); return
        
    def inc_c(self):
        if self.green==None: self.green=self.items[0]
        r=self.green.r; c=self.green.c
        c+=1
        if c==self.nc: c=0
        self.green=self.locn(r,c); self.green_set(); return
        
    def dec_c(self):
        if self.green==None: self.green=self.items[0]
        r=self.green.r; c=self.green.c
        c-=1
        if c<0: c=self.nc-1
        self.green=self.locn(r,c); self.green_set()
        
        
        
                          
    
                          
                          
        
                    
                    
        
        
        
