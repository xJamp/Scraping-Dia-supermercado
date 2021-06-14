import requests
import json
from bs4 import BeautifulSoup

class Dia():
	def __init__(self):
		pass

	def _get_fq(self, response):
		return response.text.split('/buscapagina?fq=')[1].split('&')[0].replace('%3a', ':').replace('%2f', '/')

	def _make_link(self, categoria, subcategoria, producto):
		if subcategoria:
			categoria += '/' + subcategoria
		if producto:
			categoria += '/' + producto
		return categoria

	def tiendas(self, estado = True):
		estado = 'true'if estado else 'false'

		headers = {
			'authority': 'diaonline.supermercadosdia.com.ar',
			'accept': 'application/vnd.vtex.ds.v10+json',
			'rest-range': 'resources=0-3000',
			'x-requested-with': 'XMLHttpRequest',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
			'content-type': 'application/json',
			'sec-gpc': '1',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://diaonline.supermercadosdia.com.ar/folletos',
			'accept-language': 'es-ES,es;q=0.9'
		}

		response = requests.get('https://diaonline.supermercadosdia.com.ar/api/dataentities/FL/search?_fields=id,imagen,nombre,horarios,direccion,etiqueta,lat,long,tipo,barrio,provincia,metododeentrega&_where=(estado={})'.format(estado), headers = headers)

		if response.status_code == 200:
			Json = json.loads(response.text)
			return Json

		else:
			raise Exception('Error codigo de estado ' + str(response.status_code))

	def categorias(self):
		response = requests.get('https://diaonline.supermercadosdia.com.ar/')
		soup = BeautifulSoup(response.content, 'html.parser')
		categorias_list = {}

		for categoria in soup.find('ul', class_ = 'dropdown-menu').find_all('li'):
			try:
				link = categoria.find('a').get('href').split('?')[0].split('/')[1]
				if link not in categorias_list:
					categorias_list[link] = categoria.find('span').text
			except:
				pass

		return categorias_list

	def subcategorias(self, categoria):
		response = requests.get('https://diaonline.supermercadosdia.com.ar/{}?PS=15&O=OrderByTopSaleDESC'.format(categoria))
		soup = BeautifulSoup(response.content, 'html.parser')
		subcategorias = {}

		for subcategory in soup.find('div', class_ = 'menu-departamento').find('div', class_ = 'search-single-navigator').find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
			# Conseguimos los productos de cada categoria
			productos = {}
			subcategory_ul = subcategory.find_next_siblings('ul')[0]

			for product in subcategory_ul.find_all('li'):
				product = product.find('a')
				link = product.get('href').split('?')[0].split('/')[-1]
				product_name = product.text.split(' (')[0]
				cantidad = int(product.text.split(' (')[1][:-1])
				productos[product_name] = {'link': link, 'cantidad': cantidad}


			# conseguimos la cateogira
			categoria_object = subcategory.find('a')
			try:
				link = categoria_object.get('href').split('?')[0].split('/')[-1]
				categoria_name = categoria_object.text
			except:
				link = None
				categoria_name = subcategory.text

			subcategorias[categoria_name] = {'link': link, 'productos': productos}

		return subcategorias

	def producto_by_id(self, ID):
		if isinstance(ID, int):
			productId = 'productId:' + str(ID)
		elif isinstance(ID, str):
			productId = 'productId:' + ID
		elif isinstance(ID, tuple) or isinstance(ID, list):
			productId = ''
			for x in ID:
				productId += 'productId:' + str(x) + ','
			productId = productId[:-1] #Le saco la coma de mas

		#productId:271632
		response = requests.get('https://diaonline.supermercadosdia.com.ar/api/catalog_system/pub/products/search?fq=' + productId)
		Json = json.loads(response.text)
		return Json

	def productos(self, categoria, subcategoria = None, producto = None, Max = False):
		pagina = 1
		productos = {}
		Break = False

		fq = self._get_fq(requests.get('https://diaonline.supermercadosdia.com.ar/{}?O=OrderByTopSaleDESC&PS=15'.format(self._make_link(categoria, subcategoria, producto))))

		while True:
			params = (
				('fq', fq),
				('O', 'OrderByBestDiscountDESC'),
				('PS', '50'),
				('sl', '8d6fe5d3-768b-4f53-92b9-71d5c173042f'),
				('cc', '1'),
				('sm', '0'),
				('PageNumber', str(pagina)),
			)

			response = requests.get('https://diaonline.supermercadosdia.com.ar/buscapagina', params = params)
			if response.text == '':
				break

			soup = BeautifulSoup(response.content, 'html.parser')

			for productoTag in soup.find_all('div', class_ = 'item'):
				ID = productoTag.get('id').split('-')[-1]

				nombre = productoTag.find('div', class_ = 'product-name').find('a').text.replace('\n', '').strip()
				marca = productoTag.find('div', class_ = 'marca').text
				link = productoTag.find('div', class_ = 'product-name').find('a').get('href')
				precio_viejo = productoTag.find('span', class_ = 'old-price')
				if precio_viejo:
					precio_viejo = precio_viejo.text.replace('\n', '').strip()[2:]
				precio_nuevo = productoTag.find('span', class_ = 'best-price').text.replace('\n', '').strip()[2:]
				oferta_extra = productoTag.find('div', class_ = 'ofertasHighlight').text
				if oferta_extra == '': oferta_extra = None

				productos[ID] = {'producto': nombre, 'marca': marca, 'precio_viejo': precio_viejo, 'precio_nuevo': precio_nuevo, 'oferta_extra': oferta_extra, 'link': link}

				if Max and Max <= len(productos):
					Break = True
					break

			if Break:
				break

			pagina += 1
		
		return productos

	def recetas(self):
		response = requests.get('https://diaonline.supermercadosdia.com.ar/api/dataentities/RC/search?_fields=id,coleccion,tag,categoria,fecha,imagen,Imagen_banner,ingredientes,preparacion,titulo,url')
		Json = json.loads(response.text)
		return Json

	def promociones(self):
		response = requests.get('https://diaonline.supermercadosdia.com.ar/medios-de-pago-y-promociones')
		soup = BeautifulSoup(response.content, 'html.parser')
		Dict = {}

		for promos in soup.find('div', class_ = 'promos-body').find_all('div', class_ = 'promo-dia'):
			promos_dia = []

			for promo in promos.find_all('div', class_ = 'mpp-card'):
				promo_dict = {'descuento': promo.find('h2').text, 'tope': promo.find('div', class_ = 'wysiwyg descripcion').text.split('\n')[1], 'informacion': [promo.find('div', class_ = 'wysiwyg contenido').find('p').text, promo.find('div', class_ = 'wysiwyg contenido').find_all('p')[-1].text]}
				promos_dia.append(promo_dict)

			Dict[promos.find('h3').text] = promos_dia

		return Dict

	def medios_de_pago(self):
		response = requests.get('https://diaonline.supermercadosdia.com.ar/medios-de-pago-y-promociones')
		soup = BeautifulSoup(response.content, 'html.parser')
		Dict = {}

		for types in soup.find_all('section'):
			tarjets = []	

			for tarjet in types.find_all('img'):
				if tarjet.get('title'):
					tarjets.append(tarjet.get('title'))


			Dict[types.find('h3').text] = tarjets

		return Dict