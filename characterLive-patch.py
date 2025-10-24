"""
characterLive-patch - Utility tool for characterLive project
Provides various maintenance and management features
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import json
import os
import sys
from pathlib import Path
import threading


class CharacterLivePatch:
    def __init__(self, root):
        self.root = root
        self.root.title("characterLive-patch")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Default path configuration
        self.default_paths = {
            'characterlive_path': r'E:\mine\gitspace\characterLive',
            'singsong_path': r'C:\MiaoMiao\singsong',
            'sovits_path': r'C:\MiaoMiao\so-vits-svc'
        }
        
        # Configuration file path
        self.config_file = self.get_config_path()
        
        # Load configuration
        self.config = self.load_config()
        
        # Create UI
        self.create_widgets()
        
        # Load saved paths or use defaults
        self.load_saved_paths()
    
    def get_config_path(self):
        """Get configuration file path"""
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(app_dir, "config.json")
    
    def load_config(self):
        """Load configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.log_message(f"Failed to load config: {e}")
                return {}
        return {}
    
    def save_config(self):
        """Save configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            self.log_message("Configuration saved")
        except Exception as e:
            self.log_message(f"Failed to save config: {e}")
    
    def create_widgets(self):
        """Create UI components"""
        padding = {'padx': 10, 'pady': 5}
        
        # Row 1: characterLive project path
        row1_frame = tk.Frame(self.root)
        row1_frame.pack(fill=tk.X, **padding)
        
        tk.Label(row1_frame, text="characterLive:", width=18, anchor='w').pack(side=tk.LEFT)
        self.characterlive_entry = tk.Entry(row1_frame)
        self.characterlive_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(row1_frame, text="Browse", command=lambda: self.browse_folder(self.characterlive_entry)).pack(side=tk.LEFT)
        
        # Row 2: singsong project path
        row2_frame = tk.Frame(self.root)
        row2_frame.pack(fill=tk.X, **padding)
        
        tk.Label(row2_frame, text="singsong:", width=18, anchor='w').pack(side=tk.LEFT)
        self.singsong_entry = tk.Entry(row2_frame)
        self.singsong_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(row2_frame, text="Browse", command=lambda: self.browse_folder(self.singsong_entry)).pack(side=tk.LEFT)
        
        # Row 3: so-vits-svc project path
        row3_frame = tk.Frame(self.root)
        row3_frame.pack(fill=tk.X, **padding)
        
        tk.Label(row3_frame, text="so-vits-svc:", width=18, anchor='w').pack(side=tk.LEFT)
        self.sovits_entry = tk.Entry(row3_frame)
        self.sovits_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(row3_frame, text="Browse", command=lambda: self.browse_folder(self.sovits_entry)).pack(side=tk.LEFT)
        
        # Row 4: Song name input
        row4_frame = tk.Frame(self.root)
        row4_frame.pack(fill=tk.X, **padding)
        
        tk.Label(row4_frame, text="Song name:", width=18, anchor='w').pack(side=tk.LEFT)
        self.songname_entry = tk.Entry(row4_frame)
        self.songname_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.execute_button = tk.Button(row4_frame, text="Execute", command=self.on_execute_click, bg='#ff6b6b', fg='white', font=('Arial', 10, 'bold'))
        self.execute_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Row 5: Output terminal
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.BOTH, expand=True, **padding)
        
        tk.Label(output_frame, text="Output:", anchor='w').pack(fill=tk.X)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            wrap=tk.WORD, 
            height=15,
            state='disabled',
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white',
            font=('Consolas', 9)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        self.log_message("=" * 80)
        self.log_message("Welcome to characterLive-patch!")
        self.log_message("Select project paths and enter song name to process")
        self.log_message("=" * 80)
    
    def browse_folder(self, entry_widget):
        """Browse folder"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder_path)
    
    def load_saved_paths(self):
        """Load saved paths or use defaults"""
        path = self.config.get('characterlive_path', self.default_paths['characterlive_path'])
        self.characterlive_entry.insert(0, path)
        
        path = self.config.get('singsong_path', self.default_paths['singsong_path'])
        self.singsong_entry.insert(0, path)
        
        path = self.config.get('sovits_path', self.default_paths['sovits_path'])
        self.sovits_entry.insert(0, path)
    
    def log_message(self, message):
        """Display message in output area"""
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')
        self.root.update_idletasks()
    
    def on_execute_click(self):
        """Execute button click handler"""
        characterlive_path = self.characterlive_entry.get().strip()
        singsong_path = self.singsong_entry.get().strip()
        sovits_path = self.sovits_entry.get().strip()
        song_name = self.songname_entry.get().strip()
        
        if not song_name:
            messagebox.showwarning("Warning", "Please enter song name!")
            return
        
        if not characterlive_path or not singsong_path or not sovits_path:
            messagebox.showwarning("Warning", "Please select all project paths!")
            return
        
        # Save configuration
        self.config['characterlive_path'] = characterlive_path
        self.config['singsong_path'] = singsong_path
        self.config['sovits_path'] = sovits_path
        self.save_config()
        
        # Confirm operation
        response = messagebox.askyesno(
            "Confirm", 
            f"Process all files containing '{song_name}'?\n\nThis action cannot be undone!"
        )
        
        if not response:
            self.log_message("Operation cancelled by user")
            return
        
        # Disable button to prevent duplicate clicks
        self.execute_button.config(state='disabled')
        
        # Execute operation in new thread
        thread = threading.Thread(target=self.process_files, args=(characterlive_path, singsong_path, sovits_path, song_name))
        thread.daemon = True
        thread.start()
    
    def process_files(self, characterlive_path, singsong_path, sovits_path, song_name):
        """Process files matching song name"""
        try:
            self.log_message("\n" + "=" * 80)
            self.log_message(f"Searching for files containing '{song_name}'...")
            self.log_message("=" * 80)
            
            search_dirs = []
            
            # characterLive/songs
            cl_songs = os.path.join(characterlive_path, "songs")
            if os.path.exists(cl_songs):
                search_dirs.append(("characterLive/songs", cl_songs))
            else:
                self.log_message(f"⚠ Warning: {cl_songs} does not exist")
            
            # singsong/songs
            ss_songs = os.path.join(singsong_path, "songs")
            if os.path.exists(ss_songs):
                search_dirs.append(("singsong/songs", ss_songs))
            else:
                self.log_message(f"⚠ Warning: {ss_songs} does not exist")
            
            # singsong/output
            ss_output = os.path.join(singsong_path, "output")
            if os.path.exists(ss_output):
                search_dirs.append(("singsong/output", ss_output))
            else:
                self.log_message(f"⚠ Warning: {ss_output} does not exist")
            
            total_found = 0
            total_processed = 0
            total_failed = 0
            
            for dir_name, dir_path in search_dirs:
                self.log_message(f"\n📁 Searching: {dir_name}")
                self.log_message(f"   Path: {dir_path}")
                
                found_files = []
                
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if song_name in file:
                            file_path = os.path.join(root, file)
                            found_files.append(file_path)
                
                if found_files:
                    self.log_message(f"   Found {len(found_files)} file(s):")
                    
                    for file_path in found_files:
                        total_found += 1
                        relative_path = os.path.relpath(file_path, dir_path)
                        self.log_message(f"   - {relative_path}")
                        
                        try:
                            os.remove(file_path)
                            total_processed += 1
                            self.log_message(f"     ✓ Processed")
                        except Exception as e:
                            total_failed += 1
                            self.log_message(f"     ✗ Failed: {e}")
                else:
                    self.log_message(f"   No files containing '{song_name}' found")
            
            self.log_message("\n" + "=" * 80)
            self.log_message("Operation completed!")
            self.log_message(f"Files found: {total_found}")
            self.log_message(f"Successfully processed: {total_processed}")
            if total_failed > 0:
                self.log_message(f"Failed: {total_failed}")
            self.log_message("=" * 80)
            
        except Exception as e:
            self.log_message(f"\n❌ Error: {e}")
            messagebox.showerror("Error", f"Operation failed: {e}")
        finally:
            self.root.after(0, lambda: self.execute_button.config(state='normal'))


def main():
    root = tk.Tk()
    app = CharacterLivePatch(root)
    root.mainloop()


if __name__ == "__main__":
    main()
