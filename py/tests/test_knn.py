from cppyy.gbl import std
from cppyy_simpleknn import NearestNeighbors, Point


def test_point_iter_pythonizor():
    pt = Point(1.0, 2.0)
    test = [p for p in pt]
    assert test == [1.0, 2.0]


def test_point_repr_pythonizor():
    pt = Point(1.0, 2.0)
    assert repr(pt) == '(1.0, 2.0)'


def test_knn_nearest():
    knn = NearestNeighbors()
    points = [Point(2,0), Point(1,0), Point(0,10), Point(5,5), Point(2,5)]
    knn.points = std.vector[Point](points)
    result = [tuple(res) for res in knn.nearest(Point(0.0, 0.0), 3)]
    assert result == [(1.0, 0.0), (2.0, 0.0), (2.0, 5.0)]
