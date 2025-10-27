"""
Solar Carport Array - External Automation Script
============================================================================
Author: JB
Date: 2025-10-25
Description: External Python script that connects to Allplan API and
             generates solar PV arrays from JSON configuration
Requirements: Allplan must be running with an active document
============================================================================
"""

import sys
import json
import os
from datetime import datetime

# Add Allplan Python API to path
ALLPLAN_API_PATH = "C:/Program Files/Allplan/Allplan 2026/Etc/PythonPartsFramework"
if ALLPLAN_API_PATH not in sys.path:
    sys.path.append(ALLPLAN_API_PATH)

try:
    import NemAll_Python_Geometry as AllplanGeo
    import NemAll_Python_BaseElements as AllplanBaseElements
    import NemAll_Python_BasisElements as AllplanBasisElements
    import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
except ImportError as e:
    print(f"ERROR: Cannot import Allplan Python API")
    print(f"Details: {e}")
    print(f"Make sure:")
    print(f"  1. Allplan is installed")
    print(f"  2. API path is correct: {ALLPLAN_API_PATH}")
    sys.exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

LOG_FILE = "generation_log.txt"
DEFAULT_CONFIG = "solar_config.json"

# ============================================================================
# LOGGING UTILITIES
# ============================================================================

def log(msg, level="INFO"):
    """Write message to console and log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {msg}"
    print(log_msg)
    
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")

def log_section(title):
    """Log a section header"""
    separator = "=" * 80
    log(separator)
    log(f"  {title}")
    log(separator)

# ============================================================================
# CONFIGURATION LOADING
# ============================================================================

def load_config(config_file):
    """
    Load configuration from JSON file
    
    Args:
        config_file (str): Path to JSON configuration file
    
    Returns:
        dict: Configuration dictionary
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    log(f"Loading configuration from: {config_file}")
    
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    log(f"Configuration loaded successfully")
    log(f"Version: {config.get('version', 'unknown')}")
    log(f"Projects found: {len(config.get('projects', []))}")
    
    return config

def validate_config(config):
    """
    Validate configuration structure and values
    
    Args:
        config (dict): Configuration dictionary
    
    Returns:
        bool: True if valid, raises exception otherwise
    """
    log("Validating configuration...")
    
    if 'projects' not in config:
        raise ValueError("Config must contain 'projects' key")
    
    for idx, project in enumerate(config['projects']):
        log(f"Validating project {idx + 1}: {project.get('name', 'unnamed')}")
        
        # Check required keys
        required = ['name', 'modules', 'gaps', 'plate', 'roof', 'placement']
        for key in required:
            if key not in project:
                raise ValueError(f"Project '{project.get('name')}' missing required key: {key}")
        
        # Validate ranges
        modules = project['modules']
        if not (1 <= modules['rows'] <= 20):
            raise ValueError(f"Project '{project['name']}': rows must be 1-20")
        if not (1 <= modules['cols'] <= 20):
            raise ValueError(f"Project '{project['name']}': cols must be 1-20")
    
    log("Configuration validation passed")
    return True

# ============================================================================
# GEOMETRY GENERATION
# ============================================================================

def generate_solar_array(params):
    """
    Generate solar array geometry from parameters
    
    Args:
        params (dict): Project parameters
    
    Returns:
        list: List of ModelElement3D objects
    """
    log(f"Generating solar array: {params['name']}")
    
    elements = []
    
    # Extract parameters
    rows = params['modules']['rows']
    cols = params['modules']['cols']
    module_w = params['modules']['width']
    module_h = params['modules']['height']
    module_t = params['modules']['thickness']
    row_gap = params['gaps']['row']
    col_gap = params['gaps']['col']
    plate_t = params['plate']['thickness']
    plate_off = params['plate']['offset']
    
    colors = params.get('colors', {'plate': 7, 'frame': 4, 'pv': 21})
    
    FRAME_THICKNESS = 30  # mm
    
    log(f"  Modules: {rows}x{cols} ({module_w}x{module_h}x{module_t} mm)")
    log(f"  Gaps: row={row_gap} mm, col={col_gap} mm")
    
    # === SUPPORT PLATE (GREY) ===
    plate_width = cols * module_w + (cols - 1) * col_gap
    plate_height = rows * module_h + (rows - 1) * row_gap
    
    plate_props = AllplanBaseElements.CommonProperties()
    plate_props.Color = colors['plate']
    
    plate_p1 = AllplanGeo.Point3D(0, 0, plate_off)
    plate_p2 = AllplanGeo.Point3D(plate_width, plate_height, plate_off + plate_t)
    plate = AllplanGeo.Polyhedron3D.CreateCuboid(plate_p1, plate_p2)
    
    elements.append(AllplanBasisElements.ModelElement3D(plate_props, plate))
    log(f"  Created support plate: {plate_width}x{plate_height}x{plate_t} mm")
    
    # === SOLAR MODULES ===
    module_z = plate_off + plate_t
    module_count = 0
    
    for row in range(rows):
        for col in range(cols):
            x = col * (module_w + col_gap)
            y = row * (module_h + row_gap)
            z = module_z
            
            # FRAME
            frame_props = AllplanBaseElements.CommonProperties()
            frame_props.Color = colors['frame']
            
            frame_p1 = AllplanGeo.Point3D(x, y, z)
            frame_p2 = AllplanGeo.Point3D(x + module_w, y + module_h, z + FRAME_THICKNESS)
            frame = AllplanGeo.Polyhedron3D.CreateCuboid(frame_p1, frame_p2)
            
            elements.append(AllplanBasisElements.ModelElement3D(frame_props, frame))
            
            # PV LAYER
            pv_props = AllplanBaseElements.CommonProperties()
            pv_props.Color = colors['pv']
            
            inset = FRAME_THICKNESS / 2
            pv_p1 = AllplanGeo.Point3D(x + inset, y + inset, z + FRAME_THICKNESS)
            pv_p2 = AllplanGeo.Point3D(
                x + module_w - inset,
                y + module_h - inset,
                z + FRAME_THICKNESS + (module_t - FRAME_THICKNESS)
            )
            pv_layer = AllplanGeo.Polyhedron3D.CreateCuboid(pv_p1, pv_p2)
            
            elements.append(AllplanBasisElements.ModelElement3D(pv_props, pv_layer))
            module_count += 1
    
    log(f"  Created {module_count} solar modules")
    log(f"  Total elements: {len(elements)}")
    
    return elements

