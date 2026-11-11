"""Consulta meteorológica ejecutada del lado del servidor en Vercel."""
import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

class handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        city = parse_qs(urlsplit(self.path).query).get('city', [''])[0].strip()
        if not 2 <= len(city) <= 100:
            return self.send_json(400, {'error': 'Escribe una ciudad de 2 a 100 caracteres.'})
        key = os.environ.get('WEATHERAPI_KEY', '').strip()
        if not key:
            return self.send_json(503, {'error': 'Falta configurar WEATHERAPI_KEY en el servidor.'})
        url = 'https://api.weatherapi.com/v1/current.json?' + urlencode({'key': key, 'q': city, 'lang': 'es'})
        try:
            with urlopen(url, timeout=10) as response:
                data = json.load(response)
            loc, cur = data['location'], data['current']
            result = {'location': {k: loc[k] for k in ('name','region','country','localtime')},
                      'current': {k: cur[k] for k in ('temp_c','humidity','wind_kph')}}
            result['current']['condition'] = {k: cur['condition'][k] for k in ('text','icon')}
            self.send_json(200, result)
        except HTTPError as exc:
            try: code = json.load(exc).get('error', {}).get('code')
            except (ValueError, OSError, AttributeError): code = None
            if code == 1006: return self.send_json(404, {'error': 'No encontramos esa ciudad. Prueba con otro nombre.'})
            if code in (1002, 2006, 2008): return self.send_json(502, {'error': 'La clave de WeatherAPI no es válida o no está habilitada.'})
            if code == 2007: return self.send_json(502, {'error': 'Se alcanzó el límite de consultas de WeatherAPI.'})
            self.send_json(502, {'error': 'El servicio meteorológico no está disponible. Inténtalo después.'})
        except (URLError, TimeoutError, ValueError, KeyError, TypeError, OSError):
            self.send_json(502, {'error': 'No se pudo consultar WeatherAPI. Inténtalo después.'})

    def log_message(self, format, *args):
        pass
