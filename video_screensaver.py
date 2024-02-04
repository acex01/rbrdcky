import os
import sys
import pygame
import imageio
import math

# Set the path to your video and audio files
video_path = "1.mp4"
audio_path = "1.mp3"

# Set up Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for audio playback

# Get the screen dimensions
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Set up the window
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Desktop Video Screensaver")

# Set up the clock
clock = pygame.time.Clock()

# Set the initial position and direction
x, y = screen_width // 2, screen_height // 2
dx, dy = 10, 10

# Open the video file using imageio
video = imageio.get_reader(video_path)
num_frames = len(video)

# Load the audio file
pygame.mixer.music.load(audio_path)
pygame.mixer.music.play(-1)  # -1 plays the audio in a loop

# Function to generate rainbow colors
def get_rainbow_color(position):
    frequency = 100
    red = int(127 * (1 + math.sin(frequency * position)))
    green = int(127 * (1 + math.sin(frequency * position + 2)))
    blue = int(127 * (1 + math.sin(frequency * position + 4)))
    return red, green, blue

# Main loop
running = True
current_frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the rainbow color for the background
    rainbow_color = get_rainbow_color(current_frame * 0.01)

    # Fill the screen with the rainbow color
    screen.fill(rainbow_color)

    # Read the next frame from the video
    real_frame = current_frame % 259
    image = video.get_data(real_frame)

    # Check for collision with screen edges
    if x + image.shape[1] > screen_width or x < 0:
        dx = -dx
    if y + image.shape[0] > screen_height or y < 0:
        dy = -dy

    # Move the video
    x += dx
    y += dy

    # Convert the image to a Pygame surface with per-pixel alpha
    frame_surface = pygame.surfarray.make_surface(image.swapaxes(0, 1)).convert_alpha()

    # Draw the video frame with transparency
    screen.blit(frame_surface, (x, y))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

    # Increment the frame index
    current_frame += 1
