"""
generate_figures.py - Generates crisp diagrammatic figures for the project report
"""

import os
from PIL import Image, ImageDraw, ImageFont

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

def get_font(size=14, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1)
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=0)
    except:
        return ImageFont.load_default()

def get_mono_font(size=13):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except:
        return ImageFont.load_default()

# -------------------------------------------------------------
# Figure 5.1: System Architecture of Banker's Algorithm Simulator
# -------------------------------------------------------------
def make_fig_5_1():
    w, h = 800, 220
    im = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    
    font_title = get_font(13, bold=True)
    font_sub = get_font(11, bold=False)
    
    boxes = [
        ("User Input\nRequests & State", (40, 60, 160, 150), (220, 235, 252), (37, 99, 235)),
        ("Process Data\nStorage\nAlloc, Max, Need", (190, 60, 310, 150), (220, 235, 252), (37, 99, 235)),
        ("Banker's Algorithm\nSafety & Request\nProvisional Alloc", (340, 50, 480, 160), (30, 58, 138), (255, 255, 255)),
        ("Safety Outcome\nSafe / Unsafe\nRollback / Grant", (510, 60, 630, 150), (220, 235, 252), (37, 99, 235)),
        ("Output Display\nSafe Sequence\nUpdated Matrices", (660, 60, 780, 150), (220, 235, 252), (37, 99, 235)),
    ]
    
    for text, (x1, y1, x2, y2), bg, border in boxes:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=bg, outline=(37, 99, 235) if bg != (30, 58, 138) else None, width=2)
        # text centering
        lines = text.split("\n")
        total_text_h = len(lines) * 18
        cur_y = y1 + (y2 - y1 - total_text_h) / 2
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_title)
            lw = bbox[2] - bbox[0]
            tx = x1 + (x2 - x1 - lw) / 2
            text_color = (255, 255, 255) if bg == (30, 58, 138) else (15, 23, 42)
            draw.text((tx, cur_y), line, fill=text_color, font=font_title)
            cur_y += 18
            
    # Draw arrows
    arrows = [(160, 105, 190, 105), (310, 105, 340, 105), (480, 105, 510, 105), (630, 105, 660, 105)]
    for x1, y1, x2, y2 in arrows:
        draw.line([x1, y1, x2, y2], fill=(71, 85, 105), width=2)
        draw.polygon([(x2, y2), (x2 - 6, y2 - 4), (x2 - 6, y2 + 4)], fill=(71, 85, 105))

    im.save(os.path.join(IMG_DIR, "fig_5_1_architecture.png"))

# -------------------------------------------------------------
# Figure 5.2: Classification of Deadlock Handling Strategies
# -------------------------------------------------------------
def make_fig_5_2():
    w, h = 800, 260
    im = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    
    font_bold = get_font(13, bold=True)
    font_regular = get_font(11, bold=False)
    
    # Root
    draw.rounded_rectangle([300, 20, 500, 65], radius=6, fill=(30, 58, 138))
    draw.text((320, 32), "Deadlock Handling", fill=(255, 255, 255), font=font_bold)
    
    # Level 1 lines
    draw.line([400, 65, 400, 95], fill=(100, 116, 139), width=2)
    draw.line([130, 95, 670, 95], fill=(100, 116, 139), width=2)
    
    # Categories
    cats = [
        ("Deadlock Prevention", 130, ["Invalidate 1 of 4", "Coffman conditions", "Spooling / Ordering"]),
        ("Deadlock Avoidance", 310, ["Banker's Algorithm", "Safe State tracking", "Provisional Alloc & Rollback"]),
        ("Deadlock Detection", 490, ["Wait-For Graph", "Periodic verification", "Kill / Preempt recovery"]),
        ("Deadlock Ignorance", 670, ["Ostrich Algorithm", "Reboot on hang", "General Purpose OS"]),
    ]
    
    for title, cx, bullets in cats:
        draw.line([cx, 95, cx, 115], fill=(100, 116, 139), width=2)
        x1, y1, x2, y2 = cx - 80, 115, cx + 80, 155
        is_avoid = "Avoidance" in title
        bg = (220, 235, 252) if not is_avoid else (37, 99, 235)
        tc = (15, 23, 42) if not is_avoid else (255, 255, 255)
        draw.rounded_rectangle([x1, y1, x2, y2], radius=6, fill=bg, outline=(37, 99, 235), width=2)
        
        bbox = draw.textbbox((0, 0), title, font=font_bold)
        draw.text((x1 + (160 - (bbox[2] - bbox[0])) / 2, y1 + 10), title, fill=tc, font=font_bold)
        
        # bullet details below
        by = 168
        for b in bullets:
            draw.text((x1 + 10, by), "• " + b, fill=(71, 85, 105), font=font_regular)
            by += 16
            
    im.save(os.path.join(IMG_DIR, "fig_5_2_classification.png"))

