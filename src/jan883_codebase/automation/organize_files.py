import os
import shutil
import logging
from pathlib import Path
from typing import Dict, Set

def get_category_mapping() -> Dict[str, str]:
    """Return mapping of file extensions to category folders"""
    return {
        # Images
        'jpg': 'images', 'jpeg': 'images', 'png': 'images', 'gif': 'images',
        # Documents
        'pdf': 'documents', 'doc': 'documents', 'docx': 'documents', 'txt': 'documents',
        # Audio
        'mp3': 'audio', 'wav': 'audio', 'flac': 'audio',
        # Video
        'mp4': 'video', 'avi': 'video', 'mkv': 'video',
        # Archives
        'zip': 'archives', 'rar': 'archives', '7z': 'archives'
    }

def organize_files_by_extension(directory: str, dry_run: bool = False, use_categories: bool = True) -> None:
    """
    Organize files in a directory by moving them into subdirectories based on their extensions.
    
    Args:
        directory (str): Path to the directory to organize
        dry_run (bool): If True, only preview changes without moving files
        use_categories (bool): If True, group files by categories instead of extensions
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set of files/folders to ignore
    IGNORED_ITEMS: Set[str] = {'.DS_Store', 'Thumbs.db', '.git', '__pycache__'}
    category_mapping = get_category_mapping() if use_categories else {}
    
    try:
        directory_path = Path(directory).resolve()
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        logging.info(f"{'Preview of ' if dry_run else ''}Organizing: {directory}")
        
        # Count total files for progress tracking
        total_files = sum(1 for f in directory_path.iterdir() 
                         if f.is_file() and f.name not in IGNORED_ITEMS)
        
        if total_files == 0:
            logging.info("No files to organize.")
            return
            
        processed_files = 0
        
        for file_path in directory_path.iterdir():
            if not file_path.is_file() or file_path.name in IGNORED_ITEMS:
                continue
                
            processed_files += 1
            extension = file_path.suffix.lower().lstrip('.')
            
            if not extension:
                logging.info(f"Skipping file without extension: {file_path.name}")
                continue
                
            # Determine target directory
            if use_categories and extension in category_mapping:
                target_dir_name = category_mapping[extension]
            else:
                target_dir_name = extension
                
            target_dir = directory_path / target_dir_name
            
            if not target_dir.exists() and not dry_run:
                try:
                    target_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logging.error(f"Failed to create directory {target_dir_name}: {str(e)}")
                    continue
            
            new_file_path = target_dir / file_path.name
            
            # Handle duplicate filenames
            counter = 1
            while new_file_path.exists() and not dry_run:
                stem = file_path.stem
                new_file_path = target_dir / f"{stem}_{counter}{file_path.suffix}"
                counter += 1
            
            if dry_run:
                logging.info(f"Would move: {file_path.name} -> {target_dir_name}/{new_file_path.name}")
            else:
                try:
                    shutil.move(str(file_path), str(new_file_path))
                    logging.info(f"Moved ({processed_files}/{total_files}): "
                               f"{file_path.name} -> {target_dir_name}/{new_file_path.name}")
                except PermissionError:
                    logging.error(f"Permission denied: Could not move {file_path.name}")
                except Exception as e:
                    logging.error(f"Error moving {file_path.name}: {str(e)}")
        
        # Cleanup empty directories
        if not dry_run:
            for dir_path in directory_path.iterdir():
                if dir_path.is_dir() and not any(dir_path.iterdir()):
                    try:
                        dir_path.rmdir()
                        logging.info(f"Removed empty directory: {dir_path.name}")
                    except Exception as e:
                        logging.error(f"Failed to remove empty directory {dir_path.name}: {str(e)}")
                    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        downloads_path = str(Path.home() / "Downloads")
        
        # Preview changes first
        organize_files_by_extension(downloads_path, dry_run=True, use_categories=True)
        
        # Prompt user for confirmation
        response = input("\nDo you want to proceed with organizing files? (y/n): ").lower()
        if response == 'y':
            organize_files_by_extension(downloads_path, use_categories=True)
            logging.info("Organization completed successfully.")
        else:
            logging.info("Operation cancelled.")
    except KeyboardInterrupt:
        logging.info("\nOperation interrupted by user.")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
