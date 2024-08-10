## Musical Tuner Project
# July 21st to August 10th
# Kirsten Ticzon


# Setting up environment
import pyaudio
import pygame
import numpy as np
import sys

# Pyaudio setup
sr = 48000 
bufferSamples = 2048

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=sr, input=True)

# Function to record and store audio
def recordAudio():
    audioCollected = np.frombuffer(stream.read(bufferSamples), dtype=np.int16)
    return audioCollected

# Function to get the frequency of the main pitch detected in the recording
def getFrequency(signal):
    result = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), 1/sr)
    indexAmp = np.argmax(np.abs(result))
    peak = frequencies[indexAmp]
    return abs(peak)

# Function to assign musical note to pitch
def assignNote(frequency):
    # Set base frequencies
    baseFrequencies = {
        "C": 16.35,
        "C#": 17.32,
        "D": 18.35,
        "Eb": 19.45,
        "E": 20.60,
        "F": 21.83,
        "F#": 23.12,
        "G": 24.50,
        "G#": 25.96,
        "A": 27.50,
        "Bb": 29.14,
        "B": 30.87 }
    
    noteFrequencies = {}
    for note, baseFreq in baseFrequencies.items():
        noteFrequencies[note] = [baseFreq * (2 ** i) for i in range(9)]

    # Find the closest note and octave
    minDif = float("inf")
    closestNote = None

    for note, freqs in noteFrequencies.items():
        for noteFreq in freqs:
            difference = abs(frequency - noteFreq)
            if difference < minDif:
                minDif = difference
                closestNote = note

    return closestNote

# Valid notes
validnotes = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]

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
tunerButton = pygame.Rect(300, 200, 200, 50)
targetTunerButton = pygame.Rect(300, 300, 200, 50)
start = pygame.Rect(300, 300, 100, 50)
stop = pygame.Rect(420, 300, 100, 50)
restart = pygame.Rect(340, 370, 140, 50)
backButton = pygame.Rect(50, 50, 100, 50)

# Initializing variables
isRecording = False
targetSet = False
detectedNote = ""
targetNote = ""
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
                if tunerButton.collidepoint(event.pos):
                    tuner()
                elif targetTunerButton.collidepoint(event.pos):
                    targetTuner()

        screen.fill(WHITE)
        background.topbar(screen)
        background.center(screen)

        tunerButton = pygame.Rect(300, 200, 200, 50)
        targetTunerButton = pygame.Rect(290, 300, 220, 50)
        
        pygame.draw.rect(screen, LIGHTGREEN, tunerButton)
        pygame.draw.rect(screen, LIGHTGREEN, targetTunerButton)

        tunerText = font.render("Tuner", True, BLACK)
        targetTunerText = font.render("Target Tuner", True, BLACK)

        screen.blit(tunerText, (tunerButton.x + 55, tunerButton.y + 10))
        screen.blit(targetTunerText, (targetTunerButton.x + 10, targetTunerButton.y + 10))

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
                elif backButton.collidepoint(event.pos):
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
        pygame.draw.rect(screen, LIGHTYELLOW, backButton)

        startText = font.render("Start", True, WHITE if isRecording else BLACK)
        stopText = font.render("Stop", True, WHITE if not isRecording else BLACK)
        backText = font.render("Back", True, BLACK)

        screen.blit(startText, (start.x + 10, start.y + 10))
        screen.blit(stopText, (stop.x + 10, stop.y + 10))
        screen.blit(backText, (backButton.x + 10, backButton.y + 10))

        if detectedNote:
            noteText = noteFont.render(f"{detectedNote}", True, BLACK)
            screen.blit(noteText, (380, 200))

        pygame.display.flip()
        clock.tick(60)

def targetTuner():
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
                        if noteEntry in validnotes:
                            targetNote = noteEntry
                            targetSet = True
                        else:
                            attempts += 1
                            notePrompt = "Invalid note. Try again."
                            noteEntry = ""
                            if attempts == 3:
                                notePrompt = "Please enter: "+", ".join(validnotes)
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
                    elif backButton.collidepoint(event.pos):
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
            pygame.draw.rect(screen, LAVENDER, backButton)

            startText = font.render("Start", True, WHITE if isRecording else BLACK)
            stopText = font.render("Stop", True, WHITE if not isRecording else BLACK)
            restartText = font.render("Restart", True, BLACK)
            backText = font.render("Back", True, BLACK)

            screen.blit(startText, (start.x + 10, start.y + 10))
            screen.blit(stopText, (stop.x + 10, stop.y + 10))
            screen.blit(restartText, (restart.x + 10, restart.y + 10))
            screen.blit(backText, (backButton.x + 10, backButton.y + 10))

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
