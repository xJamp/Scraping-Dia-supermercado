# [Dia scraping](https://diaonline.supermercadosdia.com.ar/) 

## Con el modulo podemos conseguir:
1. [Tiendas DIA ](#1-tiendas)
2. [Recetas ](#2-recetas)
3. [Promociones](#3-promociones)
4. [Medios de pago](#4-medios-de-pago)
5. [Productos](#5-productos)
6. [Información detalla de un producto con su ID](#6-producto-por-id)
7. [Categorias](#7-categorias)
8. [Subcategorias](#8-subcategorias)
- - -
## Instalación
- pip install beautifulsoup4
- - -
## Tecnologías
- [requests] - Envia las peticiones
- [BeautifulSoup] - Procesa la información HTML
- [json] - Carga los diccionarios
- - -
## Uso
```sh
from Dia import Dia
Object = Dia()
```
# `1. Tiendas`
- Parametros
- - estado: bool - opcional - Nos permite filtrar entre tiendas activas e inactivas

```sh
Object.tiendas()
```
# `2. Recetas`
- No recibe parametros

```sh
Object.recetas()
```
# `3. Promociones`
- No recibe parametros

```sh
Object.promociones()
```
# `4. Medios de pago`
- No recibe parametros

```sh
Object.medios_de_pago()
```
# `5. Productos`
- Parametros
- - categoria: string - obligatorio - de esta categorias se obtendran todos los productos
- - subcategoria: string - opcional - podemos filtrar por subcategoria
- - producto: string - opcional - podemos filtrar por producto
- - Max: int - opcional - establecemos un límite de busqueda de productos

```sh
Object.subcategorias(categoria = 'almacen', subcategoria = 'arroz-y-legumbres', producto = 'arroz-integral')
```
# `6. Producto por ID`
- Parametros
- - ID: string/tuple/list - obligatorio - de este ID se obtendra la información. pueden haber muchas ID en items de una lista/tupla o una ID en un string.

```sh
Object.producto_by_id(ID = '272632')
```
# `7. Categorias`
- No recibe parametros

```sh
Object.categorias()
```
# `8. Subcategorias`
- Parametros
- - categoria: string - obligatorio - de esta categorias se obtendran todas las subcategorias

```sh
Object.subcategorias('almacen')
```




## License

MIT


   [requests]: <https://docs.python-requests.org/en/master/>
   [BeautifulSoup]: <https://pypi.org/project/beautifulsoup4/#description>
   [json]: <https://docs.python.org/3/library/json.html>
