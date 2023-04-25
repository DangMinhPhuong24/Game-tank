import pgzrun
import random
TITLE="TANK"
WIDTH =800
HEIGHT=600
SIZE_TANK=25
walls=[]
bullets=[]
bullets_holdoff=0
enemy_move_count=0
enemy_bullets=[]
game_over=False
enemies=[]

# định dạng xe tăng phe mình
tank=Actor('tank_blue') 
tank.pos=(WIDTH/2,HEIGHT-SIZE_TANK)
tank.angle=90 

# định dang xe tăng địch 
for i in range(6):
    enemy=Actor('tank_red')
    enemy.x=i *100+100
    enemy.y=SIZE_TANK
    enemy.angle=270
    enemies.append(enemy)

# set up background và tường
background=Actor('grass')
for x in range(16):
    for y in range(10):
        if random.randint(0,100)<50:
            wall=Actor("wall")
            wall.x=x*50+SIZE_TANK
            wall.y=y*50+SIZE_TANK*3
            walls.append(wall)

# set up về xe tăng bên mình
def tank_set(): 
    original_x=tank.x
    original_y=tank.y
    if keyboard.left:
        tank.x=tank.x-2
        tank.angle=180
    elif keyboard.right:
        tank.x=tank.x+2
        tank.angle=0
    elif keyboard.up:
        tank.y=tank.y-2
        tank.angle=90
    elif keyboard.down:
        tank.y=tank.y+2
        tank.angle=270

    if tank.collidelist(walls)!=-1:
        tank.x=original_x
        tank.y=original_y
    if tank.x<SIZE_TANK or tank.x>(WIDTH-SIZE_TANK) or tank.y<SIZE_TANK or tank.y>(HEIGHT-SIZE_TANK):
        tank.x=original_x
        tank.y=original_y

#set up về đạn xe tăng phe mình
def tank_bullets_set():
    bullet=Actor('bulletblue2') 
    global bullets_holdoff
    if bullets_holdoff==0:
        if keyboard.space:
            bullet.angle=tank.angle
            if bullet.angle==0:
                bullet.pos=(tank.x+SIZE_TANK,tank.y)
            if bullet.angle==180:
                bullet.pos=(tank.x-SIZE_TANK, tank.y)
            if bullet.angle==90:
                bullet.pos=(tank.x,tank.y-SIZE_TANK)
            if bullet.angle==270:
                bullet.pos=(tank.x,tank.y+SIZE_TANK)
            bullets.append(bullet)
            bullets_holdoff=20
    else:
        bullets_holdoff=bullets_holdoff-1

    for bullet in bullets:
        if bullet.angle==0:
            bullet.x=bullet.x+5
        if bullet.angle==180:
            bullet.x=bullet.x-5
        if bullet.angle==90:
            bullet.y=bullet.y-5
        if bullet.angle==270:
            bullet.y=bullet.y+5

    # set up đan phá huỷ tường
    for bullet in bullets: 
        walls_index=bullet.collidelist(walls)
        if walls_index!=-1:
            sounds.gun10.play()
            del walls[walls_index]
            bullets.remove(bullet)
        if bullet.x<0 or bullet.x>WIDTH or bullet.y<0 or bullet.y>HEIGHT:
            bullets.remove(bullet)
        enemy_index=bullet.collidelist(enemies)
        if enemy_index !=-1:
            sounds.exp.play()
            bullets.remove(bullet)
            del enemies[enemy_index]
         
# set up  về xe tăng địch    
def enemy_set():
    global enemy_move_count , bullets_holdoff
    
    for enemy in enemies:
        original_x=enemy.x
        original_y=enemy.y
        choice=random.randint(0,2)
        if enemy_move_count>0:
            enemy_move_count=enemy_move_count-1
            if enemy.angle==0:
                enemy.x=enemy.x+2
            elif enemy.angle==180:
                enemy.x=enemy.x-2
            elif enemy.angle==90:
                enemy.y=enemy.y-2
            elif enemy.angle==270:
                enemy.y=enemy.y+2
            if enemy.x<SIZE_TANK or enemy.x>(WIDTH-SIZE_TANK) or enemy.y<SIZE_TANK or enemy.y>(HEIGHT-SIZE_TANK):
                enemy.x=original_x
                enemy.y=original_y
                enemy_move_count=0
            if enemy.collidelist(walls)!=-1:
                enemy.x=original_x
                enemy.y=original_y
                enemy_move_count=0
        elif choice==0:             # xe tăng địch di chuyển
            enemy_move_count=30
        elif choice==1:               # xe tăng địch đổi hướng
            enemy.angle=random.randint(0,3)*90
        else:                           # xe tăng địch bắn 
            if bullets_holdoff==0:
                bullet=Actor('bulletred2')
                bullet.angle=enemy.angle
                bullet.pos=enemy.pos
                enemy_bullets.append(bullet)
                bullets_holdoff=40
            else:
                bullets_holdoff=bullets_holdoff-1

# set up đạn xe tăng địch
def enemy_bullets_set():
    global enemies ,game_over
    for bullet in enemy_bullets:
        if bullet.angle==0:
            bullet.x=bullet.x+5
        if bullet.angle==180:
            bullet.x=bullet.x-5
        if bullet.angle==90:
            bullet.y=bullet.y-5
        if bullet.angle==270:
            bullet.y=bullet.y+5
        
        # đạn địch phá tường , phá xe
        for bullet in enemy_bullets:
            wall_index=bullet.collidelist(walls)
            if wall_index!=-1:
                sounds.gun10.play()
                del walls[wall_index]
                enemy_bullets.remove(bullet)
            if bullet.x<0 or bullet.x>WIDTH or bullet.y<0 or bullet.y>HEIGHT:
                enemy_bullets.remove(bullet)
            if bullet.colliderect(tank):
                game_over=True
                enemies=[]

def update():
    tank_set()
    tank_bullets_set()
    enemy_set()
    # enemy_bullets_set()


def draw():
    if game_over:
        screen.fill((0,0,0))
        screen.draw.text('YOU LOSE',(260,250), color=(255,255,255),fontsize=100)
    elif len(enemies)==0:
        screen.fill((0,0,0))
        screen.draw.text('YOU WIN',(260,250), color=(255,255,255),fontsize=100)
    else:

        background.draw()
        tank.draw()
        for wall in walls:
            wall.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in enemy_bullets:
            bullet.draw()
pgzrun.go() 
