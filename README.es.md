[中文](README.zh.md) | [English](README.md) | Español | [Français](README.fr.md) | [日本語](README.ja.md)

# FTIR.fun — Servidor MCP

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

Servidor MCP y cliente REST para **[FTIR.fun](https://ftir.fun)** — da a los asistentes de IA y pipelines de código acceso directo a más de 130 000 espectros FTIR infrarrojos de referencia para identificación de materiales, explicación de picos y búsqueda en la biblioteca espectral.

## Herramientas disponibles

| Herramienta | Función |
|-------------|---------|
| [`analyze_ftir_spectrum`](#analyze_ftir_spectrum) | Identificar un espectro FTIR desconocido — acepta picos, consulta en lenguaje natural o archivo de instrumento (28+ formatos). Devuelve coincidencias clasificadas con puntuaciones y DOI. |
| [`explain_peaks`](#explain_peaks) | Explicar uno o más picos infrarrojos — asignación de grupos funcionales sin búsqueda completa. |
| [`parse_ftir_spectrum`](#parse_ftir_spectrum) | Analizar un archivo de instrumento FTIR bruto en puntos de datos y picos detectados. |
| [`find_spectra`](#find_spectra) | Buscar en la biblioteca de 130 000+ espectros por nombre, CAS o palabras clave. Devuelve datos de curva. |
| [`submit_ftir_report`](#submit_ftir_report) | Enviar un espectro al flujo tri-axial completo (mismo análisis multi-etapa del sitio web). |
| [`get_ftir_report_status`](#get_ftir_report_status) | Consultar progreso del informe; devuelve resultado estructurado y URL compartible al completarse. |
| [`fetch_result`](#fetch_result) | Recuperar cualquier resultado histórico de FTIR.fun por número de informe. |

---

## Obtener una API Key

1. Inicia sesión en [ftir.fun](https://ftir.fun) — las cuentas nuevas incluyen créditos de prueba gratuitos.
2. Ve a **Cuenta → API Keys** y haz clic en **Generar**.
3. Copia la clave inmediatamente (comienza con `ftir_`; se muestra solo una vez).

La autenticación usa una sola cabecera — sin OAuth, sin redirección al navegador:

```
# Para MCP (alojado)
Authorization: Bearer ftir_your_key_here

# Para REST API
X-API-Key: ftir_your_key_here
```

---

## Herramientas MCP

El endpoint MCP alojado `https://ftir.fun/mcp` expone siete herramientas.

---

### `analyze_ftir_spectrum`

Buscar coincidencias en la biblioteca espectral FTIR para un espectro desconocido. Acepta picos, consulta en lenguaje natural o archivo de instrumento.

**Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `query` | string | No | Solicitud FTIR en lenguaje natural — posiciones de pico como "1730, 1600, 1250 cm-1" se extraen automáticamente. |
| `peaks` | number[] | No | Posiciones de pico FTIR en cm⁻¹ (ej. `[1736, 1379, 1241]`). |
| `file_base64` | string | No | Archivo de instrumento FTIR codificado en base64. Soporta 28+ formatos: Thermo `.spa`/`.spc`, Bruker `.opus`, PerkinElmer `.sp`, JCAMP-DX, CSV, Excel, etc. |
| `filename` | string | No | Nombre del archivo original para detección de formato (ej. `"sample.spa"`). |
| `top_k` | integer | No | Número de candidatos a devolver (1–50, por defecto 15). |
| `tolerance_cm1` | integer | No | Tolerancia de coincidencia de picos en cm⁻¹ (1–30, por defecto 8). |

**Devuelve:** Materiales candidatos clasificados con puntuaciones de similitud, evidencia pico a pico con DOI, y niveles de confianza.

**Ejemplo**
```
Identifica este espectro infrarrojo: picos en 2915, 1715, 1450, 1260, 1090 cm-1.
```

---

### `explain_peaks`

Explicar uno o más picos infrarrojos FTIR sin búsqueda completa en la biblioteca.

**Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `query` | string | No | Pregunta sobre picos en lenguaje natural, ej. `"¿Qué indica 1715 cm-1 en un éster?"` |
| `peaks` | number[] | No | Una o más posiciones de pico en cm⁻¹. |
| `sampling_mode` | string | No | `ATR`, `Thin Film`, `KBr Pellet`, etc. |

**Devuelve:** Explicaciones estructuradas con asignaciones de grupos funcionales.

---

### `parse_ftir_spectrum`

Analizar un archivo de instrumento FTIR codificado en base64, devolviendo puntos de curva alineados y posiciones de pico detectadas.

**Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `file_base64` | string | Sí | Archivo FTIR codificado en base64. |
| `filename` | string | Sí | Nombre del archivo original para detección de formato. |

**Devuelve:** Puntos `(número de onda, intensidad)` y lista de picos detectados en cm⁻¹.

---

### `find_spectra`

Buscar espectros FTIR de referencia por nombre de sustancia, número CAS o palabras clave.

**Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `query` | string | Sí | Nombre de sustancia, CAS, `NUM` de la biblioteca, o palabras clave. |
| `limit` | integer | No | Número de resultados (1–20, por defecto 10). |

**Devuelve:** Espectros de referencia con número, nombres, CAS, marcadores de pico y datos de curva.

---

### `submit_ftir_report`

Enviar un archivo de espectro al flujo tri-axial completo de FTIR.fun. Devuelve `task_id` y `result_num` inmediatamente.

**Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `file_base64` | string | Sí | Archivo FTIR codificado en base64. |
| `filename` | string | Sí | Nombre del archivo original. |

**Devuelve:** `{ task_id, result_num }`

---

### `get_ftir_report_status`

Consultar el estado de un informe enviado via `submit_ftir_report`. Al completarse, devuelve `report_view` y `report_url`.

**Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `task_id` | string | Sí | `task_id` devuelto por `submit_ftir_report`. |

---

### `fetch_result`

Recuperar un resultado histórico de análisis FTIR.fun por número de informe.

**Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `result_num` | string | Sí | Número de informe/resultado de FTIR.fun. |
| `language_code` | string | No | Idioma de visualización (por defecto `en`). |

---

## REST API

Llama a FTIR.fun desde cualquier lenguaje — Python, JavaScript, R, MATLAB, Go. Ideal para integraciones LIMS, procesamiento por lotes, o agregar búsqueda de espectros infrarrojos a tu aplicación.

Referencia completa: https://ftir.fun/api-docs/

### Verificación de estado (sin clave)

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### Identificar un espectro infrarrojo desconocido — picos

```bash
curl -X POST https://ftir.fun/ftir/analyze_spectrum \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"peaks": [2915, 1715, 1450, 1260, 1090], "options": {"top_k": 10}}'
```

```python
import requests

resp = requests.post(
    "https://ftir.fun/ftir/analyze_spectrum",
    headers={"X-API-Key": "ftir_your_key_here"},
    json={"peaks": [2915, 1715, 1450, 1260, 1090]},
)
print(resp.json())
```

### Identificar desde un archivo de instrumento

```python
import base64, requests

with open("sample.spa", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

resp = requests.post(
    "https://ftir.fun/ftir/analyze_spectrum",
    headers={"X-API-Key": "ftir_your_key_here"},
    json={"file_base64": b64, "filename": "sample.spa"},
)
print(resp.json())
```

### Explicar picos infrarrojos

```bash
curl -X POST https://ftir.fun/ftir/explain_peaks \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"peaks": [1715, 2915], "sampling_mode": "ATR"}'
```

### Buscar espectros de referencia por nombre o CAS

```bash
curl "https://ftir.fun/v1/search?q=polypropylene&limit=5" \
  -H "X-API-Key: ftir_your_key_here"
```

---

## Configuración de cliente MCP

El endpoint MCP alojado no requiere instalación local. URL: `https://ftir.fun/mcp` con token `Bearer`.

### VS Code (modo Agente de GitHub Copilot)

```json
{
  "inputs": [
    { "type": "promptString", "id": "ftirfun-api-key", "description": "FTIR.fun API key", "password": true }
  ],
  "servers": {
    "ftirfun": {
      "type": "http",
      "url": "https://ftir.fun/mcp",
      "headers": { "Authorization": "Bearer ${input:ftirfun-api-key}" }
    }
  }
}
```

### Claude Desktop / Claude Code

```bash
claude mcp add --transport http ftirfun https://ftir.fun/mcp \
  --header "Authorization: Bearer ftir_your_key_here"
```

### Cursor

```json
{ "mcpServers": { "ftirfun": { "url": "https://ftir.fun/mcp", "headers": { "Authorization": "Bearer ftir_your_key_here" } } } }
```

### Gemini CLI

```json
{ "mcpServers": { "ftirfun": { "httpUrl": "https://ftir.fun/mcp", "headers": { "Authorization": "Bearer ftir_your_key_here" } } } }
```

Cualquier otro cliente MCP que soporte servidores HTTP remotos funciona: URL `https://ftir.fun/mcp`, cabecera `Authorization: Bearer <tu clave>`.

---

## Auto-alojado (proxy local)

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
pip install ftirfun-mcp
ftirfun-mcp
```

Docker:

```bash
docker build -t ftirfun-mcp .
docker run --rm -p 8001:8001 -e FTIRFUN_API_KEY="your-ftirfun-api-key" ftirfun-mcp
```

---

## Acerca de FTIR.fun

**[FTIR.fun](https://ftir.fun)** es una plataforma en la nube para análisis de espectroscopía infrarroja, utilizada por investigadores e ingenieros en más de 52 países. Ofrece acceso rápido a una biblioteca en constante actualización de **más de 130 000 espectros FTIR de referencia**.

Funciones en [ftir.fun](https://ftir.fun):

- **Búsqueda en la biblioteca espectral** — coincidencias clasificadas con puntuaciones de similitud y citas DOI
- **Explicación de picos por IA** — atribuciones de grupos funcionales respaldadas por un grafo de conocimiento químico
- **Informe tri-axial completo** — identificación automática multi-etapa con URL compartible
- **Extracción de imagen a CSV** — digitaliza curvas espectrales desde figuras publicadas
- **Mesa de trabajo de formulación** — desformulación multi-componente

Guías de configuración: https://ftir.fun/ai-integration/

---

## Enlaces

| Recurso | URL |
|---------|-----|
| Sitio web | https://ftir.fun |
| Guía de configuración | https://ftir.fun/ai-integration/ |
| Documentación API | https://ftir.fun/api-docs/ |
| Endpoint MCP | https://ftir.fun/mcp |
| Server card | https://ftir.fun/.well-known/mcp/server-card.json |
| Smithery | https://smithery.ai/servers/hlin2097/ftirfun |
| MCP.so | https://mcp.so/server/ftir-spectral-search/ftir_fun |
| PyPI | https://pypi.org/project/ftirfun-mcp/ |
