#!/usr/bin/env python3
"""
Test script for the Enhanced Neural UI System
Demonstrates all the cyberpunk UI features
"""

import pygame
import math
import random
from neural_ui_system import NeuralUISystem


def main():
    """Main test function for the Neural UI System."""
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("🤖 Neural UI System Test - Cyberpunk Minesweeper")
    clock = pygame.time.Clock()
    
    # Create UI system
    font_mono = pygame.font.SysFont("monospace", 14)
    ui = NeuralUISystem(font_mono)
    
    # Test data
    test_cells = [
        (pygame.Rect(50, 50, 40, 40), 0.0),    # Safe
        (pygame.Rect(100, 50, 40, 40), 0.1),   # Very safe
        (pygame.Rect(150, 50, 40, 40), 0.25),  # Low risk
        (pygame.Rect(200, 50, 40, 40), 0.5),   # Medium risk
        (pygame.Rect(250, 50, 40, 40), 0.75),  # High risk
        (pygame.Rect(300, 50, 40, 40), 0.9),   # Very high risk
        (pygame.Rect(350, 50, 40, 40), 1.0),   # Certain mine
    ]
    
    # Buttons
    ai_solve_rect = pygame.Rect(50, 500, 120, 40)
    hints_rect = pygame.Rect(190, 500, 120, 40)
    new_game_rect = pygame.Rect(330, 500, 120, 40)
    
    # Add some example logs
    ui.add_log("Neural network initialized...", "LOGIC")
    ui.add_log("Board analysis complete", "SOLVE")
    ui.add_log("Probability matrix calculated", "PROB")
    ui.add_log("Constraint satisfaction applied", "FOGIC")
    ui.add_log("Optimal move found", "SOLVE")
    
    # Animation and interaction variables
    running = True
    mouse_pos = (0, 0)
    risk_level = 0.5
    log_counter = 0
    
    print("🤖 Neural UI System Test Started")
    print("Controls:")
    print("- Move mouse to see hover effects")
    print("- Click buttons to see active states")
    print("- Press SPACE to add random log")
    print("- Press UP/DOWN to adjust risk level")
    print("- Press ESC to exit")
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Add random log
                    log_types = ["LOGIC", "SOLVE", "PROB", "FOGIC"]
                    messages = [
                        "Analyzing cell patterns...",
                        "Found logical deduction",
                        "Probability updated",
                        "Constraint applied",
                        "Optimal path calculated",
                        "Neural network processing..."
                    ]
                    ui.add_log(random.choice(messages), random.choice(log_types))
                elif event.key == pygame.K_UP:
                    risk_level = min(1.0, risk_level + 0.1)
                    ui.set_risk_level(risk_level)
                elif event.key == pygame.K_DOWN:
                    risk_level = max(0.0, risk_level - 0.1)
                    ui.set_risk_level(risk_level)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check button clicks
                if ai_solve_rect.collidepoint(mouse_pos):
                    ui.add_log("AI Solve activated!", "SOLVE")
                elif hints_rect.collidepoint(mouse_pos):
                    ui.add_log("Hints toggled", "LOGIC")
                elif new_game_rect.collidepoint(mouse_pos):
                    ui.add_log("New game started", "LOGIC")
                    # Clear and re-add some logs
                    ui.logic_logs.clear()
                    ui.add_log("Board reset", "LOGIC")
                    ui.add_log("Ready for analysis", "SOLVE")
        
        # Update mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Update UI
        ui.update(dt)
        
        # Add periodic logs for demonstration
        log_counter += dt
        if log_counter > 2.0:  # Every 2 seconds
            log_counter = 0
            demo_logs = [
                ("Scanning for patterns...", "LOGIC"),
                ("Neural processing...", "PROB"),
                ("Optimization complete", "SOLVE"),
                ("Matrix updated", "FOGIC")
            ]
            ui.add_log(*random.choice(demo_logs))
        
        # Clear screen
        screen.fill((18, 18, 18))
        
        # Draw grid background pattern
        for x in range(0, 800, 40):
            pygame.draw.line(screen, (25, 25, 25), (x, 0), (x, 600))
        for y in range(0, 600, 40):
            pygame.draw.line(screen, (25, 25, 25), (0, y), (800, y))
        
        # Draw title
        title_font = pygame.font.SysFont("Arial", 24, bold=True)
        title_text = title_font.render("NEURAL MINESWEEPER AI", True, (0, 255, 200))
        title_shadow = title_font.render("NEURAL MINESWEEPER AI", True, (0, 0, 0))
        screen.blit(title_shadow, (152, 12))
        screen.blit(title_text, (150, 10))
        
        # Draw subtitle
        subtitle_font = pygame.font.SysFont("Arial", 14)
        subtitle_text = subtitle_font.render("Cyberpunk UI Demonstration", True, (180, 180, 180))
        screen.blit(subtitle_text, (250, 40))
        
        # Draw probability cells with different probabilities
        for i, (rect, prob) in enumerate(test_cells):
            highlight = rect.collidepoint(mouse_pos)
            ui.draw_probability_cell(screen, rect, prob, highlight)
            
            # Draw probability labels
            label_font = pygame.font.SysFont("Arial", 10)
            label_text = label_font.render(f"{prob:.0%}", True, (150, 150, 150))
            screen.blit(label_text, (rect.x + 5, rect.y - 15))
        
        # Draw sidebar
        ui.draw_sidebar(screen, 620)
        
        # Draw buttons
        ui.draw_button(screen, ai_solve_rect, "AI SOLVE", 
                      ai_solve_rect.collidepoint(mouse_pos))
        ui.draw_button(screen, hints_rect, "TOGGLE HINTS", 
                      hints_rect.collidepoint(mouse_pos))
        ui.draw_button(screen, new_game_rect, "NEW GAME", 
                      new_game_rect.collidepoint(mouse_pos))
        
        # Draw instructions
        inst_font = pygame.font.SysFont("Arial", 12)
        instructions = [
            "SPACE: Add random log",
            "↑/↓: Adjust risk level",
            "Click: Interact with buttons",
            "ESC: Exit"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = inst_font.render(instruction, True, (120, 120, 120))
            screen.blit(inst_text, (50, 120 + i * 20))
        
        # Draw current risk level
        risk_text = inst_font.render(f"Risk Level: {risk_level:.1f}", True, (0, 255, 200))
        screen.blit(risk_text, (50, 220))
        
        # Update display
        pygame.display.flip()
    
    # Cleanup
    pygame.quit()
    print("🤖 Neural UI System Test Completed")


if __name__ == "__main__":
    main()
