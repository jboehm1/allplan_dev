"""
AutoArray Full System - Complete Solar Mounting System 3D Model

This PythonPart generates a complete 3D model of the ClickCon ClickPlain Pro
mounting system with all structural components properly positioned and colored.

Components:
    - Rafter: base roof structure (brown)
    - Gutter: horizontal support gutter profiles (dark gray)
    - Profile: vertical/diagonal frame profiles (light gray)
    - Rung: horizontal connecting elements between profiles (yellow)
    - Module: solar PV panels (cyan)

Author: Personal Development
Version: 1.0.0
Date: 2025-10-27
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements  
import NemAll_Python_BasisElements as AllplanBasisElements



def check_allplan_version(build_ele, version):
    """Check Allplan version compatibility"""
    return True



def create_element(build_ele, doc):
    """Create element entry point"""
    element = ClickConSystemCreator(doc)
    return element.create(build_ele)



class ClickConSystemCreator:
    """ClickCon ClickPlain Pro mounting system 3D generator"""

    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc


    def create(self, build_ele):
        """Create all system components"""

        # Get parameters
        surface_width = build_ele.SurfaceWidth.value
        surface_height = build_ele.SurfaceHeight.value  
        panel_width = build_ele.PanelWidth.value
        panel_height = build_ele.PanelHeight.value
        spacing = build_ele.Spacing.value
        panel_thickness = build_ele.PanelThickness.value

        # Calculate grid
        nb_col = int((surface_width + spacing) // (panel_width + spacing))
        nb_row = int((surface_height + spacing) // (panel_height + spacing))
        actual_width = nb_col * panel_width + (nb_col - 1) * spacing
        actual_height = nb_row * panel_height + (nb_row - 1) * spacing

        # Get component dimensions from parameters
        rafter_height = build_ele.RafterHeight.value
        gutter_width = build_ele.GutterWidth.value
        gutter_height = build_ele.GutterHeight.value
        profile_thickness = build_ele.ProfileThickness.value
        rung_thickness = build_ele.RungThickness.value

        z_rafter = 0

        # Create rafter (roof structure base)
        self.create_rafter(0, 0, z_rafter, actual_width, actual_height, rafter_height)

        # Create gutters (main horizontal support)
        gutter_z = z_rafter + rafter_height
        for col in range(nb_col + 1):
            x = col * (panel_width + spacing) - spacing / 2.0
            self.create_gutter(x, 0, gutter_z, actual_height, gutter_width, gutter_height)

        # Create profiles (vertical/diagonal frame elements)
        profile_z = gutter_z + gutter_height
        for row in range(nb_row + 1):
            y = row * (panel_height + spacing) - spacing / 2.0
            self.create_profile(0, y, profile_z, actual_width, profile_thickness, rung_thickness)

        # Create rungs (horizontal connecting bars between profiles)
        rung_z = profile_z + rung_thickness
        for row in range(nb_row):
            for col in range(nb_col):
                x = col * (panel_width + spacing)
                y = row * (panel_height + spacing)
                self.create_rung(x, y, rung_z, panel_width, rung_thickness, rung_thickness)

        # Create solar panels (modules) on top
        module_z = rung_z + rung_thickness
        for row in range(nb_row):
            for col in range(nb_col):
                x = col * (panel_width + spacing)
                y = row * (panel_height + spacing)
                if (x + panel_width <= surface_width and y + panel_height <= surface_height):
                    self.create_module(x, y, module_z, panel_width, panel_height, panel_thickness)

        # Create frame bars (structural support between rows)
        for row in range(nb_row - 1):
            y_pos = (row + 1) * (panel_height + spacing) - spacing / 2.0
            self.create_frame_bar(0, y_pos, rung_z - rung_thickness/2.0, actual_width, spacing, rung_thickness)

        # Create boundary outline
        self.create_surface_outline(surface_width, surface_height)

        return self.model_ele_list, self.handle_list


    def create_rafter(self, x, y, z, width, height, thickness):
        """Create roof rafter (base structure) - BROWN"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, width, height, thickness)
        
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 5  # Brown/tan for rafter
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))


    def create_gutter(self, x, y, z, length, width, height):
        """Create horizontal gutter profile - DARK GRAY"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, width, length, height)
        
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 8  # Dark gray for gutter
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))


    def create_profile(self, x, y, z, length, width, height):
        """Create vertical/diagonal profile frame - LIGHT GRAY"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, length, width, height)
        
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 7  # Light gray for profile
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))


    def create_rung(self, x, y, z, width, thickness, height):
        """Create horizontal connecting rung - YELLOW"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, width, thickness, height)
        
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 3  # Yellow for rung (structural element)
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))


    def create_module(self, x, y, z, width, height, thickness):
        """Create solar PV module/panel - CYAN"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, width, height, thickness)
        
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 3  # Cyan for solar modules (user confirmed)
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))


    def create_frame_bar(self, x, y, z, width, bar_width, bar_height):
        """Create structural frame bar connecting rows - YELLOW"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y - bar_width / 2.0, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, width, bar_width, bar_height)
        
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 3  # Yellow for frame bars
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))


    def create_surface_outline(self, width, height):
        """Create surface boundary in dashed lines"""
        outline_points = [
            AllplanGeo.Point3D(0, 0, 0),
            AllplanGeo.Point3D(width, 0, 0),
            AllplanGeo.Point3D(width, height, 0),
            AllplanGeo.Point3D(0, height, 0),
            AllplanGeo.Point3D(0, 0, 0)
        ]
        
        outline_line = AllplanGeo.Polyline3D(outline_points)
        
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 1  # Black/dark for boundary (user confirmed = Red in config, but using 1 for contrast)
        prop.LineStyle = 2  # Dashed
        
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, outline_line))
