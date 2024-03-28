:: Uncomment and update paths as needed

:: Converting a single file:
:: GLB to GLTF
:: "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b -P blender.py -- "C:\Path\To\GLB_files\file.glb" "C:\Path\To\GLTF_files\file.gltf"
:: GLTF to USD
:: "C:\Program Files\Side Effects Software\Houdini 20.0.625\bin\hython3.10.exe" houdini.py -- "C:\Path\To\GLTF_files\file.gltf" "C:\Path\To\USD_files\file.usd"

:: Converting multiple files:
:: GLB to GLTF
"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b -P blender.py -- "C:\Path\To\GLB_files" "C:\Path\To\GLTF_files"
:: GLTF to USD
"C:\Program Files\Side Effects Software\Houdini 20.0.625\bin\hython3.10.exe" houdini.py -- "C:\Path\To\GLTF_files" "C:\Path\To\USD_files"
