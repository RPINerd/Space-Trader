"""
Galactic Chart Rendering Dev Tool

Proof-of-concept rendering of the Galactic Chart screen.
Generates a random universe and displays it with interactive planet selection.
Click any point on the map to select the nearest planet.
"""

import tkinter as tk
from pathlib import Path
from random import choice

from src.constants import FRG_HEX, GALAXYHEIGHT, GALAXYWIDTH, INTERNAL_RES, SCALAR, Size, TechLevel
from src.universe import Planet, Universe
from src.utils import FontManager

# Screen layout (game pixels)
TITLE_H = 15
MAP_H = GALAXYHEIGHT  # 110
MAP_W = GALAXYWIDTH  # 154
MAP_MARGIN_X = 3  # horizontal margin on each side of the map
INFO_H = INTERNAL_RES - TITLE_H - MAP_H  # 35

SCREEN_W = INTERNAL_RES  # 160
SCREEN_H = INTERNAL_RES  # 160

# Visual palette
WHITE = "#FFFFFF"
BLACK = "#000000"

# Default fuel range for the jump-range circle (parsecs)
DEFAULT_FUEL = 20


def sc(game_px: int) -> int:
    """Convert game pixels to screen pixels."""
    return game_px * SCALAR


def find_nearest_planet(universe: Universe, gx: float, gy: float) -> Planet:
    """Return the planet closest to the given game-coordinate point (gx, gy)."""
    return min(
        universe.planets.values(),
        key=lambda p: (p.x - gx) ** 2 + (p.y - gy) ** 2,
    )


def draw_rounded_rect(canvas: tk.Canvas, bbox: tuple[int, int, int, int], r: int) -> None:
    """
    Draw a rounded-rectangle outline on a canvas.

    Args:
        canvas: Target canvas widget.
        bbox: (x1, y1, x2, y2) bounding box in screen pixels.
        r: Corner radius in screen pixels.
    """
    x1, y1, x2, y2 = bbox
    canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style="arc", outline=BLACK)
    canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style="arc", outline=BLACK)
    canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style="arc", outline=BLACK)
    canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style="arc", outline=BLACK)
    canvas.create_line(x1 + r, y1, x2 - r, y1, fill=BLACK)
    canvas.create_line(x1 + r, y2, x2 - r, y2, fill=BLACK)
    canvas.create_line(x1, y1 + r, x1, y2 - r, fill=BLACK)
    canvas.create_line(x2, y1 + r, x2, y2 - r, fill=BLACK)


def planet_description(planet: Planet) -> str:
    """
    Build the size / tech-level / government description string for the info bar.

    Args:
        planet: The planet to describe.

    Returns:
        A string like "Tiny Industrial Fascist State".
    """
    return f"{Size.name(planet.size)} {TechLevel.name(planet.tech_level)} {planet.get_government_name()} State"


