import os
import random
import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import colorsys

def generate_art(temp, rain):
    """
    Generates abstract artwork based on temperature and rainfall influence.

    Args:
        temp (float): The average temperature in Celsius.
        rain (float): The average rainfall in mm.

    Returns:
        str: The path to the saved artwork ("artwork.png") if successful, None otherwise.
    """
    if temp is None or rain is None:
        print("Error: Temperature or rainfall data is missing.")
        return None

    try:
        print(f"Generating artwork for temperature: {temp}°C, rainfall: {rain}mm")

        # Create a new image
        width, height = 1200, 1200
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)

        # Add a general background color based on overall temperature feel
        base_color = (255, 255, 255) # Default white
        if temp < 10:
            base_color = (220, 230, 240) # Very light blue for cold
        elif 10 <= temp < 20:
            base_color = (230, 240, 250) # Light blue
        elif 20 <= temp < 25:
            base_color = (240, 250, 230) # Light greenish-yellow
        elif 25 <= temp < 30:
            base_color = (250, 240, 220) # Light yellowish-orange
        else: # temp >= 30
            base_color = (250, 220, 200) # Light orange

        draw.rectangle([0, 0, width, height], fill=base_color) # Draw background first

        # --- Draw shapes and elements based on temperature and rain ---

        if temp < 20:
            # Light blue/white hexagons and tiny circle shapes
            num_shapes = int(2000 + temp * 50 + rain * 10) # Influence number by rain too
            for _ in range(num_shapes):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(5, max(5, int(30 - temp + rain * 0.1))) # Size influenced by temp and rain
                color = random.choice([(200, 220, 255, 200), (255, 255, 255, 200)]) # Light blue or white

                shape_type = random.choice(['hexagon', 'circle'])
                if shape_type == 'hexagon':
                    points = []
                    for i in range(6):
                        angle = i * (math.pi / 3)
                        px = x + size * math.cos(angle)
                        py = y + size * math.sin(angle)
                        points.append((px, py))
                    draw.polygon(points, fill=color)
                else: # circle
                     circle_size = random.randint(1, max(1, int(5 - rain * 0.05))) # Tiny circles, smaller with more rain
                     x0, y0 = x - circle_size, y - circle_size
                     x1, y1 = x + circle_size, y + circle_size
                     if x0 > x1: x0, x1 = x1, x0
                     if y0 > y1: y0, y1 = y1, y0
                     draw.ellipse((x0, y0, x1, y1), fill=color)

        elif 20 <= temp < 25:
            # Darker blue, less white. Flower and grass-like shapes.
            num_shapes = int(1500 + (temp - 20) * 100 + rain * 8)
            for _ in range(num_shapes):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(10, max(10, int(50 + (temp - 20) * 5 + rain * 0.1)))
                # Darker blue, less white
                blue_shade = random.randint(100, max(100, int(180 - rain * 0.5))) # Blue shade influenced by rain
                color = random.choice([(50, 80, blue_shade, 220), (220, 220, 220, int(220 * (1 - rain * 0.01)))]) # Darker blue or less opaque white with rain

                shape_type = random.choice(['flower', 'grass'])
                if shape_type == 'flower':
                    flower_size = random.randint(size // 2, size)
                    num_petals = random.randint(5, 8)
                    petal_color = (random.randint(100, 200), random.randint(50, 150), random.randint(150, 250), 220) # Purplish/pinkish petals
                    center_color = (max(0, petal_color[0]-50), max(0, petal_color[1]-50), max(0, petal_color[2]-50), 220)
                    draw.ellipse((x-flower_size//4, y-flower_size//4, x+flower_size//4, y+flower_size//4), fill=center_color)
                    for i in range(num_petals):
                        angle = i * (2 * math.pi / num_petals)
                        petal_x = x + flower_size * math.cos(angle)
                        petal_y = y + flower_size * math.sin(angle)
                        x0_petal = min(x - flower_size//6, petal_x)
                        y0_petal = min(y - flower_size//6, petal_y)
                        x1_petal = max(x - flower_size//6, petal_x)
                        y1_petal = max(y - flower_size//6, petal_y)
                        draw.ellipse((x0_petal, y0_petal, x1_petal, y1_petal), fill=petal_color)
                else: # grass
                    grass_height = random.randint(size, size * 2)
                    grass_color = (random.randint(80, 150), random.randint(180, 255), random.randint(80, 150), 220) # Greenish
                    curve = random.randint(-size//2, size//2)
                    mid_x = x + curve
                    draw.line([(x, y), (mid_x, y - grass_height // 2), (x, y - grass_height)], fill=grass_color, width=random.randint(1, 3))

            # Add rain particles if rain is significant
            significant_rain_threshold = 10
            if rain > significant_rain_threshold:
                 num_rain_particles = int(rain * 20)
                 for _ in range(num_rain_particles):
                      px = random.randint(0, width)
                      py = random.randint(0, height)
                      particle_size = random.randint(1, 3)
                      particle_color = (100, 150, 200, random.randint(100, 200)) # Blueish rain particle
                      draw.ellipse((px-particle_size, py-particle_size, px+particle_size, py+particle_size), fill=particle_color)


        elif 25 <= temp < 30:
            # Mix of blue and yellow colored triangle and rectangle shapes.
            # Shapes like rivers sometimes with green tree leaves around.
            # If rain was significant that month than some rain particles will be on top of the temp shapes.
            num_shapes = int(1000 + (temp - 25) * 80 + rain * 5)
            significant_rain_threshold = 15 # Define what significant rain means in this range
            has_significant_rain = rain > significant_rain_threshold

            for _ in range(num_shapes):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(20, max(20, int(80 + (temp - 25) * 4 + rain * 0.1)))
                color = random.choice([(50, 100, 200, 220), (255, 220, 80, 220)]) # Blue or yellow

                shape_type = random.choice(['triangle', 'rectangle', 'river', 'leaf'])

                if shape_type == 'triangle':
                    points = []
                    for i in range(3):
                        angle = i * (2 * math.pi / 3) + random.uniform(-0.5, 0.5)
                        px = x + size * random.uniform(1, 2) * math.cos(angle)
                        py = y + size * random.uniform(1, 2) * math.sin(angle)
                        points.append((px, py))
                    draw.polygon(points, fill=color)
                elif shape_type == 'rectangle':
                    rect_width = random.randint(size // 2, size)
                    rect_height = random.randint(size // 2, size)
                    x0, y0 = x, y
                    x1, y1 = x + rect_width, y + rect_height
                    if x0 > x1: x0, x1 = x1, x0
                    if y0 > y1: y0, y1 = y1, y0
                    draw.rectangle((x0, y0, x1, y1), fill=color)
                elif shape_type == 'river':
                     river_width = random.randint(size // 4, size // 2)
                     river_length = random.randint(size * 2, size * 5)
                     angle = random.uniform(0, 2 * math.pi)
                     ex = x + int(river_length * math.cos(angle))
                     ey = y + int(river_length * math.sin(angle))
                     river_color = (50, 150, 200, 220) # Blueish for river
                     draw.line((x, y, ex, ey), fill=river_color, width=river_width, joint="curve") # Use curve joint for smoother river
                else: # leaf
                     leaf_size = random.randint(size // 4, size // 2)
                     leaf_color = (50, random.randint(150, 220), 50, 220) # Greenish for leaves
                     x0_leaf, y0_leaf = x - leaf_size, y - leaf_size
                     x1_leaf, y1_leaf = x + leaf_size, y + leaf_size
                     if x0_leaf > x1_leaf: x0_leaf, x1_leaf = x1_leaf, x0_leaf
                     if y0_leaf > y1_leaf: y0_leaf, y1_leaf = y1_leaf, y0_leaf
                     draw.ellipse((x0_leaf, y0_leaf, x1_leaf, y1_leaf), fill=leaf_color)

            # Add rain particles if rain is significant
            if has_significant_rain:
                 num_rain_particles = int(rain * 15)
                 for _ in range(num_rain_particles):
                      px = random.randint(0, width)
                      py = random.randint(0, height)
                      particle_size = random.randint(1, 4)
                      particle_color = (120, 160, 210, random.randint(120, 220)) # Slightly lighter blue rain particle
                      draw.ellipse((px-particle_size, py-particle_size, px+particle_size, py+particle_size), fill=particle_color)


        elif 30 <= temp < 40:
            # Orange and red with square shapes and some spikey shapes around.
            # If rain was significant then grayish combined with red-orange colors. Red spikes. Yellow thunder shapes.
            num_shapes = int(800 + (temp - 30) * 70 + rain * 4)
            significant_rain_threshold = 20 # Define what significant rain means in this range
            has_significant_rain = rain > significant_rain_threshold

            for _ in range(num_shapes):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(25, max(25, int(100 + (temp - 30) * 5 + rain * 0.1)))

                if has_significant_rain:
                    # Grayish combined with red-orange
                    r = random.randint(180, 220)
                    g = random.randint(80, 120)
                    b = random.randint(60, 100)
                    gray_blend = random.uniform(0.3, min(0.6, rain * 0.001)) # How much to blend with gray, more with more rain
                    color = (
                        int(r * (1 - gray_blend) + 150 * gray_blend),
                        int(g * (1 - gray_blend) + 150 * gray_blend),
                        int(b * (1 - gray_blend) + 150 * gray_blend),
                        220
                    )
                else:
                    # Orange and red
                    color = random.choice([(255, random.randint(100, 160), 0, 220), (random.randint(200, 255), 0, 0, 220)])


                shape_type = random.choice(['square', 'spikey', 'thunder'] if has_significant_rain else ['square', 'spikey'])

                if shape_type == 'square':
                    square_size = random.randint(size // 2, size)
                    x0, y0 = x, y
                    x1, y1 = x + square_size, y + square_size
                    if x0 > x1: x0, x1 = x1, x0
                    if y0 > y1: y0, y1 = y1, y0
                    draw.rectangle((x0, y0, x1, y1), fill=color)
                elif shape_type == 'spikey':
                     spike_length = random.randint(size // 2, size)
                     spike_width = random.randint(1, 5)
                     angle = random.uniform(0, 2 * math.pi)
                     ex = x + int(spike_length * math.cos(angle))
                     ey = y + int(spike_length * math.sin(angle))
                     spike_color = (255, 0, 0, 220) if has_significant_rain else color # Red spikes if significant rain
                     draw.line((x, y, ex, ey), fill=spike_color, width=spike_width)
                elif shape_type == 'thunder':
                     thunder_size = random.randint(size, size * 2)
                     thunder_color = (255, 255, 0, 220) # Yellow thunder
                     # Draw a simplified zig-zag thunder shape
                     points = [
                         (x, y),
                         (x + thunder_size // 3, y + thunder_size // 2),
                         (x, y + thunder_size),
                         (x + thunder_size // 2, y + thunder_size // 2),
                         (x + thunder_size, y)
                     ]
                     draw.line(points, fill=thunder_color, width=random.randint(2, 5))

            # Add rain particles if rain is significant
            if has_significant_rain:
                 num_rain_particles = int(rain * 10)
                 for _ in range(num_rain_particles):
                      px = random.randint(0, width)
                      py = random.randint(0, height)
                      particle_size = random.randint(1, 5)
                      particle_color = (150, 150, 150, random.randint(150, 250)) # Grayish rain particle
                      draw.ellipse((px-particle_size, py-particle_size, px+particle_size, py+particle_size), fill=particle_color)


        # Add a subtle texture overlay (optional, can be adjusted)
        # Ensure this is drawn *after* the main shapes
        add_texture(img, temp, rain)


        # Add info label
        draw = ImageDraw.Draw(img)
        # Ensure the info label rectangle coordinates are ordered correctly
        x0_label, y0_label, x1_label, y1_label = 5, 5, 250, 30
        if x0_label > x1_label: x0_label, x1_label = x1_label, x0_label
        if y0_label > y1_label: y0_label, y1_label = y1_label, y0_label
        draw.rectangle([x0_label, y0_label, x1_label, y1_label], fill=(0, 0, 0, 180))
        draw.text((10, 10), f"Temp: {temp:.1f}°C, Rain: {rain:.1f}mm", fill=(255, 255, 255))


        # Save the image
        img.save("artwork.png")
        print("Artwork generated successfully: artwork.png")
        return "artwork.png"

    except Exception as e:
        print(f"Error generating artwork: {e}")
        return None


def add_texture(img, temp, rain):
    """Add texture overlay to the image for more artistic feel."""
    # Create a texture layer
    texture = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw_texture = ImageDraw.Draw(texture)

    # Add noise pattern
    for _ in range(50000):
        x = random.randint(0, img.width-1)
        y = random.randint(0, img.height-1)
        # Vary the intensity based on position for a more natural look
        intensity = random.randint(0, 40)
        draw_texture.point((x, y), fill=(255, 255, 255, intensity))

    # Apply texture with reduced opacity
    img.paste(Image.alpha_composite(img.convert('RGBA'), texture))


if __name__ == '__main__':
    print("Testing art generation module...")
    # Test cases for different ranges
    test_cases = [
        (10.0, 5.0),  # Temp < 20, Low Rain
        (15.0, 30.0), # Temp < 20, High Rain
        (22.0, 8.0),  # 20 <= Temp < 25, Low Rain
        (23.0, 20.0), # 20 <= Temp < 25, Moderate Rain
        (27.0, 10.0), # 25 <= Temp < 30, Low Rain
        (28.0, 40.0), # 25 <= Temp < 30, Significant Rain
        (32.0, 5.0),  # 30 <= Temp < 40, Low Rain
        (35.0, 50.0), # 30 <= Temp < 40, Significant Rain
        (5.0, 150.0), # Edge case: Cold and very rainy
        (38.0, 500.0) # Edge case: Hot and extremely rainy
    ]

    for sample_temp, sample_rain in test_cases:
        print(f"\nGenerating for Temp: {sample_temp}°C, Rain: {sample_rain}mm")
        image_file = generate_art(sample_temp, sample_rain)
        if image_file:
            print(f"Test successful. Image saved to: {image_file}")
        else:
            print("Test failed.")
