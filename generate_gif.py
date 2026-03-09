import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import time

WIDTH = 900
HEIGHT = 550
BG_COLOR = (13, 17, 23)      # GitHub Dark background
TEXT_COLOR = (201, 209, 217) # GitHub Dark text
GREEN = (63, 185, 80)        # Success green
PURPLE = (163, 113, 247)     # Distinctive purple
BLUE = (88, 166, 255)        # Info blue
YELLOW = (210, 153, 34)      # Warning/Step yellow
MAC_RED = (255, 95, 86)
MAC_YELLOW = (255, 189, 46)
MAC_GREEN = (39, 201, 63)

# Note: Using default font for PIL since we can't guarantee a specific TTF is installed
# on the host system. This ensures it runs without errors.
try:
    FONT = ImageFont.truetype("Courier", 16)
    FONT_BOLD = ImageFont.truetype("Courier-Bold", 16)
    FONT_TITLE = ImageFont.truetype("Arial", 28)
except IOError:
    # Fallback to default
    FONT = ImageFont.load_default()
    FONT_BOLD = ImageFont.load_default()
    FONT_TITLE = ImageFont.load_default()

def draw_mac_window(draw):
    # Header bar
    draw.rectangle([0, 0, WIDTH, 30], fill=(22, 27, 34))
    # Mac buttons
    draw.ellipse([15, 8, 29, 22], fill=MAC_RED)
    draw.ellipse([35, 8, 49, 22], fill=MAC_YELLOW)
    draw.ellipse([55, 8, 69, 22], fill=MAC_GREEN)

