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
    """Creates solar module array with support plate"""
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
        log_debug(f"Module: {module_width}x{module_height}x{module_thickness}")
        log_debug(f"Gaps: row={row_gap}, col={col_gap}")
        
        # Calculate plate dimensions
        plate_width = num_cols * module_width + (num_cols - 1) * col_gap
        plate_height = num_rows * module_height + (num_rows - 1) * row_gap
        
        log_debug(f"Plate size: {plate_width}x{plate_height}")
        
        # Create CommonProperties
        common_props = AllplanBaseElements.CommonProperties()
        python_part_util = PythonPartUtil(common_props)
        model_ele_list = ModelEleList(common_props)
        
        # Create support plate
        plate_p1 = AllplanGeo.Point3D(0, 0, plate_offset)
        plate_p2 = AllplanGeo.Point3D(plate_width, plate_height, plate_offset + plate_thickness)
        
        log_debug("Creating support plate...")
        plate = AllplanGeo.Polyhedron3D.CreateCuboid(plate_p1, plate_p2)
        model_ele_list.append_geometry_3d(plate)
        log_debug("Support plate created OK")
        
        # Create solar modules array
        log_debug(f"Creating {num_rows}x{num_cols} modules...")
        
        module_z = plate_offset + plate_thickness  # Start above plate
        
        for row in range(num_rows):
            for col in range(num_cols):
                # Calculate position
                x = col * (module_width + col_gap)
                y = row * (module_height + row_gap)
                z = module_z
                
                # Module corners
                module_p1 = AllplanGeo.Point3D(x, y, z)
                module_p2 = AllplanGeo.Point3D(
                    x + module_width,
                    y + module_height,
                    z + module_thickness
                )
                
                # Create module
                module = AllplanGeo.Polyhedron3D.CreateCuboid(module_p1, module_p2)
                model_ele_list.append_geometry_3d(module)
                
                log_debug(f"Module [{row},{col}] created at ({x}, {y}, {z})")
        
        log_debug(f"Total modules created: {num_rows * num_cols}")
        
        # Add to view
        python_part_util.add_pythonpart_view_2d3d(model_ele_list)
        log_debug("View added OK")
        
        # Return result
        result = CreateElementResult(python_part_util.create_pythonpart(build_ele))
        log_debug("=== create_element END SUCCESS ===")
        return result
        
    except Exception as e:
        log_debug(f"ERROR: {str(e)}")
        log_debug(traceback.format_exc())
        log_debug("=== create_element END ERROR ===")
        return CreateElementResult()
