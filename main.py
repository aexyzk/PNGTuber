import random, math
import sounddevice as sd
import numpy as np
import pygame

from scripts.utils import load_image

pygame.init()

def calculate_loudness(data):
    return 20 * np.log10(np.sqrt(np.mean(data**2)))

duration = 1  # seconds
samplerate = 44100  # Hz
sd.default.samplerate = samplerate
sd.default.channels = 1  # mono

class PNGtuber():
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("PNGTUBER")
        self.display = pygame.Surface((self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.clock = pygame.time.Clock()
        self.running = False
        
        self.assets = {
            '00': load_image('pngtuber.png'),
            '01': load_image('blinking.png'),
            '10': load_image('talking.png'),
            '11': load_image('talking_blinking.png'),
        }

        self.blinking = False
        self.talking = False
        self.has_talked = False
        self.blink_timer = 0
        self.jump_timer = 0
        self.jump_duration = 5
        self.jump_height = 10

        self.wave = 0

    def run(self):
        self.running = True
        while self.running:
            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            try:
                # Record audio
                audio = sd.rec(int(duration * samplerate), dtype='float32')
                sd.wait()

                # Calculate loudness
                loudness = int(calculate_loudness(audio.flatten()) * -1)
                print(f"Loudness: {loudness}")
                if loudness < 58:
                    self.talking = True
                else:
                    self.talking = False
            except:
                print('[ERROR] Reading Microphone Data')

            if self.blink_timer <= 0:
                self.blinking = True
                if self.blink_timer <= random.randint(-3, -1):
                    self.blink_timer = random.randint(35,40)
                    self.blinking = False
            self.blink_timer -= 1

            if self.has_talked == True and self.talking == False:
                self.has_talked = False
            elif self.talking == True and self.has_talked != True:
                self.has_talked = True
                self.jump_timer = self.jump_duration

            if self.jump_timer > 0:
                jump_progress = 1 - math.cos((self.jump_timer / self.jump_duration) * 1.5)
                self.player_height = int(jump_progress * self.jump_height)
                self.jump_timer -= 1
            else:
                if self.talking:
                    self.player_height = int((math.sin(self.wave) + 1) * 4)
                    self.wave += 0.1
                else:
                    self.player_height = 0
                    self.wave = 0

            state = f"{int(self.talking)}{int(self.blinking)}"

            # render
            self.render(state)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.flip()
            self.clock.tick(10)

    def render(self, state):
        self.display.fill((0,255,0))
        self.display.blit(self.assets[state], (0,10 - self.player_height))

pngtuber = PNGtuber().run()
