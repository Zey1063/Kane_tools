# Copyright (c) KANE

# All rights reserved

# ----------------------------------------------------------------------------------------------------------------------------------------------------------|

#     - Any modification of the code is strictly prohibited.

#     - Reselling, redistributing, or claiming ownership of this tool is not allowed.

import os
import sys
import shutil
import time
import math
import subprocess
import io
import webbrowser

try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Program'))
    from Config.Config import *
    from Config.Util import *
except Exception as e:
    print(f"Error importing config: {e}")
    # Set fallback values if import fails
    try:
        os_name = os.name
        if os_name == 'nt':
            os_name = "Windows"
        else:
            os_name = "Linux"
    except:
        os_name = "Windows"
    tool_path = os.path.dirname(os.path.abspath(__file__))
    def Clear():
        try:
            if os_name == "Windows":
                os.system("cls")
            else:
                os.system("clear")
        except:
            pass

# Try to import rich for animated menu
try:
    from rich.console import Console, Group
    from rich.live import Live
    from rich.text import Text
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# --- FIXES ---
# Enable ANSI colors in Windows terminal
os.system('') 

# Force UTF-8 encoding to handle the block characters (█, ▓) without crashing
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
# ------------

ascii_art = [
    " ██ ▄█▀▄▄▄       ███▄    █ ▓█████ ",
    " ██▄█▒▒████▄     ██ ▀█   █ ▓█   ▀ ",
    "▓███▄░▒██  ▀█▄  ▓██  ▀█ ██▒▒███   ",
    "▓██ █▄░██▄▄▄▄██ ▓██▒  ▐▌██▒▒▓█  ▄ ",
    "▒██▒ █▄▓█   ▓██▒▒██░   ▓██░░▒████▒",
    "▒ ▒▒ ▓▒▒▒   ▓▒█░░ ▒░   ▒ ▒ ░░ ▒░ ░",
    "░ ░▒ ▒░ ▒   ▒▒ ░░ ░░   ░ ▒░ ░ ░  ░",
    "░ ░░ ░  ░   ▒      ░   ░ ░    ░   ",
    "░  ░        ░  ░         ░    ░  ░",
    "                                  "
]

# Color Palette: Bright Red (Top) to Dark Crimson (Bottom)
start_color = (255, 30, 30)
end_color = (60, 0, 0)

# We use the length of the art minus the last line (if it's just blank space)
# to calculate the gradient properly.
gradient_length = len(ascii_art) - 1

def interpolate(start, end, step, total):
    """Calculates the color for a specific line number."""
    r = int(start[0] + (end[0] - start[0]) * step / total)
    g = int(start[1] + (end[1] - start[1]) * step / total)
    b = int(start[2] + (end[2] - start[2]) * step / total)
    return r, g, b

def colored_print(text, r, g, b):
    """Prints text with TrueColor ANSI escape codes."""
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")

def get_logo_rich():
    """Build a Rich Text version of the ASCII logo with gradient coloring."""
    if not RICH_AVAILABLE:
        return None
    # Center-justify inside the logo block so the lines under the art
    # sit centered directly beneath it.
    logo = Text(justify="center")
    for i, line in enumerate(ascii_art):
        if i < gradient_length:
            r, g, b = interpolate(start_color, end_color, i, gradient_length - 1)
        else:
            r, g, b = end_color
        logo.append(line, style=f"rgb({r},{g},{b})")
        logo.append("\n")
    # Extra lines under logo
    logo.append("\n")
    logo.append("t.me/kane_tools\n")
    return logo

