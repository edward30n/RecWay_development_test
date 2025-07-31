"""
Simple script to check for non-ASCII characters in files
"""

import os
import sys

def check_file_for_non_ascii(file_path):
    """Check if a file contains non-ASCII characters"""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # Try to decode as ASCII (which will fail on non-ASCII chars)
        try:
            content.decode('ascii')
            return False, None  # No non-ASCII chars found
        except UnicodeDecodeError as e:
            # Found non-ASCII chars
            position = e.start
            problematic_bytes = content[position:position+10]  # Show up to 10 bytes
            
            # Try to locate the line number
            content_before = content[:position]
            line_count = content_before.count(b'\n') + 1
            
            return True, {
                'position': position,
                'bytes': problematic_bytes,
                'line': line_count,
                'message': str(e)
            }
    except Exception as e:
        return True, {'error': f'Error reading file: {str(e)}'}

def scan_directory(directory, extensions=None):
    """Scan a directory for files with non-ASCII characters"""
    problems = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            # Check only files with specified extensions
            if extensions and not any(file.endswith(ext) for ext in extensions):
                continue
                
            file_path = os.path.join(root, file)
            has_problem, details = check_file_for_non_ascii(file_path)
            
            if has_problem:
                problems.append({
                    'file': file_path,
                    'details': details
                })
                
    return problems

# Main execution
if __name__ == "__main__":
    # Directory to scan (default to current directory)
    directory = "."  
    
    # Extensions to check
    extensions = ['.py', '.sql']
    
    print(f"Scanning directory: {directory}")
    problems = scan_directory(directory, extensions)
    
    if problems:
        print(f"Found {len(problems)} files with non-ASCII characters:")
        for problem in problems:
            print(f"\n{problem['file']}:")
            details = problem['details']
            
            if 'error' in details:
                print(f"  Error: {details['error']}")
            else:
                print(f"  Line {details['line']}, Position {details['position']}")
                print(f"  Bytes: {details['bytes']}")
                print(f"  Message: {details['message']}")
    else:
        print("No files with non-ASCII characters found.")
