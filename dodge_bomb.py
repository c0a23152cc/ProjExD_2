import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DICT_MV={ #移動量指定
        pg.K_UP: (0,-5), 
        pg.K_DOWN: (0,5), 
        pg.K_LEFT: (-5,0), 
        pg.K_RIGHT: (5,0),
        }
        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    bm_img = pg.Surface((20,20))
    pg.draw.circle(bm_img, (255,0,0), (10,10), 10)
    bm_img.set_colorkey((0, 0, 0))
    bm_rct = bm_img.get_rect()
    bm_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    
    vx, vy = 5, 5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bm_rct):
            Gameover(screen)
            return
            
        screen.blit(bg_img, [0, 0]) 
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DICT_MV.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        
        kkn_img = pg.transform.rotozoom(kk_img,-0.5,1)

       
        bm_mv = [vx, vy]
        

        kk_rct.move_ip(sum_mv)
        if hante(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kkn_img, kk_rct)
        bm_rct.move_ip(bm_mv)
        yoko, tate = hante(bm_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        screen.blit(bm_img,bm_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


def hante(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数: こうかとんのレクト or ボムのレクと
    戻り値: 真理値タプル（横方向、縦方向）
    画面内ならTrue、画面外ならFalse
    """
    tate, yoko = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

#課題3
def Gameover(screen):
    bla_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bla_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bla_img.set_alpha(170)
    bla_rct = bla_img.get_rect()
    bla_rct.center = WIDTH/2,HEIGHT/2
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver",
                       True, (255, 255, 255))
    kkf_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    screen.blit(bla_img, bla_rct) # 黒画面の表示
    screen.blit(txt, [WIDTH/2, HEIGHT/2]) #  GameOverの文字の表示
    screen.blit(kkf_img, [WIDTH/2-100, HEIGHT/2-50])  # こうかとん表示
    screen.blit(kkf_img, [WIDTH/2+300, HEIGHT/2-50])  # こうかとん表示
    pg.display.update()
    time.sleep(5)  # 5秒待機

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
