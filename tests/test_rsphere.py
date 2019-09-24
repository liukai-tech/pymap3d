#!/usr/bin/env python3
import pytest
from pytest import approx
import pymap3d as pm

ell = pm.Ellipsoid()
A = ell.semimajor_axis


def test_rsphere_eqavol():
    assert pm.rsphere_eqavol() == approx(6371000.8049)


def test_rsphere_authalic():
    assert pm.rsphere_authalic() == approx(6371007.1809)


def test_rsphere_rectifying():
    assert pm.rsphere_rectifying() == approx(6367449.1458)


def test_rsphere_biaxial():
    assert pm.rsphere_biaxial() == approx(6367444.657)


def test_rsphere_triaxial():
    assert pm.rsphere_triaxial() == approx(6371008.77)


def test_rsphere_euler():
    assert pm.rsphere_euler(42, 82, 44, 100) == approx(6386606.829131)


if __name__ == "__main__":
    pytest.main(["-v", __file__])