import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import math
import os
import traceback

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from TypeCollections.ModelEleList import ModelEleList

try:
    from __BuildingElementStubFiles.SolarCarportRoofBuildingElement import SolarCarportRoofBuildingElement as BuildingElement
except ImportError:
    from BuildingElement import BuildingElement

DEBUG_FILE = os.path.expanduser("~/Desktop/SolarCarport_Debug.txt")

def log_debug(msg):
    with open(DEBUG_FILE, "a") as f:
        f.write(msg + "\n")

def check_allplan_version(build_ele, version):
    log_debug("check_allplan_version called")
    return True

def create_element(build_ele: BuildingElement, 
                  doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Creates solar carport roof with two angled sides"""
    log_debug("=== create_element START ===")
    try:
        # Get parameters
        num_rows = int(build_ele.NumRows.value)
        num_cols = int(build_ele.NumCols.value)
        
        module_width = build_ele.ModuleWidth.value
        module_height = build_ele.ModuleHeight.value
        module_thickness = build_ele.ModuleThickness.value
        row_gap = build_ele.RowGap.value
        col_gap = build_ele.ColGap.value
        
        plate_thickness = build_ele.PlateThickness.value
        plate_offset = build_ele.PlateOffset.value
        
        create_second_side = build_ele.CreateSecondSide.value
        roof_angle_degrees = build_ele.RoofAngle.value
        ridge_height = build_ele.RidgeHeight.value
        
        log_debug(f"Rows: {num_rows}, Cols: {num_cols}")
        log_debug(f"CreateSecondSide: {create_second_side}")
        log_debug(f"RoofAngle: {roof_angle_degrees}°")
        
        # Calculate dimensions
        plate_width = num_cols * module_width + (num_cols - 1) * col_gap
        plate_height = num_rows * module_height + (num_rows - 1) * row_gap
        
        # PythonPartUtil
        common_props = AllplanBaseElements.CommonProperties()
        python_part_util = PythonPartUtil(common_props)
        
        # --- FIRST SIDE (NO ROTATION) ---
        log_debug("Creating first roof side...")
        create_roof_side(
            python_part_util,
            num_rows, num_cols,
            module_width, module_height, module_thickness,
            row_gap, col_gap,
            plate_thickness, plate_offset,
            origin=AllplanGeo.Point3D(0, 0, 0),
            rotation_matrix=None  # No rotation
        )
        log_debug("First roof side created OK")
        
        # --- SECOND SIDE (WITH ROTATION) ---
        if create_second_side:
            log_debug("Creating second roof side...")
            
            # Convert angle to radians
            angle_rad = math.radians(roof_angle_degrees)
            
            # Calculate offset for second side
            # The second side is translated at the ridge
            offset_y = plate_height + ridge_height * math.tan(angle_rad)
            
            # Create rotation matrix [226]
            rotation_matrix = AllplanGeo.Matrix3D()
            
            # Rotate around Y-axis at the ridge line [226]
            rotation_matrix.SetRotation(AllplanGeo.AxisPlacement3D(
                AllplanGeo.Point3D(0, plate_height, plate_offset + plate_thickness),
                AllplanGeo.Vector3D(0, 1, 0),  # Y-axis
                AllplanGeo.Vector3D(1, 0, 0)
            ))
            
            # Apply rotation
            rotation_matrix.RotateX(angle_rad * 2)  # Double angle for symmetric roof
            
            # Set translation to position at ridge
            rotation_matrix.SetTranslation(AllplanGeo.Vector3D(
                0, 
                plate_height, 
                plate_offset + plate_thickness + ridge_height
            ))
            
            create_roof_side(
                python_part_util,
                num_rows, num_cols,
                module_width, module_height, module_thickness,
                row_gap, col_gap,
                plate_thickness, plate_offset,
                origin=AllplanGeo.Point3D(0, 0, 0),
                rotation_matrix=rotation_matrix
            )
            log_debug("Second roof side created OK")
        
        # Return result
        result = CreateElementResult(python_part_util.create_pythonpart(build_ele))
        log_debug("=== create_element END SUCCESS ===")
        return result
        
    except Exception as e:
        log_debug(f"ERROR: {str(e)}")
        log_debug(traceback.format_exc())
        return CreateElementResult()

def create_roof_side(python_part_util, num_rows, num_cols,
                     module_width, module_height, module_thickness,
                     row_gap, col_gap,
                     plate_thickness, plate_offset,
                     origin, rotation_matrix):
    """Helper function to create one roof side (with optional rotation)"""
    
    frame_thickness = 30  # mm
    
    # === SUPPORT PLATE ===
    plate_props = AllplanBaseElements.CommonProperties()
    plate_props.Color = 7  # Grey
    plate_list = ModelEleList(plate_props)
    
    plate_width = num_cols * module_width + (num_cols - 1) * col_gap
    plate_height = num_rows * module_height + (num_rows - 1) * row_gap
    
    plate_p1 = origin + AllplanGeo.Point3D(0, 0, plate_offset)
    plate_p2 = origin + AllplanGeo.Point3D(plate_width, plate_height, 
                                          plate_offset + plate_thickness)
    plate = AllplanGeo.Polyhedron3D.CreateCuboid(plate_p1, plate_p2)
    
    if rotation_matrix:
        plate = plate.Transform(rotation_matrix)
    
    plate_list.append_geometry_3d(plate)
    python_part_util.add_pythonpart_view_2d3d(plate_list)
    
    # === SOLAR MODULES ===
    module_z = plate_offset + plate_thickness
    
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * (module_width + col_gap)
            y = row * (module_height + row_gap)
            z = module_z
            
            # BLUE FRAME
            frame_props = AllplanBaseElements.CommonProperties()
            frame_props.Color = 4  # Blue
            frame_list = ModelEleList(frame_props)
            
            frame_p1 = origin + AllplanGeo.Point3D(x, y, z)
            frame_p2 = origin + AllplanGeo.Point3D(x + module_width, y + module_height,
                                                   z + frame_thickness)
            frame = AllplanGeo.Polyhedron3D.CreateCuboid(frame_p1, frame_p2)
            
            if rotation_matrix:
                frame = frame.Transform(rotation_matrix)
            
            frame_list.append_geometry_3d(frame)
            python_part_util.add_pythonpart_view_2d3d(frame_list)
            
            # DARK BLUE PV LAYER
            pv_props = AllplanBaseElements.CommonProperties()
            pv_props.Color = 21  # Dark blue
            pv_list = ModelEleList(pv_props)
            
            inset = frame_thickness / 2
            pv_p1 = origin + AllplanGeo.Point3D(x + inset, y + inset, 
                                               z + frame_thickness)
            pv_p2 = origin + AllplanGeo.Point3D(x + module_width - inset, 
                                               y + module_height - inset,
                                               z + frame_thickness + 
                                               (module_thickness - frame_thickness))
            pv_layer = AllplanGeo.Polyhedron3D.CreateCuboid(pv_p1, pv_p2)
            
            if rotation_matrix:
                pv_layer = pv_layer.Transform(rotation_matrix)
            
            pv_list.append_geometry_3d(pv_layer)
            python_part_util.add_pythonpart_view_2d3d(pv_list)
