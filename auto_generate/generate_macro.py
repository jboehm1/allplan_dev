"""
Solar Carport Array - Allplan Macro Generator
Read JSON config and generate solar arrays in Allplan
"""

import json
import sys
from datetime import datetime

# Allplan Python API - available when running as macro
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

# Get config file from command line argument
config_file = sys.argv[1] if len(sys.argv) > 1 else "solar_config.json"

print("\n" + "=" * 50)
print("  Solar Carport Array Generator")
print("=" * 50 + "\n")

print(f"Config file: {config_file}\n")

try:
    # Load configuration from JSON
    with open(config_file) as f:
        config = json.load(f)
    
    # Get active Allplan document
    doc = AllplanElementAdapter.DocumentAdapter.GetActiveDocument()
    if not doc:
        print("ERROR: No active Allplan document!")
        print("Please open Allplan with an active document first.\n")
        sys.exit(1)
    
    print(f"Connected to: {doc.GetDocumentName()}\n")
    
    # Process each project in configuration
    total_projects = len(config.get('projects', []))
    print(f"Found {total_projects} project(s)\n")
    
    for project_idx, project in enumerate(config.get('projects', []), 1):
        # Skip disabled projects
        if not project.get('enabled', True):
            print(f"[{project_idx}] SKIPPED: {project['name']} (disabled)\n")
            continue
        
        try:
            print(f"[{project_idx}] Generating: {project['name']}")
            
            # Extract parameters from JSON
            rows = project['modules']['rows']
            cols = project['modules']['cols']
            module_w = project['modules']['width']
            module_h = project['modules']['height']
            module_t = project['modules']['thickness']
            row_gap = project['gaps']['row']
            col_gap = project['gaps']['col']
            plate_t = project['plate']['thickness']
            plate_off = project['plate']['offset']
            colors = project.get('colors', {'plate': 7, 'frame': 4, 'pv': 21})
            
            print(f"      Config: {rows}x{cols} modules, {plate_t}mm plate")
            
            elements = []
            FRAME_THICKNESS = 30  # mm
            
            # === CREATE SUPPORT PLATE (GREY) ===
            plate_width = cols * module_w + (cols - 1) * col_gap
            plate_height = rows * module_h + (rows - 1) * row_gap
            
            plate_props = AllplanBaseElements.CommonProperties()
            plate_props.Color = colors['plate']  # Grey
            
            plate = AllplanGeo.Polyhedron3D.CreateCuboid(
                AllplanGeo.Point3D(0, 0, plate_off),
                AllplanGeo.Point3D(plate_width, plate_height, plate_off + plate_t)
            )
            elements.append(AllplanBasisElements.ModelElement3D(plate_props, plate))
            
            print(f"      + Support plate: {plate_width}x{plate_height}x{plate_t} mm")
            
            # === CREATE SOLAR MODULES ===
            module_count = 0
            for row in range(rows):
                for col in range(cols):
                    x = col * (module_w + col_gap)
                    y = row * (module_h + row_gap)
                    z = plate_off + plate_t
                    
                    # FRAME (BLUE)
                    frame_props = AllplanBaseElements.CommonProperties()
                    frame_props.Color = colors['frame']  # Blue
                    
                    frame = AllplanGeo.Polyhedron3D.CreateCuboid(
                        AllplanGeo.Point3D(x, y, z),
                        AllplanGeo.Point3D(x + module_w, y + module_h, z + FRAME_THICKNESS)
                    )
                    elements.append(AllplanBasisElements.ModelElement3D(frame_props, frame))
                    
                    # PV LAYER (DARK BLUE)
                    pv_props = AllplanBaseElements.CommonProperties()
                    pv_props.Color = colors['pv']  # Dark Blue
                    
                    inset = FRAME_THICKNESS / 2
                    pv = AllplanGeo.Polyhedron3D.CreateCuboid(
                        AllplanGeo.Point3D(x + inset, y + inset, z + FRAME_THICKNESS),
                        AllplanGeo.Point3D(
                            x + module_w - inset,
                            y + module_h - inset,
                            z + FRAME_THICKNESS + (module_t - FRAME_THICKNESS)
                        )
                    )
                    elements.append(AllplanBasisElements.ModelElement3D(pv_props, pv))
                    
                    module_count += 1
            
            print(f"      + {module_count} solar modules")
            print(f"      + Total elements: {len(elements)}")
            
            # === INSERT INTO DOCUMENT ===
            placement = project['placement']
            transform = AllplanGeo.Matrix3D()
            transform.SetTranslation(AllplanGeo.Vector3D(
                placement['x'],
                placement['y'],
                placement['z']
            ))
            
            AllplanBaseElements.CreateElements(doc, transform, elements, [], None)
            
            print(f"      ✓ SUCCESS\n")
            
        except Exception as e:
            print(f"      ✗ ERROR: {str(e)}\n")
            import traceback
            traceback.print_exc()
            print()
    
    print("=" * 50)
    print("  Generation Complete!")
    print("=" * 50 + "\n")
    
except FileNotFoundError:
    print(f"ERROR: Config file not found: {config_file}\n")
    sys.exit(1)
    
except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON in config file: {str(e)}\n")
    sys.exit(1)
    
except Exception as e:
    print(f"ERROR: {str(e)}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
