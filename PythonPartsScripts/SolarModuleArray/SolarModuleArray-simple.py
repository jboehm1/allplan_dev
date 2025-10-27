import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import os
import traceback

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from TypeCollections.ModelEleList import ModelEleList

try:
    from __BuildingElementStubFiles.SolarModuleArrayBuildingElement import SolarModuleArrayBuildingElement as BuildingElement
except ImportError:
    from BuildingElement import BuildingElement

DEBUG_FILE = os.path.expanduser("~/Desktop/SolarArray_Debug.txt")

def log_debug(msg):
    with open(DEBUG_FILE, "a") as f:
        f.write(msg + "\n")

def check_allplan_version(build_ele, version):
    log_debug("check_allplan_version called")
    return True

def create_element(build_ele: BuildingElement, 
                  doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Creates solar module array with colored components based on GitHub example"""
    log_debug("=== create_element START ===")
    try:
        # Array parameters
        num_rows = int(build_ele.NumRows.value)
        num_cols = int(build_ele.NumCols.value)
        
        # Module parameters
        module_width = build_ele.ModuleWidth.value
        module_height = build_ele.ModuleHeight.value
        module_thickness = build_ele.ModuleThickness.value
        row_gap = build_ele.RowGap.value
        col_gap = build_ele.ColGap.value
        
        # Plate parameters
        plate_thickness = build_ele.PlateThickness.value
        plate_offset = build_ele.PlateOffset.value
        
        log_debug(f"Rows: {num_rows}, Cols: {num_cols}")
        
        # Calculate dimensions
        plate_width = num_cols * module_width + (num_cols - 1) * col_gap
        plate_height = num_rows * module_height + (num_rows - 1) * row_gap
        
        # Frame thickness (around each module)
        frame_thickness = 30  # mm
        
        # PythonPartUtil
        common_props = AllplanBaseElements.CommonProperties()
        python_part_util = PythonPartUtil(common_props)
        
        # === 1. CREATE SUPPORT PLATE (GREY) ===
        log_debug("Creating grey support plate...")
        plate_props = AllplanBaseElements.CommonProperties()
        plate_props.Color = 7  # Grey color (Allplan color ID)
        
        plate_list = ModelEleList(plate_props)
        
        plate_p1 = AllplanGeo.Point3D(0, 0, plate_offset)
        plate_p2 = AllplanGeo.Point3D(plate_width, plate_height, plate_offset + plate_thickness)
        plate = AllplanGeo.Polyhedron3D.CreateCuboid(plate_p1, plate_p2)
        plate_list.append_geometry_3d(plate)
        
        python_part_util.add_pythonpart_view_2d3d(plate_list)
        log_debug("Support plate created OK")
        
        # === 2. CREATE SOLAR MODULES WITH FRAMES ===
        module_z = plate_offset + plate_thickness
        
        for row in range(num_rows):
            for col in range(num_cols):
                x = col * (module_width + col_gap)
                y = row * (module_height + row_gap)
                z = module_z
                
                log_debug(f"Creating module [{row},{col}]...")
                
                # --- BLUE FRAME (around module) ---
                frame_props = AllplanBaseElements.CommonProperties()
                frame_props.Color = 4  # Blue color for frame
                frame_list = ModelEleList(frame_props)
                
                # Frame outer dimensions
                frame_p1 = AllplanGeo.Point3D(x, y, z)
                frame_p2 = AllplanGeo.Point3D(
                    x + module_width,
                    y + module_height,
                    z + frame_thickness
                )
                frame = AllplanGeo.Polyhedron3D.CreateCuboid(frame_p1, frame_p2)
                frame_list.append_geometry_3d(frame)
                python_part_util.add_pythonpart_view_2d3d(frame_list)
                
                # --- BLUE PV LAYER (solar cells) ---
                pv_props = AllplanBaseElements.CommonProperties()
                pv_props.Color = 21  # Dark blue for PV cells
                pv_list = ModelEleList(pv_props)
                
                # PV layer sits above frame, slightly inset
                inset = frame_thickness / 2
                pv_p1 = AllplanGeo.Point3D(
                    x + inset,
                    y + inset,
                    z + frame_thickness
                )
                pv_p2 = AllplanGeo.Point3D(
                    x + module_width - inset,
                    y + module_height - inset,
                    z + frame_thickness + (module_thickness - frame_thickness)
                )
                pv_layer = AllplanGeo.Polyhedron3D.CreateCuboid(pv_p1, pv_p2)
                pv_list.append_geometry_3d(pv_layer)
                python_part_util.add_pythonpart_view_2d3d(pv_list)
                
                log_debug(f"Module [{row},{col}] created with frame and PV layer")
        
        log_debug(f"Total modules: {num_rows * num_cols}")
        
        # Return result
        result = CreateElementResult(python_part_util.create_pythonpart(build_ele))
        log_debug("=== create_element END SUCCESS ===")
        return result
        
    except Exception as e:
        log_debug(f"ERROR: {str(e)}")
        log_debug(traceback.format_exc())
        log_debug("=== create_element END ERROR ===")
        return CreateElementResult()
