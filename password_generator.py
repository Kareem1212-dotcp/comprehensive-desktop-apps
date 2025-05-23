#!/usr/bin/env python3
"""
Professional Password Generator Desktop Application
A secure, feature-rich password generator with GUI interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import secrets
import string
import re
import os
from datetime import datetime
import webbrowser

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        self.setup_keyboard_shortcuts()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Professional Password Generator")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
    def setup_variables(self):
        """Initialize tkinter variables"""
        self.length_var = tk.IntVar(value=12)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)
        self.password_count_var = tk.IntVar(value=1)
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Password Generator", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Configuration Frame
        config_frame = ttk.LabelFrame(main_frame, text="Password Configuration", 
                                     padding="15")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                         pady=(0, 15))
        config_frame.columnconfigure(1, weight=1)
        
        # Password Length
        ttk.Label(config_frame, text="Password Length:").grid(row=0, column=0, 
                                                              sticky=tk.W, pady=5)
        length_frame = ttk.Frame(config_frame)
        length_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        self.length_scale = ttk.Scale(length_frame, from_=8, to=50, 
                                     variable=self.length_var, orient=tk.HORIZONTAL,
                                     command=self.on_length_change)
        self.length_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.length_label = ttk.Label(length_frame, text="12")
        self.length_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Character Sets
        ttk.Label(config_frame, text="Character Sets:").grid(row=1, column=0, 
                                                             sticky=(tk.W, tk.N), pady=5)
        
        char_frame = ttk.Frame(config_frame)
        char_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Checkbutton(char_frame, text="Uppercase (A-Z)", 
                       variable=self.uppercase_var).pack(anchor=tk.W)
        ttk.Checkbutton(char_frame, text="Lowercase (a-z)", 
                       variable=self.lowercase_var).pack(anchor=tk.W)
        ttk.Checkbutton(char_frame, text="Numbers (0-9)", 
                       variable=self.numbers_var).pack(anchor=tk.W)
        ttk.Checkbutton(char_frame, text="Symbols (!@#$%^&*)", 
                       variable=self.symbols_var).pack(anchor=tk.W)
        ttk.Checkbutton(char_frame, text="Exclude ambiguous (0, O, l, 1)", 
                       variable=self.exclude_ambiguous_var).pack(anchor=tk.W)
        
        # Number of passwords
        ttk.Label(config_frame, text="Number of Passwords:").grid(row=2, column=0, 
                                                                  sticky=tk.W, pady=5)
        count_frame = ttk.Frame(config_frame)
        count_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        count_spinbox = ttk.Spinbox(count_frame, from_=1, to=50, width=10,
                                   textvariable=self.password_count_var)
        count_spinbox.pack(side=tk.LEFT)
        
        # Generation Frame
        gen_frame = ttk.Frame(main_frame)
        gen_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        gen_frame.columnconfigure(1, weight=1)
        
        # Generate Button
        self.generate_btn = ttk.Button(gen_frame, text="Generate Password(s)", 
                                      command=self.generate_passwords,
                                      style='Accent.TButton')
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear Button
        clear_btn = ttk.Button(gen_frame, text="Clear", command=self.clear_passwords)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Copy Button
        self.copy_btn = ttk.Button(gen_frame, text="Copy to Clipboard", 
                                  command=self.copy_to_clipboard, state='disabled')
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save Button
        self.save_btn = ttk.Button(gen_frame, text="Save to File", 
                                  command=self.save_to_file, state='disabled')
        self.save_btn.pack(side=tk.LEFT)
        
        # Password Display Frame
        display_frame = ttk.LabelFrame(main_frame, text="Generated Passwords", 
                                      padding="15")
        display_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=(0, 15))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Password Text Area
        self.password_text = scrolledtext.ScrolledText(display_frame, height=8, width=70,
                                                      font=('Courier', 11),
                                                      wrap=tk.WORD, state='disabled')
        self.password_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Strength Indicator Frame
        strength_frame = ttk.LabelFrame(main_frame, text="Password Strength", 
                                       padding="15")
        strength_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                           pady=(0, 15))
        strength_frame.columnconfigure(0, weight=1)
        
        # Strength Progress Bar
        self.strength_var = tk.StringVar(value="No password generated")
        self.strength_label = ttk.Label(strength_frame, textvariable=self.strength_var)
        self.strength_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.strength_progress = ttk.Progressbar(strength_frame, length=400, mode='determinate')
        self.strength_progress.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready to generate passwords")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Menu Bar
        self.create_menu()
        
        # Configure main frame row weights for responsive design
        main_frame.rowconfigure(3, weight=1)
        
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Passwords", command=self.save_to_file,
                             accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit,
                             accelerator="Ctrl+Q")
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Generate", command=self.generate_passwords,
                             accelerator="Ctrl+G")
        edit_menu.add_command(label="Copy to Clipboard", command=self.copy_to_clipboard,
                             accelerator="Ctrl+C")
        edit_menu.add_command(label="Clear", command=self.clear_passwords,
                             accelerator="Ctrl+L")
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        help_menu.add_command(label="About", command=self.show_about)
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-g>', lambda e: self.generate_passwords())
        self.root.bind('<Control-c>', lambda e: self.copy_to_clipboard())
        self.root.bind('<Control-l>', lambda e: self.clear_passwords())
        self.root.bind('<Control-s>', lambda e: self.save_to_file())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F1>', lambda e: self.show_instructions())
        
    def on_length_change(self, value):
        """Update length label when scale changes"""
        length = int(float(value))
        self.length_label.config(text=str(length))
        
    def get_character_set(self):
        """Build character set based on selected options"""
        charset = ""
        
        if self.uppercase_var.get():
            charset += string.ascii_uppercase
        if self.lowercase_var.get():
            charset += string.ascii_lowercase
        if self.numbers_var.get():
            charset += string.digits
        if self.symbols_var.get():
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        # Remove ambiguous characters if selected
        if self.exclude_ambiguous_var.get():
            ambiguous = "0O1lI"
            charset = ''.join(c for c in charset if c not in ambiguous)
            
        return charset
        
    def generate_password(self, length, charset):
        """Generate a single secure password"""
        if not charset:
            raise ValueError("No character sets selected")
            
        if length < 8 or length > 50:
            raise ValueError("Password length must be between 8 and 50 characters")
            
        # Use secrets module for cryptographically secure generation
        password = ''.join(secrets.choice(charset) for _ in range(length))
        return password
        
    def calculate_strength(self, password):
        """Calculate password strength score and description"""
        if not password:
            return 0, "No password"
            
        score = 0
        feedback = []
        
        # Length scoring
        length = len(password)
        if length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        else:
            feedback.append("Too short")
            
        # Character variety scoring
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        variety_count = sum([has_upper, has_lower, has_digit, has_symbol])
        score += variety_count * 15
        
        # Complexity bonus
        if variety_count >= 3:
            score += 15
        if variety_count == 4:
            score += 10
            
        # Pattern penalties
        if re.search(r'(.)\1{2,}', password):  # Repeated characters
            score -= 10
            feedback.append("Avoid repeated characters")
            
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            score -= 5
            feedback.append("Avoid sequential numbers")
            
        # Cap at 100
        score = min(100, max(0, score))
        
        # Determine strength level
        if score >= 80:
            strength = "Very Strong"
            color = "green"
        elif score >= 60:
            strength = "Strong"
            color = "blue"
        elif score >= 40:
            strength = "Moderate"
            color = "orange"
        elif score >= 20:
            strength = "Weak"
            color = "red"
        else:
            strength = "Very Weak"
            color = "red"
            
        return score, f"{strength} ({score}/100)"
        
    def generate_passwords(self):
        """Generate passwords based on current settings"""
        try:
            # Validate settings
            if not any([self.uppercase_var.get(), self.lowercase_var.get(),
                       self.numbers_var.get(), self.symbols_var.get()]):
                messagebox.showerror("Error", "Please select at least one character set.")
                return
                
            charset = self.get_character_set()
            length = self.length_var.get()
            count = self.password_count_var.get()
            
            # Generate passwords
            passwords = []
            for _ in range(count):
                password = self.generate_password(length, charset)
                passwords.append(password)
                
            # Display passwords
            self.password_text.config(state='normal')
            self.password_text.delete(1.0, tk.END)
            
            for i, password in enumerate(passwords, 1):
                if count > 1:
                    self.password_text.insert(tk.END, f"Password {i}: {password}\n")
                else:
                    self.password_text.insert(tk.END, password)
                    
            self.password_text.config(state='disabled')
            
            # Update strength indicator (use first password)
            score, strength_text = self.calculate_strength(passwords[0])
            self.strength_var.set(strength_text)
            self.strength_progress['value'] = score
            
            # Update status
            if count == 1:
                self.status_var.set("Password generated successfully")
            else:
                self.status_var.set(f"{count} passwords generated successfully")
                
            # Enable buttons
            self.copy_btn.config(state='normal')
            self.save_btn.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {str(e)}")
            self.status_var.set("Error generating password")
            
    def copy_to_clipboard(self):
        """Copy generated passwords to clipboard"""
        try:
            password_content = self.password_text.get(1.0, tk.END).strip()
            if not password_content:
                messagebox.showwarning("Warning", "No passwords to copy.")
                return
                
            # Use tkinter's built-in clipboard functionality
            self.root.clipboard_clear()
            self.root.clipboard_append(password_content)
            self.root.update()  # Keep clipboard content after window closes
            
            self.status_var.set("Passwords copied to clipboard")
            messagebox.showinfo("Success", "Passwords copied to clipboard successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
            
    def save_to_file(self):
        """Save generated passwords to a text file"""
        try:
            password_content = self.password_text.get(1.0, tk.END).strip()
            if not password_content:
                messagebox.showwarning("Warning", "No passwords to save.")
                return
                
            # Open file dialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Passwords"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Generated Passwords - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*50 + "\n\n")
                    f.write(password_content)
                    f.write(f"\n\nGenerated with Password Generator v1.0")
                    
                self.status_var.set(f"Passwords saved to {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"Passwords saved to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
            
    def clear_passwords(self):
        """Clear all generated passwords"""
        self.password_text.config(state='normal')
        self.password_text.delete(1.0, tk.END)
        self.password_text.config(state='disabled')
        
        # Reset strength indicator
        self.strength_var.set("No password generated")
        self.strength_progress['value'] = 0
        
        # Disable buttons
        self.copy_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        
        self.status_var.set("Passwords cleared")
        
    def show_instructions(self):
        """Show help instructions"""
        instructions = """