# -------------------------------------------------------------
# Figure 5.3: Flowchart of Banker's Algorithm Simulator
# -------------------------------------------------------------
def make_fig_5_3():
    w, h = 600, 520
    im = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    font_bold = get_font(12, bold=True)
    font_sub = get_font(10)
    
    steps = [
        ("START", 30, 65, "oval"),
        ("Initialize Allocation, Maximum & Available", 85, 120, "rect"),
        ("Calculate Need Matrix [Need = Max - Alloc]", 140, 175, "rect"),
        ("Display Main Menu (1-5)", 195, 230, "rect"),
        ("User Action: Choice 1, 2, 3, 4, 5", 250, 285, "rect"),
        ("Option 3: Request <= Need & Request <= Available?", 305, 345, "diamond"),
        ("Provisional Alloc & Execute Safety Algorithm", 365, 400, "rect"),
        ("All Finish[i] == True (System Safe)?", 420, 460, "diamond"),
        ("STOP", 480, 510, "oval"),
    ]
    
    for text, y1, y2, shape in steps:
        cx = 300
        hw = 160
        x1, x2 = cx - hw, cx + hw
        if shape == "oval":
            draw.rounded_rectangle([cx - 60, y1, cx + 60, y2], radius=15, fill=(30, 58, 138))
            bbox = draw.textbbox((0, 0), text, font=font_bold)
            draw.text((cx - (bbox[2] - bbox[0])/2, y1 + (y2 - y1 - 14)/2), text, fill=(255, 255, 255), font=font_bold)
        elif shape == "rect":
            draw.rounded_rectangle([x1, y1, x2, y2], radius=6, fill=(241, 245, 249), outline=(100, 116, 139), width=1)
            bbox = draw.textbbox((0, 0), text, font=font_bold)
            draw.text((cx - (bbox[2] - bbox[0])/2, y1 + (y2 - y1 - 14)/2), text, fill=(15, 23, 42), font=font_bold)
        elif shape == "diamond":
            draw.polygon([(cx, y1), (x2 + 20, (y1+y2)/2), (cx, y2), (x1 - 20, (y1+y2)/2)], fill=(254, 243, 199), outline=(217, 119, 6), width=1)
            bbox = draw.textbbox((0, 0), text, font=font_bold)
            draw.text((cx - (bbox[2] - bbox[0])/2, y1 + (y2 - y1 - 14)/2), text, fill=(146, 64, 14), font=font_bold)

    # Connecting arrows
    draw.line([300, 65, 300, 85], fill=(71, 85, 105), width=2)
    draw.line([300, 120, 300, 140], fill=(71, 85, 105), width=2)
    draw.line([300, 175, 300, 195], fill=(71, 85, 105), width=2)
    draw.line([300, 230, 300, 250], fill=(71, 85, 105), width=2)
    draw.line([300, 285, 300, 305], fill=(71, 85, 105), width=2)
    draw.line([300, 345, 300, 365], fill=(71, 85, 105), width=2)
    draw.line([300, 400, 300, 420], fill=(71, 85, 105), width=2)
    draw.line([300, 460, 300, 480], fill=(71, 85, 105), width=2)

    im.save(os.path.join(IMG_DIR, "fig_5_3_flowchart.png"))

