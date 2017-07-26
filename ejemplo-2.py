#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

# Ejemplo similar al ejemplo-1, pero acá se obtienen además el PDF, el PDF-Cedible y el XML desde SuperFactura.

from SuperFacturaAPI import SuperFacturaAPI

# 1) Generar arreglo con datos del DTE

datos = {
	'Encabezado': {
		'IdDoc': {
			'TipoDTE': 33,
			# 'FchEmis': '2015-01-01', # Opcional
		},
		'Emisor': {
			'RUTEmisor': '99581150-2',
			# Los demás datos serán agregados por SuperFactura
		},
		'Receptor': {
			'RUTRecep': '1-9',
			'RznSocRecep': 'Test',
			'GiroRecep': 'Giro',
			'DirRecep': 'Dirección',
			'CmnaRecep': 'Comuna',
			'CiudadRecep': 'Ciudad',
		},
		# 'Totales' será agregado por SuperFactura
	},
	'Detalles': [
		{
			# 'NroLinDet' será agregado por SuperFactura
			'NmbItem': 'Item 1',
			'DscItem': 'Descripción del item 1',
			'QtyItem': 3,
			'UnmdItem': 'KG',
			'PrcItem': 100
		},
		{
			'NmbItem': 'Item 2',
			'DscItem': 'Descripción del item 2',
			'QtyItem': 5,
			'UnmdItem': 'KG',
			'PrcItem': 65
		}
	]
}

# 2) Usar API para generar y enviar el DTE al SII

api = SuperFacturaAPI.SuperFacturaAPI('usuario@cliente.cl', 'mypassword')

resultado = api.SendDTE(
	datos,								# Datos del DTE
	'cer',								# Ambiente: 'pro' = producción y 'cer' = certificación
	{									# El tercer argumento puede contener un arreglo con opciones
		'savePDF': '/tmp/dte-123',		# Descarga y almacena el PDF
		'saveXML': '/tmp/dte-123'		# Descarga y almacena el XML
	}
)

# 3) Procesar salida de la API

if resultado['ok']:
	print 'Folio: ', resultado['folio']
else:
	print 'Error'
