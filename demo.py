#!/usr/bin/env python3
"""
Demo script for Gource GUI
This script demonstrates the functionality without requiring user interaction
"""
import os
import sys
import subprocess
import tempfile

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.gource_runner import GourceRunner
from core.repository_validator import RepositoryValidator

def create_sample_repo():
    """Create a sample git repository for testing"""
    temp_dir = tempfile.mkdtemp(prefix="gource_demo_")
    
    print(f"Creating sample repository in: {temp_dir}")
    
    # Initialize git repo
    subprocess.run(['git', 'init'], cwd=temp_dir, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Demo User'], cwd=temp_dir, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'demo@example.com'], cwd=temp_dir, capture_output=True)
    
    # Create some files and commits
    files_to_create = [
        ('README.md', '# Demo Project\n\nThis is a demonstration repository for Gource GUI.'),
        ('src/main.py', 'print("Hello, Gource!")'),
        ('src/utils.py', 'def greet(name):\n    return f"Hello, {name}!"'),
        ('docs/guide.md', '# User Guide\n\nHow to use this project.'),
        ('tests/test_main.py', 'import unittest\n\nclass TestMain(unittest.TestCase):\n    pass')
    ]
    
    for i, (filepath, content) in enumerate(files_to_create):
        full_path = os.path.join(temp_dir, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
        
        subprocess.run(['git', 'add', filepath], cwd=temp_dir, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Add {filepath}'], cwd=temp_dir, capture_output=True)
    
    return temp_dir

def test_repository_validation(repo_path):
    """Test repository validation functionality"""
    print("\n=== Testing Repository Validation ===")
    
    validator = RepositoryValidator()
    repo_info = validator.validate_repository(repo_path)
    
    if repo_info.is_valid:
        print(f"✓ Repository is valid: {repo_info.repo_type}")
        print(f"  - Name: {repo_info.name}")
        print(f"  - Commits: {repo_info.commit_count}")
        print(f"  - Contributors: {repo_info.contributor_count}")
        if repo_info.contributors:
            print(f"    Contributors: {', '.join(repo_info.contributors[:3])}")
        print(f"  - Date range: {repo_info.date_range[0]} to {repo_info.date_range[1]}")
        if repo_info.primary_languages:
            print(f"  - Languages: {', '.join(repo_info.primary_languages[:3])}")
    else:
        print(f"✗ Repository validation failed: {repo_info.error_message}")
    
    return repo_info.is_valid

def test_command_generation(repo_path):
    """Test Gource command generation"""
    print("\n=== Testing Command Generation ===")
    
    runner = GourceRunner()
    
    if not runner.check_gource_installed():
        print("✗ Gource is not installed")
        print("Install with: brew install gource")
        return False
    
    print("✓ Gource is installed")
    
    # Test different settings
    test_settings = [
        {
            'name': 'Basic settings',
            'settings': {
                'resolution': '1280x720',
                'seconds_per_day': 5.0,
                'fullscreen': False
            }
        },
        {
            'name': 'Advanced settings',
            'settings': {
                'resolution': '1920x1080',
                'seconds_per_day': 2.0,
                'fullscreen': False,
                'hide_filenames': True,
                'background_color': '#001122',
                'font_scale': 1.2
            }
        }
    ]
    
    for test_case in test_settings:
        print(f"\n{test_case['name']}:")
        cmd = runner.build_command(repo_path, test_case['settings'])
        print(f"  Command: {' '.join(cmd)}")
    
    return True

def main():
    """Main demo function"""
    print("🎬 Gource GUI Demo")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("Please run this script from the gource-gui directory")
        sys.exit(1)
    
    try:
        # Create sample repository
        repo_path = create_sample_repo()
        
        # Test repository validation
        if test_repository_validation(repo_path):
            # Test command generation
            test_command_generation(repo_path)
            
            print("\n=== GUI Application Info ===")
            print("To run the GUI application:")
            print("1. Run: ./run_gui.sh")
            print("   OR")
            print("2. Run: source venv/bin/activate && python3 main.py")
            print()
            print("Features available in the GUI:")
            print("- Browse and select repository folders")
            print("- Configure visualization settings")
            print("- Preview generated commands")
            print("- Run Gource visualizations")
            print("- Export to video (requires FFmpeg)")
            
            print(f"\n📁 Sample repository created at: {repo_path}")
            print("   You can use this path to test the GUI!")
            
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
