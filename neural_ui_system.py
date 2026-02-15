import pygame
import math

# --- UI CONSTANTS ---
BG_COLOR = (18, 18, 18)
CELL_SLATE = (30, 30, 30)
TEXT_GRAY = (180, 180, 180)
ACCENT_CYAN = (0, 255, 200)
DANGER_RED = (255, 60, 60)
NEON_GREEN = (0, 255, 100)
NEON_ORANGE = (255, 150, 0)
NEON_PURPLE = (200, 100, 255)


class NeuralUISystem:
    def __init__(self, font_mono):
        self.font = font_mono
        self.logic_logs = []
        self.risk_level = 0.5  # 0 = Conservative, 1 = Aggressive
        self.animation_time = 0
        
    def add_log(self, message, log_type="INFO"):
        """Adds a message to the logic feed with enhanced formatting."""
        # Format with timestamp and enhanced type indicators
        timestamp = pygame.time.get_ticks() // 1000
        formatted_message = f"[{log_type}] {message}"
        self.logic_logs.append({
            'text': formatted_message,
            'type': log_type,
            'timestamp': timestamp,
            'alpha': 255
        })
        
        # Keep only recent logs
        if len(self.logic_logs) > 12:
            self.logic_logs.pop(0)
    
    def set_risk_level(self, level):
        """Set the risk level for the AI strategy."""
        self.risk_level = max(0, min(1, level))
    
    def draw_probability_cell(self, surface, rect, prob, highlight=False):
        """Renders a cell with enhanced neon heat-glow based on mine probability."""
        # Enhanced color calculation with more vibrant cyberpunk colors
        if prob < 0.1:
            # Safe - Green glow
            r = int(50 * prob)
            g = int(255 * (1 - prob * 2))
            b = int(100 * (1 - prob))
            glow_color = (0, 255, 100)
        elif prob < 0.3:
            # Low risk - Cyan to Green
            t = (prob - 0.1) / 0.2
            r = int(100 * t)
            g = 255
            b = int(200 * (1 - t))
            glow_color = (0, 255, 200)
        elif prob < 0.6:
            # Medium risk - Orange to Yellow
            t = (prob - 0.3) / 0.3
            r = 255
            g = int(255 * (1 - t * 0.5))
            b = int(50 * (1 - t))
            glow_color = (255, 200, 0)
        elif prob < 0.8:
            # High risk - Red to Orange
            t = (prob - 0.6) / 0.2
            r = 255
            g = int(150 * (1 - t))
            b = int(50 * (1 - t))
            glow_color = (255, 100, 0)
        else:
            # Very high risk - Purple to Red
            t = (prob - 0.8) / 0.2
            r = int(255 * (0.7 + 0.3 * t))
            g = int(100 * (1 - t))
            b = int(255 * t)
            glow_color = (255, 60, 60)
        
        # 1. Draw the base cell with rounded corners
        pygame.draw.rect(surface, CELL_SLATE, rect, border_radius=6)
        
        # 2. Draw enhanced neon glow effect
        if prob > 0.01:
            # Multi-layer glow for more depth
            for i in range(4, 0, -1):
                alpha = int(80 / i)
                glow_intensity = 1.0 + 0.3 * math.sin(self.animation_time * 0.05 + i)
                expanded_rect = rect.inflate(i * 3, i * 3)
                
                # Create glow surface
                glow_surface = pygame.Surface((expanded_rect.width, expanded_rect.height), pygame.SRCALPHA)
                
                # Draw glowing border
                border_color = (*glow_color, min(alpha, int(100 * glow_intensity)))
                pygame.draw.rect(glow_surface, border_color, glow_surface.get_rect(), 
                               border_radius=6 + i, width=2)
                
                # Apply glow with blending
                surface.blit(glow_surface, expanded_rect.topleft, special_flags=pygame.BLEND_ADD)
        
        # 3. Draw probability text with enhanced styling
        if 0.01 < prob < 0.99:
            # Format percentage
            prob_text = f"{int(prob * 100)}%"
            
            # Text with shadow effect
            shadow_surf = self.font.render(prob_text, True, (0, 0, 0))
            text_surf = self.font.render(prob_text, True, TEXT_GRAY)
            
            text_rect = text_surf.get_rect(center=rect.center)
            shadow_rect = shadow_surf.get_rect(center=(rect.centerx + 1, rect.centery + 1))
            
            surface.blit(shadow_surf, shadow_rect)
            surface.blit(text_surf, text_rect)
        
        # 4. Draw highlight effect if specified
        if highlight:
            highlight_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, (*ACCENT_CYAN, 30), highlight_surface.get_rect(), border_radius=6)
            surface.blit(highlight_surface, rect.topleft)
    
    def draw_sidebar(self, surface, x_offset):
        """Renders the enhanced terminal-style Logic Feed."""
        # Animated title with glow effect
        title_glow = int(128 + 127 * math.sin(self.animation_time * 0.03))
        title_color = (0, title_glow, 200)
        
        # Draw title with shadow
        title_shadow = self.font.render("LOGIC FEED", True, (0, 0, 0))
        title_surf = self.font.render("LOGIC FEED", True, title_color)
        surface.blit(title_shadow, (x_offset + 2, 22))
        surface.blit(title_surf, (x_offset, 20))
        
        # Draw separator line
        pygame.draw.line(surface, ACCENT_CYAN, (x_offset, 50), (x_offset + 180, 50), 2)
        
        # Draw logs with enhanced formatting
        y_offset = 70
        for i, log_entry in enumerate(self.logic_logs):
            log_text = log_entry['text']
            log_type = log_entry['type']
            
            # Color coding based on log type
            if log_type == "SOLVE":
                color = NEON_GREEN
            elif log_type == "LOGIC":
                color = ACCENT_CYAN
            elif log_type == "PROB":
                color = NEON_ORANGE
            elif log_type == "FOGIC":
                color = NEON_PURPLE
            elif log_type == "ERROR":
                color = DANGER_RED
            else:
                color = TEXT_GRAY
            
            # Add fade effect for older logs
            alpha = max(100, 255 - (len(self.logic_logs) - i - 1) * 20)
            color = (*color, alpha)
            
            # Render log with shadow
            shadow_surf = self.font.render(log_text, True, (0, 0, 0))
            log_surf = self.font.render(log_text, True, color[:3])
            
            surface.blit(shadow_surf, (x_offset + 2, y_offset + 2))
            surface.blit(log_surf, (x_offset, y_offset))
            
            y_offset += 22
        
        # Draw risk slider section
        self.draw_risk_slider(surface, x_offset, y_offset + 20)
    
    def draw_risk_slider(self, surface, x_offset, y_offset):
        """Draw the risk slider with enhanced styling."""
        # Slider title
        slider_title = self.font.render("RISK STRATEGY", True, TEXT_GRAY)
        surface.blit(slider_title, (x_offset, y_offset))
        
        # Slider track
        track_rect = pygame.Rect(x_offset, y_offset + 25, 180, 8)
        pygame.draw.rect(surface, CELL_SLATE, track_rect, border_radius=4)
        
        # Gradient track
        for i in range(180):
            t = i / 180
            if t < 0.5:
                color = (int(255 * t * 2), 255, 0)  # Green to Yellow
            else:
                color = (255, int(255 * (2 - t * 2)), 0)  # Yellow to Red
            
            pygame.draw.line(surface, color, 
                           (x_offset + i, y_offset + 25), 
                           (x_offset + i, y_offset + 33))
        
        # Slider handle
        handle_x = x_offset + int(self.risk_level * 180)
        handle_rect = pygame.Rect(handle_x - 6, y_offset + 20, 12, 16)
        
        # Glow effect for handle
        for i in range(3, 0, -1):
            glow_surface = pygame.Surface((handle_rect.width + i*4, handle_rect.height + i*4), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*ACCENT_CYAN, 50 // i), glow_surface.get_rect(), border_radius=6)
            surface.blit(glow_surface, (handle_rect.x - i*2, handle_rect.y - i*2))
        
        pygame.draw.rect(surface, ACCENT_CYAN, handle_rect, border_radius=6)
        
        # Labels
        conservative_text = self.font.render("CONSERVATIVE", True, NEON_GREEN)
        aggressive_text = self.font.render("AGGRESSIVE", True, DANGER_RED)
        
        surface.blit(conservative_text, (x_offset, y_offset + 50))
        surface.blit(aggressive_text, (x_offset + 100, y_offset + 50))
    
    def update(self, dt):
        """Update animation timers."""
        self.animation_time += dt
        
        # Fade out old logs
        for log_entry in self.logic_logs:
            age = pygame.time.get_ticks() // 1000 - log_entry['timestamp']
            if age > 10:
                log_entry['alpha'] = max(50, log_entry['alpha'] - 2)
    
    def draw_button(self, surface, rect, text, hover=False, active=False):
        """Draw a cyberpunk-styled button."""
        # Button background
        if active:
            bg_color = ACCENT_CYAN
            text_color = BG_COLOR
        elif hover:
            bg_color = (50, 50, 50)
            text_color = ACCENT_CYAN
        else:
            bg_color = CELL_SLATE
            text_color = TEXT_GRAY
        
        # Draw button with glow effect if active or hover
        if active or hover:
            for i in range(3, 0, -1):
                glow_surface = pygame.Surface((rect.width + i*4, rect.height + i*4), pygame.SRCALPHA)
                glow_color = (*ACCENT_CYAN, (30 if hover else 60) // i)
                pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=8)
                surface.blit(glow_surface, (rect.x - i*2, rect.y - i*2))
        
        # Draw button background
        pygame.draw.rect(surface, bg_color, rect, border_radius=8)
        
        # Draw button border
        border_color = ACCENT_CYAN if active or hover else CELL_SLATE
        pygame.draw.rect(surface, border_color, rect, border_radius=8, width=2)
        
        # Draw text
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)


