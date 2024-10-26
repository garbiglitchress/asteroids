import pygame
from constants import *
import math
class GameOverScreen():#return keys, would also save score?
    def __init__(self,  con_surface,screen, ast, p1, score, mode):
        
        self.con_surface=con_surface
        self.screen=screen
        self.ast=ast
        self.p1=p1
        self.score=score
        self.mode=mode
    def show(self):
        self.screen.blit(self.con_surface, (SCREEN_WIDTH*.5, SCREEN_HEIGHT*.8))
        for a in self.ast:
            a.kill()
        self.p1.kill()
    def save(self):
        if self.mode=='t':
            file_name='best_times.txt'
        
        elif self.mode=='p':
            file_name='score_attack.txt'
        elif self.mode=='s':
            file_name='survival.txt'
        high_scores=self.return_scores(file_name)
        if high_scores[0]=='':
            high_scores[0]=self.score
        elif len(high_scores)==0:
            high_scores.append(self.score)
        else:
            if self.mode=='t':
                for i in range(0, len(high_scores)):
                    if self.score<float(high_scores[i]):
                        if len(high_scores)==3:
                            high_scores.pop()
                        high_scores.insert(i, str(self.score))
                        break
                    if i==len(high_scores)-1:#if less than 3 entries, insert to end of list
                        high_scores.append(str(self.score))
            else:
                for i in range(0, len(high_scores)):
                    if self.score>float(high_scores[i]):
                        if len(high_scores)==3:
                            high_scores.pop()
                        high_scores.insert(i, str(self.score))
                        break
                    if i==len(high_scores)-1:#if less than 3 entries, insert to end of list
                        high_scores.append(str(self.score))
        new_file=open(file_name, "w")
        for score_index in range(0,len(high_scores)):
            if score_index!=len(high_scores)-1:
                new_file.write(f"{high_scores[score_index]}\n")
            else:
                new_file.write(f"{high_scores[score_index]}")
        new_file.close()
        return high_scores[0:3]
               
            
        
    def return_scores(self, file_name):#return list of scores?
        f = open(file_name, "a")
        high_score_return=''
        with open(file_name, encoding="utf-8") as f:
            current_high_scores=f.read().split('\n')
        f.close()
        for i in range(0,min(len(current_high_scores),4)):
            high_score_return+=f"{current_high_scores[i]}\n"
        return current_high_scores
    
        
        
