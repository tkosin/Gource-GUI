"""Configuration management for Gource GUI"""
import json
import os
from typing import Dict, Any, List

class ConfigManager:
    """Manages application configuration and user preferences"""
    
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.gource-gui")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.defaults = self._get_defaults()
        self.config = self.load_config()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values"""
        return {
            "window": {
                "width": 900,
                "height": 700,
                "x": None,
                "y": None
            },
            "gource": {
                "resolution": "1280x720",
                "custom_width": 1920,
                "custom_height": 1080,
                "seconds_per_day": 10.0,
                "auto_skip_seconds": 3.0,
                "framerate": 60,
                "fullscreen": False,
                "multi_sampling": False,
                "hide_filenames": False,
                "hide_dirnames": False,
                "hide_usernames": False,
                "hide_bloom": False,
                "hide_progress": False,
                "background_color": "#000000",
                "font_scale": 1.0,
                "camera_mode": "overview",
                "start_date": "",
                "stop_date": "",
                "user_image_dir": "",
                "elasticity": 0.0
            },
            "recent_repositories": [],
            "last_export_dir": "",
            "theme": "system"
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            return self.defaults.copy()
        
        try:
            with open(self.config_file, 'r') as f:
                loaded = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            config = self.defaults.copy()
            self._deep_update(config, loaded)
            return config
            
        except (json.JSONDecodeError, FileNotFoundError, PermissionError):
            return self.defaults.copy()
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except (PermissionError, OSError):
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def add_recent_repository(self, repo_path: str) -> None:
        """Add repository to recent list"""
        recent = self.config.get("recent_repositories", [])
        
        # Remove if already exists
        if repo_path in recent:
            recent.remove(repo_path)
        
        # Add to front
        recent.insert(0, repo_path)
        
        # Keep only last 10
        self.config["recent_repositories"] = recent[:10]
    
    def get_recent_repositories(self) -> List[str]:
        """Get list of recent repositories"""
        return self.config.get("recent_repositories", [])
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults"""
        self.config = self.defaults.copy()
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict) -> None:
        """Recursively update nested dictionary"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