# --- EXAMPLE USAGE IN MAIN LOOP ---
# Initialize Pygame
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# font_mono = pygame.font.SysFont("monospace", 14)
# clock = pygame.time.Clock()

# Create UI system
# ui = NeuralUISystem(font_mono)

# Add some example logs
# ui.add_log("Analyzing board state...", "LOGIC")
# ui.add_log("Found certain mine at (3, 4)", "SOLVE")
# ui.add_log("Probability: 0.25 for cell (2, 5)", "PROB")

# Main game loop
# running = True
# while running:
#     dt = clock.tick(60) / 1000.0
#     
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     
#     # Update
#     ui.update(dt)
#     
#     # Draw
#     screen.fill(BG_COLOR)
#     
#     # Draw example probability cell
#     cell_rect = pygame.Rect(50, 50, 40, 40)
#     ui.draw_probability_cell(screen, cell_rect, 0.75)
#     
#     # Draw sidebar
#     ui.draw_sidebar(screen, 620)
#     
#     # Draw example buttons
#     ai_solve_rect = pygame.Rect(50, 500, 120, 40)
#     hints_rect = pygame.Rect(190, 500, 120, 40)
#     new_game_rect = pygame.Rect(330, 500, 120, 40)
#     
#     mouse_pos = pygame.mouse.get_pos()
#     
#     ui.draw_button(screen, ai_solve_rect, "AI SOLVE", 
#                    ai_solve_rect.collidepoint(mouse_pos))
#     ui.draw_button(screen, hints_rect, "TOGGLE HINTS", 
#                    hints_rect.collidepoint(mouse_pos))
#     ui.draw_button(screen, new_game_rect, "NEW GAME", 
#                    new_game_rect.collidepoint(mouse_pos))
#     
#     pygame.display.flip()
# 
# pygame.quit()
