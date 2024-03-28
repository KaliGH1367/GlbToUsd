import hou
import os
import sys

if __name__ == "__main__":
    sys.path.insert(1, os.path.dirname(__file__))
import path_utils

class GltfToUsd:
    def __init__(self):
        # Create the node network
        # /obj
        # Import the GLTF mesh and materials
        self.node_gltf_hierarchy = hou.node("/obj").createNode("gltf_hierarchy")
        self.node_gltf_hierarchy.parm("flattenhierarchy").set(1)
        
        # /stage
        # Primitive with asset name
        self.node_stage = hou.node("/stage")
        self.node_primitive = self.node_stage.createNode("primitive")
        self.node_primitive.parm("primkind").set("Component")

        # SOP Create
        self.node_sopcreate = self.node_stage.createNode("sopcreate", "Subcomponents")
        self.node_sopcreate.parm("enable_partitionattribs").set(0)
        self.node_sopcreate.parm("pathprefix").set("/")

        # SOP Create / sopnet / create / Object Merge
        self.node_object_merge = self.node_sopcreate.node("./sopnet/create").createNode("object_merge")
        self.node_object_merge.parm("objpath1").set("/obj/gltf_hierarchy1/geo1")

        # SOP Create / sopnet / create / Output
        self.node_object_merge.createOutputNode("output")

        # Graft stages
        self.node_graftstages =self. node_primitive.createOutputNode("graftstages")
        self.node_graftstages.parm("destpath").set("/")
        self.node_graftstages.setNextInput(self.node_sopcreate)

        # USD ROP
        self.node_usd_rop = self.node_graftstages.createOutputNode("usd_rop")

        self.node_stage.layoutChildren()

    def __ConvertFile(self, input_filepath:str, output_path:str) -> str:
        # Sanitizing paths
        input_filepath = path_utils.SanitizePath(input_filepath)
        output_path = path_utils.SanitizePath(output_path)

        # Convert a single GLTF file to USD
        filename = os.path.basename(input_filepath)
        path = os.path.dirname(input_filepath)
        asset_name = filename.replace(".gltf", "")

        if output_path.endswith(".usd"):
            # ensure the path exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        else:
            # Place each GLTF in their own directory to avoid any conflict
            output_path = path_utils.CreateUniquePath(f"{output_path}/{asset_name}")
            output_path = f"{output_path}/{asset_name}.usd"

        # /obj
        # Import the GLTF mesh and materials
        self.node_gltf_hierarchy.parm("filename").set(input_filepath)
        self.node_gltf_hierarchy.parm("assetfolder").set(path)
        self.node_gltf_hierarchy.parm("buildscene").pressButton()
        
        # /stage
        # Primitive with asset name
        self.node_primitive.setName(asset_name.title())

        # SOP Create - Auto populate materials
        self.node_sopcreate.parm("fillmaterials").pressButton()

        # USD ROP
        self.node_usd_rop.parm("lopoutput").set(output_path)
        self.node_usd_rop.parm("execute").pressButton()

        print(f"Converted: {output_path}")

        return output_path
        
    def __ConvertDir(self, input_path:str, output_path:str) -> list[str]:
        # Convert multiple GLTF files to USD
        gltf_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames if os.path.splitext(f)[1] == '.gltf']
        out = []
        if gltf_files is not None and len(gltf_files) > 0:
            out = [self.__ConvertFile(gltf_file, output_path) for gltf_file in gltf_files]
            print(f"{len(out)} GLTF files converted to USD.")
        else:
            print("No GLTF file found.")
        return out

    def Convert(self, input_path:str, output_path:str) -> None:
        # Single file
        if os.path.isfile(input_path) and input_path.lower().endswith('.gltf'):
            self.__ConvertFile(input_path, output_path)
        # Multiple files
        elif os.path.isdir(input_path):
            self.__ConvertDir(input_path, output_path)
        else:
            raise SystemExit(f"Input file or path does not exist. {input_path}")

if __name__ == "__main__":
    # The input and ouput arguments must be placed after a double dash
    argv = sys.argv[sys.argv.index("--") + 1:]
    if argv is not None and len(argv) > 1:
        gltf_to_usd = GltfToUsd()
        gltf_to_usd.Convert(argv[0], argv[1])
    else:
        raise SystemExit(f"Usage: blender.exe -b -P {__file__} input output.\nInput can either be a file or a path.")