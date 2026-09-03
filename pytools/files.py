import os

# Change this path to the folder you want to scan, e.g., '/' for the entire disk
scan_path = os.path.expanduser('~')  # your home directory

# Set the minimum file size to consider (in bytes)
min_size_bytes = 50 * 1024 * 1024  # 500 MB

large_files = []

# Walk through directories
for root, dirs, files in os.walk(scan_path):
    for name in files:
        try:
            file_path = os.path.join(root, name)
            size = os.path.getsize(file_path)
            if size >= min_size_bytes:
                large_files.append((size, file_path))
        except (PermissionError, FileNotFoundError):
            # Skip files we can't access
            continue

# Sort files by size, largest first
large_files.sort(reverse=True, key=lambda x: x[0])

# Print results
print(f"Files larger than {min_size_bytes / (1024*1024)} MB:\n")
for size, path in large_files:
    print(f"{size / (1024*1024):.2f} MB - {path}")