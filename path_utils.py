def SanitizePath(path:str) -> str:
    path = path.replace('\\', '/')
    if path.endswith('/'):
            path = path[:-1]
    return path

def SanitizePaths(paths:list[str]) -> list[str]:
    return [SanitizePath(path) for path in paths]

def CreateUniquePath(path:str) -> str:
    import os
    # Add a suffix if output path already exist
    if os.path.isdir(path):
        suffix = 1
        while os.path.isdir(f"{path}_{suffix:03d}"):
            suffix += 1
        path = f"{path}_{suffix:03d}"
    os.makedirs(path, exist_ok=True)
    return path