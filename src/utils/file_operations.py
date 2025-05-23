"""
File Operations Utility Module
Advanced file and folder operations
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict
import threading

class FileOperations:
    def __init__(self):
        self.operation_in_progress = False
        
    def copy_files(self, source_paths: List[Path], destination: Path, 
                   progress_callback=None) -> bool:
        """Copy multiple files/folders with progress tracking"""
        try:
            self.operation_in_progress = True
            total_files = sum(1 for path in source_paths for _ in self._count_files(path))
            processed = 0
            
            for source_path in source_paths:
                dest_path = destination / source_path.name
                
                if source_path.is_file():
                    shutil.copy2(source_path, dest_path)
                    processed += 1
                    if progress_callback:
                        progress_callback(processed, total_files)
                elif source_path.is_dir():
                    shutil.copytree(source_path, dest_path)
                    processed += len(list(self._count_files(source_path)))
                    if progress_callback:
                        progress_callback(processed, total_files)
                        
            return True
        except Exception as e:
            print(f"Copy error: {e}")
            return False
        finally:
            self.operation_in_progress = False
            
    def move_files(self, source_paths: List[Path], destination: Path,
                   progress_callback=None) -> bool:
        """Move multiple files/folders"""
        try:
            self.operation_in_progress = True
            total_files = len(source_paths)
            
            for i, source_path in enumerate(source_paths):
                dest_path = destination / source_path.name
                shutil.move(source_path, dest_path)
                
                if progress_callback:
                    progress_callback(i + 1, total_files)
                    
            return True
        except Exception as e:
            print(f"Move error: {e}")
            return False
        finally:
            self.operation_in_progress = False
            
    def delete_files(self, file_paths: List[Path], progress_callback=None) -> bool:
        """Delete multiple files/folders"""
        try:
            self.operation_in_progress = True
            total_files = len(file_paths)
            
            for i, file_path in enumerate(file_paths):
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    
                if progress_callback:
                    progress_callback(i + 1, total_files)
                    
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False
        finally:
            self.operation_in_progress = False
            
    def calculate_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory"""
        total_size = 0
        try:
            for path in directory.rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except PermissionError:
            pass
        return total_size
        
    def find_duplicate_files(self, directory: Path) -> Dict[str, List[Path]]:
        """Find duplicate files based on content hash"""
        file_hashes = {}
        duplicates = {}
        
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    file_hash = self._calculate_file_hash(file_path)
                    if file_hash:
                        if file_hash in file_hashes:
                            if file_hash not in duplicates:
                                duplicates[file_hash] = [file_hashes[file_hash]]
                            duplicates[file_hash].append(file_path)
                        else:
                            file_hashes[file_hash] = file_path
        except Exception as e:
            print(f"Error finding duplicates: {e}")
            
        return duplicates
        
    def compress_folder(self, folder_path: Path, output_path: Path) -> bool:
        """Compress folder to zip file"""
        try:
            shutil.make_archive(str(output_path.with_suffix('')), 'zip', folder_path)
            return True
        except Exception as e:
            print(f"Compression error: {e}")
            return False
            
    def extract_archive(self, archive_path: Path, destination: Path) -> bool:
        """Extract archive file"""
        try:
            shutil.unpack_archive(archive_path, destination)
            return True
        except Exception as e:
            print(f"Extraction error: {e}")
            return False
            
    def _count_files(self, path: Path):
        """Count files in directory recursively"""
        if path.is_file():
            yield path
        elif path.is_dir():
            try:
                for item in path.rglob('*'):
                    if item.is_file():
                        yield item
            except PermissionError:
                pass
                
    def _calculate_file_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate MD5 hash of file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None