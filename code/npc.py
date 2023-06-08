import pygame
from settings import *
from entity import Entety
from ui import UI
from support import *

class NPC(Entety):
    def __init__(self, npc_name,pos,groups,obstacle_sprites,player):
        #general set up
        super().__init__(groups)
        self.sprite_type = 'npc'
        # graphics setup
        self.import_graphics(npc_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        #interakcje
        self.ui = UI()
        
        #ruch
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        
        #statystyki
        
        self.npc_name = npc_name
        npc_info = npc_data[self.npc_name]
        self.health = npc_info['health']
        self.speed = npc_info['speed']
        self.notice_radius = npc_info['notice_radius']

        self.pos = pos
        self.player = player
        ''' # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300'''
    
    def import_graphics(self,name):
        #self.animations = {'idle':[],'move':[],'attack':[]}
        self.animations = {'idle':[]}
        main_path = f'../graphics/npc/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
            
    def get_player_distance_direction(self,player):
        
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance >0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        
        return(distance,direction)
            
    def get_status(self,player):
        distance = self.get_player_distance_direction(player)[0]
        
        #ustawienie aby przecownik nie wchodził w gracza (nie całkowiecie przynajmneij)
        if distance <= 50:
            self.status = 'idle'
        elif distance <= self.notice_radius:
            #self.status = 'move'
            self.ui.show_interactions()
            
        else:
            self.status = 'idle'
            self.interactionStatus = False
            
    def actions(self,player):
        
        if self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

            
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        '''if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)'''
            
    
            
    def update(self):
        self.move(self.speed)
        self.animate()
        self.get_status(self.player)
        self.actions(self.player)
        
    
