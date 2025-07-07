import json
import os
from typing import Dict, Any

class JsonHandler:
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in file {file_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading JSON file {file_path}: {e}")
    
    @staticmethod
    def save_json(file_path: str, data: Dict[str, Any]) -> None:
        """Save JSON data to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Error saving JSON file {file_path}: {e}")
    
    @staticmethod
    def validate_warudo_scene(data: Dict[str, Any]) -> bool:
        """Validate if the JSON data is a valid Warudo scene"""
        required_fields = ['name', 'appVersion', 'graphs']
        return all(field in data for field in required_fields)
    
    @staticmethod
    def format_json_string(data: Dict[str, Any]) -> str:
        """Format JSON data as a readable string"""
        return json.dumps(data, indent=2, ensure_ascii=False)
