"""
AutoArray - Solar Mounting System with Real Aluminum Profiles

Components (couleurs):
    - Modules: panneaux solaires (bleu, 7)
    - Rungs: barres verticales sous bords gauche/droite de chaque panneau (vert, 4)
    - Profiles: vrais profils alu horizontaux pour montage (cyan, 3)
    - Gutters: barres verticales épaisses aux extrémités du système (jaune/orange, 8)

Version: 1.2.0
Date: 2025-10-28
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

def check_allplan_version(build_ele, version):
    return True

def create_element(build_ele, doc):
    element = SystemCreator(doc)
    return element.create(build_ele)

class SystemCreator:
    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc
        self.module_count = 0

    def create(self, build_ele):
        # Paramètres utilisateurs
        surface_width = build_ele.SurfaceWidth.value
        surface_height = build_ele.SurfaceHeight.value
        panel_width = build_ele.PanelWidth.value
        panel_height = build_ele.PanelHeight.value
        spacing = build_ele.Spacing.value
        panel_thickness = build_ele.PanelThickness.value
        is_horizontal = build_ele.PanelOrientation.value
        gutter_width = build_ele.GutterWidth.value
        gutter_height = build_ele.GutterHeight.value
        profile_thickness = build_ele.ProfileThickness.value
        rung_thickness = build_ele.RungThickness.value

        # Orientation des panneaux
        if is_horizontal:
            panel_width, panel_height = panel_height, panel_width

        nb_col = int((surface_width + spacing) // (panel_width + spacing))
        nb_row = int((surface_height + spacing) // (panel_height + spacing))

        actual_width = nb_col * panel_width + (nb_col - 1) * spacing
        actual_height = nb_row * panel_height + (nb_row - 1) * spacing

        z_base = 0

        # Gutters: à gauche et à droite de tout l'ensemble
        gutter_z = z_base
        self.create_gutter(-gutter_width/2, 0, gutter_z, actual_height, gutter_width, gutter_height)
        self.create_gutter(actual_width - gutter_width/2, 0, gutter_z, actual_height, gutter_width, gutter_height)

        # Profiles: vrais profils alu horizontaux sous chaque rangée
        profile_z = gutter_z + gutter_height
        for row in range(nb_row + 1):
            y = row * (panel_height + spacing) - spacing / 2
            self.create_profile_alu(0, y, profile_z, actual_width)

        # Rungs: barres verticales SOUS bords gauche/droite de chaque panneau
        rung_z = profile_z + profile_thickness
        for row in range(nb_row):
            for col in range(nb_col):
                x_left = col * (panel_width + spacing)
                x_right = x_left + panel_width - rung_thickness
                y = row * (panel_height + spacing)
                # sous bord gauche
                self.create_rung(x_left, y, rung_z, rung_thickness, panel_height, panel_thickness)
                # sous bord droit
                self.create_rung(x_right, y, rung_z, rung_thickness, panel_height, panel_thickness)

        # Modules: panneaux bleus
        module_z = rung_z + panel_thickness
        self.module_count = 0
        for row in range(nb_row):
            for col in range(nb_col):
                x = col * (panel_width + spacing)
                y = row * (panel_height + spacing)
                if (x + panel_width <= surface_width and y + panel_height <= surface_height):
                    self.create_module(x, y, module_z, panel_width, panel_height, panel_thickness)
                    self.module_count += 1

        # Contour global
        self.create_surface_outline(actual_width, actual_height)
        build_ele.ModuleCount.value = self.module_count

        return self.model_ele_list, self.handle_list

    def create_gutter(self, x, y, z, length, width, height):
        """Gutter: barre verticale simple (cuboïde)"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, width, length, height)
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 8 # Jaune/orange
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))

    def create_profile_alu(self, x, y, z, length):
        """Profile alu réel: appelle un profil existant d'Allplan"""
        try:
            # Placement du profil
            placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
            
            # Nom du profil alu standard (à adapter selon ton catalogue Allplan)
            # Exemples: "ITEM 40x40", "Bosch 45x45", "DIN 10305", etc.
            profile_name = "ITEM_40x40"
            
            # Essaie de créer un profil alu
            profile_elem = AllplanBasisElements.ProfileElement(
                AllplanBaseElements.CommonProperties(),
                profile_name,
                placement,
                int(length)
            )
            prop = AllplanBaseElements.CommonProperties()
            prop.Color = 3 # Cyan
            
            self.model_ele_list.append(profile_elem)
            
        except:
            # Fallback: si le profil n'existe pas, utilise un cuboïde
            placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
            solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, 40, length, 40)
            prop = AllplanBaseElements.CommonProperties()
            prop.Color = 3 # Cyan
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))

    def create_rung(self, x, y, z, width, height, thickness):
        """Rung: barre verticale sous bord de panneau"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, width, height, thickness)
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 4 # Vert
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))

    def create_module(self, x, y, z, width, height, thickness):
        """Module: panneau solaire bleu"""
        placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x, y, z))
        solid = AllplanGeo.Polyhedron3D.CreateCuboid(placement, width, height, thickness)
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 7 # Bleu
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, solid))

    def create_surface_outline(self, width, height):
        """Contour de la zone"""
        points = [
            AllplanGeo.Point3D(0, 0, 0),
            AllplanGeo.Point3D(width, 0, 0),
            AllplanGeo.Point3D(width, height, 0),
            AllplanGeo.Point3D(0, height, 0),
            AllplanGeo.Point3D(0, 0, 0)
        ]
        outline_line = AllplanGeo.Polyline3D(points)
        prop = AllplanBaseElements.CommonProperties()
        prop.Color = 1
        prop.LineStyle = 2
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(prop, outline_line))
