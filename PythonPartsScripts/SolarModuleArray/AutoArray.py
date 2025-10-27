""" Script for AutoArray
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements  
import NemAll_Python_BasisElements as AllplanBasisElements


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """
    return True


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """
    element = AutoArrayCreator(doc)

    return element.create(build_ele)


class AutoArrayCreator:
    """
    Definition of class AutoArrayCreator
    """

    def __init__(self, doc):
        """
        Initialisation of class AutoArrayCreator

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            created element result
        """

        # Get parameters
        surface_width = build_ele.SurfaceWidth.value
        surface_height = build_ele.SurfaceHeight.value  
        panel_width = build_ele.PanelWidth.value
        panel_height = build_ele.PanelHeight.value
        spacing = build_ele.Spacing.value
        panel_thickness = build_ele.PanelThickness.value
        frame_bar_height = build_ele.FrameBarHeight.value

        # Calculate number of panels automatically
        nb_col = int((surface_width + spacing) // (panel_width + spacing))
        nb_row = int((surface_height + spacing) // (panel_height + spacing))

        # Create panels
        for row in range(nb_row):
            for col in range(nb_col):
                x = col * (panel_width + spacing)
                y = row * (panel_height + spacing)
                z = frame_bar_height  # Panneaux au-dessus des barres

                # Check if panel fits in surface
                if (x + panel_width <= surface_width and 
                    y + panel_height <= surface_height):
                    
                    self.create_solar_panel(x, y, z, panel_width, panel_height, panel_thickness)

        # Create horizontal frame bars between rows (jaunes)
        for row in range(nb_row - 1):
            y_pos = (row + 1) * (panel_height + spacing) - spacing / 2.0
            self.create_frame_bar(0, y_pos, 0, surface_width, spacing, frame_bar_height)

        # Create surface outline
        self.create_surface_outline(surface_width, surface_height)

        return self.model_ele_list, self.handle_list

    def create_solar_panel(self, x, y, z, width, height, thickness):
        """
        Create a solar panel with frame

        Args:
            x, y, z:      position
            width, height: panel dimensions
            thickness:    panel thickness
        """
        
        # Create main panel (bleu)
        panel_placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        panel_solid = AllplanGeo.Polyhedron3D.CreateCuboid(panel_placement, width, height, thickness)
        
        panel_prop = AllplanBaseElements.CommonProperties()
        panel_prop.Color = 1  # Blue for solar panels
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(panel_prop, panel_solid))

        # Create frame outline on top (rouge)
        frame_points = [
            AllplanGeo.Point3D(x, y, z + thickness),
            AllplanGeo.Point3D(x + width, y, z + thickness),
            AllplanGeo.Point3D(x + width, y + height, z + thickness),
            AllplanGeo.Point3D(x, y + height, z + thickness),
            AllplanGeo.Point3D(x, y, z + thickness)
        ]
        
        frame_line = AllplanGeo.Polyline3D(frame_points)
        
        frame_prop = AllplanBaseElements.CommonProperties()
        frame_prop.Color = 6  # Red for panel frame
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(frame_prop, frame_line))

    def create_frame_bar(self, x, y, z, width, bar_width, bar_height):
        """
        Create horizontal frame bar connecting rows

        Args:
            x, y, z:      position (start)
            width:        length of bar (full surface width)
            bar_width:    width of the bar (2 * spacing)
            bar_height:   height/thickness of the bar
        """
        
        bar_placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y - bar_width / 2.0, z))
        bar_solid = AllplanGeo.Polyhedron3D.CreateCuboid(bar_placement, width, bar_width, bar_height)
        
        bar_prop = AllplanBaseElements.CommonProperties()
        bar_prop.Color = 3  # Yellow for structural bars
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(bar_prop, bar_solid))

    def create_surface_outline(self, width, height):
        """
        Create surface boundary outline

        Args:
            width, height: surface dimensions
        """
        
        outline_points = [
            AllplanGeo.Point3D(0, 0, 0),
            AllplanGeo.Point3D(width, 0, 0),
            AllplanGeo.Point3D(width, height, 0),
            AllplanGeo.Point3D(0, height, 0),
            AllplanGeo.Point3D(0, 0, 0)
        ]
        
        outline_line = AllplanGeo.Polyline3D(outline_points)
        
        outline_prop = AllplanBaseElements.CommonProperties()
        outline_prop.Color = 7  # Black for boundary
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(outline_prop, outline_line))