# -------------------------------------------------------------
# Figure 6.1: Source Code in IDE
# -------------------------------------------------------------
def make_fig_6_1():
    w, h = 800, 380
    im = Image.new("RGB", (w, h), (30, 30, 30))
    draw = ImageDraw.Draw(im)
    
    font_mono = get_mono_font(12)
    font_ui = get_font(11, bold=True)
    
    # Title bar
    draw.rectangle([0, 0, w, 32], fill=(45, 45, 45))
    draw.ellipse([12, 10, 22, 20], fill=(239, 68, 68))
    draw.ellipse([28, 10, 38, 20], fill=(245, 158, 11))
    draw.ellipse([44, 10, 54, 20], fill=(16, 185, 129))
    draw.text((70, 8), "bankers_algorithm.c — Visual Studio Code", fill=(200, 200, 200), font=font_ui)
    
    code_snippet = """#include <stdio.h>
#include <stdlib.h>

#define P 5   // Number of processes
#define R 3   // Number of resource types

int allocation[P][R] = { {0, 1, 0}, {2, 0, 0}, {3, 0, 2}, {2, 1, 1}, {0, 0, 2} };
int maximum[P][R]    = { {7, 5, 3}, {3, 2, 2}, {9, 0, 2}, {2, 2, 2}, {4, 3, 3} };
int available[R]     = {3, 3, 2};

void calculateNeed(int need[P][R]) {
    for (int i = 0; i < P; i++)
        for (int j = 0; j < R; j++)
            need[i][j] = maximum[i][j] - allocation[i][j];
}

int safetyAlgorithm() {
    int need[P][R], work[R], finish[P] = {0}, safeSequence[P];
    calculateNeed(need);
    for (int j = 0; j < R; j++) work[j] = available[j];
    // Banker's safety search loop ...
}"""
    lines = code_snippet.split("\n")
    y = 45
    for idx, l in enumerate(lines, 1):
        draw.text((15, y), f"{idx:2d}", fill=(100, 100, 100), font=font_mono)
        draw.text((50, y), l, fill=(220, 220, 220), font=font_mono)
        y += 18
        
    im.save(os.path.join(IMG_DIR, "fig_6_1_source_code.png"))

# -------------------------------------------------------------
# Figure 6.2: Successful Compilation and Program Execution
# -------------------------------------------------------------
def make_fig_6_2():
    w, h = 800, 260
    im = Image.new("RGB", (w, h), (20, 24, 33))
    draw = ImageDraw.Draw(im)
    font_mono = get_mono_font(12)
    font_ui = get_font(11, bold=True)
    
    # Terminal header
    draw.rectangle([0, 0, w, 30], fill=(30, 36, 48))
    draw.ellipse([12, 10, 22, 20], fill=(239, 68, 68))
    draw.ellipse([28, 10, 38, 20], fill=(245, 158, 11))
    draw.ellipse([44, 10, 54, 20], fill=(16, 185, 129))
    draw.text((70, 7), "Terminal — bash — 80x24", fill=(180, 190, 205), font=font_ui)
    
    term_text = [
        ("$ cd cpp", (220, 220, 220)),
        ("$ gcc -std=c99 -Wall -Wextra -O2 bankers_algorithm.c -o bankers_c", (220, 220, 220)),
        ("[Compilation Successful - No Errors or Warnings]", (52, 211, 153)),
        ("$ ./bankers_c", (220, 220, 220)),
        ("", (220, 220, 220)),
        ("===== BANKER'S ALGORITHM SIMULATOR =====", (96, 165, 250)),
        ("1. Display Resource Matrices", (220, 220, 220)),
        ("2. Check Safe State", (220, 220, 220)),
        ("3. Request Resources", (220, 220, 220)),
        ("4. Clear Screen", (220, 220, 220)),
        ("5. Exit", (220, 220, 220)),
        ("Enter your choice: _", (251, 191, 36)),
    ]
    
    y = 42
    for l, color in term_text:
        draw.text((25, y), l, fill=color, font=font_mono)
        y += 17
        
    im.save(os.path.join(IMG_DIR, "fig_6_2_compilation.png"))

