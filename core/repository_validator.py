"""Repository validation and analysis functionality"""
import os
import subprocess
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from collections import Counter

try:
    import git
    GITPYTHON_AVAILABLE = True
except ImportError:
    GITPYTHON_AVAILABLE = False

class RepositoryInfo:
    """Container for repository information"""
    
    def __init__(self):
        self.is_valid = False
        self.repo_type = None
        self.path = ""
        self.name = ""
        self.error_message = ""
        self.commit_count = 0
        self.contributor_count = 0
        self.contributors = []
        self.date_range = ("", "")
        self.file_extensions = []
        self.primary_languages = []

class RepositoryValidator:
    """Validates and analyzes version control repositories"""
    
    SUPPORTED_VCS = {
        '.git': 'git',
        '.svn': 'svn',
        '.hg': 'mercurial',
        '.bzr': 'bazaar'
    }
    
    LANGUAGE_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript', 
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.c': 'C',
        '.h': 'C/C++',
        '.hpp': 'C++',
        '.cs': 'C#',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.go': 'Go',
        '.rs': 'Rust',
        '.kt': 'Kotlin',
        '.swift': 'Swift',
        '.scala': 'Scala',
        '.r': 'R',
        '.m': 'Objective-C',
        '.pl': 'Perl',
        '.sh': 'Shell',
        '.bash': 'Shell',
        '.zsh': 'Shell',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.less': 'Less',
        '.vue': 'Vue',
        '.jsx': 'JSX',
        '.tsx': 'TSX'
    }
    
    def validate_repository(self, repo_path: str) -> RepositoryInfo:
        """Validate and analyze a repository"""
        info = RepositoryInfo()
        info.path = repo_path
        info.name = os.path.basename(repo_path) if repo_path else "Unknown"
        
        if not repo_path or not os.path.exists(repo_path):
            info.error_message = "Path does not exist"
            return info
        
        if not os.path.isdir(repo_path):
            info.error_message = "Path is not a directory"
            return info
        
        # Check for version control systems
        repo_type = self._detect_vcs_type(repo_path)
        if not repo_type:
            info.error_message = "No supported version control system detected"
            return info
        
        info.repo_type = repo_type
        
        # Analyze repository based on type
        try:
            if repo_type == 'git':
                self._analyze_git_repository(repo_path, info)
            else:
                # For non-git repos, do basic analysis
                self._analyze_generic_repository(repo_path, info)
            
            info.is_valid = True
            
        except Exception as e:
            info.error_message = f"Failed to analyze repository: {str(e)}"
            
        return info
    
    def _detect_vcs_type(self, repo_path: str) -> Optional[str]:
        """Detect version control system type"""
        for vcs_dir, vcs_type in self.SUPPORTED_VCS.items():
            if os.path.exists(os.path.join(repo_path, vcs_dir)):
                return vcs_type
        
        # Check if we're inside a git repository
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--is-inside-work-tree'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip() == 'true':
                return 'git'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return None
    
    def _analyze_git_repository(self, repo_path: str, info: RepositoryInfo) -> None:
        """Analyze Git repository using GitPython or git commands"""
        if GITPYTHON_AVAILABLE:
            self._analyze_git_with_gitpython(repo_path, info)
        else:
            self._analyze_git_with_commands(repo_path, info)
    
    def _analyze_git_with_gitpython(self, repo_path: str, info: RepositoryInfo) -> None:
        """Analyze Git repository using GitPython library"""
        try:
            repo = git.Repo(repo_path)
            
            # Get commits
            commits = list(repo.iter_commits())
            info.commit_count = len(commits)
            
            if commits:
                # Get contributors
                contributors = set()
                for commit in commits:
                    if commit.author.name:
                        contributors.add(commit.author.name)
                
                info.contributors = list(contributors)
                info.contributor_count = len(contributors)
                
                # Get date range
                oldest_commit = commits[-1]
                newest_commit = commits[0]
                
                info.date_range = (
                    oldest_commit.committed_datetime.strftime("%Y-%m-%d"),
                    newest_commit.committed_datetime.strftime("%Y-%m-%d")
                )
            
            # Analyze file types
            self._analyze_file_types(repo_path, info)
            
        except Exception as e:
            raise Exception(f"GitPython analysis failed: {str(e)}")
    
    def _analyze_git_with_commands(self, repo_path: str, info: RepositoryInfo) -> None:
        """Analyze Git repository using git commands"""
        try:
            # Get commit count
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                info.commit_count = int(result.stdout.strip())
            
            # Get contributors
            result = subprocess.run(
                ['git', 'log', '--format=%an', '--all'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                contributors = set(line.strip() for line in result.stdout.splitlines() if line.strip())
                info.contributors = list(contributors)
                info.contributor_count = len(contributors)
            
            # Get date range
            result = subprocess.run(
                ['git', 'log', '--format=%ci', '--reverse', '--all'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                dates = result.stdout.strip().splitlines()
                if dates:
                    first_date = dates[0].split()[0]
                    last_date = dates[-1].split()[0]
                    info.date_range = (first_date, last_date)
            
            # Analyze file types
            self._analyze_file_types(repo_path, info)
            
        except Exception as e:
            raise Exception(f"Git command analysis failed: {str(e)}")
    
    def _analyze_generic_repository(self, repo_path: str, info: RepositoryInfo) -> None:
        """Basic analysis for non-git repositories"""
        self._analyze_file_types(repo_path, info)
    
    def _analyze_file_types(self, repo_path: str, info: RepositoryInfo) -> None:
        """Analyze file types in the repository"""
        extension_count = Counter()
        
        # Walk through directory structure
        for root, dirs, files in os.walk(repo_path):
            # Skip VCS directories
            dirs[:] = [d for d in dirs if not d.startswith('.git') and not d.startswith('.svn') 
                      and not d.startswith('.hg') and not d.startswith('.bzr')]
            
            for file in files:
                if not file.startswith('.'):
                    _, ext = os.path.splitext(file)
                    if ext:
                        extension_count[ext.lower()] += 1
        
        # Get top extensions
        info.file_extensions = [ext for ext, _ in extension_count.most_common(10)]
        
        # Map to languages
        languages = Counter()
        for ext, count in extension_count.items():
            if ext in self.LANGUAGE_EXTENSIONS:
                languages[self.LANGUAGE_EXTENSIONS[ext]] += count
        
        info.primary_languages = [lang for lang, _ in languages.most_common(5)]
    
    def check_gource_compatibility(self, repo_path: str) -> Tuple[bool, str]:
        """Check if repository is compatible with Gource"""
        try:
            result = subprocess.run(
                ['gource', '--log-command', 'git'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return True, "Repository is compatible with Gource"
            else:
                return False, f"Gource compatibility check failed: {result.stderr}"
                
        except FileNotFoundError:
            return False, "Gource not found. Please install Gource first."
        except subprocess.TimeoutExpired:
            return False, "Gource compatibility check timed out"
        except Exception as e:
            return False, f"Error checking Gource compatibility: {str(e)}"
