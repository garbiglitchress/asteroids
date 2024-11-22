import pygame
from player import *
from asteroid import *
from constants import *
from asteroidfield import *
from powerup import *
from gameoverscreen import *
import random
import sys

def main():
    play_again='Yes'
    is_game_over=False
    has_printed=False
    is_debug=False
    if len(sys.argv)>1:
        if sys.argv[1]=='-d':
            is_debug=True
    pygame.init()
    if is_debug:
        instructions='n'
    else:
        instructions=input('Do you want instructions?').lower()
    
    #instructions='n'
    is_ready=False

    if instructions=='y':
        print('''Keyboard Controls: WASD to move, and space to shoot.
              Mouse controls: Left click to shoot, and Right Click to move ship toward cursor.
              If you run into blue asteroids, you'll get a multiplier.''')

    if is_debug==True:
        mode='t'
        control='k'
    else:
        mode=input('Do you want to play Point Attack(P) or Survival(S) or Time Attack(T)?').lower()
        control=input('Keyboard controls(K) or Mouse(M) controls?').lower()
    while mode not in ['p','s', 't']:
    #while mode not in OPTIONS
        mode=input('Invalid mode. Please enter P for point attack, T for time attack or S for survival.')
    while control not in ['k','m']:
        control=input('Invalid selection. Please enter K for keyboard or M for mouse.')
    while play_again:
        score=0
        
        score_font=pygame.font.SysFont('Comic Sans MS', 30)
        time_font=pygame.font.SysFont('Comic Sans MS', 30)
        confirmation_font = pygame.font.SysFont('Comic Sans MS', 30)
        multiplier_font = pygame.font.SysFont('Comic Sans MS', 30)
        high_score_font = pygame.font.SysFont('Comic Sans MS', 30)
        
        clock = pygame.time.Clock()
        total_time=0#time elapsed in game
        multiplier=1
        powerup_timers=[]
        iframe_timer=0
        score_surface=score_font.render(str(score), False, (0,255,0))
        time_surface = time_font.render(str(total_time), False, (0,255,0))
        
        confirmation_surface = confirmation_font.render('Y to play again, any other key to end.', False, (0,255,0))
        multiplier_surface= multiplier_font.render(f"x{multiplier}", False, (0,255,0))
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        high_score_surface_two=None
        high_score_surface_three=None
        should_spawn_powerup=False
        time_started_powerup = 0
        has_showed_scores=False
        dt=0
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        print('Starting asteroids!')
        print(f"Screen width: {SCREEN_WIDTH}")
        print(f"Screen height: {SCREEN_HEIGHT}")
        Player.containers=(updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable)
        Shot.containers = (updatable, drawable, shots)
        Powerup.containers = (drawable, updatable, powerups)

        
        p1=Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, control, PLAYER_ACCEL)
        is_in_infinite=True
        asteroid_field=AsteroidField()
        while (is_in_infinite):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            pygame.Surface.fill(screen, (0,0,0))

            for s in shots:
                if s.distance>SHOT_DISTANCE:
                    s.kill()

            for up in updatable:
                up.update(dt)
            for ast in asteroids:
                for s in shots:
                    if ast.check_collision(s)==True:
                        ast.split()
                        score+=ASTEROID_POINTS*multiplier
                        score_surface=score_font.render(str(score), False, (0,255,0))#update score in hud
                        s.kill()
                    
                if (ast.check_collision(p1)==True and p1.invincible==False):
                    iframe_timer=total_time
                    p1.invincible=True
                    if mode=='s':
                        is_game_over=True
                        ending_message=f"Game Over! You scored {str(score)}!"
#                        score_surface=score_font.render(ending_message, False, (0,255,0))
#                        confirmation_surface=confirmation_font.render('Y to play again, E to end.', False, (0,255,0))
#                        screen.blit(confirmation_surface, (SCREEN_WIDTH*.5, SCREEN_HEIGHT*.7))
#                        for ast in asteroids:
#                            ast.kill()
                        #del asteroid_field#prevent more asteroids from spawning
