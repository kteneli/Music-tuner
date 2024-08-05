##tuner
# July 21st 2024 - August 5th 2024
# Kirsten Ticzon

## Set up environment
import numpy as np
import pyaudio
import pygame
import sys

## Capture audio
# Constants in hertz
sr = 48000
# Middle point of lag versus quick output
bufferSamples = 2048

# PyAudio setup
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=sr,
                 input=True)

## Create function to record and store audio
def recordAudio():
    audioCollected = np.frombuffer(stream.read(bufferSamples), dtype=np.int16)
    return audioCollected

## Isolate main pitch detected in recording
def getFrequency(signal):
    result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), 1/sr)
    indexAmp = np.argmax(np.abs(result))
    peak = frequencies[indexAmp]
    return abs(peak)

## Adding musical value to pitch
def assignNote (frequency):
    A4 = 440.0
    notes = {
        "C": A4 * 2 ** (-9/12),
        "C#": A4 * 2 ** (-8/12),
        "D": A4 * 2 ** (-7/12),
        "D#": A4 * 2 ** (-6/12),
        "E": A4 * 2 ** (-5/12),
        "F": A4 * 2 ** (-4/12),
        "F#": A4 * 2 ** (-3/12),
        "G": A4 * 2 ** (-2/12),
        "G#": A4 * 2 ** (-1/12),
        "A": A4,
        "A#": A4 * 2 ** (1/12),
        "B": A4 * 2 ** (2/12),
        "C5": A4 * 2 ** (3/12),
    }
    minDif = float("inf")
    closestNote = None
    for note, noteFrequency in notes.items():
        difference = abs(frequency - noteFrequency)
        if difference < minDif:
            minDif = difference
            closestNote = note
    return closestNote

# Valid notes
notes = {
    "C": 261.63,
    "C#": 277.18,
    "D": 293.66,
    "D#": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "G#": 415.30,
    "A": 440.00,
    "A#": 466.16,
    "B": 493.88,
    "C5": 523.25,
}

## Pygame setup
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Music Tuner")

font = pygame.font.SysFont("Roboto", 48)
noteFont = pygame.font.SysFont("Roboto", 100)
inputFont = pygame.font.SysFont("Roboto", 36)
directionsFont = pygame.font.SysFont("Roboto", 25)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTYELLOW = (246, 237, 212)
LAVENDER = (232, 212, 246)
LIGHTGREEN = (206, 241, 195)
PINK = (255, 204, 229)

class Background():
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.font = pygame.font.SysFont('Ariel', 25, False)

    def topbar(self, screen):
        x = self.xPos
        y = self.yPos
        text = self.font.render("Music Tuner", True, BLACK)
        pygame.draw.rect(screen, LAVENDER, [x, y, 800, 40])
        pygame.draw.rect(screen, BLACK, [x, y, 800, 40], 2)
        screen.blit(text, [350, 15])

    def center(self, screen):
        x = 50
        y = 110
        pygame.draw.rect(screen, LAVENDER, [x, y, 700, 410])

# Buttons
tuner_button = pygame.Rect(300, 200, 200, 50)
target_tuner_button = pygame.Rect(300, 300, 200, 50)
start = pygame.Rect(300, 300, 100, 50)
stop = pygame.Rect(420, 300, 100, 50)
restart = pygame.Rect(340, 370, 140, 50)
back_button = pygame.Rect(50, 50, 100, 50)

# Initializing variables
isRecording = False
detectedNote = ""
targetNote = ""
targetSet = False
noteEntry = ""
attempts = 0
done = False
clock = pygame.time.Clock()
background = Background()

def main_menu():
    global done
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if tuner_button.collidepoint(event.pos):
                    tuner()
                elif target_tuner_button.collidepoint(event.pos):
                    target_tuner()

        screen.fill(WHITE)
        background.topbar(screen)
        background.center(screen)

        tuner_button = pygame.Rect(300, 200, 200, 50)
        target_tuner_button = pygame.Rect(290, 300, 220, 50)
        
        pygame.draw.rect(screen, LIGHTGREEN, tuner_button)
        pygame.draw.rect(screen, LIGHTGREEN, target_tuner_button)

        tunerText = font.render("Tuner", True, BLACK)
        targetTunerText = font.render("Target Tuner", True, BLACK)

        screen.blit(tunerText, (tuner_button.x + 55, tuner_button.y + 10))
        screen.blit(targetTunerText, (target_tuner_button.x + 10, target_tuner_button.y + 10))

        pygame.display.flip()
        clock.tick(60)

