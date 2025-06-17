# -*- coding: utf-8 -*-
"""
Copyright (C) 2025 The Nathan Network, Inc.
This free software is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3, see LICENSE.md.
"""
import pygame
import math
import os
import sys
import struct
import random
import tkinter.messagebox

def resource_path(relative_path: str) -> str:
    """Return the proper path to bundled data (for onefile .exe or dev mode)."""
    try:
        base_path = sys._MEIPASS  # type: ignore | PyInstaller sets this at runtime
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def splash_screen() -> None:
    font_path = os.path.join(assetsdir, 'fonts', "Orbitron-Bold.ttf")
    font_size = 96
    font = pygame.font.Font(font_path, font_size)
    start_time = pygame.time.get_ticks()
    duration = random.randint(6000, 8000)
    bar_width = 400
    bar_height = 24
    bar_color = (80, 200, 255)
    bar_bg = (60, 60, 60)
    while pygame.time.get_ticks() - start_time < duration:
        win.fill((30, 30, 30))
        t = (pygame.time.get_ticks() - start_time) / duration
        # Animate color
        scale = 1.0
        color = (
            max(0, min(255, 102 + int(55 * math.sin(t * 2 * math.pi)))),
            max(0, min(255, 0 + int(55 * math.sin(t * 3 * math.pi + 1)))),
            153
        )
        text_surf = font.render("Wilco", True, color)
        w, h = text_surf.get_size()
        text_surf = pygame.transform.smoothscale(
            text_surf, (int(w * scale), int(h * scale))
        )
        win.blit(
            text_surf,
            (
                win.get_width() // 2 - text_surf.get_width() // 2,
                win.get_height() // 2 - text_surf.get_height() // 2,
            ),
        )
        # Draw loading bar background
        bar_x = win.get_width() // 2 - bar_width // 2
        bar_y = win.get_height() // 2 + h // 2 + 40
        pygame.draw.rect(win, bar_bg, (bar_x, bar_y, bar_width, bar_height), border_radius=8)
        # Draw loading bar progress
        progress = min(1.0, t)
        pygame.draw.rect(win, bar_color, (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=8)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)

