"""
AutoArray - Solar Panel Grid Generator for Allplan

This PythonPart automatically generates a grid of solar panels based on available
surface dimensions. It calculates the optimal number of panels that fit within
the given area and creates a complete 3D model with panels, structural frame bars,
and boundary outline.

Author: Personal Development
Version: 1.0.0
Date: 2025-10-27

Description:
    - Automatically calculates panel grid layout
    - Creates 3D panel models (blue color)
    - Generates structural frame bars (yellow) connecting rows and edges
    - Draws surface boundary with dashed lines
    - Supports customizable panel dimensions and spacing

Parameters:
    - SurfaceWidth: Total available surface width (mm)
    - SurfaceHeight: Total available surface height (mm)
    - PanelWidth: Width of single solar panel (mm)
    - PanelHeight: Height of single solar panel (mm)
    - Spacing: Gap between panels (mm)
    - PanelThickness: Thickness of panel (mm)
    - FrameBarHeight: Height of structural frame bars (mm)

Returns:
    List of ModelElement3D objects representing the complete solar array
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
    AutoArrayCreator - Main class for solar panel array generation
    
    Handles automatic calculation and 3D modeling of solar panel grids
    based on surface dimensions and panel specifications.
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
            created element result (tuple of model_ele_list, handle_list)
        """

        # Get parameters from user input
        surface_width = build_ele.SurfaceWidth.value
        surface_height = build_ele.SurfaceHeight.value  
        panel_width = build_ele.PanelWidth.value
        panel_height = build_ele.PanelHeight.value
        spacing = build_ele.Spacing.value
        panel_thickness = build_ele.PanelThickness.value
        frame_bar_height = build_ele.FrameBarHeight.value

        # Calculate number of panels that fit automatically
        nb_col = int((surface_width + spacing) // (panel_width + spacing))
        nb_row = int((surface_height + spacing) // (panel_height + spacing))

        # Calculate actual used dimensions (excluding trailing spacing)
        actual_width = nb_col * panel_width + (nb_col - 1) * spacing
        actual_height = nb_row * panel_height + (nb_row - 1) * spacing

        # Generate panel grid
        for row in range(nb_row):
            for col in range(nb_col):
                x = col * (panel_width + spacing)
                y = row * (panel_height + spacing)
                z = frame_bar_height  # Panels positioned above frame bars

                # Verify panel remains within surface boundaries
                if (x + panel_width <= surface_width and 
                    y + panel_height <= surface_height):
                    
                    self.create_solar_panel(x, y, z, panel_width, panel_height, panel_thickness)

        # Generate structural support frame bars between panel rows (horizontal)
        for row in range(nb_row - 1):
            y_pos = (row + 1) * (panel_height + spacing) - spacing / 2.0
            self.create_frame_bar(0, y_pos, 0, actual_width, spacing, frame_bar_height)

        # Create frame bar at bottom
        self.create_frame_bar(0, -spacing / 2.0, 0, actual_width, spacing, frame_bar_height)

        # Create frame bar at top
        top_y = nb_row * (panel_height + spacing) - spacing / 2.0
        self.create_frame_bar(0, top_y, 0, actual_width, spacing, frame_bar_height)

        # Create boundary outline of the surface area
        self.create_surface_outline(surface_width, surface_height)

        return self.model_ele_list, self.handle_list


    def create_solar_panel(self, x, y, z, width, height, thickness):
        """
        Create a single solar panel 3D model

        Args:
            x (float):      X coordinate of panel position (mm)
            y (float):      Y coordinate of panel position (mm)
            z (float):      Z coordinate of panel position (mm)
            width (float):  Width of panel (mm)
            height (float): Height of panel (mm)
            thickness (float): Thickness/depth of panel (mm)
        """
        
        # Create 3D solid representing the solar panel
        panel_placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        panel_solid = AllplanGeo.Polyhedron3D.CreateCuboid(panel_placement, width, height, thickness)
        
        # Set panel properties (color: blue)
        panel_prop = AllplanBaseElements.CommonProperties()
        panel_prop.Color = 2  # Blue for solar panels
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(panel_prop, panel_solid))


    def create_frame_bar(self, x, y, z, width, bar_width, bar_height):
        """
        Create horizontal structural frame bar connecting panel rows

        Args:
            x (float):        X coordinate of bar start position (mm)
            y (float):        Y coordinate of bar position (mm)
            z (float):        Z coordinate of bar position (mm)
            width (float):    Length of bar (actual panel grid width) (mm)
            bar_width (float):  Width of bar perpendicular to length (mm)
            bar_height (float): Height/thickness of bar (mm)
        """
        
        # Create 3D solid representing the structural frame bar
        bar_placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y - bar_width / 2.0, z))
        bar_solid = AllplanGeo.Polyhedron3D.CreateCuboid(bar_placement, width, bar_width, bar_height)
        
        # Set bar properties (color: yellow)
        bar_prop = AllplanBaseElements.CommonProperties()
        bar_prop.Color = 3  # Yellow for structural bars
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(bar_prop, bar_solid))


    def create_surface_outline(self, width, height):
        """
        Create surface boundary outline in dashed lines

        Args:
            width (float):  Width of surface boundary (mm)
            height (float): Height of surface boundary (mm)
        """
        
        # Define boundary corner points
        outline_points = [
            AllplanGeo.Point3D(0, 0, 0),
            AllplanGeo.Point3D(width, 0, 0),
            AllplanGeo.Point3D(width, height, 0),
            AllplanGeo.Point3D(0, height, 0),
            AllplanGeo.Point3D(0, 0, 0)  # Close the loop
        ]
        
        # Create polyline representing the boundary
        outline_line = AllplanGeo.Polyline3D(outline_points)
        
        # Set outline properties (color: black, style: dashed)
        outline_prop = AllplanBaseElements.CommonProperties()
        outline_prop.Color = 7  # Black for boundary
        outline_prop.LineStyle = 2  # Dashed line style
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(outline_prop, outline_line))
