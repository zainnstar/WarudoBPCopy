import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.gui.blueprint_list_frame import BlueprintListFrame
from src.models.blueprint_data import BlueprintData

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Warudo Blueprint Copy Tool")
        self.root.geometry("1600x800")
        self.root.minsize(1200, 600)
        
        # Initialize data
        self.left_scene = None
        self.right_scene = None
        
        self.setup_ui()
        self.setup_menu()
    
    def setup_ui(self):
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create toolbar
        toolbar = ttk.Frame(main_container)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Load buttons
        ttk.Button(toolbar, text="Load Source Scene", 
                  command=self.load_source_scene).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Load Target Scene", 
                  command=self.load_target_scene).pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Action buttons
        ttk.Button(toolbar, text="Copy Selected →", 
                  command=self.copy_to_target).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="← Copy Selected", 
                  command=self.copy_to_source).pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Utility buttons
        ttk.Button(toolbar, text="Refresh", 
                  command=self.refresh_both_scenes).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Create New Scene", 
                  command=self.create_new_scene).pack(side=tk.LEFT, padx=5)
        
        # Create main content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left panel (source)
        self.left_frame = BlueprintListFrame(content_frame, "Source Scene")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Create center panel (controls)
        center_frame = ttk.Frame(content_frame)
        center_frame.pack(side=tk.LEFT, padx=10)
        
        # Copy controls
        copy_frame = ttk.LabelFrame(center_frame, text="Copy Options")
        copy_frame.pack(pady=20)
        
        # Copy mode selection
        self.copy_mode = tk.StringVar(value="copy")
        ttk.Radiobutton(copy_frame, text="Copy (Keep Original)", 
                       variable=self.copy_mode, value="copy").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Radiobutton(copy_frame, text="Move (Remove Original)", 
                       variable=self.copy_mode, value="move").pack(anchor=tk.W, padx=10, pady=2)
        
        # Replace option
        self.replace_existing = tk.BooleanVar()
        ttk.Checkbutton(copy_frame, text="Replace if exists", 
                       variable=self.replace_existing).pack(anchor=tk.W, padx=10, pady=2)
        
        # Rename option
        self.auto_rename = tk.BooleanVar(value=True)
        ttk.Checkbutton(copy_frame, text="Auto-rename duplicates", 
                       variable=self.auto_rename).pack(anchor=tk.W, padx=10, pady=2)
        
        # Keep original ID option
        self.keep_original_id = tk.BooleanVar(value=True)
        ttk.Checkbutton(copy_frame, text="Keep original ID", 
                       variable=self.keep_original_id).pack(anchor=tk.W, padx=10, pady=2)
        
        # Action buttons
        ttk.Button(copy_frame, text="Copy →", 
                  command=self.copy_to_target).pack(pady=10, fill=tk.X, padx=10)
        ttk.Button(copy_frame, text="← Copy", 
                  command=self.copy_to_source).pack(pady=2, fill=tk.X, padx=10)
        
        # Create right panel (target)
        self.right_frame = BlueprintListFrame(content_frame, "Target Scene")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Create status bar
        self.status_bar = ttk.Label(main_container, text="Ready", 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Source Scene...", command=self.load_source_scene)
        file_menu.add_command(label="Load Target Scene...", command=self.load_target_scene)
        file_menu.add_separator()
        file_menu.add_command(label="Save Source Scene", command=self.save_source_scene)
        file_menu.add_command(label="Save Target Scene", command=self.save_target_scene)
        file_menu.add_separator()
        file_menu.add_command(label="Create New Scene...", command=self.create_new_scene)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy Selected to Target", command=self.copy_to_target)
        edit_menu.add_command(label="Copy Selected to Source", command=self.copy_to_source)
        edit_menu.add_separator()
        edit_menu.add_command(label="Refresh Both Scenes", command=self.refresh_both_scenes)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def load_source_scene(self):
        """Load source scene file"""
        file_path = filedialog.askopenfilename(
            title="Select Source Scene File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.left_scene = BlueprintData(file_path)
                self.left_frame.set_file_path(file_path)
                self.left_frame.load_blueprints(self.left_scene)
                self.update_status(f"Source scene loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load source scene:\n{str(e)}")
                self.update_status("Failed to load source scene")
    
    def load_target_scene(self):
        """Load target scene file"""
        file_path = filedialog.askopenfilename(
            title="Select Target Scene File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.right_scene = BlueprintData(file_path)
                self.right_frame.set_file_path(file_path)
                self.right_frame.load_blueprints(self.right_scene)
                self.update_status(f"Target scene loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load target scene:\n{str(e)}")
                self.update_status("Failed to load target scene")
    
    def save_source_scene(self):
        """Save source scene"""
        if not self.left_scene:
            messagebox.showwarning("Warning", "No source scene loaded")
            return
        
        try:
            self.left_scene.save()
            self.update_status("Source scene saved")
            messagebox.showinfo("Success", "Source scene saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save source scene:\n{str(e)}")
    
    def save_target_scene(self):
        """Save target scene"""
        if not self.right_scene:
            messagebox.showwarning("Warning", "No target scene loaded")
            return
        
        try:
            self.right_scene.save()
            self.update_status("Target scene saved")
            messagebox.showinfo("Success", "Target scene saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save target scene:\n{str(e)}")
    
    def copy_to_target(self):
        """Copy selected blueprints from source to target"""
        if not self.left_scene or not self.right_scene:
            messagebox.showwarning("Warning", "Please load both source and target scenes")
            return
        
        selected_bps = self.left_frame.get_selected_blueprints()
        if not selected_bps:
            messagebox.showinfo("Info", "No blueprints selected in source scene")
            return
        
        success_count = 0
        failed_count = 0
        for bp_id in selected_bps:
            try:
                bp_data = self.left_scene.get_blueprint_by_id(bp_id)
                if bp_data:
                    # Determine new name
                    new_name = None
                    if not self.auto_rename.get() and not self.replace_existing.get() and not self.keep_original_id.get():
                        new_name = bp_data["name"]
                    
                    # Copy blueprint
                    if self.left_scene.copy_blueprint_to_scene(
                        bp_id, self.right_scene, new_name, self.replace_existing.get(), 
                        self.keep_original_id.get()):
                        success_count += 1
                        
                        # Remove from source if move mode
                        if self.copy_mode.get() == "move":
                            self.left_scene.remove_blueprint(bp_id)
                    else:
                        failed_count += 1
                        if self.keep_original_id.get():
                            messagebox.showwarning("Warning", 
                                f"Blueprint '{bp_data['name']}' could not be copied because a blueprint with the same ID already exists in the target scene.")
            except Exception as e:
                failed_count += 1
                messagebox.showerror("Error", f"Failed to copy blueprint:\n{str(e)}")
                continue
        
        if success_count > 0:
            # Save and refresh
            self.right_scene.save()
            self.right_frame.load_blueprints(self.right_scene)
            
            if self.copy_mode.get() == "move":
                self.left_scene.save()
                self.left_frame.load_blueprints(self.left_scene)
            
            self.left_frame.clear_selection()
            
            action = "moved" if self.copy_mode.get() == "move" else "copied"
            message = f"{success_count} blueprints {action} to target scene"
            if failed_count > 0:
                message += f" ({failed_count} failed)"
            self.update_status(message)
            messagebox.showinfo("Success", f"{success_count} blueprints {action} successfully" + 
                               (f"\n{failed_count} failed due to ID conflicts" if failed_count > 0 else ""))
        elif failed_count > 0:
            messagebox.showerror("Error", f"Failed to copy {failed_count} blueprints")
    
    def copy_to_source(self):
        """Copy selected blueprints from target to source"""
        if not self.left_scene or not self.right_scene:
            messagebox.showwarning("Warning", "Please load both source and target scenes")
            return
        
        selected_bps = self.right_frame.get_selected_blueprints()
        if not selected_bps:
            messagebox.showinfo("Info", "No blueprints selected in target scene")
            return
        
        success_count = 0
        failed_count = 0
        for bp_id in selected_bps:
            try:
                bp_data = self.right_scene.get_blueprint_by_id(bp_id)
                if bp_data:
                    # Determine new name
                    new_name = None
                    if not self.auto_rename.get() and not self.replace_existing.get() and not self.keep_original_id.get():
                        new_name = bp_data["name"]
                    
                    # Copy blueprint
                    if self.right_scene.copy_blueprint_to_scene(
                        bp_id, self.left_scene, new_name, self.replace_existing.get(), 
                        self.keep_original_id.get()):
                        success_count += 1
                        
                        # Remove from target if move mode
                        if self.copy_mode.get() == "move":
                            self.right_scene.remove_blueprint(bp_id)
                    else:
                        failed_count += 1
                        if self.keep_original_id.get():
                            messagebox.showwarning("Warning", 
                                f"Blueprint '{bp_data['name']}' could not be copied because a blueprint with the same ID already exists in the source scene.")
            except Exception as e:
                failed_count += 1
                messagebox.showerror("Error", f"Failed to copy blueprint:\n{str(e)}")
                continue
        
        if success_count > 0:
            # Save and refresh
            self.left_scene.save()
            self.left_frame.load_blueprints(self.left_scene)
            
            if self.copy_mode.get() == "move":
                self.right_scene.save()
                self.right_frame.load_blueprints(self.right_scene)
            
            self.right_frame.clear_selection()
            
            action = "moved" if self.copy_mode.get() == "move" else "copied"
            message = f"{success_count} blueprints {action} to source scene"
            if failed_count > 0:
                message += f" ({failed_count} failed)"
            self.update_status(message)
            messagebox.showinfo("Success", f"{success_count} blueprints {action} successfully" + 
                               (f"\n{failed_count} failed due to ID conflicts" if failed_count > 0 else ""))
        elif failed_count > 0:
            messagebox.showerror("Error", f"Failed to copy {failed_count} blueprints")
    
    def refresh_both_scenes(self):
        """Refresh both scene displays"""
        if self.left_scene:
            try:
                self.left_scene.load()
                self.left_frame.load_blueprints(self.left_scene)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to refresh source scene:\n{str(e)}")
        
        if self.right_scene:
            try:
                self.right_scene.load()
                self.right_frame.load_blueprints(self.right_scene)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to refresh target scene:\n{str(e)}")
        
        self.update_status("Scenes refreshed")
    
    def create_new_scene(self):
        """Create a new empty scene"""
        file_path = filedialog.asksaveasfilename(
            title="Create New Scene File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        
        if file_path:
            try:
                # Create new scene data
                new_scene = BlueprintData()
                new_scene.data = {
                    "name": "New Scene",
                    "appVersion": "0.13.1",
                    "selectedAssetId": "00000000-0000-0000-0000-000000000000",
                    "selectedGraphId": "00000000-0000-0000-0000-000000000000",
                    "assets": [],
                    "assetHierarchy": {"collapsed": False, "key": "", "children": []},
                    "graphs": [],
                    "graphHierarchy": {"collapsed": False, "key": "", "children": []},
                    "plugins": {"Warudo.Core": {"version": "0.13.1", "data": "null"}}
                }
                new_scene.file_path = file_path
                new_scene.save()
                
                # Ask which side to load it on
                result = messagebox.askyesnocancel(
                    "Load New Scene",
                    "New scene created successfully!\n\nLoad as:\nYes = Source Scene\nNo = Target Scene\nCancel = Don't load"
                )
                
                if result is True:  # Yes - load as source
                    self.left_scene = new_scene
                    self.left_frame.set_file_path(file_path)
                    self.left_frame.load_blueprints(self.left_scene)
                    self.update_status(f"New source scene created: {file_path}")
                elif result is False:  # No - load as target
                    self.right_scene = new_scene
                    self.right_frame.set_file_path(file_path)
                    self.right_frame.load_blueprints(self.right_scene)
                    self.update_status(f"New target scene created: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create new scene:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Warudo Blueprint Copy Tool v1.0

A tool for copying blueprints between Warudo scene files.

Features:
- Load and view blueprints from Warudo scene files
- Copy blueprints between scenes
- Move blueprints between scenes
- Auto-rename duplicate blueprints
- Replace existing blueprints
- View blueprint details
- Create new scene files

Author: AI Assistant
"""
        messagebox.showinfo("About", about_text)
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