def generate_frames():
    frames = []
    
    # Frame generation helper
    def add_frame(lines, show_cursor=False, duration_multiplier=1):
        img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
        draw = ImageDraw.Draw(img)
        draw_mac_window(draw)
        
        y = 50
        for i, (text, color) in enumerate(lines):
            draw.text((20, y), text, font=FONT, fill=color)
            y += 25
            
            if show_cursor and i == len(lines) - 1:
                # Draw cursor
                text_width = draw.textlength(text, font=FONT)
                draw.rectangle([20 + text_width + 5, y - 20, 20 + text_width + 15, y], fill=TEXT_COLOR)
                
        for _ in range(duration_multiplier):
            frames.append(img.copy())
            
    # Initial state
    lines = [("$ python flight_optimizer_qaoa.py", TEXT_COLOR)]
    add_frame(lines, show_cursor=True, duration_multiplier=10) # Pause before typing
    
    # Simulate typing the command line
    command = "$ python flight_optimizer_qaoa.py"
    current_cmd = ""
    for char in command:
        current_cmd += char
        lines = [(current_cmd, TEXT_COLOR)]
        add_frame(lines, show_cursor=True, duration_multiplier=2)
    
    add_frame(lines, show_cursor=False, duration_multiplier=5) # Hit enter
    
    # Output sequence
    outputs = [
        ("Welcome to the Quantum Aviation Optimizer (PoC) powered by QAOA.", BLUE),
        ("[INFO] Initializing Qrisp QAOA Backend...", TEXT_COLOR),
        ("[INFO] Building Conflict Graph from Flights (Nodes: 5, Edges: 5)", TEXT_COLOR),
        ("[INFO] Creating MaxCut Cost Operator...", TEXT_COLOR),
        ("[INFO] Creating RX_Mixer Operator...", TEXT_COLOR),
        ("[Q-RUN] Optimization Step 1/3: Loss = 5.0000", YELLOW),
        ("[Q-RUN] Optimization Step 2/3: Loss = 3.3333", YELLOW),
        ("[Q-RUN] Optimization Step 3/3: Loss = 2.5000", YELLOW),
        ("[INFO] QAOA Execution Complete. Retrieving measurements.", GREEN),
        ("", TEXT_COLOR),
        ("============================================================", TEXT_COLOR),
        ("State      | Probability  | Estimated Cut Size", TEXT_COLOR),
        ("============================================================", TEXT_COLOR),
        ("01010      | 0.4210       | 4", TEXT_COLOR),
        ("10101      | 0.4180       | 4", TEXT_COLOR),
        ("00110      | 0.0510       | 2", TEXT_COLOR),
        ("11001      | 0.0450       | 2", TEXT_COLOR),
        ("============================================================", TEXT_COLOR),
        ("", TEXT_COLOR),
        ("[SUCCESS] Optimal Fleet Partition Bitstring: 01010", PURPLE),
        ("✈️  Fleet A Assignments: FL102, FL104", GREEN),
        ("✈️  Fleet B Assignments: FL101, FL103, FL105", GREEN),
        ("$", TEXT_COLOR)
    ]
    
    current_lines = [lines[0]]
    for out_text, out_color in outputs:
        current_lines.append((out_text, out_color))
        # Keep only the last 18 lines to fit in window
        if len(current_lines) > 18:
            current_lines = current_lines[-18:]
        add_frame(current_lines, show_cursor=False, duration_multiplier=4)
        
    # Hold terminal result
    add_frame(current_lines, show_cursor=True, duration_multiplier=20)
    
    # --- TRANSITION TO UI COMPONENT ---
    # Fade overlay
    for alpha in range(0, 255, 50):
        img = frames[-1].copy()
        overlay = Image.new('RGBA', (WIDTH, HEIGHT), (13, 17, 23, alpha))
        img.paste(overlay, (0,0), overlay)
        frames.append(img.convert('RGB'))
    
    # Ensure there is a UI Component as requested (Stats Dashboard)
    ui_img = Image.new('RGB', (WIDTH, HEIGHT), color=(18, 22, 29))
    draw = ImageDraw.Draw(ui_img)
    draw_mac_window(draw)
    
    # Draw UI Cards
    # Header
    draw.text((300, 60), "QUANTUM ROUTING ENGINE", font=FONT_TITLE, fill=PURPLE)
    draw.text((360, 100), "Optimization Results", font=FONT, fill=TEXT_COLOR)
    
    # Card 1
    draw.rounded_rectangle([100, 160, 400, 300], radius=15, fill=(30, 35, 45), outline=BLUE, width=2)
    draw.text((120, 180), "- FLEET A -", font=FONT_BOLD, fill=BLUE)
    draw.text((120, 220), "✈ FL102 (NYC -> LND)", font=FONT, fill=TEXT_COLOR)
    draw.text((120, 250), "✈ FL104 (LND -> LAX)", font=FONT, fill=TEXT_COLOR)
    
    # Card 2
    draw.rounded_rectangle([480, 160, 780, 300], radius=15, fill=(30, 35, 45), outline=GREEN, width=2)
    draw.text((500, 180), "- FLEET B -", font=FONT_BOLD, fill=GREEN)
    draw.text((500, 210), "✈ FL101 (CDG -> DXB)", font=FONT, fill=TEXT_COLOR)
    draw.text((500, 240), "✈ FL103 (DXB -> SIN)", font=FONT, fill=TEXT_COLOR)
    draw.text((500, 270), "✈ FL105 (SIN -> SYD)", font=FONT, fill=TEXT_COLOR)
    
    # Stats Area at bottom
    draw.rounded_rectangle([100, 350, 780, 450], radius=15, fill=(20, 25, 35), outline=PURPLE, width=2)
    draw.text((130, 370), "METRICS", font=FONT_BOLD, fill=PURPLE)
    draw.text((130, 400), "Conflict Graph Edges: 5", font=FONT, fill=TEXT_COLOR)
    draw.text((450, 400), "QAOA Optimizations: 3 Steps", font=FONT, fill=TEXT_COLOR)
    draw.text((130, 420), "MaxCut Achieved: 4", font=FONT, fill=GREEN)
    draw.text((450, 420), "Optimal State Probability: 42.1%", font=FONT, fill=GREEN)
    
    # Add UI frame
    for _ in range(40): # Hold for 2 seconds
        frames.append(ui_img.copy())
        
    print("Generating global palette and saving GIF...")
    
    # STICT LINKEDIN REQUIREMENT: GLOBAL PALETTE CONVERSION
    # Generate global palette from sample frames
    sample = Image.new("RGB", (WIDTH, HEIGHT * 3))
    sample.paste(frames[0], (0,0))
    sample.paste(frames[len(frames)//2], (0,HEIGHT))
    sample.paste(frames[-1], (0,HEIGHT*2))
    palette = sample.quantize(colors=256, method=2)
    
    # Convert all frames to P-mode using global palette (No Dither)
    final_frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    
    os.makedirs("images", exist_ok=True)
    final_frames[0].save(
        "images/title-animation.gif", 
        save_all=True, 
        append_images=final_frames[1:], 
        optimize=True, 
        loop=0,
        duration=50
    )
    print("Successfully saved images/title-animation.gif")

if __name__ == "__main__":
    generate_frames()
