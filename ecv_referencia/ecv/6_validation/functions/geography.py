"""Geographic checks."""
from . import implements
from .support import Unavailable


@implements("dentroDe")
def inside(latitude, longitude, area, *, contexts):
    """Verdadeira quando o ponto (latitude, longitude) está dentro da área, um polígono de vértices (latitude, longitude)."""
    if latitude is None or longitude is None:
        raise Unavailable("falta a latitude ou a longitude")
    points = [(float(a), float(b)) for a, b in area]
    x, y, result = float(latitude), float(longitude), False
    j = len(points) - 1
    for i in range(len(points)):                      # ray casting
        (xi, yi), (xj, yj) = points[i], points[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            result = not result
        j = i
    return result
