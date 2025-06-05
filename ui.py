# ui.py

import pygame

class Button:
    def __init__(self, rect, text, font, bg_color=(50,50,50), text_color=(255,255,255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.surface = pygame.Surface(self.rect.size)
        self.render()

    def render(self):
        self.surface.fill(self.bg_color)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.rect.width//2, self.rect.height//2))
        self.surface.blit(text_surf, text_rect)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered(event.pos):
                return True
        return False

class HUD:
    def __init__(self, font):
        self.font = font

    def draw_score(self, screen, score):
        score_surf = self.font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_surf, (10, 10))

    def draw_lives(self, screen, lives):
        lives_surf = self.font.render(f"Lives: {lives}", True, (255,255,255))
        screen.blit(lives_surf, (10, 40))
