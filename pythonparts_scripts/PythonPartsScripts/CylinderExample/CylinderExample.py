import NemAll_Python_Geometry as Geo
import NemAll_Python_BaseElements as BaseElements
import NemAll_Python_BasisElements as BasisElements

def check_allplan_version(build_ele, version):
    return True

def create_element(build_ele, doc):
    # Valeurs de secours si les paramètres foirent
    radius = getattr(build_ele, 'Radius', None)
    height = getattr(build_ele, 'Height', None)
    r = radius.value if radius else 500
    h = height.value if height else 2000
    if r <= 0: r = 500
    if h <= 0: h = 2000

    axis = Geo.AxisPlacement3D()
    apex = Geo.Point3D(0, 0, h)
    cyl = Geo.Cylinder3D(axis, r, r, apex)

    com_prop = BaseElements.CommonProperties()
    com_prop.GetGlobalProperties()
    model_elem = BasisElements.ModelElement3D(com_prop, cyl)
    return [model_elem]
