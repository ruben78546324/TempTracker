'use strict';
const $ = selector => document.querySelector(selector);
const form = $('#buscador'), city = $('#ciudad'), status = $('#estado'), result = $('#resultado');
form.addEventListener('submit', async event => {
  event.preventDefault();
  const q = city.value.trim(); result.hidden = true;
  if (q.length < 2) { status.textContent = 'Escribe al menos dos caracteres para buscar una ciudad.'; return; }
  const button = form.querySelector('button'); button.disabled = true; status.textContent = 'Buscando el clima…';
  try {
    const response = await fetch('/api/weather?' + new URLSearchParams({city:q}));
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'No se pudo consultar el clima.');
    const {location, current} = data;
    if (!location || !current || !current.condition || !Number.isFinite(current.temp_c) || !Number.isFinite(current.humidity) || !Number.isFinite(current.wind_kph)) throw new Error('La respuesta del servicio está incompleta.');
    $('#lugar').textContent = [location.name, location.region, location.country].filter(Boolean).join(', ');
    $('#fecha').textContent = 'Hora local de los datos: ' + location.localtime;
    $('#temperatura').textContent = current.temp_c.toLocaleString('es-PE') + ' °C';
    $('#condicion').textContent = current.condition.text;
    const icon = $('#icono');
    const iconURL = 'https:' + current.condition.icon;
    if (current.condition.icon && /^https:\/\/cdn\.weatherapi\.com\//.test(iconURL)) icon.src = iconURL;
    else icon.src = 'assets/clima.svg';
    icon.alt = current.condition.text;
    $('#humedad').textContent = current.humidity + ' %';
    $('#viento').textContent = current.wind_kph.toLocaleString('es-PE') + ' km/h';
    status.textContent = 'Consulta realizada.'; result.hidden = false;
  } catch (error) { status.textContent = error.message || 'Revisa tu conexión e inténtalo de nuevo.'; }
  finally { button.disabled = false; }
});