def print_logo():
    """Print the art with gradient coloring, centered."""
    # Get terminal width, default to 80 if unavailable
    try:
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80
    try:
        terminal_height = shutil.get_terminal_size().lines
    except Exception:
        terminal_height = 24
    
    # Find the longest line to determine the art width
    max_line_length = max(len(line) for line in ascii_art)
    
    # Rough vertical centering for non-rich mode
    logo_height = len(ascii_art) + 2 + 2  # art + extra blank lines + 2 extra lines
    top_pad = max(0, (terminal_height - logo_height) // 2)
    if top_pad:
        print("\n" * top_pad, end="")
    print("\n")
    for i, line in enumerate(ascii_art):
        # Calculate padding to center the line
        padding = (terminal_width - len(line)) // 2
        centered_line = " " * padding + line
        
        # Only calculate the color for the main art lines
        if i < gradient_length:
            r, g, b = interpolate(start_color, end_color, i, gradient_length - 1)
        else:
            # Use the final color for the last line if it exists
            r, g, b = end_color

        colored_print(centered_line, r, g, b)
    print("\n")
    # Extra lines under logo (centered)
    link = "t.me/kane_tools"
    padding = max(0, (terminal_width - len(link)) // 2)
    print((" " * padding) + link)
    print("\n")

# Options dictionary
OPTIONS = {
    '01': 'Website-Strength-Scanner',
    '02': 'Website-Status',
    '10': 'Discord-RAt',
    '11': 'Ransomware',
    '12': 'Grabber',
    '20': 'Cookie-Login',
    '21': 'Id-Details',
    '30': 'Nitro-Gen',
    '31': 'Token-Info',
    '32': 'Token-Login',
    '33': 'Token-Server-Join',
    '34': 'Token-Block-Friends',
    '35': 'Token-Change-Language',
    '36': 'Delete-Webhook',
    '37': 'Webhook-Spammer',
}

# Menu pages configuration - Each category on its own page
MENU_PAGES = {
    '1': {
        'title': ' Network ',
        'categories': [
            {
                'title': ' Network ',
                'options': ['01', '02'],
                'color': '#FF4444'
            }
        ]
    },
    '2': {
        'title': ' Paid ',
        'categories': [
            {
                'title': ' Paid ',
                'options': ['10', '11', '12'],
                'color': '#4444FF'
            }
        ]
    },
    '3': {
        'title': ' Roblox ',
        'categories': [
            {
                'title': ' Roblox ',
                'options': ['20', '21'],
                'color': '#FF8844'
            }
        ]
    },
    '4': {
        'title': ' Discord ',
        'categories': [
            {
                'title': ' Discord ',
                'options': ['30', '31', '32', '33', '34', '35', '36', '37'],
                'color': '#FFD700'
            }
        ]
    }
}

# Animated menu configuration
BASE_BOX_WIDTH = 45
MIN_BOX_WIDTH = 28
FPS = 30
FLOW_SPEED = 0.25
VIS_THRESHOLD = 0.35
BOX_SPACING = "   "

def wave(step, offset=0.0):
    """Generate wave value for animation."""
    return (math.sin(step * FLOW_SPEED + offset) + 1) / 2

def animated_hline(length, step, offset=0.0):
    """Create animated horizontal line."""
    if not RICH_AVAILABLE:
        return "─" * length
    chars = []
    for i in range(length):
        chars.append("─" if wave(step, i * 0.15 + offset) > VIS_THRESHOLD else " ")
    return "".join(chars)

def get_option_color(opt_num):
    """Get the color for an option based on which page it's on."""
    for page_num, page_config in MENU_PAGES.items():
        for category in page_config['categories']:
            if opt_num in category['options']:
                return category['color']
    return '#FFFFFF'  # Default white if not found

def format_option_text(opt_num, max_width=25, color=None):
    """Format option text for display with optional color."""
    opt_name = OPTIONS.get(opt_num, 'Unknown')
    # Replace hyphens with spaces and truncate
    display_name = opt_name.replace('-', ' ')[:max_width]
    text = f"[{opt_num}] {display_name}"
    
    if color and RICH_AVAILABLE:
        # Return Text object with color styling
        return Text(text, style=color)
    return text

def render_box(step: int, category: dict, box_width: int, page_num: str):
    """Render a single category box."""
    category_color = category['color']
    
    if not RICH_AVAILABLE:
        # Fallback to simple text
        lines = []
        lines.append(f"╭{'─' * (box_width - 2)}╮")
        lines.append(f"│{category['title'].center(box_width - 2)}│")
        # Handle empty options gracefully
        if category.get('options'):
            for opt_num in category['options']:
                opt_text = format_option_text(opt_num, box_width - 6, color=None)
                lines.append(f"│{opt_text.ljust(box_width - 2)}│")
        else:
            # Add a message when no options are available
            no_options_msg = "No options available"
            lines.append(f"│{no_options_msg.center(box_width - 2)}│")
        lines.append(f"╰{'─' * (box_width - 2)}╯")
        return lines
    
    lines = []
    title = category['title']
    options = category.get('options', [])
    
    # Top border - all in category color
    top_line = Text("╭", style=category_color)
    top_hline = animated_hline(box_width - 2, step)
    title_start = (box_width - len(title)) // 2 - 1
    if title_start >= 0:
        # Split the hline and insert title with color
        before_title = top_hline[:title_start]
        after_title = top_hline[title_start + len(title):]
        top_line.append(before_title, style=category_color)
        top_line.append(title, style=category_color)
        top_line.append(after_title, style=category_color)
    else:
        top_line.append(top_hline, style=category_color)
    top_line.append("╮", style=category_color)
    lines.append(top_line)
    
    # Middle - options with matching colors
    if options:
        for i, opt_num in enumerate(options):
            opt_text_obj = format_option_text(opt_num, box_width - 6, color=category_color)
            
            # Get the text string for width calculation
            if isinstance(opt_text_obj, Text):
                opt_text_str = opt_text_obj.plain
            else:
                opt_text_str = str(opt_text_obj)
            
            # Pad to fill the box width
            padding_needed = box_width - 2 - len(opt_text_str)
            
            left = "│" if wave(step, i) > VIS_THRESHOLD else " "
            right = "│" if wave(step, i + 1.5) > VIS_THRESHOLD else " "
            
            # Create the line with colored option text
            line = Text(left, style=category_color)
            if isinstance(opt_text_obj, Text):
                line.append(opt_text_obj)
            else:
                line.append(opt_text_obj, style=category_color)
            # Add padding with same color
            if padding_needed > 0:
                line.append(" " * padding_needed, style=category_color)
            line.append(right, style=category_color)
            
            lines.append(line)
    else:
        # Add a message when no options are available
        no_options_msg = "No options available"
        padding_needed = box_width - 2 - len(no_options_msg)
        line = Text("│", style=category_color)
        line.append(no_options_msg.center(box_width - 2), style=category_color)
        line.append("│", style=category_color)
        lines.append(line)
    
    # Bottom border - all in category color
    bottom_line = Text("╰", style=category_color)
    bottom_hline = animated_hline(box_width - 2, step, offset=2.0)
    bottom_line.append(bottom_hline, style=category_color)
    bottom_line.append("╯", style=category_color)
    lines.append(bottom_line)
    
    return lines

def _get_menu_layout(page_categories):
    """Compute responsive layout settings based on current terminal width."""
    try:
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    n = len(page_categories)
    spacing = len(BOX_SPACING)
    
    # Since we have one category per page, make the box wider
    if n == 1:
        # Use more of the terminal width for single category
        box_width = min(70, max(BASE_BOX_WIDTH, width - 10))
        return {"mode": "horizontal", "box_width": box_width}
    
    min_total = (MIN_BOX_WIDTH * n) + (spacing * (n - 1))
    if width < min_total:
        # Too narrow for boxes side-by-side; stack vertically.
        return {"mode": "vertical", "box_width": min(BASE_BOX_WIDTH, max(MIN_BOX_WIDTH, width - 4))}
    available = width - (spacing * (n - 1))
    box_width = max(MIN_BOX_WIDTH, min(BASE_BOX_WIDTH, available // n))
    return {"mode": "horizontal", "box_width": box_width}

def render_menu(step: int, page_num: str):
    """Render the complete menu with all categories for a page."""
    if not RICH_AVAILABLE:
        return None
    
    page_config = MENU_PAGES.get(page_num, MENU_PAGES['1'])
    categories = page_config['categories']
    
    layout = _get_menu_layout(categories)
    box_width = layout["box_width"]
    mode = layout["mode"]

    boxes = [render_box(step, category, box_width, page_num) for category in categories]
    frame = Text()
    
    # Add navigation info at top
    try:
        term_width = shutil.get_terminal_size().columns
    except:
        term_width = 80
    nav_text = f"Page {page_num}/4 | [N]   Next | [B]   Back | [I]   Info"
    frame.append(nav_text.center(term_width), style="dim")
    frame.append("\n\n")
    
    # Find max rows - handle empty boxes gracefully
    if boxes:
        max_rows = max(len(box) for box in boxes) if boxes else 3
        if max_rows < 3:
            max_rows = 3  # Minimum box size (top border, title, bottom border)
    else:
        max_rows = 3
    
    for row in range(max_rows):
        # Center the box horizontally (we have one box per page)
        if len(boxes) == 1:
            # Single box - center it
            box = boxes[0]
            if row < len(box):
                # Get the text content length for centering
                line_content = box[row]
                # Estimate width (box_width should be close)
                padding = max(0, (term_width - box_width) // 2)
                if padding > 0:
                    frame.append(" " * padding)
                frame.append(line_content)
            else:
                # Empty line for shorter boxes
                padding = max(0, (term_width - box_width) // 2)
                if padding > 0:
                    frame.append(" " * padding)
                frame.append(" " * box_width)
        else:
            # Multiple boxes (shouldn't happen with current structure, but keep for compatibility)
            total_width = sum(box_width for _ in boxes) + (len(boxes) - 1) * len(BOX_SPACING)
            padding = max(0, (term_width - total_width) // 2)
            if padding > 0:
                frame.append(" " * padding)
            for i, box in enumerate(boxes):
                if row < len(box):
                    frame.append(box[row])
                else:
                    frame.append(Text(" " * box_width))
                if i < len(boxes) - 1:
                    frame.append(BOX_SPACING)
        if row < max_rows - 1:
            frame.append("\n")
    
    return frame

def display_animated_menu(page_num='1'):
    """Display the animated menu."""
    # Clear screen aggressively using both ANSI codes and system command
    try:
        # Clear using ANSI escape codes first
        print("\033[2J\033[H", end="", flush=True)
        # Also use system command
        if 'os_name' not in globals():
            os_name = "Windows" if os.name == 'nt' else "Linux"
        if os_name == "Windows":
            os.system("cls")
        elif os_name == "Linux":
            os.system("clear")
        else:
            os.system("clear")
    except:
        pass
    
    if RICH_AVAILABLE:
        try:
            console = Console(force_terminal=True)
            logo = get_logo_rich()
            
            # Show animated menu for a short time, then static
            menu_frame = render_menu(0, page_num)
            if menu_frame:
                combined = Group(
                    Align.center(logo) if logo else Text(),
                    Align.center(menu_frame),
                )
                # Use Live with screen=True to ensure clean display and no duplication
                with Live(
                    Align.center(combined),
                    refresh_per_second=FPS,
                    screen=True,
                    transient=False,
                ) as live:
                    for step in range(30):  # Show animation for ~1 second
                        menu_frame = render_menu(step, page_num)
                        if menu_frame:
                            combined = Group(
                                Align.center(logo) if logo else Text(),
                                Align.center(menu_frame),
                            )
                            live.update(Align.center(combined))
                        time.sleep(1 / FPS)
                    # Final static frame - update one more time
                    final_frame = render_menu(30, page_num)
                    if final_frame:
                        combined = Group(
                            Align.center(logo) if logo else Text(),
                            Align.center(final_frame),
                        )
                        live.update(Align.center(combined))
                        # Keep the final frame visible by not exiting Live context immediately
                        time.sleep(0.1)
                
                # After Live context, print the final frame again to ensure it stays visible
                final_frame = render_menu(30, page_num)
                if final_frame:
                    combined = Group(
                        Align.center(logo) if logo else Text(),
                        Align.center(final_frame),
                    )
                    console.print(Align.center(combined))
        except Exception:
            # Fallback if rich fails
            print_logo()
            display_simple_menu(page_num)
    else:
        # Simple text menu
        print_logo()
        display_simple_menu(page_num)

def display_simple_menu(page_num='1'):
    """Display simple text-based menu as fallback."""
    try:
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    
    page_config = MENU_PAGES.get(page_num, MENU_PAGES['1'])
    print(f"\n{page_config['title'].center(width)}")
    print(f"Page {page_num}/4 | [N]   Next | [B]   Back | [I]   Info".center(width))
    print()
    
    for category in page_config['categories']:
        category_color = category['color']
        print("\n" + category['title'].center(width))
        # Handle empty options gracefully
        if category.get('options'):
            for opt_num in category['options']:
                opt_text = format_option_text(opt_num, color=None)
                # Apply ANSI color code for the category color
                # Convert hex color to RGB
                hex_color = category_color.lstrip('#')
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                colored_text = f"\033[38;2;{r};{g};{b}m{opt_text}\033[0m"
                print(("  " + colored_text).center(width))
        else:
            # Display message when no options available
            no_options_msg = "No options available"
            print(("  " + no_options_msg).center(width))

class ColorFilter:
    """Filter to apply category color to program output and filter ASCII art banners."""
    def __init__(self, original, color_rgb):
        self.original = original
        self.color_code = f"\033[38;2;{color_rgb[0]};{color_rgb[1]};{color_rgb[2]}m"
        self.reset_code = "\033[0m"
        import re
        # Pattern to match ANSI escape codes
        self.ansi_pattern = re.compile(r'\033\[[0-9;]*[a-zA-Z]|\x1b\[[0-9;]*[a-zA-Z]')
        # Track consecutive ASCII art lines
        self.ascii_art_line_count = 0
        self.in_ascii_art_block = False
    
    def _is_ascii_art_line(self, line):
        """Check if a line is ASCII art - only filter actual banners, keep functional text."""
        if not line or not line.strip():
            return False
        
        clean_line = line.strip()
        
        # NEVER filter Title banners (they use ╔╗║╚╝═ characters)
        # Title banners have a specific pattern: ╔══...══╗, ║...║, ╚══...══╝
        title_banner_patterns = ['╔', '╗', '║', '╚', '╝', '═']
        if any(char in clean_line for char in title_banner_patterns):
            return False  # Keep Title banners
        
        # NEVER filter lines that look like prompts or functional text
        prompt_patterns = [
            '[', ']', '->', '|', ':',  # Common prompt characters
            'Ip ->', 'Token ->', 'Url ->', 'Email ->',  # Specific prompts
            'Press', 'Enter', 'continue', 'Choice', 'Option',  # Common words
            'INFO', 'ERROR', 'WAIT', 'INPUT',  # Status indicators
        ]
        
        # If line contains prompt-like patterns, it's functional text - keep it
        if any(pattern in clean_line for pattern in prompt_patterns):
            return False
        
        # If line starts with common prompt formats, keep it
        if clean_line.startswith(('[', '(', '>', '|')):
            return False
        
        # Count different character types
        non_whitespace = [c for c in clean_line if not c.isspace()]
        if len(non_whitespace) < 5:  # Very short lines might be functional
            return False
        
        # ASCII art character set (excluding Title banner characters)
        ascii_art_chars = set('@#*:=-+%.0123456789^Mv_|{};aOj>pJ^╭╮│─├┼┴┬┌┐└┘▓█░▒')
        
        ascii_count = sum(1 for c in non_whitespace if c in ascii_art_chars)
        letter_count = sum(1 for c in non_whitespace if c.isalpha())
        symbol_count = sum(1 for c in non_whitespace if not c.isalnum() and c not in '.,!?[]->|:')
        
        total_chars = len(non_whitespace)
        
        ascii_ratio = ascii_count / total_chars if total_chars > 0 else 0
        letter_ratio = letter_count / total_chars if total_chars > 0 else 0
        symbol_ratio = symbol_count / total_chars if total_chars > 0 else 0
        
        # Only filter if it's clearly ASCII art (banner-like):
        if len(non_whitespace) > 30 and ascii_ratio > 0.4 and letter_ratio < 0.05:
            return True
        if ascii_ratio > 0.5 and letter_ratio < 0.03:
            return True
        if len(non_whitespace) > 50 and symbol_ratio > 0.6 and letter_ratio < 0.1:
            return True
        if any(pattern in clean_line for pattern in ['@@@', '###', '***', '===']):
            if letter_ratio < 0.05:
                return True
        
        return False
    
    def write(self, text):
        if not text:
            self.original.write(text)
            return
        
        # Remove all ANSI codes first
        cleaned = self.ansi_pattern.sub('', text)
        
        # Split into lines and filter out ASCII art
        lines = cleaned.split('\n')
        filtered_lines = []
        
        for line in lines:
            # Check if this line is ASCII art
            if self._is_ascii_art_line(line):
                self.ascii_art_line_count += 1
                self.in_ascii_art_block = True
                continue  # Skip ASCII art lines
            else:
                # Reset counter when we find non-ASCII art
                if self.in_ascii_art_block and self.ascii_art_line_count > 0:
                    self.ascii_art_line_count = 0
                    self.in_ascii_art_block = False
                filtered_lines.append(line)
        
        # Join filtered lines
        output_text = '\n'.join(filtered_lines)
        
        # Only output if there's actual content (not just ASCII art)
        if output_text.strip():
            # Always apply our color code first
            self.original.write(self.color_code)
            # Write the filtered text
            self.original.write(output_text)
            # Only reset color if it ends with newline (complete line)
            if text.endswith('\n') or text.endswith('\r\n'):
                self.original.write(self.reset_code)
        elif not cleaned.strip():
            # Preserve empty lines/newlines for structure only if not in ASCII art block
            if not self.in_ascii_art_block and text.endswith('\n'):
                self.original.write('\n')
    
    def flush(self):
        self.original.flush()
    
    def __getattr__(self, name):
        return getattr(self.original, name)

def start_program(program_name):
    """Launch a program from the Program directory and apply category color to all output."""
    try:
        # Get the color for this option
        opt_num = None
        for key, value in OPTIONS.items():
            if value == program_name:
                opt_num = key
                break
        
        category_color = get_option_color(opt_num) if opt_num else '#FFFFFF'
        
        # Convert hex to RGB
        hex_color = category_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        color_rgb = (r, g, b)
        
        # Get tool_path - always calculate it directly
        tool_path = os.path.dirname(os.path.abspath(__file__))
        program_path = os.path.join(tool_path, "Program", f"{program_name}.py")
        
        # Verify the program file exists and is the correct one
        if not os.path.exists(program_path):
            print(f"[!] Program not found: {program_name}.py")
            print(f"[!] Expected path: {program_path}")
            input("\nPress Enter to continue...")
            return
        
        # Double-check we're launching the correct program (safety check)
        expected_programs = {
            '10': 'Discord-RAt',
            '11': 'Ransomware', 
            '12': 'Grabber',
            '01': 'Website-Strength-Scanner'
        }
        if opt_num and opt_num in expected_programs:
            if program_name != expected_programs[opt_num]:
                print(f"[!] Error: Option {opt_num} should launch {expected_programs[opt_num]}, but got {program_name}")
                input("\nPress Enter to continue...")
                return
        
        # Save original stdout/stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        import builtins
        original_input = builtins.input
        
        # Create color filters
        color_filter_stdout = ColorFilter(original_stdout, color_rgb)
        color_filter_stderr = ColorFilter(original_stderr, color_rgb)
        
        # Wrap stdout and stderr
        sys.stdout = color_filter_stdout
        sys.stderr = color_filter_stderr
        
        # Wrap input function to ensure prompts stay colored
        def colored_input(prompt=''):
            """Wrapper for input() that ensures prompts are colored."""
            if prompt:
                sys.stdout.write(str(prompt))
                sys.stdout.flush()
            return original_input('')
        
        # Replace built-in input
        builtins.input = colored_input
        
        # Patch subprocess.run to prevent launching RedTiger.py
        original_subprocess_run = subprocess.run
        def patched_subprocess_run(*args, **kwargs):
            """Patch subprocess.run to prevent launching RedTiger.py."""
            if args and len(args) > 0:
                cmd = args[0]
                if isinstance(cmd, (list, tuple)) and len(cmd) > 0:
                    if any('RedTiger.py' in str(arg) for arg in cmd):
                        sys.exit(0)
            return original_subprocess_run(*args, **kwargs)
        subprocess.run = patched_subprocess_run
        
        # Create no-op Reset function
        def create_no_reset():
            def no_reset():
                sys.exit(0)
            return no_reset
        
        try:
            script_dir = os.path.dirname(program_path)
            original_cwd = os.getcwd()
            original_path = sys.path[:]  # Save original sys.path
            
            # Add Program directory to sys.path for imports
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)
            
            os.chdir(script_dir)
            
            try:
                # Read and execute the script
                with open(program_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                
                # Create execution namespace
                namespace = {
                    '__name__': '__main__',
                    '__file__': program_path,
                    '__package__': None,
                }
                
                # Execute the script
                try:
                    exec(compile(code, program_path, 'exec'), namespace)
                    
                    # After execution, patch Reset if Config.Util was imported
                    if 'Config' in namespace and hasattr(namespace['Config'], 'Util'):
                        util_module = namespace['Config'].Util
                        if hasattr(util_module, 'Reset'):
                            util_module.Reset = create_no_reset()
                except SystemExit:
                    pass
                except Exception as exec_error:
                    # Print error for debugging
                    print(f"[!] Error executing program: {exec_error}")
                    # If Config.Util is already imported globally, patch it
                    try:
                        import Config.Util as util_module
                        if hasattr(util_module, 'Reset'):
                            util_module.Reset = create_no_reset()
                    except:
                        pass
            finally:
                os.chdir(original_cwd)
                # Restore original sys.path
                sys.path[:] = original_path
        finally:
            # Restore original stdout/stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            # Restore original input
            import builtins
            builtins.input = original_input
            # Restore original subprocess.run
            subprocess.run = original_subprocess_run
        
        # Clear screen after program exits and return to menu
        if 'Clear' in globals():
            Clear()
        else:
            try:
                if 'os_name' in globals():
                    os_name_val = os_name
                else:
                    os_name_val = "Windows" if os.name == 'nt' else "Linux"
                if os_name_val == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
            except:
                pass
    except Exception as e:
        print(f"[!] Error launching program: {e}")
        input("\nPress Enter to continue...")
        if 'Clear' in globals():
            Clear()
        else:
            try:
                if 'os_name' in globals() and os_name == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
            except:
                pass

# Main menu loop
menu_number = '1'
# Get tool_path
tool_path = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.join(tool_path, "Program", "Config", "Menu.txt")

# Load saved menu number
try:
    if os.path.exists(menu_path):
        with open(menu_path, "r") as file:
            saved_menu = file.read().strip()
            if saved_menu in ['1', '2', '3', '4']:
                menu_number = saved_menu
except:
    pass

while True:
    try:
        os.system("title Kane_tools")
    except:
        pass
    
    display_animated_menu(menu_number)
    print("")
    
    try:
        width = shutil.get_terminal_size().columns
    except:
        width = 80
    
    choice = input(f"Option: ".center(width // 2)).strip()
    
    # Navigation
    if choice.lower() in ['n', 'next']:
        menu_number = {"1": "2", "2": "3", "3": "4", "4": "1"}.get(menu_number, "1")
        try:
            with open(menu_path, "w") as file:
                file.write(menu_number)
        except:
            pass
        continue
    
    elif choice.lower() in ['b', 'back']:
        menu_number = {"2": "1", "3": "2", "4": "3", "1": "4"}.get(menu_number, "1")
        try:
            with open(menu_path, "w") as file:
                file.write(menu_number)
        except:
            pass
        continue
    
    elif choice.lower() in ['i', 'info']:
        webbrowser.open("https://t.me/kane_tools")
        webbrowser.open("https://guns.lol/zey1063")
        continue
    
    elif choice.lower() in ['exit', 'quit', 'q']:
        break
    
    # Handle option selection - check exact match first (two-digit options like 10, 11, 12, etc.)
    if choice in OPTIONS:
        option_name = OPTIONS[choice]
        start_program(option_name)
        continue  # Refresh menu after program execution
    
    # Handle single digit options (01-09) - convert to two-digit format
    # Only process if it's a single digit AND the two-digit version exists
    # AND the current page actually has single-digit options (page 1 has 01, 02)
    elif len(choice) == 1 and choice.isdigit():
        # Check if current page has single-digit options
        current_page_config = MENU_PAGES.get(menu_number, MENU_PAGES['1'])
        has_single_digit_options = False
        for category in current_page_config.get('categories', []):
            for opt in category.get('options', []):
                if len(opt) == 2 and opt.startswith('0'):
                    has_single_digit_options = True
                    break
            if has_single_digit_options:
                break
        
        # Only convert single digit to "0X" format if current page has single-digit options
        if has_single_digit_options:
            option_key = '0' + choice
            if option_key in OPTIONS:
                option_name = OPTIONS[option_key]
                start_program(option_name)
                continue  # Refresh menu after program execution
        
        # If we get here, the single digit is not valid for this page
        print("[!] Invalid option. Please choose a valid option number or type 'exit' to quit.")
        time.sleep(1)
    
    else:
        print("[!] Invalid option. Please choose a valid option number or type 'exit' to quit.")
        time.sleep(1)
