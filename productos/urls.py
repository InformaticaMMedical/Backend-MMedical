from django.urls import path
from productos.views.AtributoValorView import ValorAtributoProductoDetailAPIView, ValorAtributoProductoListCreateAPIView
from productos.views.AtributoView import AtributoDetailAPIView, AtributoListCreateAPIView
from productos.views.CategoriaView import CategoriaDetailAPIView, CategoriaListCreateAPIView
from productos.views.ProveedorView import ProveedorDetailAPIView, ProveedorListCreateAPIView
from productos.views.ProductoView import ProductoDetailAPIView, ProductoListCreateAPIView

# Fabricantes
from productos.views.FabricanteView import FabricanteDetailAPIView, FabricanteListCreateAPIView
from productos.views.ModeloFabricanteView import ModeloFabricanteDetailAPIView, ModeloFabricanteListCreateAPIView
from productos.views.ProductoCompatibilidadView import ProductoCompatibilidadDetailAPIView, ProductoCompatibilidadListCreateAPIView

urlpatterns = [
    # Categorías
    path('categorias/', CategoriaListCreateAPIView.as_view(), name='categorias'),
    path('categorias/<int:pk>/', CategoriaDetailAPIView.as_view(), name='categoria-detalle'),

    # Proveedores
    path('proveedores/', ProveedorListCreateAPIView.as_view(), name='proveedores'),
    path('proveedores/<int:pk>/', ProveedorDetailAPIView.as_view(), name='proveedor-detalle'),

    # Atributos
    path('atributos/', AtributoListCreateAPIView.as_view(), name='atributos'),
    path('atributos/<int:pk>/', AtributoDetailAPIView.as_view(), name='atributo-detalle'),

    # Valores de Atributo
    path('atributos/valores/', ValorAtributoProductoListCreateAPIView.as_view(), name='atributo-valores'),
    path('atributos/valores/<int:pk>/', ValorAtributoProductoDetailAPIView.as_view(), name='atributo-valor-detalle'),

    # Productos
    path('productos/', ProductoListCreateAPIView.as_view(), name='productos'),
    path('productos/<int:pk>/', ProductoDetailAPIView.as_view(), name='producto-detalle'),

    # Fabricantes
    path('fabricantes/', FabricanteListCreateAPIView.as_view(), name='fabricantes'),
    path('fabricantes/<int:pk>/', FabricanteDetailAPIView.as_view(), name='fabricante-detalle'),

    # Modelos de Fabricante
    path('modelos/', ModeloFabricanteListCreateAPIView.as_view(), name='modelos'),
    path('modelos/<int:pk>/', ModeloFabricanteDetailAPIView.as_view(), name='modelo-detalle'),

    # Compatibilidad de Productos
    path('compatibilidades/', ProductoCompatibilidadListCreateAPIView.as_view(), name='compatibilidades'),
    path('compatibilidades/<int:pk>/', ProductoCompatibilidadDetailAPIView.as_view(), name='compatibilidad-detalle'),

    # Modelos de fabricantes
    path("modelos/", ModeloFabricanteListCreateAPIView.as_view(), name="modelos-list"),
    path("modelos/<int:pk>/", ModeloFabricanteDetailAPIView.as_view(), name="modelos-detail"),
]
