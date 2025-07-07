from src.utils.json_handler import JsonHandler
from typing import Dict, Any, List, Optional
import copy

class BlueprintData:
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.data = {}
        if file_path:
            self.load()
    
    def load(self):
        """Load blueprint data from JSON file"""
        self.data = JsonHandler.load_json(self.file_path)
        if not JsonHandler.validate_warudo_scene(self.data):
            raise ValueError("Invalid Warudo scene format")
    
    def save(self):
        """Save blueprint data to JSON file"""
        if self.file_path:
            JsonHandler.save_json(self.file_path, self.data)
    
    def get_blueprint_list(self) -> List[Dict[str, Any]]:
        """Get list of all blueprints in the scene"""
        if not self.data or "graphs" not in self.data:
            return []
        
        # Build category mapping from graphHierarchy
        category_map = self._build_category_map()
        
        blueprints = []
        for graph in self.data["graphs"]:
            bp_info = {
                "id": graph.get("id", ""),
                "name": graph.get("name", "Unknown"),
                "enabled": graph.get("enabled", True),
                "order": graph.get("order", 0),
                "group": graph.get("group", None),
                "category": category_map.get(graph.get("id", ""), "Uncategorized"),
                "node_count": len(graph.get("nodes", {})),
                "connection_count": len(graph.get("dataConnections", [])) + len(graph.get("flowConnections", [])),
                "has_variables": len(graph.get("properties", {}).get("dataInputs", {}).get("Variables", {}).get("value", "[]")) > 2
            }
            blueprints.append(bp_info)
        
        return blueprints
    
    def _build_category_map(self) -> Dict[str, str]:
        """Build mapping from blueprint ID to category name"""
        category_map = {}
        
        if not self.data or "graphHierarchy" not in self.data:
            return category_map
        
        def traverse_hierarchy(node, current_category=""):
            if not node:
                return
            
            key = node.get("key", "")
            children = node.get("children", [])
            
            if children:
                # This is a category node
                category_name = key if key else "Uncategorized"
                for child in children:
                    traverse_hierarchy(child, category_name)
            else:
                # This is a blueprint node (leaf)
                if key and self._is_blueprint_id(key):
                    category_map[key] = current_category or "Uncategorized"
        
        # Start traversal from root
        hierarchy_root = self.data["graphHierarchy"]
        if "children" in hierarchy_root:
            for child in hierarchy_root["children"]:
                traverse_hierarchy(child)
        
        return category_map
    
    def _is_blueprint_id(self, key: str) -> bool:
        """Check if a key is a blueprint ID (UUID format)"""
        import re
        # UUID pattern: 8-4-4-4-12 hexadecimal characters
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, key.lower()))
    
    def get_blueprint_by_id(self, bp_id: str) -> Optional[Dict[str, Any]]:
        """Get blueprint data by ID"""
        if not self.data or "graphs" not in self.data:
            return None
        
        for graph in self.data["graphs"]:
            if graph.get("id") == bp_id:
                return graph
        return None
    
    def get_blueprint_by_name(self, bp_name: str) -> Optional[Dict[str, Any]]:
        """Get blueprint data by name"""
        if not self.data or "graphs" not in self.data:
            return None
        
        for graph in self.data["graphs"]:
            if graph.get("name") == bp_name:
                return graph
        return None
    
    def copy_blueprint_to_scene(self, bp_id: str, target_scene: 'BlueprintData', 
                               new_name: str = None, replace_existing: bool = False, 
                               keep_original_id: bool = False) -> bool:
        """Copy a blueprint to another scene"""
        source_bp = self.get_blueprint_by_id(bp_id)
        if not source_bp:
            return False
        
        # Create deep copy of the blueprint
        new_bp = copy.deepcopy(source_bp)
        
        # Generate new ID if not replacing and not keeping original ID
        if not replace_existing and not keep_original_id:
            import uuid
            new_bp["id"] = str(uuid.uuid4())
        
        # Set new name if provided
        if new_name:
            new_bp["name"] = new_name
        
        # Initialize target scene data if needed
        if not target_scene.data:
            target_scene.data = {
                "name": "New Scene",
                "appVersion": "0.13.1",
                "graphs": []
            }
        
        if "graphs" not in target_scene.data:
            target_scene.data["graphs"] = []
        
        # Check if blueprint with same ID already exists (when keeping original ID)
        if keep_original_id:
            existing_bp_with_id = target_scene.get_blueprint_by_id(new_bp["id"])
            if existing_bp_with_id and not replace_existing:
                # If same ID exists and not replacing, this is an error
                return False
            elif existing_bp_with_id and replace_existing:
                # Remove existing blueprint with same ID
                target_scene.data["graphs"] = [g for g in target_scene.data["graphs"] 
                                             if g.get("id") != new_bp["id"]]
        
        # Check if blueprint with same name already exists
        existing_bp = target_scene.get_blueprint_by_name(new_bp["name"])
        if existing_bp and not replace_existing and not keep_original_id:
            # Generate unique name only if not keeping original ID
            base_name = new_bp["name"]
            counter = 1
            while target_scene.get_blueprint_by_name(f"{base_name} ({counter})"):
                counter += 1
            new_bp["name"] = f"{base_name} ({counter})"
        elif existing_bp and replace_existing:
            # Remove existing blueprint with same name
            target_scene.data["graphs"] = [g for g in target_scene.data["graphs"] 
                                         if g.get("name") != new_bp["name"]]
        
        # Add the new blueprint
        target_scene.data["graphs"].append(new_bp)
        
        # Update graph hierarchy if needed
        source_category = self._get_blueprint_category(bp_id)
        self._update_graph_hierarchy(target_scene, new_bp, source_category)
        
        return True
    
    def _get_blueprint_category(self, bp_id: str) -> str:
        """Get the category of a blueprint from graph hierarchy"""
        category_map = self._build_category_map()
        return category_map.get(bp_id, "Bp")
    
    def _update_graph_hierarchy(self, target_scene: 'BlueprintData', new_bp: Dict[str, Any], category: str = "Bp"):
        """Update graph hierarchy to include the new blueprint with proper category"""
        if "graphHierarchy" not in target_scene.data:
            target_scene.data["graphHierarchy"] = {
                "collapsed": False,
                "key": "",
                "children": []
            }
        
        # Find or create the category group
        category_group = None
        for child in target_scene.data["graphHierarchy"]["children"]:
            if child.get("key") == category:
                category_group = child
                break
        
        if not category_group:
            category_group = {
                "collapsed": False,
                "key": category,
                "children": []
            }
            target_scene.data["graphHierarchy"]["children"].append(category_group)
        
        # Add new blueprint to hierarchy
        bp_hierarchy_entry = {
            "collapsed": False,
            "key": new_bp["id"],
            "children": None
        }
        
        # Check if already exists
        existing_entry = None
        for child in category_group["children"]:
            if child.get("key") == new_bp["id"]:
                existing_entry = child
                break
        
        if not existing_entry:
            category_group["children"].append(bp_hierarchy_entry)
    
    def remove_blueprint(self, bp_id: str) -> bool:
        """Remove a blueprint from the scene"""
        if not self.data or "graphs" not in self.data:
            return False
        
        # Remove from graphs
        original_count = len(self.data["graphs"])
        self.data["graphs"] = [g for g in self.data["graphs"] if g.get("id") != bp_id]
        
        if len(self.data["graphs"]) == original_count:
            return False  # Blueprint not found
        
        # Remove from hierarchy
        self._remove_from_hierarchy(bp_id)
        
        return True
    
    def _remove_from_hierarchy(self, bp_id: str):
        """Remove blueprint from graph hierarchy"""
        if "graphHierarchy" not in self.data:
            return
        
        def remove_recursive(node):
            if "children" in node and node["children"]:
                node["children"] = [child for child in node["children"] 
                                  if child.get("key") != bp_id]
                for child in node["children"]:
                    remove_recursive(child)
        
        remove_recursive(self.data["graphHierarchy"])
    
    def get_scene_info(self) -> Dict[str, Any]:
        """Get basic scene information"""
        return {
            "name": self.data.get("name", "Unknown"),
            "appVersion": self.data.get("appVersion", "Unknown"),
            "blueprint_count": len(self.data.get("graphs", [])),
            "asset_count": len(self.data.get("assets", [])),
            "file_path": self.file_path
        }
