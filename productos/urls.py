from django.urls import path

# Vistas principales
from productos.views.AtributoView import AtributoListCreateAPIView, AtributoDetailAPIView
from productos.views.AtributoValorView import ValorAtributoProductoListCreateAPIView, ValorAtributoProductoDetailAPIView
from productos.views.CategoriaView import CategoriaListCreateAPIView, CategoriaDetailAPIView
from productos.views.ProveedorView import ProveedorListCreateAPIView, ProveedorDetailAPIView
from productos.views.ProductoView import ProductoListCreateAPIView, ProductoDetailAPIView
from productos.views.ProductoCompatibilidadView import ProductoCompatibilidadListCreateAPIView, ProductoCompatibilidadDetailAPIView

# Fabricantes y modelos
from productos.views.FabricanteView import FabricanteListCreateAPIView, FabricanteDetailAPIView
from productos.views.ModeloFabricanteView import ModeloFabricanteListCreateAPIView, ModeloFabricanteDetailAPIView

# Imágenes
from productos.views.ImagenesProductoView import (ImagenesProductoCollectionView, ImagenProductoDetailView,)

urlpatterns = [
    # Categorías    
    path('categorias/', CategoriaListCreateAPIView.as_view(), name='categorias-list'),
    path('categorias/<int:pk>/', CategoriaDetailAPIView.as_view(), name='categorias-detail'),

    # Proveedor
    path('proveedores/', ProveedorListCreateAPIView.as_view(), name='proveedores-list'),
    path('proveedores/<int:pk>/', ProveedorDetailAPIView.as_view(), name='proveedores-detail'),

    # Atributos
    path('atributos/', AtributoListCreateAPIView.as_view(), name='atributos-list'),
    path('atributos/<int:pk>/', AtributoDetailAPIView.as_view(), name='atributos-detail'),

    # Valor Atributo
    path('atributos/valores/', ValorAtributoProductoListCreateAPIView.as_view(), name='atributos-valores-list'),
    path('atributos/valores/<int:pk>/', ValorAtributoProductoDetailAPIView.as_view(), name='atributos-valores-detail'),

    # Productos
    path('productos/', ProductoListCreateAPIView.as_view(), name='productos-list'),
    path('productos/<int:pk>/', ProductoDetailAPIView.as_view(), name='productos-detail'),

    # Fabricantes
    path('fabricantes/', FabricanteListCreateAPIView.as_view(), name='fabricantes-list'),
    path('fabricantes/<int:pk>/', FabricanteDetailAPIView.as_view(), name='fabricantes-detail'),

    # Modelo Fabricante
    path('modelos-fabricante/', ModeloFabricanteListCreateAPIView.as_view(), name='modelos-fabricante-list'),
    path('modelos-fabricante/<int:pk>/', ModeloFabricanteDetailAPIView.as_view(), name='modelos-fabricante-detail'),

    # Compatibilidad
    path('compatibilidades/', ProductoCompatibilidadListCreateAPIView.as_view(), name='compatibilidades-list'),
    path('compatibilidades/<int:pk>/', ProductoCompatibilidadDetailAPIView.as_view(), name='compatibilidades-detail'),

    # Imagen
    path('productos/<int:producto_id>/imagenes/', ImagenesProductoCollectionView.as_view(), name='imagenes-producto-list'),
    path('imagenes/<int:imagen_id>/', ImagenProductoDetailView.as_view(), name='imagenes-producto-detail'),
]
