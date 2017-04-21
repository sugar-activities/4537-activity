# g.py - globals
import pygame,utils,random

app='Trans'; ver='1'
ver='21'
ver='22'
# retains current pic state
ver='23'
# double click to get new picture - fixed layout for any resolution
ver='24'
# wrong pic bug fixed
ver='25'
# wrong pic bug fixed
ver='26'
# new pic on menu pic click always
# fixed widescreen layout

UP=(264,273)
DOWN=(258,274)
LEFT=(260,276)
RIGHT=(262,275)
CROSS=(259,120)
CIRCLE=(265,111)
SQUARE=(263,32)
TICK=(257,13)
NUMBERS={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,\
           pygame.K_5:5,pygame.K_6:6,pygame.K_7:7,pygame.K_8:8,\
           pygame.K_9:9,pygame.K_0:0}

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(40*imgf); font1=pygame.font.Font(None,t)
        t=int(80*imgf); font2=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    
    # this activity only
    global level,pic,arrows,arrows_xy,target,digits,state,best,star,pic_n
    global smiley,smiley_c
    level=1
    pic=None
    arrows=utils.load_image('arrows.png',True)
    arrows_xy=None # set in main, buttons_setup
    target=utils.load_image('target.png',True)
    digits=[]
    for i in range(10):
        img=utils.load_image(str(i)+'.png',True,'digits'); digits.append(img)
    state='menu' # else 'jigsaw'
    best=[0]*16
    star=utils.load_image('star.png',True)
    pic_n=0 # set when pic selected
    smiley=utils.load_image('smiley.png',True)
    smiley_c=(sx(16),sy(19))
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
