import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional

class BlueprintListFrame(ttk.Frame):
    def __init__(self, parent, title: str):
        super().__init__(parent)
        self.title = title
        self.file_path = ""
        self.blueprint_data = None
        self.current_sort_column = None
        self.sort_reverse = False
        self.blueprints_data = []  # Store original data for sorting
        self.setup_ui()
    
    def setup_ui(self):
        # Create title label
        title_label = ttk.Label(self, text=self.title, font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Create file path label
        self.file_label = ttk.Label(self, text="No file loaded", foreground="gray")
        self.file_label.pack(pady=(0, 5))
        
        # Create tree view for blueprint list
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbar
        self.tree = ttk.Treeview(self.tree_frame, columns=("name", "id", "enabled", "nodes", "connections"), 
                                show="tree headings", height=15)
        
        # Configure columns
        self.tree.heading("#0", text="Category")
        self.tree.heading("name", text="Name")
        self.tree.heading("id", text="ID")
        self.tree.heading("enabled", text="Enabled")
        self.tree.heading("nodes", text="Nodes")
        self.tree.heading("connections", text="Connections")
        
        # Configure column widths
        self.tree.column("#0", width=120, minwidth=100)
        self.tree.column("name", width=200, minwidth=150)
        self.tree.column("id", width=120, minwidth=100)
        self.tree.column("enabled", width=80, minwidth=60)
        self.tree.column("nodes", width=80, minwidth=60)
        self.tree.column("connections", width=100, minwidth=80)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy Blueprint JSON", command=self.copy_selected_blueprint)
        self.context_menu.add_command(label="Copy Blueprint ID", command=self.copy_blueprint_id)
        self.context_menu.add_command(label="Rename Blueprint", command=self.rename_selected_blueprint)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="View Details", command=self.view_blueprint_details)
        
        # Bind events
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right click
        self.tree.bind("<Double-1>", self.on_double_click)    # Double click
        
        # Bind header click events for sorting
        self.tree.heading("#0", command=lambda: self.sort_column("#0", "Category"))
        self.tree.heading("name", command=lambda: self.sort_column("name", "Name"))
        self.tree.heading("id", command=lambda: self.sort_column("id", "ID"))
        self.tree.heading("enabled", command=lambda: self.sort_column("enabled", "Enabled"))
        self.tree.heading("nodes", command=lambda: self.sort_column("nodes", "Nodes"))
        self.tree.heading("connections", command=lambda: self.sort_column("connections", "Connections"))
        
        # Create info frame
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.info_label = ttk.Label(self.info_frame, text="No blueprints loaded", 
                                   foreground="gray", font=("Arial", 9))
        self.info_label.pack()
    
    def set_file_path(self, file_path: str):
        """Set the file path and update the label"""
        self.file_path = file_path
        import os
        filename = os.path.basename(file_path)
        self.file_label.config(text=f"File: {filename}")
    
    def sort_column(self, column_id: str, column_name: str):
        """Sort the tree view by the specified column"""
        if not self.blueprints_data:
            return
        
        # Toggle sort order if clicking the same column
        if self.current_sort_column == column_id:
            self.sort_reverse = not self.sort_reverse
        else:
            self.current_sort_column = column_id
            self.sort_reverse = False
        
        # Update header text to show sort direction
        for col in ["#0", "name", "id", "enabled", "nodes", "connections"]:
            if col == "#0":
                header_text = "Category"
            elif col == "name":
                header_text = "Name"
            elif col == "id":
                header_text = "ID"
            elif col == "enabled":
                header_text = "Enabled"
            elif col == "nodes":
                header_text = "Nodes"
            elif col == "connections":
                header_text = "Connections"
            
            if col == column_id:
                arrow = " ↓" if self.sort_reverse else " ↑"
                header_text += arrow
            
            self.tree.heading(col, text=header_text)
        
        # Sort the data
        if column_id == "#0":
            # Sort by category
            self.blueprints_data.sort(key=lambda x: x.get("category", ""), reverse=self.sort_reverse)
        elif column_id == "name":
            # Sort by name
            self.blueprints_data.sort(key=lambda x: x.get("name", ""), reverse=self.sort_reverse)
        elif column_id == "id":
            # Sort by ID
            self.blueprints_data.sort(key=lambda x: x.get("id", ""), reverse=self.sort_reverse)
        elif column_id == "enabled":
            # Sort by enabled status
            self.blueprints_data.sort(key=lambda x: x.get("enabled", True), reverse=self.sort_reverse)
        elif column_id == "nodes":
            # Sort by node count
            self.blueprints_data.sort(key=lambda x: x.get("node_count", 0), reverse=self.sort_reverse)
        elif column_id == "connections":
            # Sort by connection count
            self.blueprints_data.sort(key=lambda x: x.get("connection_count", 0), reverse=self.sort_reverse)
        
        # If sorting by category, also sort by name within each category
        if column_id == "#0":
            from itertools import groupby
            grouped_data = []
            # First sort by category, then by name within each category
            self.blueprints_data.sort(key=lambda x: (x.get("category", ""), x.get("name", "")), reverse=self.sort_reverse)
        
        # Refresh the display
        self.refresh_tree_display()
    
    def refresh_tree_display(self):
        """Refresh the tree display with current data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add blueprints to tree
        for bp in self.blueprints_data:
            bp_id_short = bp["id"][:8] + "..." if len(bp["id"]) > 8 else bp["id"]
            enabled_text = "Yes" if bp["enabled"] else "No"
            category = bp.get("category", "Uncategorized")
            
            self.tree.insert("", "end", 
                           text=category,
                           values=(bp["name"], bp_id_short, enabled_text, bp["node_count"], bp["connection_count"]),
                           tags=("blueprint",))
    
    def load_blueprints(self, blueprint_data):
        """Load blueprints into the tree view"""
        self.blueprint_data = blueprint_data
        
        # Get blueprint list and store it
        self.blueprints_data = blueprint_data.get_blueprint_list()
        
        # Default sort by category, then by name
        self.blueprints_data.sort(key=lambda x: (x.get("category", ""), x.get("name", "")))
        
        # Refresh the display
        self.refresh_tree_display()
        
        # Update info label
        scene_info = blueprint_data.get_scene_info()
        info_text = f"Scene: {scene_info['name']} | Blueprints: {len(self.blueprints_data)} | Version: {scene_info['appVersion']}"
        self.info_label.config(text=info_text)
    
    def get_selected_blueprints(self) -> List[str]:
        """Get selected blueprint IDs"""
        selected_items = self.tree.selection()
        if not selected_items or not self.blueprints_data:
            return []
        
        selected_bps = []
        for item in selected_items:
            item_index = self.tree.index(item)
            if item_index < len(self.blueprints_data):
                selected_bps.append(self.blueprints_data[item_index]["id"])
        
        return selected_bps
    
    def clear_selection(self):
        """Clear tree selection"""
        self.tree.selection_remove(self.tree.selection())
    
    def show_context_menu(self, event):
        """Show context menu on right click"""
        if self.tree.selection():
            self.context_menu.post(event.x_root, event.y_root)
    
    def on_double_click(self, event):
        """Handle double click on blueprint"""
        self.view_blueprint_details()
    
    def copy_selected_blueprint(self):
        """Copy selected blueprint to clipboard (as JSON)"""
        selected_bps = self.get_selected_blueprints()
        if not selected_bps:
            messagebox.showinfo("Info", "No blueprint selected")
            return
        
        bp_id = selected_bps[0]
        bp_data = self.blueprint_data.get_blueprint_by_id(bp_id)
        
        if bp_data:
            import json
            json_str = json.dumps(bp_data, indent=2, ensure_ascii=False)
            
            # Copy to clipboard
            self.clipboard_clear()
            self.clipboard_append(json_str)
            self.update()
            
            messagebox.showinfo("Success", f"Blueprint '{bp_data['name']}' copied to clipboard as JSON")
    
    def copy_blueprint_id(self):
        """Copy selected blueprint ID to clipboard"""
        selected_bps = self.get_selected_blueprints()
        if not selected_bps:
            messagebox.showinfo("Info", "No blueprint selected")
            return
        
        bp_id = selected_bps[0]
        bp_data = self.blueprint_data.get_blueprint_by_id(bp_id)
        
        if bp_data:
            # Copy ID to clipboard
            self.clipboard_clear()
            self.clipboard_append(bp_id)
            self.update()
            
            messagebox.showinfo("Success", f"Blueprint ID '{bp_id}' copied to clipboard")
    
    def rename_selected_blueprint(self):
        """Rename selected blueprint"""
        selected_bps = self.get_selected_blueprints()
        if not selected_bps:
            messagebox.showinfo("Info", "No blueprint selected")
            return
        
        bp_id = selected_bps[0]
        bp_data = self.blueprint_data.get_blueprint_by_id(bp_id)
        
        if bp_data:
            # Create rename dialog
            dialog = tk.Toplevel(self)
            dialog.title("Rename Blueprint")
            dialog.geometry("300x100")
            dialog.resizable(False, False)
            dialog.transient(self)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
            y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
            dialog.geometry(f"+{x}+{y}")
            
            # Create entry
            ttk.Label(dialog, text="New name:").pack(pady=5)
            name_var = tk.StringVar(value=bp_data["name"])
            entry = ttk.Entry(dialog, textvariable=name_var, width=30)
            entry.pack(pady=5)
            entry.focus()
            entry.select_range(0, tk.END)
            
            # Create buttons
            btn_frame = ttk.Frame(dialog)
            btn_frame.pack(pady=10)
            
            def on_ok():
                new_name = name_var.get().strip()
                if new_name and new_name != bp_data["name"]:
                    bp_data["name"] = new_name
                    self.blueprint_data.save()
                    self.load_blueprints(self.blueprint_data)
                    messagebox.showinfo("Success", "Blueprint renamed successfully")
                dialog.destroy()
            
            def on_cancel():
                dialog.destroy()
            
            ttk.Button(btn_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)
            
            # Bind Enter key
            entry.bind("<Return>", lambda e: on_ok())
    
    def view_blueprint_details(self):
        """View blueprint details in a new window"""
        selected_bps = self.get_selected_blueprints()
        if not selected_bps:
            messagebox.showinfo("Info", "No blueprint selected")
            return
        
        bp_id = selected_bps[0]
        bp_data = self.blueprint_data.get_blueprint_by_id(bp_id)
        
        if bp_data:
            # Create details window
            details_window = tk.Toplevel(self)
            details_window.title(f"Blueprint Details: {bp_data['name']}")
            details_window.geometry("600x500")
            details_window.transient(self)
            
            # Create text widget with scrollbar
            text_frame = ttk.Frame(details_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
            scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Insert blueprint data
            import json
            json_str = json.dumps(bp_data, indent=2, ensure_ascii=False)
            text_widget.insert(tk.END, json_str)
            text_widget.config(state=tk.DISABLED)
            
            # Create close button
            ttk.Button(details_window, text="Close", 
                      command=details_window.destroy).pack(pady=10)
