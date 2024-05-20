import shapely.ops
import pyproj


# https://github.com/OSGeo/PROJ-data/tree/master/fi_nls
fn_ykj_etrs_json = './fi_nls_ykj_etrs35fin.json'
transform = pyproj.Proj.from_pipeline(f'+proj=tinshift +file={fn_ykj_etrs_json}').transform


def project_to_epsg_3067_if_needed(geometry):
    """
    geometry: A single Shapely geometry
    transform: pyproj.Proj instance
    """
    #
    # Get the coordinates of one vertex of the geometry.
    #
    if geometry.geom_type == 'Polygon':
        c = geometry.exterior.coords[0]
    else:
        c = geometry.coords[0]

    #
    # If the coordinates are in the KKJ (epsg:2393) coordinate system, the
    # value of the first component will be too large to produce a valid
    # ETRS-TM35FIN coordinate.
    #
    transform_needed = c[0] > 800000

    if transform_needed:
        geometry = shapely.ops.transform(transform, geometry)

    return geometry
