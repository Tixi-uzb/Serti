import os
from PIL import Image, ImageDraw

def create_real_signature(filename):
    # Larger canvas for better quality
    img = Image.new('RGBA', (600, 200), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Define several strokes for "D. Raximov"
    # D
    strokes = [
        [(50, 40), (52, 140), (55, 150), (100, 145), (120, 110), (110, 60), (70, 45), (45, 50)], # D
        [(135, 145), (137, 147)], # dot
        # R
        [(160, 40), (170, 150)], # vertical
        [(155, 55), (200, 45), (220, 80), (165, 95), (225, 145)], # R loop
        # a
        [(240, 100), (230, 140), (250, 150), (265, 120), (265, 150)],
        # x
        [(275, 105), (310, 145)],
        [(310, 105), (275, 145)],
        # i
        [(325, 105), (325, 150), (340, 145)],
        [(327, 85), (328, 86)], # dot i
        # m
        [(350, 105), (350, 150)],
        [(350, 115), (370, 105), (370, 150)],
        [(370, 115), (390, 105), (390, 140), (410, 135)],
        # o
        [(425, 120), (415, 140), (425, 155), (435, 140), (425, 120)],
        # v
        [(445, 110), (455, 150), (490, 100), (580, 130), (480, 160)], # complex swoosh v
    ]
    
    def draw_realistic_stroke(points, width):
        if len(points) < 2: return
        import random
        # Sub-divide for jitter
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            dist = int(((x2-x1)**2 + (y2-y1)**2)**0.5) * 2
            for t in range(dist + 1):
                ratio = t / float(dist if dist > 0 else 1)
                jx = random.uniform(-0.5, 0.5)
                jy = random.uniform(-0.5, 0.5)
                px = x1 * (1 - ratio) + x2 * ratio + jx
                py = y1 * (1 - ratio) + y2 * ratio + jy
                # Vary radius for pressure
                r = width * (0.8 + 0.4 * random.random())
                draw.ellipse((px-r, py-r, px+r, py+r), fill=(10, 20, 120, 230))
    
    for s in strokes:
        draw_realistic_stroke(s, 2.5)
        # Adding a second shadow layer for "ink" effect
        draw_realistic_stroke(s, 1.2)

    img.save(filename)
    print(f"{filename} created!")

create_real_signature('sign.png')
