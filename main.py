import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pygame


# -----------------------------
# User settings
# -----------------------------
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 1500
FULLSCREEN = True

BACKGROUND_VIDEO = "background.mp4"   # put your looping background video next to this script
CAMERA_INDEX = 0                      # change to 1, 2, etc. if needed
MICROSCOPE_RECT = (220, 0, 1500, 1080)  # x, y, width, height on the portrait display
TARGET_FPS = 30

SHOW_DEBUG_TEXT = False
ESC_TO_QUIT = True


# -----------------------------
# Helpers
# -----------------------------
def script_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def load_video_capture(video_path: Path):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open background video: {video_path}")
    return cap


def load_camera_capture(index: int):
    # Try DirectShow first on Windows for better USB camera behavior.
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {index}")
    return cap


def cv_frame_to_surface(frame_bgr, size=None):
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    if size is not None:
        frame_rgb = cv2.resize(frame_rgb, size, interpolation=cv2.INTER_LINEAR)
    frame_rgb = np.rot90(frame_rgb)  # pygame expects width/height orientation for surfarray
    return pygame.surfarray.make_surface(frame_rgb)


def fit_cover(src_w, src_h, dst_w, dst_h):
    src_ratio = src_w / src_h
    dst_ratio = dst_w / dst_h
    if src_ratio > dst_ratio:
        scale = dst_h / src_h
    else:
        scale = dst_w / src_w
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    x = (dst_w - new_w) // 2
    y = (dst_h - new_h) // 2
    return x, y, new_w, new_h


def read_looping_video_frame(video_cap):
    ok, frame = video_cap.read()
    if ok:
        return frame

    video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ok, frame = video_cap.read()
    if ok:
        return frame

    raise RuntimeError("Unable to read background video frame, even after rewind")


def draw_camera_border(screen, rect, thickness=6, corner=20):
    x, y, w, h = rect
    pygame.draw.rect(screen, (245, 245, 245), (x, y, w, h), thickness, border_radius=corner)


def draw_debug_text(screen, font, clock, cam_ok, video_ok):
    lines = [
        f"FPS: {clock.get_fps():.1f}",
        f"camera: {'OK' if cam_ok else 'ERROR'}",
        f"background video: {'OK' if video_ok else 'ERROR'}",
        "ESC quits" if ESC_TO_QUIT else "",
    ]
    y = 20
    for line in lines:
        if not line:
            continue
        surf = font.render(line, True, (255, 255, 255))
        bg = pygame.Surface((surf.get_width() + 16, surf.get_height() + 10), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 140))
        screen.blit(bg, (20, y - 4))
        screen.blit(surf, (28, y))
        y += surf.get_height() + 12


# -----------------------------
# Main
# -----------------------------
def main():
    base = script_dir()
    bg_path = base / BACKGROUND_VIDEO

    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)
    flags = pygame.FULLSCREEN if FULLSCREEN else 0
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
    pygame.display.set_caption("Scope on a Rope Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28)

    if not bg_path.exists():
        raise FileNotFoundError(
            f"Background video not found:\n{bg_path}\n\n"
            f"Put your MP4 next to this script and name it {BACKGROUND_VIDEO}."
        )

    video_cap = load_video_capture(bg_path)
    camera_cap = load_camera_capture(CAMERA_INDEX)

    last_camera_frame = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if ESC_TO_QUIT and event.key == pygame.K_ESCAPE:
                    running = False

        # --- Background video ---
        video_ok = True
        try:
            bg_frame = read_looping_video_frame(video_cap)
            bh, bw = bg_frame.shape[:2]
            x, y, w, h = fit_cover(bw, bh, WINDOW_WIDTH, WINDOW_HEIGHT)
            bg_surface = cv_frame_to_surface(bg_frame, size=(w, h))
            screen.fill((0, 0, 0))
            screen.blit(bg_surface, (x, y))
        except Exception:
            video_ok = False
            screen.fill((25, 25, 25))

        # --- Microscope camera overlay ---
        cam_ok = False
        ok, cam_frame = camera_cap.read()
        if ok and cam_frame is not None:
            last_camera_frame = cam_frame
            cam_ok = True
        elif last_camera_frame is not None:
            cam_frame = last_camera_frame

        if cam_frame is not None:
            x, y, w, h = MICROSCOPE_RECT
            cam_surface = cv_frame_to_surface(cam_frame, size=(w, h))
            screen.blit(cam_surface, (x, y))
            draw_camera_border(screen, MICROSCOPE_RECT)

        if SHOW_DEBUG_TEXT:
            draw_debug_text(screen, font, clock, cam_ok, video_ok)

        pygame.display.flip()
        clock.tick(TARGET_FPS)

    camera_cap.release()
    video_cap.release()
    pygame.quit()


if __name__ == "__main__":
    main()
