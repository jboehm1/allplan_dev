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
    from __BuildingElementStubFiles.TestCubeBuildingElement import TestCubeBuildingElement as BuildingElement
except ImportError:
    from BuildingElement import BuildingElement

DEBUG_FILE = os.path.expanduser("~/Desktop/PythonPart_Debug.txt")

def log_debug(msg):
    with open(DEBUG_FILE, "a") as f:
        f.write(msg + "\n")

def check_allplan_version(build_ele, version):
    log_debug("check_allplan_version called")
    return True

def create_element(build_ele: BuildingElement, 
                  doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Crée un array de cubes avec paramètres - COPIE EXACTE de l'exemple GitHub"""
    log_debug("=== create_element START ===")
    try:
        # Récupère les paramètres
        cube_size = build_ele.CubeSize.value
        repeat_count = int(build_ele.RepeatCount.value)
        distance = build_ele.Distance.value
        
        log_debug(f"CubeSize: {cube_size}")
        log_debug(f"RepeatCount: {repeat_count}")
        log_debug(f"Distance: {distance}")
        
        # PythonPartUtil avec CommonProperties (IMPORTANT : pas de .value !)
        common_props = AllplanBaseElements.CommonProperties()
        python_part_util = PythonPartUtil(common_props)
        log_debug("PythonPartUtil created OK")
        
        # Crée la liste des éléments
        model_ele_list = ModelEleList(common_props)
        
        # Crée un array de cubes
        for i in range(repeat_count):
            log_debug(f"Creating cube {i+1}/{repeat_count}")
            
            # Positionne chaque cube selon l'index
            offset_x = i * (cube_size + distance)
            offset_y = 0
            offset_z = 0
            
            # Point de départ du cuboid
            p1 = AllplanGeo.Point3D(offset_x, offset_y, offset_z)
            
            # Signature CORRECTE de CreateCuboid : (double length, double width, double height)
            # OU : (Point3D p1, Point3D p2)
            p2 = p1 + AllplanGeo.Point3D(cube_size, cube_size, cube_size)
            
            cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(p1, p2)
            log_debug(f"Cuboid {i+1} created OK")
            
            # Ajoute à la liste
            model_ele_list.append_geometry_3d(cuboid_geo)
        
        log_debug(f"Total cubes added: {repeat_count}")
        
        # Ajoute via PythonPartUtil
        python_part_util.add_pythonpart_view_2d3d(model_ele_list)
        log_debug("View added OK")
        
        # Crée et retourne (COPIE EXACTE de l'exemple ligne 91)
        result = CreateElementResult(python_part_util.create_pythonpart(build_ele))
        log_debug("=== create_element END SUCCESS ===")
        return result
        
    except Exception as e:
        log_debug(f"ERROR: {str(e)}")
        log_debug(traceback.format_exc())
        log_debug("=== create_element END ERROR ===")
        return CreateElementResult()