def tuner():
    global isRecording, detectedNote, done
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start.collidepoint(event.pos):
                    isRecording = True
                elif stop.collidepoint(event.pos):
                    isRecording = False
                    detectedNote = ""
                elif back_button.collidepoint(event.pos):
                    return main_menu()

        if isRecording:
            audioCollected = recordAudio()
            frequency = getFrequency(audioCollected)
            detectedNote = assignNote(frequency)

        screen.fill(WHITE)
        background.topbar(screen)
        background.center(screen)

        pygame.draw.rect(screen, LIGHTGREEN if isRecording else LIGHTYELLOW, start)
        pygame.draw.rect(screen, LIGHTGREEN if not isRecording else LIGHTYELLOW, stop)
        pygame.draw.rect(screen, LIGHTYELLOW, back_button)

        startText = font.render("Start", True, WHITE if isRecording else BLACK)
        stopText = font.render("Stop", True, WHITE if not isRecording else BLACK)
        backText = font.render("Back", True, BLACK)

        screen.blit(startText, (start.x + 10, start.y + 10))
        screen.blit(stopText, (stop.x + 10, stop.y + 10))
        screen.blit(backText, (back_button.x + 10, back_button.y + 10))

        if detectedNote:
            noteText = noteFont.render(f"{detectedNote}", True, BLACK)
            screen.blit(noteText, (380, 200))

        pygame.display.flip()
        clock.tick(60)

def target_tuner():
    global isRecording, detectedNote, targetNote, targetSet, noteEntry, attempts, done
    targetSet = False
    notePrompt = "Type the note you want to hit:"
    noteEntry = ""
    attempts = 0
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not targetSet:
                    if event.key == pygame.K_RETURN:
                        if noteEntry in notes:
                            targetNote = noteEntry
                            targetSet = True
                        else:
                            attempts += 1
                            notePrompt = "Invalid note. Try again."
                            noteEntry = ""
                            if attempts == 3:
                                notePrompt = "Please enter: "+", ".join(notes.keys())
                                attempts = 0
                    elif event.key == pygame.K_BACKSPACE:
                        noteEntry = noteEntry[:-1]
                    else:
                        noteEntry += event.unicode.upper()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if targetSet:
                    if start.collidepoint(event.pos):
                        isRecording = True
                    elif stop.collidepoint(event.pos):
                        isRecording = False
                        detectedNote = ""
                    elif restart.collidepoint(event.pos):
                        targetSet = False
                        notePrompt = "What note do you want to hit?"
                        noteEntry = ""
                        attempts = 0
                    elif back_button.collidepoint(event.pos):
                        return main_menu()

        if isRecording:
            audioCollected = recordAudio()
            frequency = getFrequency(audioCollected)
            detectedNote = assignNote(frequency)

        screen.fill(WHITE)
        background.topbar(screen)
        background.center(screen)

        if not targetSet:
            input_box = pygame.Rect(150, 200, 500, 50)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            notePromptText = inputFont.render(notePrompt, True, BLACK)
            noteEntryText = inputFont.render(noteEntry, True, BLACK)
            enterInstructionText = directionsFont.render("(Press Enter when done)", True, BLACK)
            screen.blit(notePromptText, (90, 170))
            screen.blit(noteEntryText, (input_box.x + 10, input_box.y + 10))
            screen.blit(enterInstructionText, (input_box.x + 150, input_box.y + 60))

        else:

            screen.fill(RED if not targetSet or detectedNote != targetNote else GREEN)
            background.topbar(screen)
            background.center(screen)

            pygame.draw.rect(screen, LIGHTGREEN if isRecording else LIGHTYELLOW, start)
            pygame.draw.rect(screen, LIGHTGREEN if not isRecording else LIGHTYELLOW, stop)
            pygame.draw.rect(screen, PINK, restart)
            pygame.draw.rect(screen, LAVENDER, back_button)

            startText = font.render("Start", True, WHITE if isRecording else BLACK)
            stopText = font.render("Stop", True, WHITE if not isRecording else BLACK)
            restartText = font.render("Restart", True, BLACK)
            backText = font.render("Back", True, BLACK)

            screen.blit(startText, (start.x + 10, start.y + 10))
            screen.blit(stopText, (stop.x + 10, stop.y + 10))
            screen.blit(restartText, (restart.x + 10, restart.y + 10))
            screen.blit(backText, (back_button.x + 10, back_button.y + 10))

            if detectedNote:
                noteText = noteFont.render(f"{detectedNote}", True, BLACK)
                screen.blit(noteText, (380, 200))

        pygame.display.flip()
        clock.tick(60)

main_menu()
stream.stop_stream()
stream.close()
pa.terminate()
pygame.quit()
sys.exit()