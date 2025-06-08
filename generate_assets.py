import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import wave
import struct

ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_background():
    # Starry space background 800x600 black with white dots
    width, height = 800, 600
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    # Draw random stars
    for _ in range(200):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        brightness = np.random.randint(150, 256)
        draw.point((x, y), fill=(brightness, brightness, brightness))
    img.save(os.path.join(ASSETS_DIR, "background.png"))
    print("Created background.png")

def create_ship():
    # Simple white triangle pointing up on transparent background (50x50)
    size = 50
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    points = [(size//2, 5), (5, size-5), (size-5, size-5)]
    draw.polygon(points, fill=(255, 255, 255, 255))
    img.save(os.path.join(ASSETS_DIR, "ship.png"))
    print("Created ship.png")

def create_asteroid():
    # Gray lumpy circle approx 80x80
    size = 80
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    center = size//2
    points = []
    num_points = 12
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        radius = center - np.random.randint(5, 20)
        x = center + int(radius * np.cos(angle))
        y = center + int(radius * np.sin(angle))
        points.append((x,y))
    draw.polygon(points, fill=(120,120,120,255), outline=(170,170,170,255))
    img.save(os.path.join(ASSETS_DIR, "asteroid.png"))
    print("Created asteroid.png")

def create_bullet():
    # Small white circle 10x10
    size = 10
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((1,1,size-2,size-2), fill=(255,255,255,255))
    img.save(os.path.join(ASSETS_DIR, "bullet.png"))
    print("Created bullet.png")

def create_bomb():
    # Red circle with black outline 20x20
    size = 20
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((1,1,size-2,size-2), fill=(255,0,0,255), outline=(0,0,0,255), width=2)
    img.save(os.path.join(ASSETS_DIR, "bomb.png"))
    print("Created bomb.png")

def create_wav(filename, frequency=440, duration=0.3, volume=0.5):
    # Generate a simple sine wave .wav sound
    framerate = 44100
    amplitude = 32767 * volume
    nframes = int(duration * framerate)
    comptype = "NONE"
    compname = "not compressed"
    nchannels = 1
    sampwidth = 2

    wav_file = wave.open(filename, "w")
    wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

    for i in range(nframes):
        t = i / framerate
        value = int(amplitude * np.sin(2 * np.pi * frequency * t))
        data = struct.pack('<h', value)
        wav_file.writeframesraw(data)

    wav_file.close()
    print(f"Created {os.path.basename(filename)}")

def create_shoot_sound():
    # high short beep ~880Hz
    create_wav(os.path.join(ASSETS_DIR, "shoot.wav"), frequency=880, duration=0.15, volume=0.4)

def create_bomb_sound():
    # lower frequency beep ~220Hz longer
    create_wav(os.path.join(ASSETS_DIR, "bomb.wav"), frequency=220, duration=0.5, volume=0.4)

def create_explosion_sound():
    # Noise burst explosion
    framerate = 44100
    duration = 0.5
    amplitude = 32767 * 0.4
    nframes = int(duration * framerate)
    nchannels = 1
    sampwidth = 2

    filename = os.path.join(ASSETS_DIR, "explosion.wav")
    wav_file = wave.open(filename, "w")
    wav_file.setparams((nchannels, sampwidth, framerate, nframes, "NONE", "not compressed"))

    for i in range(nframes):
        # random noise scaled by a decreasing envelope
        envelope = 1 - (i / nframes)
        value = int(amplitude * envelope * np.random.uniform(-1,1))
        data = struct.pack('<h', value)
        wav_file.writeframesraw(data)

    wav_file.close()
    print("Created explosion.wav")

def create_background_music():
    # simple soft looping tone with slowly changing pitch
    framerate = 44100
    duration = 10  # 10 seconds
    amplitude = 32767 * 0.1
    nframes = int(duration * framerate)
    nchannels = 1
    sampwidth = 2

    filename = os.path.join(ASSETS_DIR, "background.wav")
    wav_file = wave.open(filename, "w")
    wav_file.setparams((nchannels, sampwidth, framerate, nframes, "NONE", "not compressed"))

    for i in range(nframes):
        t = i / framerate
        # frequency modulated sine wave between 220Hz and 440Hz
        freq = 220 + 110 * np.sin(2 * np.pi * 0.1 * t)
        value = int(amplitude * np.sin(2 * np.pi * freq * t))
        data = struct.pack('<h', value)
        wav_file.writeframesraw(data)

    wav_file.close()
    print("Created background.wav")

def main():
    create_background()
    create_ship()
    create_asteroid()
    create_bullet()
    create_bomb()
    create_shoot_sound()
    create_bomb_sound()
    create_explosion_sound()
    create_background_music()

if __name__ == "__main__":
    main()
