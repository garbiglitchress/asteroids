import pygame
from player import *
from asteroid import *
from constants import *
from asteroidfield import *
from powerup import *
import random

def main():
    play_again='Yes'
    is_game_over=False
    pygame.init()
    mode=input('Do you want to play Time Attack(T) or Survival?(S)?')
    if mode not in ['T','S']:
        print('Invalid mode.')
        return
    while play_again:
        score=0
        
        score_font=pygame.font.SysFont('Comic Sans MS', 30)
        time_font=pygame.font.SysFont('Comic Sans MS', 30)
        confirmation_font = pygame.font.SysFont('Comic Sans MS', 30)
        clock = pygame.time.Clock()
        total_time=0#time elapsed in game
        score_surface=score_font.render(str(score), False, (0,255,0))
        time_surface = time_font.render(str(total_time), False, (0,255,0))
        confirmation_surface = confirmation_font.render('Y to play again, any other key to end.', False, (0,255,0))
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        
        should_spawn_powerup=False
        time_started_powerup = 0
        has_powerup=False
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

        
        p1=Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        is_in_infinite=True
        asteroid_field=AsteroidField()
        while (is_in_infinite):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            pygame.Surface.fill(screen, (0,0,0))

            for up in updatable:
                up.update(dt)
            for ast in asteroids:
                for s in shots:
                    if ast.check_collision(s)==True:
                        ast.split()
                        if has_powerup:
                            score+=ASTEROID_POINTS*2
                        else:
                            score+=ASTEROID_POINTS
                        score_surface=score_font.render(str(score), False, (0,255,0))#update score in hud
                        s.kill()
                    
                if (ast.check_collision(p1)==True):
                    if mode=='S':
                        is_game_over=True
                        score_surface=score_font.render(f"Game Over! You scored {str(score)}!", False, (0,255,0))
                        confirmation_surface=confirmation_font.render('Y to play again, E to end.', False, (0,255,0))
                        screen.blit(confirmation_surface, (SCREEN_WIDTH*.5, SCREEN_HEIGHT*.8))
                        for ast in asteroids:
                            ast.kill()
                        #del asteroid_field#prevent more asteroids from spawning
                        p1.kill()
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_y]:
                            is_in_infinite=False
                        elif keys[pygame.K_e]:
                            return
                        else:
                            pass
                    elif mode=='T':
                        score-=HIT_PENALTY#if doing time attack, just lose points
                        score_surface=score_font.render(str(score), False, (0,255,0))#update score in hud
                        
                        
                        
            for draw in drawable:
                draw.draw(screen)
            for power in powerups:
                if power.check_collision(p1)==True:
                    has_powerup=True
                    time_started_powerup=total_time
                    power.kill()
            if total_time>(time_started_powerup+10):#powerup wears off after 10 seconds
                has_powerup=False
            if int(total_time)>=TIME_LIMIT and mode=='T':
                is_game_over=True
                score_surface=score_font.render(f"Time Up! You scored {str(score)}!", False, (0,255,0))
                confirmation_surface=confirmation_font.render('Y to play again, E to end.', False, (0,255,0))
                screen.blit(confirmation_surface, (SCREEN_WIDTH*.5, SCREEN_HEIGHT*.8))
                for ast in asteroids:
                    ast.kill()
                    #del asteroid_field#prevent more asteroids from spawning
                    p1.kill()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_y]:
                        is_in_infinite=False
                    elif keys[pygame.K_e]:
                        return
                    else:
                        pass            
            screen.blit(score_surface, (SCREEN_WIDTH*.7, SCREEN_HEIGHT*.9))
            screen.blit(time_surface, (SCREEN_WIDTH*.8, SCREEN_HEIGHT*.9))

            pygame.display.update()
            pygame.display.flip()
            
            dt=(clock.tick(FRAMES_PER_SECOND)/1000)
            total_time+=dt
            if mode=='T':
                time_surface = time_font.render(str((int)(TIME_LIMIT-total_time)), False, (0,255,0))
            elif mode=='S':
                time_surface = time_font.render(str((int)(total_time)), False, (0,255,0))
        
        
    

if __name__=="__main__":
    main()
