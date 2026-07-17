[中文](README.zh.md) | [English](README.md) | Español | [Français](README.fr.md) | [日本語](README.ja.md)

# FTIR.fun — Servidor MCP

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

Servidor MCP y cliente REST para **[FTIR.fun](https://ftir.fun)** — plataforma en la nube para análisis de espectroscopía infrarroja e identificación de materiales.

---

## ¿Qué es FTIR.fun?

**[FTIR.fun](https://ftir.fun)** es una plataforma en la nube para análisis de espectroscopía infrarroja, utilizada por investigadores e ingenieros en más de 52 países. Ofrece acceso rápido a una biblioteca en constante actualización de **más de 130 000 espectros FTIR de referencia**, que abarca polímeros, aditivos, recubrimientos, fármacos y productos químicos industriales.

Funciones principales en [ftir.fun](https://ftir.fun):

- **Búsqueda en la biblioteca espectral** — sube un archivo de instrumento o pega posiciones de pico; obtén coincidencias ordenadas con puntuaciones de similitud y citas DOI
- **Explicación de picos por IA** — pregunta sobre cualquier número de onda y recibe asignaciones de grupos funcionales respaldadas por un grafo de conocimiento químico
- **Informe tri-axial completo** — identificación automática multi-etapa con URL de resultado compartible
- **Extracción de imagen a CSV** — digitaliza una curva espectral desde una figura publicada
- **Mesa de trabajo de formulación** — desformulación multi-componente y análisis de mezclas desconocidas

Este paquete permite que tu asistente de IA (Claude, Cursor, VS Code Copilot, Gemini CLI…) o tu pipeline de código llame directamente a FTIR.fun sin cambiar al navegador.

**Guías de configuración paso a paso y documentación API:** https://ftir.fun/ai-integration/

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

## MCP Alojado (Recomendado)

Conéctate directamente al endpoint de producción — no se requiere instalación local.

### VS Code (modo Agente de GitHub Copilot)

Crea `.vscode/mcp.json` en tu proyecto:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "ftirfun-api-key",
      "description": "FTIR.fun API key",
      "password": true
    }
  ],
  "servers": {
    "ftirfun": {
      "type": "http",
      "url": "https://ftir.fun/mcp",
      "headers": {
        "Authorization": "Bearer ${input:ftirfun-api-key}"
      }
    }
  }
}
```

### Claude Desktop / Claude Code

```
URL:    https://ftir.fun/mcp
Header: Authorization: Bearer ftir_your_key_here
```

Configuración en una línea para **Claude Code**:

```bash
claude mcp add --transport http ftirfun https://ftir.fun/mcp \
  --header "Authorization: Bearer ftir_your_key_here"
```

### Cursor

Crea o edita `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "ftirfun": {
      "url": "https://ftir.fun/mcp",
      "headers": { "Authorization": "Bearer ftir_your_key_here" }
    }
  }
}
```

### Gemini CLI

Edita `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "ftirfun": {
      "httpUrl": "https://ftir.fun/mcp",
      "headers": { "Authorization": "Bearer ftir_your_key_here" }
    }
  }
}
```

### Prompts de prueba

```
Usa FTIR.fun para explicar el pico FTIR a 1715 cm-1.
Identifica este polímero a partir de sus picos FTIR: 2915, 1715, 1450 cm-1.
Busca espectros de referencia de polipropileno en FTIR.fun.
```

---

## REST API

Llama a FTIR.fun desde cualquier lenguaje — Python, JavaScript, R, MATLAB, Go.

Referencia completa: https://ftir.fun/api-docs/

### Verificación de estado (sin clave)

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### Identificar un espectro desconocido — picos

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

Soporta 28+ formatos: Thermo `.spa`/`.spc`, Bruker `.opus`, PerkinElmer `.sp`, JCAMP-DX, CSV, Excel, etc.

---

## Herramientas (Tools)

| Herramienta | Descripción |
|-------------|-------------|
| `parse_ftir_spectrum` | Analiza un archivo de instrumento codificado en base64 |
| `analyze_ftir_spectrum` | Busca coincidencias en la biblioteca para un espectro desconocido |
| `submit_ftir_report` | Envía un espectro al flujo tri-axial completo |
| `get_ftir_report_status` | Consulta el estado de un informe enviado |
| `explain_peaks` | Explica uno o más picos sin búsqueda completa |
| `find_spectra` | Encuentra espectros de referencia por nombre, CAS o palabras clave |
| `fetch_result` | Recupera un resultado histórico por número de informe |

---

## Auto-alojado (proxy local)

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
pip install ftirfun-mcp
ftirfun-mcp
```

---

## Enlaces

| Recurso | URL |
|---------|-----|
| Sitio web | https://ftir.fun |
| Guía de configuración | https://ftir.fun/ai-integration/ |
| Documentación API | https://ftir.fun/api-docs/ |
| Endpoint MCP | https://ftir.fun/mcp |
| Smithery | https://smithery.ai/servers/hlin2097/ftirfun |
| PyPI | https://pypi.org/project/ftirfun-mcp/ |