#                        p1.kill()
#                        keys = pygame.key.get_pressed()
#                        if keys[pygame.K_y]:
#                            is_in_infinite=False
#                        elif keys[pygame.K_e]:
#                            return
#                        else:
#                            pass
                    elif mode!='s':
                        score=int(score*.9)#if not doing survival, just lose points
                        score_surface=score_font.render(str(score), False, (0,255,0))#update score in hud
                        
                        
                        
            for draw in drawable:
                draw.draw(screen)
            for power in powerups:
                if power.check_collision(p1)==True:
                    multiplier+=1
                    powerup_timers.append(total_time)
                    power.kill()
            if len(powerup_timers)>0:
                if total_time>(powerup_timers[0]+10):#powerup wears off after 10 seconds
                    powerup_timers=powerup_timers[1:]
                    multiplier-=1
            if total_time>iframe_timer+1:
                p1.invincible=False
            
            if is_debug:
                if int(total_time)>=DEBUG_TIME_LIMIT and mode=='p':
                    is_game_over=True
                    ending_message=f"Time Up! You scored {str(score)}!"
            else:
                if int(total_time)>=TIME_LIMIT and mode=='p':
                    is_game_over=True
                    ending_message=f"Time Up! You scored {str(score)}!"            
            if is_debug:
                if score>=DEBUG_SCORE_GOAL and mode=='t':
                
                    if not is_game_over:
                        final_time=round(total_time, 2)
                    is_game_over=True
                
                    ending_message=f"Congratulations! You scored {DEBUG_SCORE_GOAL} points in {final_time} seconds!"
            else:

                
                if score>=SCORE_GOAL and mode=='t':
                
                    if not is_game_over:
                        final_time=round(total_time, 2)
                    is_game_over=True
                
                    ending_message=f"Congratulations! You scored {SCORE_GOAL} points in {final_time} seconds!"
            if is_game_over:
                score_surface=score_font.render(ending_message, False, (0,255,0))
                confirmation_surface=confirmation_font.render('Y to play again, E to end.', False, (0,255,0))
                
                if mode=='t':
                    game_over_screen=GameOverScreen(confirmation_surface,
                                                screen,asteroids,p1, final_time, mode) 
                else:                  

                    game_over_screen=GameOverScreen(confirmation_surface,
                                                screen,asteroids,p1, score, mode)
                if not has_showed_scores:
                    high_scores=game_over_screen.save()
                    has_showed_scores=True
                

                high_score_surface_one=high_score_font.render(f"1: {high_scores[0]}",False,(0,255,0))
                if len(high_scores)>1:
                    high_score_surface_two=high_score_font.render(f"2: {high_scores[1]}",False,(0,255,0))
                if len(high_scores)>2:
                    high_score_surface_three=high_score_font.render(f"3: {high_scores[2]}",False,(0,255,0))                    

                game_over_screen.show()
                keys=pygame.key.get_pressed()
                if high_score_surface_one!=None:    
                    screen.blit(high_score_surface_one, (SCREEN_WIDTH*.1, SCREEN_HEIGHT*.5))
                if high_score_surface_two!=None:
                    screen.blit(high_score_surface_two, (SCREEN_WIDTH*.1, SCREEN_HEIGHT*.55))
                if high_score_surface_three!=None:
                    screen.blit(high_score_surface_three, (SCREEN_WIDTH*.1, SCREEN_HEIGHT*.6))
                if keys[pygame.K_y]:
                    has_showed_scores=False
                    is_in_infinite=False
                    is_game_over=False
                elif keys[pygame.K_e]:
                    return
                else:
                    pass
            
            screen.blit(score_surface, (SCREEN_WIDTH*.4, SCREEN_HEIGHT*.9))
            
            if not is_game_over:
                screen.blit(time_surface, (SCREEN_WIDTH*.8, SCREEN_HEIGHT*.9))
                screen.blit(multiplier_surface, (SCREEN_WIDTH*.5, SCREEN_HEIGHT*.9))

            pygame.display.update()
            pygame.display.flip()
            
            dt=(clock.tick(FRAMES_PER_SECOND)/1000)
            
            total_time+=dt
            multiplier_surface= multiplier_font.render(f"x{multiplier}" , False, (0,255,0))
            if mode=='p':
                if is_debug:
                    time_surface = time_font.render(str((int)(DEBUG_TIME_LIMIT-total_time)), False, (0,255,0))
                else:
                    time_surface = time_font.render(str((int)(TIME_LIMIT-total_time)), False, (0,255,0))
            elif mode=='s' or mode=='t':
                time_surface = time_font.render(str((int)(total_time)), False, (0,255,0))
        
        
    

if __name__=="__main__":
    main()