# ============================================================================
# ALLPLAN INTEGRATION
# ============================================================================

def connect_to_allplan():
    """
    Connect to active Allplan document
    
    Returns:
        DocumentAdapter: Active document or None if connection fails
    """
    log("Connecting to Allplan...")
    
    try:
        doc = AllplanElementAdapter.DocumentAdapter.GetActiveDocument()
        
        if not doc:
            log("ERROR: No active Allplan document found", "ERROR")
            log("Please open an Allplan project and document first", "ERROR")
            return None
        
        log(f"Connected to document: {doc.GetDocumentName()}")
        return doc
        
    except Exception as e:
        log(f"ERROR connecting to Allplan: {str(e)}", "ERROR")
        return None

def insert_into_allplan(doc, elements, placement):
    """
    Insert elements into Allplan document
    
    Args:
        doc: DocumentAdapter instance
        elements (list): List of ModelElement3D
        placement (dict): Placement coordinates {'x', 'y', 'z'}
    
    Returns:
        bool: True if successful, False otherwise
    """
    log(f"Inserting {len(elements)} elements at ({placement['x']}, {placement['y']}, {placement['z']})")
    
    try:
        # Create transformation matrix for placement
        transform = AllplanGeo.Matrix3D()
        transform.SetTranslation(AllplanGeo.Vector3D(
            placement['x'],
            placement['y'],
            placement['z']
        ))
        
        # Insert elements
        AllplanBaseElements.CreateElements(doc, transform, elements, [], None)
        
        log("Elements inserted successfully")
        return True
        
    except Exception as e:
        log(f"ERROR inserting elements: {str(e)}", "ERROR")
        return False

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    log_section("SOLAR CARPORT ARRAY - EXTERNAL AUTOMATION")
    
    # Load configuration
    config_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG
    
    try:
        config = load_config(config_file)
        validate_config(config)
    except Exception as e:
        log(f"Configuration error: {str(e)}", "ERROR")
        return 1
    
    # Connect to Allplan
    doc = connect_to_allplan()
    if not doc:
        return 1
    
    # Process each project
    projects = [p for p in config['projects'] if p.get('enabled', True)]
    log(f"Processing {len(projects)} enabled projects")
    
    success_count = 0
    fail_count = 0
    
    for idx, project in enumerate(projects, 1):
        log_section(f"PROJECT {idx}/{len(projects)}: {project['name']}")
        
        try:
            # Generate geometry
            elements = generate_solar_array(project)
            
            # Insert into Allplan
            if insert_into_allplan(doc, elements, project['placement']):
                log(f"PROJECT COMPLETED: {project['name']}", "SUCCESS")
                success_count += 1
            else:
                log(f"PROJECT FAILED: {project['name']} insertion failed", "ERROR")
                fail_count += 1
                
        except Exception as e:
            log(f"PROJECT FAILED: {project['name']} - {str(e)}", "ERROR")
            fail_count += 1
    
    # Summary
    log_section("GENERATION SUMMARY")
    log(f"Total projects: {len(projects)}")
    log(f"Successful: {success_count}")
    log(f"Failed: {fail_count}")
    
    if fail_count == 0:
        log("All projects completed successfully!", "SUCCESS")
        return 0
    else:
        log(f"{fail_count} project(s) failed", "WARNING")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        log("Execution interrupted by user", "WARNING")
        sys.exit(130)
    except Exception as e:
        log(f"Unexpected error: {str(e)}", "ERROR")
        sys.exit(1)