def main() -> None:
    """Entry point for the Galactic Chart rendering dev tool."""
    font_dir = Path("assets/fonts")
    FontManager.load_font(font_dir / "palm-pilot-bold.ttf")
    FontManager.load_font(font_dir / "palm-pilot-small.ttf")

    universe = Universe()
    current_planet = choice(list(universe.planets.values()))

    # selected_planet is mutated via closure in on_click
    state: dict = {"selected": current_planet}

    root = tk.Tk()
    root.title("Galactic Chart - Dev")
    root.geometry(f"{sc(SCREEN_W)}x{sc(SCREEN_H)}")
    root.resizable(False, False)
    root.configure(background=BLACK)

    title_font = ("Palm Pilot Bold", -sc(9))
    info_font = ("Palm Pilot Bold", -sc(8))

    # ── Title bar ─────────────────────────────────────────────────────────────
    title_canvas = tk.Canvas(
        root, bg=BLACK, width=sc(SCREEN_W), height=sc(TITLE_H), highlightthickness=0
    )
    title_canvas.pack(side="top", fill="x")

    title_canvas.create_text(
        sc(2), sc(TITLE_H) // 2,
        text="Galactic Chart",
        fill=WHITE,
        anchor="w",
        font=title_font,
    )

    # B, S, Y, W shortcut buttons (right-aligned, drawn right-to-left)
    btn_w = sc(TITLE_H)  # square buttons
    for i, label in enumerate(["W", "Y", "S", "B"]):
        bx = sc(SCREEN_W) - (i + 1) * btn_w
        title_canvas.create_rectangle(bx, 0, bx + btn_w, sc(TITLE_H) - 1, fill=WHITE, outline=BLACK)
        title_canvas.create_text(bx + btn_w // 2, sc(TITLE_H) // 2, text=label, fill=BLACK, font=title_font)

    # ── Map canvas ────────────────────────────────────────────────────────────
    map_canvas = tk.Canvas(
        root,
        bg=WHITE,
        width=sc(MAP_W),
        height=sc(MAP_H),
        highlightthickness=0,
    )
    map_canvas.pack(side="top", padx=sc(MAP_MARGIN_X))

    # ── Info area ─────────────────────────────────────────────────────────────
    info_canvas = tk.Canvas(
        root, bg=WHITE, width=sc(SCREEN_W), height=sc(INFO_H), highlightthickness=0
    )
    info_canvas.pack(side="top", fill="x")

    def redraw() -> None:
        """Redraw map and info area for the current planet selection."""
        selected = state["selected"]
        map_canvas.delete("all")
        info_canvas.delete("all")

        # Draw all planets as scaled squares
        for planet in universe.planets.values():
            sx, sy = planet.x * SCALAR, planet.y * SCALAR
            map_canvas.create_rectangle(
                sx - SCALAR, sy - SCALAR, sx + SCALAR, sy + SCALAR,
                fill=FRG_HEX, outline=FRG_HEX,
            )

        # Jump-range circle around the player's current system
        cx, cy = current_planet.x * SCALAR, current_planet.y * SCALAR
        r = DEFAULT_FUEL * SCALAR
        map_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=BLACK, width=1)

        # Crosshair on the selected planet
        sx, sy = selected.x * SCALAR, selected.y * SCALAR
        arm = sc(4)
        map_canvas.create_line(sx - arm, sy, sx + arm, sy, fill=BLACK)
        map_canvas.create_line(sx, sy - arm, sx, sy + arm, fill=BLACK)

        # ── Info line 1: name / parsecs / Find ──────────────────────────────
        dist = current_planet.get_distance(selected)
        line1_y = sc(INFO_H) // 3

        info_canvas.create_text(sc(2), line1_y, text=selected.name, fill=BLACK, anchor="w", font=info_font)
        info_canvas.create_text(
            sc(SCREEN_W) // 2, line1_y,
            text=f"{dist} parsecs",
            fill=BLACK, anchor="center", font=info_font,
        )

        # "Find" rounded-rect button
        find_h = sc(10)
        find_w = sc(22)
        find_x2 = sc(SCREEN_W) - sc(3)
        find_x1 = find_x2 - find_w
        find_y1 = line1_y - find_h // 2
        find_y2 = line1_y + find_h // 2
        draw_rounded_rect(info_canvas, (find_x1, find_y1, find_x2, find_y2), find_h // 2)
        info_canvas.create_text(
            (find_x1 + find_x2) // 2, line1_y,
            text="Find", fill=BLACK, anchor="center", font=info_font,
        )

        # ── Info line 2: planet description ─────────────────────────────────
        info_canvas.create_text(
            sc(2), sc(INFO_H) * 2 // 3,
            text=planet_description(selected),
            fill=BLACK, anchor="w", font=info_font,
        )

    def on_click(event: tk.Event) -> None:
        """Select the nearest planet to the click position."""
        state["selected"] = find_nearest_planet(universe, event.x / SCALAR, event.y / SCALAR)
        redraw()

    map_canvas.bind("<Button-1>", on_click)

    redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
