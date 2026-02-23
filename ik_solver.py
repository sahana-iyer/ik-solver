import pygame
import numpy as np
import math

# Window settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 65)
DARK_GREEN = (0, 180, 40)
DIM_GREEN = (0, 60, 20)
WHITE = (255, 255, 255)
RED = (255, 60, 60)

# Arm settings
L1 = 150  # Length of link 1
L2 = 120  # Length of link 2
BASE = (WIDTH // 2, HEIGHT // 2)  # Base position at center

def inverse_kinematics(tx, ty, l1, l2):
    """
    Analytical 2DOF IK solution
    Given target (tx, ty), find joint angles theta1 and theta2
    """
    # Distance from base to target
    d = math.sqrt(tx**2 + ty**2)

    # Check if target is reachable
    if d > l1 + l2:
        d = l1 + l2  # Clamp to max reach
    if d < abs(l1 - l2):
        d = abs(l1 - l2)  # Clamp to min reach

    # Law of cosines to find theta2
    cos_theta2 = (d**2 - l1**2 - l2**2) / (2 * l1 * l2)
    cos_theta2 = max(-1, min(1, cos_theta2))  # Clamp for safety
    theta2 = math.acos(cos_theta2)

    # Find theta1
    k1 = l1 + l2 * math.cos(theta2)
    k2 = l2 * math.sin(theta2)
    theta1 = math.atan2(ty, tx) - math.atan2(k2, k1)

    return theta1, theta2

def forward_kinematics(theta1, theta2, l1, l2):
    """
    FK — given angles, find joint and end-effector positions
    """
    # Joint 1 position
    j1x = l1 * math.cos(theta1)
    j1y = l1 * math.sin(theta1)

    # End effector position
    ex = j1x + l2 * math.cos(theta1 + theta2)
    ey = j1y + l2 * math.sin(theta1 + theta2)

    return (j1x, j1y), (ex, ey)

def draw_arm(screen, base, joint, end, target):
    # Draw reach circle
    pygame.draw.circle(screen, DIM_GREEN, base, L1 + L2, 1)

    # Draw links
    pygame.draw.line(screen, GREEN, base, joint, 6)
    pygame.draw.line(screen, DARK_GREEN, joint, end, 5)

    # Draw joints
    pygame.draw.circle(screen, GREEN, base, 10)
    pygame.draw.circle(screen, GREEN, joint, 8)
    pygame.draw.circle(screen, WHITE, end, 6)

    # Draw target
    pygame.draw.circle(screen, RED, target, 8)
    pygame.draw.line(screen, RED, (target[0]-12, target[1]), (target[0]+12, target[1]), 2)
    pygame.draw.line(screen, RED, (target[0], target[1]-12), (target[0], target[1]+12), 2)

def draw_ui(screen, font, theta1, theta2, target, base):
    tx = target[0] - base[0]
    ty = -(target[1] - base[1])  # Flip Y for display
    d = math.sqrt(tx**2 + ty**2)

    lines = [
        "IOT-SHIELD  2DOF IK SOLVER",
        "─────────────────────────────",
        f"Target     x: {tx:.1f}  y: {ty:.1f}",
        f"Distance   {d:.1f} px",
        f"Theta 1    {math.degrees(theta1):.1f} deg",
        f"Theta 2    {math.degrees(theta2):.1f} deg",
        "─────────────────────────────",
        "Click anywhere to move arm",
    ]

    for i, line in enumerate(lines):
        color = GREEN if i != 0 else WHITE
        text = font.render(line, True, color)
        screen.blit(text, (20, 20 + i * 22))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("IK Solver — 2DOF | Sahana G Iyer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 15)

    target = (BASE[0] + 100, BASE[1] - 100)
    theta1, theta2 = 0, 0

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]:
                target = pygame.mouse.get_pos()

        # IK calculation
        tx = target[0] - BASE[0]
        ty = -(target[1] - BASE[1])  # Flip Y axis
        theta1, theta2 = inverse_kinematics(tx, ty, L1, L2)

        # FK to get joint positions for drawing
        joint, end = forward_kinematics(theta1, theta2, L1, L2)

        # Convert to screen coordinates
        joint_screen = (int(BASE[0] + joint[0]), int(BASE[1] - joint[1]))
        end_screen = (int(BASE[0] + end[0]), int(BASE[1] - end[1]))

        # Draw everything
        draw_arm(screen, BASE, joint_screen, end_screen, target)
        draw_ui(screen, font, theta1, theta2, target, BASE)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
