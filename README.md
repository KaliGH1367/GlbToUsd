# GlbToUsd
GLB to GLTF to USD batch file converter using Blender and Houdini

## Requirements
Blender is required to use the GLB to GLTF conversion (tested with Blender 4.0)
Houdini is required to use the GLTF to USD conversion (tested with Houdini 20.0)

## For Windows users: glb_to_usd.bat
Edit this file to uncomment and update paths as needed

## Converting a single file
GLB to GLTF
```
"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b -P blender.py -- "C:\Path\To\GLB_files\file.glb" "C:\Path\To\GLTF_files\file.gltf"
```
GLTF to USD
```
"C:\Program Files\Side Effects Software\Houdini 20.0.625\bin\hython3.10.exe" houdini.py -- "C:\Path\To\GLTF_files\file.gltf" "C:\Path\To\USD_files\file.usd"
```

## Converting multiple files
GLB to GLTF
```
"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b -P blender.py -- "C:\Path\To\GLB_files" "C:\Path\To\GLTF_files"
```
GLTF to USD
```
"C:\Program Files\Side Effects Software\Houdini 20.0.625\bin\hython3.10.exe" houdini.py -- "C:\Path\To\GLTF_files" "C:\Path\To\USD_files"
```