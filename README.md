# TempTracker

Proyecto académico: consulta del clima actual por ciudad. Interfaz HTML, CSS y JavaScript; función Python en `api/weather.py` que consulta WeatherAPI desde el servidor.

## Despliegue en Vercel

Importa este repositorio en Vercel y configura `WEATHERAPI_KEY` como variable de entorno privada en el proyecto (Production, Preview y/o Development según corresponda). Nunca incluyas su valor en archivos, capturas ni el repositorio. Tras agregar o cambiar la variable, realiza un nuevo despliegue. La consulta del navegador usa `/api/weather?city=...`; la clave no se envía al navegador. Sin variable configurada, la API muestra un error 503.

El servidor local de la versión anterior no se ha incluido en este repositorio. La función serverless se basa en la documentación de Vercel para funciones Python en `/api`. No hay límite de consultas propio: para uso público real añade controles contra abuso y considera cuotas y costes del proveedor. La funcionalidad y los tiempos deben comprobarse una vez desplegada.

Desarrollado con asistencia de IA; revisar y comprender el código antes de entregarlo.
