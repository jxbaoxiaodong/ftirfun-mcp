[中文](README.zh.md) | [English](README.md) | [Español](README.es.md) | Français | [日本語](README.ja.md)

# FTIR.fun — Serveur MCP

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

Serveur MCP et client REST pour **[FTIR.fun](https://ftir.fun)** — donne aux assistants IA et pipelines de code un accès direct à plus de 130 000 spectres FTIR infrarouges de référence pour l'identification de matériaux, l'explication de pics et la recherche dans la bibliothèque spectrale.

## Outils disponibles

| Outil | Fonction |
|-------|----------|
| [`analyze_ftir_spectrum`](#analyze_ftir_spectrum) | Identifier un spectre FTIR inconnu — accepte des pics, une requête en langage naturel ou un fichier instrument (28+ formats). Retourne des correspondances classées avec scores et DOI. |
| [`explain_peaks`](#explain_peaks) | Expliquer un ou plusieurs pics infrarouges — attribution de groupes fonctionnels sans recherche complète. |
| [`parse_ftir_spectrum`](#parse_ftir_spectrum) | Analyser un fichier instrument FTIR brut en points de données et pics détectés. |
| [`find_spectra`](#find_spectra) | Rechercher dans la bibliothèque de 130 000+ spectres par nom, CAS ou mots-clés. Retourne les données de courbe. |
| [`submit_ftir_report`](#submit_ftir_report) | Soumettre un spectre au workflow tri-axial complet (même analyse multi-étapes que le site). |
| [`get_ftir_report_status`](#get_ftir_report_status) | Interroger la progression du rapport ; retourne le résultat structuré et l'URL partageable. |
| [`fetch_result`](#fetch_result) | Récupérer un résultat historique FTIR.fun par numéro de rapport. |

---

## Obtenir une clé API

1. Connectez-vous sur [ftir.fun](https://ftir.fun) — les nouveaux comptes incluent des crédits d'essai gratuits.
2. Accédez à **Compte → Clés API** et cliquez sur **Générer**.
3. Copiez la clé immédiatement (commence par `ftir_` ; affichée une seule fois).

```
# Pour MCP (hébergé)
Authorization: Bearer ftir_your_key_here

# Pour l'API REST
X-API-Key: ftir_your_key_here
```

---

## Outils MCP

Le point de terminaison MCP hébergé `https://ftir.fun/mcp` expose sept outils.

---

### `analyze_ftir_spectrum`

Rechercher des correspondances dans la bibliothèque spectrale FTIR pour un spectre inconnu.

**Paramètres**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `query` | string | Non | Requête FTIR en langage naturel — les positions de pics sont extraites automatiquement. |
| `peaks` | number[] | Non | Positions de pics FTIR en cm⁻¹ (ex. `[1736, 1379, 1241]`). |
| `file_base64` | string | Non | Fichier instrument FTIR encodé en base64. Supporte 28+ formats. |
| `filename` | string | Non | Nom de fichier original pour la détection de format. |
| `top_k` | integer | Non | Nombre de candidats à retourner (1–50, défaut 15). |
| `tolerance_cm1` | integer | Non | Tolérance de correspondance en cm⁻¹ (1–30, défaut 8). |

**Retourne :** Matériaux candidats classés avec scores de similarité, preuves par pic (DOI), et niveaux de confiance.

**Exemple**
```
Identifie ce spectre infrarouge : pics à 2915, 1715, 1450, 1260, 1090 cm-1.
```

---

### `explain_peaks`

Expliquer un ou plusieurs pics infrarouges FTIR sans recherche complète.

**Paramètres**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `query` | string | Non | Question sur les pics en langage naturel. |
| `peaks` | number[] | Non | Une ou plusieurs positions de pics en cm⁻¹. |
| `sampling_mode` | string | Non | `ATR`, `Thin Film`, `KBr Pellet`, etc. |

---

### `parse_ftir_spectrum`

Analyser un fichier instrument FTIR encodé en base64 en points de courbe alignés et pics détectés.

**Paramètres**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `file_base64` | string | Oui | Fichier FTIR encodé en base64. |
| `filename` | string | Oui | Nom de fichier original. |

---

### `find_spectra`

Trouver des spectres FTIR de référence par nom, CAS ou mots-clés.

**Paramètres**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `query` | string | Oui | Nom de substance, CAS, `NUM`, ou mots-clés. |
| `limit` | integer | Non | Nombre de résultats (1–20, défaut 10). |

---

### `submit_ftir_report`

Soumettre un spectre au workflow tri-axial complet. Retourne `task_id` et `result_num`.

**Paramètres**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `file_base64` | string | Oui | Fichier FTIR encodé en base64. |
| `filename` | string | Oui | Nom de fichier original. |

---

### `get_ftir_report_status`

Interroger le statut d'un rapport soumis. Retourne `report_view` et `report_url` une fois terminé.

**Paramètres**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `task_id` | string | Oui | `task_id` retourné par `submit_ftir_report`. |

---

### `fetch_result`

Récupérer un résultat historique FTIR.fun par numéro de rapport.

**Paramètres**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `result_num` | string | Oui | Numéro de rapport FTIR.fun. |
| `language_code` | string | Non | Langue d'affichage (défaut `en`). |

---

## API REST

Appelez FTIR.fun depuis n'importe quel langage — Python, JavaScript, R, MATLAB, Go. Idéal pour les intégrations LIMS, le traitement par lots de spectres infrarouges, ou l'ajout de recherche spectrale à votre application.

Référence complète : https://ftir.fun/api-docs/

### Vérification de l'état (sans clé)

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### Identifier un spectre infrarouge inconnu — pics

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

### Identifier depuis un fichier instrument

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

### Expliquer des pics infrarouges

```bash
curl -X POST https://ftir.fun/ftir/explain_peaks \
  -H "X-API-Key: ftir_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"peaks": [1715, 2915], "sampling_mode": "ATR"}'
```

---

## Configuration client MCP

URL : `https://ftir.fun/mcp` avec token `Bearer`. Aucune installation locale requise.

### VS Code

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

### Claude Code

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

---

## Auto-hébergement (proxy local)

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
pip install ftirfun-mcp
ftirfun-mcp
```

---

## À propos de FTIR.fun

**[FTIR.fun](https://ftir.fun)** est une plateforme cloud d'analyse par spectrométrie infrarouge, utilisée par des chercheurs et ingénieurs dans plus de 52 pays. Elle donne accès à une bibliothèque constamment mise à jour de **plus de 130 000 spectres FTIR de référence**.

Fonctionnalités sur [ftir.fun](https://ftir.fun) :

- **Recherche dans la bibliothèque spectrale** — correspondances classées avec scores et citations DOI
- **Explication des pics par IA** — groupes fonctionnels via graphe de connaissances chimiques
- **Rapport tri-axial complet** — identification multi-étapes avec URL partageable
- **Extraction image vers CSV** — numérisation de courbes spectrales
- **Atelier de formulation** — déformulation multi-composants

Guides de configuration : https://ftir.fun/ai-integration/

---

## Liens

| Ressource | URL |
|-----------|-----|
| Site web | https://ftir.fun |
| Guide de configuration | https://ftir.fun/ai-integration/ |
| Documentation API | https://ftir.fun/api-docs/ |
| Endpoint MCP | https://ftir.fun/mcp |
| Server card | https://ftir.fun/.well-known/mcp/server-card.json |
| Smithery | https://smithery.ai/servers/hlin2097/ftirfun |
| MCP.so | https://mcp.so/server/ftir-spectral-search/ftir_fun |
| PyPI | https://pypi.org/project/ftirfun-mcp/ |