Password Generator Instructions

BASIC USAGE:
1. Set your desired password length (8-50 characters)
2. Select character sets to include in your password
3. Choose the number of passwords to generate
4. Click 'Generate Password(s)' or press Ctrl+G

CHARACTER SETS:
• Uppercase: A-Z
• Lowercase: a-z  
• Numbers: 0-9
• Symbols: !@#$%^&*()_+-=[]{}|;:,.<>?
• Exclude Ambiguous: Removes confusing characters (0, O, l, 1, I)

FEATURES:
• Real-time password strength analysis
• Copy passwords to clipboard (Ctrl+C)
• Save passwords to text file (Ctrl+S)
• Generate multiple passwords at once
• Clear all passwords (Ctrl+L)

KEYBOARD SHORTCUTS:
• Ctrl+G: Generate passwords
• Ctrl+C: Copy to clipboard
• Ctrl+S: Save to file
• Ctrl+L: Clear passwords
• Ctrl+Q: Exit application
• F1: Show this help

SECURITY TIPS:
• Use passwords of at least 12 characters
• Include multiple character types
• Avoid using the same password for multiple accounts
• Store passwords securely
• Change passwords regularly
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Instructions")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Center the help window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (help_window.winfo_screenheight() // 2) - (500 // 2)
        help_window.geometry(f"600x500+{x}+{y}")
        
        text_frame = ttk.Frame(help_window, padding="20")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                               font=('Arial', 10))
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, instructions)
        text_widget.config(state='disabled')
        
        close_btn = ttk.Button(text_frame, text="Close", 
                              command=help_window.destroy)
        close_btn.pack(pady=(10, 0))
        
    def show_about(self):
        """Show about dialog"""
        about_text = """Professional Password Generator v1.0

A secure, feature-rich password generator built with Python and Tkinter.

Features:
• Cryptographically secure password generation
• Customizable length and character sets
• Real-time strength analysis
• Clipboard integration
• Export functionality
• Cross-platform compatibility

Developed with security and usability in mind.

© 2024 - Built with Python"""
        
        messagebox.showinfo("About Password Generator", about_text)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PasswordGenerator(root)
    
    # Handle window closing
    def on_closing():
        root.quit()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    finally:
        root.destroy()

if __name__ == "__main__":
    main()
