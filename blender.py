import bpy
import os
import sys

if __name__ == "__main__":
    sys.path.insert(1, os.path.dirname(__file__))
import path_utils


class GlbToGltf:
    def __NewScene(self) -> None:
        # Create a new scene and clear it of any geometry
        bpy.ops.wm.read_homefile(app_template="")
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()

    def __ConvertFile(self, glb_filepath:str, output_path:str) -> str:
        # Convert a single GLB file to GLTF
        # Sanitizing paths
        glb_filepath = path_utils.SanitizePath(glb_filepath)
        output_path = path_utils.SanitizePath(output_path)

        print(f"Processing: {glb_filepath}")
        self.__NewScene()
        if output_path.endswith(".gltf"):
            # ensure the path exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            gltf_filepath = output_path
        else:
            # Place each GLTF in their own directory to avoid any conflict
            output_path = path_utils.CreateUniquePath(f"{output_path}/{os.path.basename(glb_filepath).replace('.glb', '')}")
            gltf_filepath = f"{output_path}/{os.path.basename(glb_filepath).replace('.glb', '.gltf')}"
        bpy.ops.import_scene.gltf(filepath=glb_filepath)
        bpy.ops.export_scene.gltf(filepath=gltf_filepath, export_format='GLTF_SEPARATE', export_texture_dir='textures')
        print(f"Converted: {gltf_filepath}")
        return gltf_filepath

    def __ConvertDir(self, input_path:str, output_path:str) -> list[str]:
        # Convert multiple GLB files to GLTF
        glb_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames if os.path.splitext(f)[1] == '.glb']
        out = []
        if glb_files is not None and len(glb_files) > 0:
            out = [self.__ConvertFile(glb_file, output_path) for glb_file in glb_files]
            print(f"{len(out)} GLB files converted to GLTF.")
        else:
            print("No GLB file found.")
        return out

    def Convert(self, input_path:str, output_path:str) -> None:
        # Single file
        if os.path.isfile(input_path) and input_path.lower().endswith('.glb'):
            self.__ConvertFile(input_path, output_path)
        # Multiple files
        elif os.path.isdir(input_path) and not output_path.lower().endswith('.gltf'):
            self.__ConvertDir(input_path, output_path)
        else:
            raise SystemExit(f"Input file or path does not exist. {input_path}")

if __name__ == "__main__":
    # The input and ouput arguments must be placed after a double dash
    argv = sys.argv[sys.argv.index("--") + 1:]
    if argv is not None and len(argv) > 1:
        glb_to_gltf = GlbToGltf()
        glb_to_gltf.Convert(argv[0], argv[1])
    else:
        raise SystemExit(f"Usage: blender.exe -b -P {__file__} input output.\nInput can either be a file or a path.")