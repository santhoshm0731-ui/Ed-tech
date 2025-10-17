"""
eco_levels_table.py
Generates a table image for the EcoLearn 10-levels using Pillow (PIL).
Save and run: python eco_levels_table.py
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import platform

# ---------- Configuration ----------
OUT_PATH = "eco_levels_table.png"
WIDTH = 1400
PADDING = 12
HEADER_HEIGHT = 70
ROW_MIN_HEIGHT = 110
LINE_COLOR = (60, 60, 60)
BG_COLOR = (255, 255, 255)
HEADER_BG = (230, 245, 230)
TEXT_COLOR = (25, 25, 25)

# Column widths (tuned for the content)
COL_WIDTHS = [120, 230, 300, 540, 200]

# Table data
HEADERS = ["Level", "Theme / Focus Area", "Learning Goal",
           "Gamified Challenge (Real-World or Virtual)", "Impact Created"]

ROWS = [
    ["1. Eco Explorer", "🌍 Introduction to Earth & Sustainability",
     "Understand basics of environment, climate, and sustainability.",
     "Interactive story game on how human actions affect the planet.",
     "Builds awareness and curiosity."],

    ["2. Waste Wizard", "♻️ Waste Segregation & Management",
     "Learn about biodegradable vs non-biodegradable waste.",
     "Virtual waste segregation mini-game + Real task: segregate home waste for 3 days.",
     "Promotes daily sustainable habit."],

    ["3. Water Warrior", "💧 Water Conservation",
     "Learn about water scarcity & simple conservation techniques.",
     "Virtual “Save the Drops” challenge + real-life task: check and fix household leaks.",
     "Reduces water waste locally."],

    ["4. Energy Saver", "⚡ Energy & Power Awareness",
     "Understand renewable vs non-renewable energy.",
     "Game: Build your own solar-powered city. Real task: Track daily power use and reduce.",
     "Encourages energy-saving mindset."],

    ["5. Green Guardian", "🌳 Afforestation & Urban Greening",
     "Learn importance of trees & reforestation.",
     "Game: Grow a digital forest that reflects real planted trees. Real task: Plant 1 sapling and log it.",
     "Contributes to carbon reduction."],

    ["6. Plastic Buster", "🚯 Plastic Pollution Awareness",
     "Learn about plastic impact and alternatives.",
     "Game: “Plastic Attack” — eliminate plastics in a digital city. Real task: Avoid single-use plastic for a week.",
     "Builds zero-plastic habits."],

    ["7. Biodiversity Hero", "🐝 Wildlife & Ecosystem Balance",
     "Understand ecosystems, endangered species, and balance.",
     "Game: Create and balance your own ecosystem. Real task: Document 3 local species.",
     "Promotes respect for nature."],

    ["8. Clean Air Champion", "🌫️ Air Pollution & Climate Change",
     "Learn about causes, AQI, and prevention measures.",
     "Virtual air quality simulation game. Real task: Use public transport/cycle for a week.",
     "Reduces personal carbon footprint."],

    ["9. Sustainable Innovator", "🔧 Upcycling & Green Innovation",
     "Learn how innovation can reduce waste.",
     "Game: Design eco-products using virtual materials. Real task: Create DIY recycled product.",
     "Encourages creativity and problem-solving."],

    ["10. Eco Leader", "🏆 Community Leadership & Impact",
     "Empower students to lead eco-projects locally.",
     "Game: Manage a virtual eco-community. Real task: Conduct local eco-drive (tree, clean-up, or awareness).",
     "Fosters environmental leadership & teamwork."]
]

# ---------- Helper: load font ----------
def load_font(size=16, bold=False):
    system_name = platform.system()
    possible = []

    if system_name == "Windows":
        base_path = "C:\\Windows\\Fonts\\"
        if bold:
            possible = [
                os.path.join(base_path, "arialbd.ttf"),
                os.path.join(base_path, "segoeui.ttf")
            ]
        possible += [
            os.path.join(base_path, "arial.ttf"),
            os.path.join(base_path, "segoeui.ttf")
        ]
    else:  # Linux / Mac
        if bold:
            possible = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ]
        possible += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
        ]
    for p in possible:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_HEADER = load_font(20, bold=True)
FONT_CELL = load_font(16)

# ---------- Build image canvas ----------
num_rows = len(ROWS)
height_est = HEADER_HEIGHT + num_rows * ROW_MIN_HEIGHT + 2 * PADDING
img = Image.new("RGB", (WIDTH, height_est), color=BG_COLOR)
draw = ImageDraw.Draw(img)

# Draw header background
draw.rectangle([(0, 0), (WIDTH, HEADER_HEIGHT)], fill=HEADER_BG)

# Draw headers
x = PADDING
y = int(PADDING * 0.5) + 6
for i, h in enumerate(HEADERS):
    draw.text((x + 6, y), h, font=FONT_HEADER, fill=TEXT_COLOR)
    x += COL_WIDTHS[i]

# ---------- Draw rows ----------
y_cursor = HEADER_HEIGHT + PADDING
for r_idx, row in enumerate(ROWS):
    wrapped_cols = []
    max_cell_h = 0
    for c_idx, cell_text in enumerate(row):
        col_w = COL_WIDTHS[c_idx] - 2 * PADDING

        # approximate width of a character
        bbox_a = FONT_CELL.getbbox("a")
        avg_char_w = max(6, bbox_a[2] - bbox_a[0])
        max_chars = max(20, int(col_w / avg_char_w))

        wrapped = textwrap.fill(cell_text, width=max_chars)
        wrapped_cols.append(wrapped)

        # calculate height
        lines = wrapped.count("\n") + 1
        bbox_A = FONT_CELL.getbbox("A")
        line_h = (bbox_A[3] - bbox_A[1]) + 6
        text_h = lines * line_h
        if text_h + 2 * PADDING > max_cell_h:
            max_cell_h = text_h + 2 * PADDING

    row_h = max(ROW_MIN_HEIGHT, max_cell_h)

    # optional alternating background
    if r_idx % 2 == 0:
        draw.rectangle([(0, y_cursor), (WIDTH, y_cursor + row_h)], fill=(250, 255, 250))

    # draw each cell border and text
    x = 0
    for c_idx, wrapped in enumerate(wrapped_cols):
        w = COL_WIDTHS[c_idx]
        draw.rectangle([(x, y_cursor), (x + w, y_cursor + row_h)], outline=LINE_COLOR, width=1)
        tx = x + PADDING
        ty = y_cursor + PADDING // 2
        if c_idx == 0:
            draw.text((tx, ty), wrapped, font=FONT_HEADER, fill=TEXT_COLOR)
        else:
            draw.text((tx, ty), wrapped, font=FONT_CELL, fill=TEXT_COLOR)
        x += w

    y_cursor += row_h

# Draw outer border
draw.rectangle([(0, 0), (WIDTH - 1, y_cursor)], outline=LINE_COLOR, width=2)

# Crop to actual content height
img = img.crop((0, 0, WIDTH, y_cursor + PADDING))
img.save(OUT_PATH)
print(f"Saved table image to: {OUT_PATH}")
