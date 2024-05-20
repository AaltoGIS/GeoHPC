import shapely.ops


def merge_geometries(geometries):
    """
    geometries: A list of Shapely geometries.

    Try to join the given geometries in the list to a single geometry. If the
    join results into a multigeometry, return the parts in a list. If the join
    results into multiple types of geometries, raise an error.
    """
    if len(geometries) < 2:
        return geometries

    if geometries[0].geom_type == 'LineString':
        return merge_linestrings(geometries)

    elif geometries[0].geom_type == 'Polygon':
        return merge_polygons(geometries)

    else:
        raise Exception(f'merge_geometries() called with a geometry type "{geometries[0].geom_type}".')


def merge_polygons(polygons):
    """
    Try the merge the polygons into a single polygon. If a MultiPolygon is created,
    return the parts as a list of Polygons.
    """
    joined = shapely.ops.unary_union(polygons)

    if joined.geom_type == 'Polygon':
        return [joined]

    elif joined.geom_type == 'MultiPolygon':
        return [g for g in joined.geoms]
    else:
        raise Exception(f'merge_geometries() returned {joined.geom_type}.')


def merge_linestrings(lines):
    """
    Try the merge the linestrings into a single linestring. If a MultiLineString is created,
    return the parts as a list of LineStrings.
    """
    joined = shapely.ops.linemerge(lines)

    if joined.geom_type == 'LineString':
        return [joined]

    elif joined.geom_type == 'MultiLineString':
        return [g for g in joined.geoms]

    else:
        raise Exception(f'merge_linestrings() returned {joined.geom_type}.')
