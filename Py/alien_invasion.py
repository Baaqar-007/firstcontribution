
import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
class AlienInvasion:
    def __init__(self):
        #initialise the game
        pygame.init()
        self.settings=Settings()

        self.screen=pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        #setting background color
        self.bg_color=(230,230,230)


    def run_game(self):
        #main loop of the game
        while True:
            #watching for keyboard and mouse events
          self._check_events()
          self.ship.update()
          self._update_bullets()
          self._update_screen()

    def _create_fleet(self):
        """Create a fleet of aliens"""
        #Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width - (2*alien_width)
        number_aliens_x=available_space_x // (2*alien_width)
        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -(3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleetfirst row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
             #Create an alien and place it in the row.
             self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width+2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)





    def _check_events(self):
        #respond to keypresses and mouse events
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self,event):
        #respond to key presses
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
    #respond to key releases
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets)< self.settings.bullets_allowed:
           new_bullet=Bullet(self)
           self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet positions.
        self.bullets.update()

        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

    def _update_screen(self):
        """Update images on the screen , and flip to the new screen"""
        #redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #make the most recently drawn screen visible
        pygame.display.flip()

if __name__=='__main__':
    #make a instance and run the game
  ai=AlienInvasion()
  ai.run_game()
