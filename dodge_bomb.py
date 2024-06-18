import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DICT_MV={ #移動量指定
        pg.K_UP: (0, -5), 
        pg.K_DOWN: (0, 5), 
        pg.K_LEFT: (-5, 0), 
        pg.K_RIGHT: (5, 0),
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

        #課題1
        if sum_mv != [0, 0]:
            kk_img = Muki()[tuple(sum_mv)]  # 辞書から値を取り出して向く方向決める
            if sum_mv == [-5, -5] or sum_mv == [-5, 0] or sum_mv == [-5, 5]:  # 左行きたいとき以外左右反転させる
                pass
            else:
                kk_img = pg.transform.flip(kk_img, True, False)

        #課題2
        bm_accs, bm_imgs = Bomb_DX()
        avx = vx*bm_accs[min(tmr//500, 9)]  # 速度を加速度ごとに時間経過で変える
        avy = vy*bm_accs[min(tmr//500, 9)]
        bm_mv = [avx, avy]
        bm_img = bm_imgs[min(tmr//500, 9)]  # 大きさを時間経過で変える
        bm_img.set_colorkey((0, 0, 0))
        
        kk_rct.move_ip(sum_mv)
        if hante(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
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


#課題1
def Muki():
    DICT_MUKI={  # 向きの指定の辞書作成
    (0, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 2.0),
    (5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 2.0),
    (5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
    (5, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0),
    (0, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2.0),
    (-5, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0),
    (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
    (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 2.0),
    }
    return DICT_MUKI


#課題2
def Bomb_DX():
    accs = [a for a in range(1, 11)]
    big = []  #空のリストを用意
    for r in range(1, 11):  # 10回まわす
        bm_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bm_img, (255, 0, 0), (10*r, 10*r), 10*r)  # ボムの大きさをrごとに指定する
        big.append(bm_img)  # リストに追加する
    return accs,big  # リスト2つをタプルにして返す


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