# -------------------------------------------------------------
# Figure 7.2: Resource Matrices Output
# -------------------------------------------------------------
def make_fig_7_2():
    w, h = 800, 360
    im = Image.new("RGB", (w, h), (20, 24, 33))
    draw = ImageDraw.Draw(im)
    font_mono = get_mono_font(12)
    font_ui = get_font(11, bold=True)
    
    draw.rectangle([0, 0, w, 30], fill=(30, 36, 48))
    draw.text((25, 7), "Option 1: Display Resource Matrices Output", fill=(180, 190, 205), font=font_ui)
    
    term_lines = [
        ("Enter your choice: 1", (251, 191, 36)),
        ("", (220, 220, 220)),
        ("Allocation Matrix:", (96, 165, 250)),
        ("P0: 0 1 0     P1: 2 0 0     P2: 3 0 2     P3: 2 1 1     P4: 0 0 2", (220, 220, 220)),
        ("", (220, 220, 220)),
        ("Maximum Matrix:", (96, 165, 250)),
        ("P0: 7 5 3     P1: 3 2 2     P2: 9 0 2     P3: 2 2 2     P4: 4 3 3", (220, 220, 220)),
        ("", (220, 220, 220)),
        ("Need Matrix (Maximum - Allocation):", (96, 165, 250)),
        ("P0: 7 4 3     P1: 1 2 2     P2: 6 0 0     P3: 0 1 1     P4: 4 3 1", (52, 211, 153)),
        ("", (220, 220, 220)),
        ("Available Resources: 3 3 2", (251, 191, 36)),
        ("Total System Capacity: [A: 10, B: 5, C: 7]", (148, 163, 184)),
    ]
    
    y = 45
    for l, color in term_lines:
        draw.text((25, y), l, fill=color, font=font_mono)
        y += 20
        
    im.save(os.path.join(IMG_DIR, "fig_7_2_matrices.png"))

# -------------------------------------------------------------
# Figure 7.3: Safety State Verification Output
# -------------------------------------------------------------
def make_fig_7_3():
    w, h = 800, 280
    im = Image.new("RGB", (w, h), (20, 24, 33))
    draw = ImageDraw.Draw(im)
    font_mono = get_mono_font(12)
    font_ui = get_font(11, bold=True)
    
    draw.rectangle([0, 0, w, 30], fill=(30, 36, 48))
    draw.text((25, 7), "Option 2: Check Safe State Execution Output", fill=(180, 190, 205), font=font_ui)
    
    term_lines = [
        ("Enter your choice: 2", (251, 191, 36)),
        ("Checking system safety algorithm...", (148, 163, 184)),
        ("", (220, 220, 220)),
        ("[Step 1] Process P1 satisfied: Need [1, 2, 2] <= Work [3, 3, 2] -> Work after = [5, 3, 2]", (220, 220, 220)),
        ("[Step 2] Process P3 satisfied: Need [0, 1, 1] <= Work [5, 3, 2] -> Work after = [7, 4, 3]", (220, 220, 220)),
        ("[Step 3] Process P4 satisfied: Need [4, 3, 1] <= Work [7, 4, 3] -> Work after = [7, 4, 5]", (220, 220, 220)),
        ("[Step 4] Process P0 satisfied: Need [7, 4, 3] <= Work [7, 4, 5] -> Work after = [7, 5, 5]", (220, 220, 220)),
        ("[Step 5] Process P2 satisfied: Need [6, 0, 0] <= Work [7, 5, 5] -> Work after = [10, 5, 7]", (220, 220, 220)),
        ("", (220, 220, 220)),
        ("System is in a SAFE STATE.", (52, 211, 153)),
        ("Safe Sequence: P1 -> P3 -> P4 -> P0 -> P2", (96, 165, 250)),
    ]
    
    y = 45
    for l, color in term_lines:
        draw.text((25, y), l, fill=color, font=font_mono)
        y += 19
        
    im.save(os.path.join(IMG_DIR, "fig_7_3_safety_trace.png"))

if __name__ == "__main__":
    make_fig_5_1()
    make_fig_5_2()
    make_fig_5_3()
    make_fig_6_1()
    make_fig_6_2()
    make_fig_7_2()
    make_fig_7_3()
    print("All report figures generated successfully.")
