#!/usr/bin/python
# Trans.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,load_save,buttons,menu,slider
try:
    import gtk
except:
    pass
import tr

class Trans:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((0,0,0))
        g.level=self.levels[self.menu.green.n]
        if g.state=='menu':
            self.menu.draw()
            n=self.slider_n()
            if n!=None: self.slider[n].draw()
        else:
            self.tr[g.level].draw()
            buttons.off(['1','2','3','4'])
            if not self.tr[g.level].complete():
                buttons.on(['1','2','3','4'])
                g.screen.blit(g.arrows,g.arrows_xy)
            elif self.tr[g.level].success:
                utils.centre_blit(g.screen,g.smiley,g.smiley_c)
            buttons.draw()

    def slider_n(self):
        n=self.menu.green.n
        if g.best[n]==1: return 0
        elif g.best[n] in (2,3): return 1
        return None

    def do_click(self):
        if g.state=='menu':
            n=self.slider_n()
            if n!=None:
                if self.slider[n].mouse():
                    self.levels[self.menu.green.n]=g.level
                    return True# g.level changed
            if self.menu.check_mouse():
                n=self.menu.green.n
                if n==g.pic_n:
                    g.level=self.levels[n]
                    g.pic=utils.load_image(str(n)+'.jpg',False,'pics')
                    self.tr[g.level]=tr.Tr(g.level)
                    self.tr[g.level].setup()
                    g.state='jigsaw'
                g.pic_n=n
                return True
        else:
            return self.tr[g.level].click()

    def do_button(self,bu):
        if bu=='new': g.state='menu'; self.menu.green_set()
        elif bu>'0' and bu<'5': self.tr[g.level].button(bu)

    def do_key(self,key):
        if key in g.SQUARE: self.do_button('new'); return
        if g.state=='menu':
            if key in g.DOWN: self.menu.inc_r(); return
            if key in g.UP: self.menu.dec_r(); return
            if key in g.RIGHT: self.menu.inc_c(); return
            if key in g.LEFT: self.menu.dec_c(); return
            if key in g.CROSS: self.do_click(); return
            if key in g.TICK: self.inc_level()
        else: # jigsaw
            if not self.tr[g.level].complete():
                if key in g.CROSS: self.do_click(); return
                if key in g.LEFT: self.tr[g.level].left(); return
                if key in g.RIGHT: self.tr[g.level].right(); return
                if key in g.UP: self.tr[g.level].up(); return
                if key in g.DOWN: self.tr[g.level].down(); return
                if key==pygame.K_1: self.tr[g.level].button('1'); return
                if key==pygame.K_2: self.tr[g.level].button('2'); return
                if key==pygame.K_3: self.tr[g.level].button('3'); return
                if key==pygame.K_4: self.tr[g.level].button('4'); return
        if key==pygame.K_v: g.version_display=not g.version_display; return

    def inc_level(self):
        n=self.slider_n()
        if n!=None:
            g.level+=1
            if g.level>self.slider[n].steps: g.level=1
            self.levels[self.menu.green.n]=g.level

    def buttons_setup(self):
        x=g.sx(3.5); y=g.sy(19); dx=g.sy(5)
        g.arrows_xy=(x+g.sy(5),y-g.sy(1.9))
        g.score_c=(x,y)
        x+=dx # since we dropped '0'
        for i in range(1,5):
            buttons.Button(str(i),(x,y)); x+=dx
        buttons.Button('new',(x,y))

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True

    def run(self):
        g.init()
        if not self.journal: utils.load()
        self.tr=[None,None,None,None]
        self.menu=menu.Menu(4,4,g.sy(.2),g.sy(1.3),g.sy(.2))
        load_save.retrieve()
        self.buttons_setup()
        self.slider=[None,None]
        self.slider[0]=slider.Slider(g.sx(16),g.sy(20.8),2,utils.GREEN)
        self.slider[1]=slider.Slider(g.sx(16),g.sy(20.8),3,utils.GREEN)
        self.levels=[1]*16
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==1:
                        if self.do_click():
                            pass
                        else:
                            if g.state=='jigsaw':
                                bu=buttons.check()
                                if bu!='':
                                    self.do_button(bu); self.flush_queue()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode()
    game=Trans()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
