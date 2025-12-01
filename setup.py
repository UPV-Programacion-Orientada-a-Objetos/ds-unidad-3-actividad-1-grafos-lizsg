from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Definir la extensión
extensions = [
    Extension(
        "neuronet",
        sources=[
            "src/cython/neuronet.pyx",
            "src/cpp/SparseGraph.cpp"
        ],
        include_dirs=["src/cpp"],
        language="c++",
        extra_compile_args=["/std:c++14"] if os.name == 'nt' else ["-std=c++14"],
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
