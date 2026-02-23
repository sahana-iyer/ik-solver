import pygame
import numpy as np
import math

# Window settings
WIDTH, HEIGHT = 900, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 65)
DARK_GREEN = (0, 180, 40)
DIM_GREEN = (0, 60, 20)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
YELLOW = (255, 220, 0)

# Arm settings
L1 = 150
L2 = 120
BASE = (450, 350)

def inverse_kinematics(tx, ty, l1, l2):
    d = math.sqrt(tx**2 + ty**2)
    if d > l1 + l2:
        d = l1 + l2
    if d < abs(l1 - l2):
        d = abs(l1 - l2)
    cos_theta2 = (d**2 - l1**2 - l2**2) / (2 * l1 * l2)
    cos_theta2 = max(-1, min(1, cos_theta2))
    theta2 = math.acos(cos_theta2)
    k1 = l1 + l2 * math.cos(theta2)
    k2 = l2 * math.sin(theta2)
    theta1 = math.atan2(ty, tx) - math.atan2(k2, k1)
    return theta1, theta2

def forward_kinematics(theta1, theta2, l1, l2):
    j1x = l1 * math.cos(theta1)
    j1y = l1 * math.sin(theta1)
    ex = j1x + l2 * math.cos(theta1 + theta2)
    ey = j1y + l2 * math.sin(theta1 + theta2)
    return (j1x, j1y), (ex, ey)

def draw_arm(screen, base, joint, end, target):
    pygame.draw.circle(screen, DIM_GREEN, base, L1 + L2, 1)
    pygame.draw.line(screen, GREEN, base, joint, 6)
    pygame.draw.line(screen, DARK_GREEN, joint, end, 5)
    pygame.draw.circle(screen, GREEN, base, 10)
    pygame.draw.circle(screen, GREEN, joint, 8)
    pygame.draw.circle(screen, WHITE, end, 6)
    pygame.draw.circle(screen, RED, target, 8)
    pygame.draw.line(screen, RED, (target[0]-12, target[1]), (target[0]+12, target[1]), 2)
    pygame.draw.line(screen, RED, (target[0], target[1]-12), (target[0], target[1]+12), 2)

def draw_ui(screen, font, font_small, theta1, theta2, target, base, mode, input_x, input_y, active_field):
    tx = target[0] - base[0]
    ty = -(target[1] - base[1])
    d = math.sqrt(tx**2 + ty**2)

    # Info panel
    lines = [
        ("2DOF IK SOLVER", WHITE),
        ("─────────────────────────", GREEN),
        (f"Mode       {'MANUAL INPUT' if mode == 'manual' else 'MOUSE'}", YELLOW),
        (f"Target     x: {tx:.1f}  y: {ty:.1f}", GREEN),
        (f"Distance   {d:.1f} px", GREEN),
        (f"Theta 1    {math.degrees(theta1):.2f} deg", GREEN),
        (f"Theta 2    {math.degrees(theta2):.2f} deg", GREEN),
        ("─────────────────────────", GREEN),
        ("M — toggle mouse mode", GREEN),
        ("I — toggle input mode", GREEN),
    ]

    for i, (line, color) in enumerate(lines):
        text = font.render(line, True, color)
        screen.blit(text, (20, 20 + i * 22))

    # Manual input boxes
    if mode == "manual":
        pygame.draw.rect(screen, DIM_GREEN, (20, 260, 200, 30), border_radius=4)
        pygame.draw.rect(screen, GREEN if active_field == "x" else DARK_GREEN, (20, 260, 200, 30), 2, border_radius=4)
        x_label = font.render(f"X: {input_x}", True, GREEN)
        screen.blit(x_label, (30, 267))

        pygame.draw.rect(screen, DIM_GREEN, (20, 300, 200, 30), border_radius=4)
        pygame.draw.rect(screen, GREEN if active_field == "y" else DARK_GREEN, (20, 300, 200, 30), 2, border_radius=4)
        y_label = font.render(f"Y: {input_y}", True, GREEN)
        screen.blit(y_label, (30, 307))

        hint = font_small.render("Enter to apply  |  Click box to select", True, DARK_GREEN)
        screen.blit(hint, (20, 340))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("IK Solver — 2DOF | Sahana G Iyer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 15)
    font_small = pygame.font.SysFont("monospace", 12)

    target = (BASE[0] + 100, BASE[1] - 100)
    theta1, theta2 = 0, 0
    mode = "mouse"
    input_x = ""
    input_y = ""
    active_field = "x"

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mode = "mouse"
                if event.key == pygame.K_i:
                    mode = "manual"
                    active_field = "x"

                if mode == "manual":
                    if event.key == pygame.K_TAB:
                        active_field = "y" if active_field == "x" else "x"
                    elif event.key == pygame.K_RETURN:
                        try:
                            tx = float(input_x)
                            ty = float(input_y)
                            target = (int(BASE[0] + tx), int(BASE[1] - ty))
                        except:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        if active_field == "x":
                            input_x = input_x[:-1]
                        else:
                            input_y = input_y[:-1]
                    else:
                        char = event.unicode
                        if char in "0123456789.-":
                            if active_field == "x":
                                input_x += char
                            else:
                                input_y += char

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "manual":
                    mx, my = pygame.mouse.get_pos()
                    if 20 <= mx <= 220 and 260 <= my <= 290:
                        active_field = "x"
                    elif 20 <= mx <= 220 and 300 <= my <= 330:
                        active_field = "y"

            if mode == "mouse":
                if pygame.mouse.get_pressed()[0]:
                    target = pygame.mouse.get_pos()

        # IK calculation
        tx = target[0] - BASE[0]
        ty = -(target[1] - BASE[1])
        theta1, theta2 = inverse_kinematics(tx, ty, L1, L2)
        joint, end = forward_kinematics(theta1, theta2, L1, L2)

        joint_screen = (int(BASE[0] + joint[0]), int(BASE[1] - joint[1]))
        end_screen = (int(BASE[0] + end[0]), int(BASE[1] - end[1]))

        draw_arm(screen, BASE, joint_screen, end_screen, target)
        draw_ui(screen, font, font_small, theta1, theta2, target, BASE, mode, input_x, input_y, active_field)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