def character_selection_screen() -> str:
    """Interactive character selection screen. Returns chosen image filename."""
    win.fill((30, 30, 40))
    pygame.display.set_caption("Select Character | Wilco")
    choices: list[tuple[str, str]] = [
        ('cat.png', "Cat"),
        ('dog.png', "Dog")
    ]
    selected = 0
    bytesized_path: str = os.path.join(assetsdir, 'fonts', "Bytesized-Regular.ttf")
    font = pygame.font.Font(bytesized_path, 48)
    running = True
    while running:
        win.fill((30, 30, 40))
        # Draw title
        title = font.render("Select Your Character", True, (200, 220, 255))
        win.blit(title, (win.get_width() // 2 - title.get_width() // 2, 40))
        # Draw character images and names
        for i, (imgfile, label) in enumerate(choices):
            try:
                if os.path.exists(os.path.join(assetsdir, 'images', 'front-'+imgfile)):
                    img = pygame.image.load(os.path.join(assetsdir, 'images', 'front-'+imgfile)).convert_alpha()
                else:
                    img = pygame.image.load(os.path.join(assetsdir, 'images', imgfile)).convert_alpha()
                img = pygame.transform.smoothscale(img, (120, 120))
            except Exception:
                img = pygame.Surface((120, 120))
                img.fill((80, 80, 80))
            x = win.get_width() // 2 + (i - selected) * 200 - 60
            y = win.get_height() // 2
            border_color = (255, 255, 0) if i == selected else (100, 100, 100)
            pygame.draw.rect(win, border_color, (x-10, y-10, 140, 140), 4)
            win.blit(img, (x, y))
            label_surf = font.render(label, True, border_color)
            win.blit(label_surf, (x + 60 - label_surf.get_width() // 2, y + 130))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    selected = (selected + 1) % len(choices)
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    selected = (selected - 1) % len(choices)
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    running = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A button
                    running = False
                if event.button == 4:  # LB
                    selected = (selected - 1) % len(choices)
                if event.button == 5:  # RB
                    selected = (selected + 1) % len(choices)
        clock.tick(30)
    return choices[selected][0]

def credits_screen() -> None:
    """Display scrolling credits with centered lines and gradient background."""
    lines: list[tuple[str, bool, bool, str]] = [
        ("Credits", True, True, None),  # (text, is_title, is_centered)
        ('-'.center(win.get_width(), "-"), False, False, None),
        ("", False, False, None),
        ("Programming by:    Nathan Chonot", False, True, "programmer"),
        ("Game engine by:    Nathan Chonot", False, True, "programmer"),
        ("Idea by:           Kath Hill", False, True, 'idea'),
        ("Music by: ", False, True, "subtitle"),
        ("    - BGM - Gloomy_Background755", False, True, "programmer"),
        ("    - Credits BGM - JXM & Polaris", False, True, "programmer"),
        ("", False, False, None),
        ('-'.center(win.get_width(), "-"), False, False, ""),
        ("", False, False, None),
        ("Early testers:", False, True, 'subtitle'),
        ("    - Kath Hill", False, True, "tester"),
        ("    - Ahshanti Poulard", False, True, "tester"),
        ("    - Karla Zavala", False, True, "tester"),
        ("", False, False, ""),
        ('-'.center(win.get_width(), "-"), False, False, ""),
        ("", False, False, ""),
        ("Fonts by:", False, True, 'subtitle'),
        ("    - Matt McInerney - Orbitron", False, True, "Orbitron"),
        ("    - Peter Hull - VT323", False, True, "VT323"),
        ("    - Craig Rozynski - Comic Neue", False, True, "ComicNeue"),
        ("    - Baltdev - Bytesized", False, True, "Bytesized"),
        ("    - WDXLLubrifontTC - NightFurySL2001", False, True, "WDXLLubrifontTC"),
        ("", False, False, ""),
        ('-'.center(win.get_width(), "-"), False, False, ""),
        ("", False, False, ""),
        ("Special thanks to:", False, True, 'subtitle'),
        ("    - The pygame community", False, True, "programmer"),
        ("", False, False, ""),
    ]
    orbitron_path: str = os.path.join(assetsdir, 'fonts', "Orbitron-Bold.ttf")
    regular_font: pygame.font.Font = pygame.font.Font(None, 40)
    title_font: pygame.font.Font = pygame.font.Font(orbitron_path, 64)
    VT323_fontpath: str = os.path.join(assetsdir, 'fonts', "VT323-Regular.ttf")
    ComicNeue_fontpath: str = os.path.join(assetsdir, 'fonts', "ComicNeue-Regular.ttf")
    bytesized_path: str = os.path.join(assetsdir, 'fonts', "Bytesized-Regular.ttf")
    WDXLLubrifontTC_path: str = os.path.join(assetsdir, 'fonts', "WDXLLubrifontTC-Regular.ttf")
    spacing: int = 60
    # Pre-render surfaces and calculate heights
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(os.path.join(assetsdir, 'sounds', 'bgm-credits.mp3'))
    except pygame.error as e:
        print(f"Error loading music ({os.path.join(assetsdir, 'bgm-credits.mp3')}): {e}")
        pygame.quit()
        sys.exit()
    pygame.mixer.music.play(-1)
    rendered = []
    for text, is_title, is_centered, tag in lines:
        if is_centered:
            text = text.center(WIDTH, " ")
        font = title_font if is_title else regular_font
        try:
            if tag == 'programmer':
                font = pygame.font.Font(VT323_fontpath, 40) if os.path.exists(VT323_fontpath) else pygame.font.Font(None, 40)
            elif tag == 'idea' or tag == 'tester':
                font = pygame.font.Font(ComicNeue_fontpath, 40) if os.path.exists(ComicNeue_fontpath) else pygame.font.Font(None, 40)
            elif tag == 'subtitle':
                font = pygame.font.Font(WDXLLubrifontTC_path, 40) if os.path.exists(WDXLLubrifontTC_path) else pygame.font.Font(None, 40)
            elif tag == 'Orbitron':
                font = pygame.font.Font(orbitron_path, 40) if os.path.exists(orbitron_path) else pygame.font.Font(None, 40)
            elif tag == 'ComicNeue':
                font = pygame.font.Font(ComicNeue_fontpath, 40) if os.path.exists(ComicNeue_fontpath) else pygame.font.Font(None, 40)
            elif tag == 'VT323':
                font = pygame.font.Font(VT323_fontpath, 40) if os.path.exists(VT323_fontpath) else pygame.font.Font(None, 40)
            elif tag == 'WDXLLubrifontTC':
                font = pygame.font.Font(WDXLLubrifontTC_path, 40) if os.path.exists(WDXLLubrifontTC_path) else pygame.font.Font(None, 40)
            elif tag == 'Bytesized':
                font = pygame.font.Font(bytesized_path, 40) if os.path.exists(bytesized_path) else pygame.font.Font(None, 40)
            surf = font.render(text, True, (200, 220, 255) if is_title else (220, 220, 220))
        except Exception as e:
            font = pygame.font.Font(None, 40)
            surf = font.render(text, True, (200, 220, 255) if is_title else (220, 220, 220))
        rendered.append((surf, is_title))
    # Calculate total height for scrolling
    total_height = 0
    for surf, is_title in rendered:
        total_height += 200 if is_title else spacing
    start_y = win.get_height() + total_height // 2
    scroll_speed = 2.5
    y_offset = start_y

    def draw_gradient_background(surface, top_color, bottom_color):
        """Draw a vertical gradient from top_color to bottom_color."""
        for y in range(surface.get_height()):
            ratio = y / surface.get_height()
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

    running = True
    while running:
        # Gradient from black to dark grey
        draw_gradient_background(win, (0, 0, 0), (40, 40, 40))
        y = y_offset
        for surf, is_title in rendered:
            new_spacing = 200 if is_title else spacing
            rect = surf.get_rect(center=(WIDTH // 2, int(y)))
            win.blit(surf, rect)
            y += new_spacing
        pygame.display.update()
        y_offset -= scroll_speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        if y_offset + total_height < 0:
            pygame.time.wait(1000)
            break
        clock.tick(60)
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(os.path.join(assetsdir, 'sounds', 'bgm.mp3'))
    except pygame.error as e:
        print(f"Error loading music ({os.path.join(assetsdir, 'bgm.mp3')}): {e}")
        pygame.quit()
        sys.exit()
    pygame.mixer.music.play(-1)

pygame.init()
WIDTH, HEIGHT = 640, 480
assetsdir = resource_path('assets')
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wilco | Game")

clock = pygame.time.Clock()
pygame.mixer.init()
try:
    pygame.mixer.music.load(bgmpath := os.path.join(assetsdir, 'sounds', 'bgm.mp3'))
except pygame.error as e:
    print(f"Error loading music ({os.path.join(assetsdir, 'bgm.mp3')}): {e}")
    pygame.quit()
    sys.exit()
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

# Load cat texture
try:
    player_img = pygame.image.load(os.path.join(assetsdir, 'images', 'cat.png')).convert_alpha()
except (pygame.error, FileNotFoundError) as e:
    print(f"Error loading cat texture: {e}")
    pygame.quit()
    sys.exit()
pygame.display.set_icon(pygame.image.load(os.path.join(assetsdir, 'images', 'front-cat.png')).convert_alpha())
width, height = player_img.get_size()
player_img = pygame.transform.scale(player_img, (width * 3, height * 3))
# 3D player properties
player_pos = [0.0, 0.0, 0.0]
player_size = 5.0
vel_y = 0
is_cat = True  # Default character
jumping = False
gravity = 0.5
move_speed = 0.2

# Camera control state
camera_yaw = 0.0
camera_pitch = 0.0
third_person = False

def setmouse(visible: bool) -> None:
    """Set mouse visibility and grab state."""
    pygame.mouse.set_visible(visible)
    pygame.event.set_grab(not visible)

setmouse(False)  # Hide mouse cursor initially

# --- Joystick support ---
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joy in joysticks:
    joy.init()
if joysticks:
    print(f"Detected {len(joysticks)} joystick(s): {[joy.get_name() for joy in joysticks]}")

# --- World data ---
WORLD_FILE = "world.wlco"
WORLD_SIZE = 30  # -10..19
def save_world(blocks, WORLD_FILE):
    """Save the world blocks to a binary file."""
    if not blocks:
        print("No blocks to save, skipping world save.")
        return
    with open(WORLD_FILE, "wb") as f:
        f.write(struct.pack("<I", len(blocks)))
        for x, z in blocks:
            f.write(struct.pack("<ii", x, z))

def load_world(WORLD_FILE):
    if not os.path.exists(WORLD_FILE):
        # Generate flat world
        return set((x, z) for x in range(-10, 20) for z in range(-10, 20))
    with open(WORLD_FILE, "rb") as f:
        n, = struct.unpack("<I", f.read(4))
        blocks = set()
        for _ in range(n):
            x, z = struct.unpack("<ii", f.read(8))
            blocks.add((x, z))
        return blocks

blocks = load_world(WORLD_FILE)

def get_camera():
    global camera_yaw, camera_pitch, third_person
    pitch = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, camera_pitch))
    fx = math.cos(pitch) * math.cos(camera_yaw)
    fy = math.sin(pitch)
    fz = math.cos(pitch) * math.sin(camera_yaw)
    if third_person:
        cam_dist = 5
        cam_height = 2
        cam_x = player_pos[0] - fx * cam_dist
        cam_y = player_pos[1] + cam_height
        cam_z = player_pos[2] - fz * cam_dist
        look_x = player_pos[0]
        look_y = player_pos[1] + 1
        look_z = player_pos[2]
    else:
        cam_x = player_pos[0]
        cam_y = player_pos[1] + 1
        cam_z = player_pos[2]
        look_x = cam_x + fx
        look_y = cam_y + fy
        look_z = cam_z + fz
    return (cam_x, cam_y, cam_z), (look_x, look_y, look_z)

def project_point(
    px: float, py: float, pz: float,
    cam_pos: tuple[float, float, float],
    cam_look: tuple[float, float, float]
) -> tuple[tuple[int, int], float]:
    cx, cy, cz = cam_pos
    lx, ly, lz = cam_look
    fx, fy, fz = lx - cx, ly - cy, lz - cz
    flen = math.sqrt(fx*fx + fy*fy + fz*fz)
    fx, fy, fz = fx/flen, fy/flen, fz/flen
    up = (0, 1, 0)
    rx = fy*up[2] - fz*up[1]
    ry = fz*up[0] - fx*up[2]
    rz = fx*up[1] - fy*up[0]
    rlen = math.sqrt(rx*rx + ry*ry + rz*rz)
    rx, ry, rz = rx/rlen, ry/rlen, rz/rlen
    ux = ry*fz - rz*fy
    uy = rz*fx - rx*fz
    uz = rx*fy - ry*fx
    dx, dy, dz = px-cx, py-cy, pz-cz
    cam_x = dx*rx + dy*ry + dz*rz
    cam_y = dx*ux + dy*uy + dz*uz
    cam_z = dx*fx + dy*fy + dz*fz
    if cam_z <= 0.1:
        return None
    fov = 90
    win_width = win.get_width()
    win_height = win.get_height()
    scale = win_width / (2 * math.tan(math.radians(fov/2)))
    sx = int(win_width/2 + cam_x * scale / cam_z)
    sy = int(win_height/2 - cam_y * scale / cam_z)
    return (sx, sy), cam_z

def draw_player(center, size, cam_pos, cam_look):
    proj = project_point(center[0], center[1] + size/2, center[2], cam_pos, cam_look)
    if proj is None:
        return
    (sx, sy), cam_z = proj
    # Scale the cat image based on distance and player size
    scale = max(1, int(size * 120 / cam_z))
    img = pygame.transform.smoothscale(player_img, (scale, scale))
    win.blit(img, (sx - scale//2, sy - scale//2))

def draw_cube(center, size, cam_pos, cam_look, color=(255,0,0), width=2):
    x, y, z = center
    s = size/2
    corners = [
        (x-s, y-s, z-s), (x+s, y-s, z-s), (x+s, y+s, z-s), (x-s, y+s, z-s),
        (x-s, y-s, z+s), (x+s, y-s, z+s), (x+s, y+s, z+s), (x-s, y+s, z+s)
    ]
    proj = [project_point(*c, cam_pos, cam_look) for c in corners]
    edges = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    for a,b in edges:
        if proj[a] is not None and proj[b] is not None:
            pygame.draw.line(win, color, proj[a][0], proj[b][0], width) # type: ignore

def raycast_block(cam_pos, cam_dir, blocks, max_dist=8):
    """Returns (x, z) of first block hit, or None."""
    x, y, z = cam_pos
    dx, dy, dz = cam_dir
    for step in range(int(max_dist * 20)):
        t = step * 0.05
        bx = int(round(x + dx * t))
        bz = int(round(z + dz * t))
        if (bx, bz) in blocks and abs(y + dy * t) < 1.5:
            return (bx, bz)
    return None

def draw_crosshair():
    cx, cy = win.get_width() // 2, win.get_height() // 2
    size = 10
    color = (0, 0, 0)
    pygame.draw.line(win, color, (cx - size, cy), (cx + size, cy), 2)
    pygame.draw.line(win, color, (cx, cy - size), (cx, cy + size), 2)

run = True
highlighted_block = None
splash_screen()
while run:
    clock.tick(60)
    pygame.event.pump()  # Prevent controller disconnects
    pygame.draw.rect(win, (135, 206, 235), (0, 0, WIDTH, HEIGHT))
    pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
    # --- Controller input defaults ---
    joy_move_x, joy_move_y = 0, 0
    joy_cam_x, joy_cam_y = 0, 0
    joy_jump = False
    joy_toggle_view = False

    # --- Poll joystick axes/buttons ---
    if joysticks:
        joy = joysticks[0]  # Use first controller
        # Left stick: axes 0 (left/right), 1 (up/down)
        joy_move_x = joy.get_axis(0)
        joy_move_y = joy.get_axis(1)
        # Right stick: axes 2 (left/right), 3 (up/down) or 3/4 depending on OS
        if joy.get_numaxes() >= 4:
            joy_cam_x = joy.get_axis(2)
            joy_cam_y = joy.get_axis(3)
        # A button (jump): usually button 1 on Switch Pro Controller
        joy_jump = joy.get_button(1)
        # X button (toggle view): usually button 3
        joy_toggle_view = joy.get_button(3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.rel
            camera_yaw += mx * 0.005
            camera_pitch -= my * 0.005
            camera_pitch = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, camera_pitch))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            setmouse(True)
            if tkinter.messagebox.askyesno("Leave World", "Are you sure you want to leave?"):
                run = False
            else:
                setmouse(False)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            third_person = not third_person
        if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
            credits_screen()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            selectedchar: str = character_selection_screen()
            if selectedchar is not None:
                is_cat = selectedchar.startswith('cat')
                try:
                    player_img = pygame.image.load(os.path.join(assetsdir, 'images', selectedchar)).convert_alpha()
                except (pygame.error, FileNotFoundError) as e:
                    print(f"Error loading texture: {e}")
                    pygame.quit()
                    sys.exit()
        # Controller: toggle view on X button press
        if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
            third_person = not third_person
        # Block breaking: left mouse button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cam_pos, cam_look = get_camera()
            dx = cam_look[0] - cam_pos[0]
            dy = cam_look[1] - cam_pos[1]
            dz = cam_look[2] - cam_pos[2]
            norm = math.sqrt(dx*dx + dy*dy + dz*dz)
            dir_vec = (dx/norm, dy/norm, dz/norm)
            hit = raycast_block(cam_pos, dir_vec, blocks)
            if hit:
                blocks.remove(hit)
                save_world(blocks, WORLD_FILE)

    keys = pygame.key.get_pressed()
    move_dx, move_dz = 0, 0

    # Keyboard movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move_dx -= math.cos(camera_yaw + math.pi/2)
        move_dz -= math.sin(camera_yaw + math.pi/2)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move_dx += math.cos(camera_yaw + math.pi/2)
        move_dz += math.sin(camera_yaw + math.pi/2)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        move_dx += math.cos(camera_yaw)
        move_dz += math.sin(camera_yaw)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move_dx -= math.cos(camera_yaw)
        move_dz -= math.sin(camera_yaw)

    # Controller movement (left stick)
    if abs(joy_move_x) > 0.15 or abs(joy_move_y) > 0.15:
        move_dx += joy_move_x * math.cos(camera_yaw + math.pi/2) + joy_move_y * math.cos(camera_yaw)
        move_dz += joy_move_x * math.sin(camera_yaw + math.pi/2) + joy_move_y * math.sin(camera_yaw)

    # --- SOLID BLOCK COLLISION ---
    # Predict new position
    norm = math.hypot(move_dx, move_dz)
    new_x, new_z = player_pos[0], player_pos[2]
    if norm > 0:
        step_x = move_speed * move_dx / norm
        step_z = move_speed * move_dz / norm
        # Try X movement
        test_x = new_x + step_x
        bx = int(round(test_x))
        bz = int(round(player_pos[2]))
        if (bx, bz) not in blocks or abs(player_pos[1]) > 1.5:
            new_x = test_x
        # Try Z movement
        test_z = new_z + step_z
        bx = int(round(new_x))
        bz = int(round(test_z))
        if (bx, bz) not in blocks or abs(player_pos[1]) > 1.5:
            new_z = test_z
    player_pos[0], player_pos[2] = new_x, new_z

    # Keyboard jump
    jump_pressed = keys[pygame.K_SPACE]
    # Controller jump (A button)
    if joy_jump:
        jump_pressed = True
    if not jumping and jump_pressed:
        vel_y = 0.30
        jumping = True
    if jumping:
    
        player_pos[1] += vel_y
        vel_y -= gravity * 0.02
    
        if player_pos[1] <= 0:
            player_pos[1] = 0
            jumping = False
            vel_y = 0
    # Camera control with right stick (controller)
    if abs(joy_cam_x) > 0.15 or abs(joy_cam_y) > 0.15:
        camera_yaw += joy_cam_x * 0.05
        camera_pitch -= joy_cam_y * 0.05
        camera_pitch = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, camera_pitch))

    cam_pos, cam_look = get_camera()

    # --- Block Highlighting ---
    dx = cam_look[0] - cam_pos[0]
    dy = cam_look[1] - cam_pos[1]
    dz = cam_look[2] - cam_pos[2]
    norm_dir = math.sqrt(dx*dx + dy*dy + dz*dz)
    dir_vec = (dx/norm_dir, dy/norm_dir, dz/norm_dir)
    highlighted_block = raycast_block(cam_pos, dir_vec, blocks)

    win.fill((135, 206, 235))
    # Draw blocks
    for (gx, gz) in blocks:
        draw_cube((gx, 0.5, gz), 1, cam_pos, cam_look, color=((0,128,0)))
    # Draw highlighted block
    if highlighted_block:
        draw_cube((highlighted_block[0], 0.5, highlighted_block[1]), 1, cam_pos, cam_look, color=(255,255,0), width=4)
    if third_person:
        draw_player(player_pos, player_size, cam_pos, cam_look)
    # Draw crosshair
    draw_crosshair()
    if is_cat:
        gravity = 0.5
        move_speed = 0.5
    else:
        gravity = 0.3
        move_speed = 0.2
    pygame.display.update()
pygame.quit()
