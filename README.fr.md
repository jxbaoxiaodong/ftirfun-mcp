[中文](README.zh.md) | [English](README.md) | [Español](README.es.md) | Français | [日本語](README.ja.md)

# FTIR.fun — Serveur MCP

[![smithery badge](https://smithery.ai/badge/hlin2097/ftirfun)](https://smithery.ai/servers/hlin2097/ftirfun)
[![MCP.so](https://img.shields.io/badge/MCP.so-listed-blue)](https://mcp.so/server/ftir-spectral-search/ftir_fun)
[![PyPI](https://img.shields.io/pypi/v/ftirfun-mcp)](https://pypi.org/project/ftirfun-mcp/)

Serveur MCP et client REST pour **[FTIR.fun](https://ftir.fun)** — plateforme en ligne de spectrométrie infrarouge et d'identification de matériaux.

---

## Qu'est-ce que FTIR.fun ?

**[FTIR.fun](https://ftir.fun)** est une plateforme cloud d'analyse par spectrométrie infrarouge, utilisée par des chercheurs et ingénieurs dans plus de 52 pays. Elle donne accès à une bibliothèque constamment mise à jour de **plus de 130 000 spectres FTIR de référence**, couvrant les polymères, les additifs, les revêtements, les excipients pharmaceutiques et les produits chimiques industriels.

Fonctionnalités principales sur [ftir.fun](https://ftir.fun) :

- **Recherche dans la bibliothèque spectrale** — déposez un fichier instrument ou saisissez des positions de pics ; obtenez des correspondances classées avec scores de similarité et citations DOI
- **Explication des pics par IA** — interrogez n'importe quel nombre d'onde ; recevez des attributions de groupes fonctionnels appuyées sur un graphe de connaissances chimiques
- **Rapport tri-axial complet** — identification automatique multi-étapes avec URL de résultat partageable
- **Extraction image vers CSV** — numérisez une courbe spectrale depuis une figure publiée
- **Atelier de formulation** — déformulation multi-composants et analyse de mélanges inconnus

Ce package permet à votre assistant IA (Claude, Cursor, VS Code Copilot, Gemini CLI…) ou à votre pipeline de code d'appeler FTIR.fun directement, sans changer de navigateur.

**Guides de configuration pas à pas et documentation API :** https://ftir.fun/ai-integration/

---

## Obtenir une clé API

1. Connectez-vous sur [ftir.fun](https://ftir.fun) — les nouveaux comptes incluent des crédits d'essai gratuits.
2. Accédez à **Compte → Clés API** et cliquez sur **Générer**.
3. Copiez la clé immédiatement (commence par `ftir_` ; affichée une seule fois).

L'authentification utilise un seul en-tête — sans OAuth, sans redirection navigateur :

```
# Pour MCP (hébergé)
Authorization: Bearer ftir_your_key_here

# Pour l'API REST
X-API-Key: ftir_your_key_here
```

---

## MCP Hébergé (Recommandé)

Connectez-vous directement au point de terminaison de production — aucune installation locale requise.

### VS Code (mode Agent GitHub Copilot)

Créez `.vscode/mcp.json` dans votre projet :

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
URL :    https://ftir.fun/mcp
En-tête : Authorization: Bearer ftir_your_key_here
```

Configuration en une ligne pour **Claude Code** :

```bash
claude mcp add --transport http ftirfun https://ftir.fun/mcp \
  --header "Authorization: Bearer ftir_your_key_here"
```

### Cursor

Créez ou éditez `~/.cursor/mcp.json` :

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

Éditez `~/.gemini/settings.json` :

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

### Prompts de test

```
Utilise FTIR.fun pour expliquer le pic FTIR à 1715 cm-1.
Identifie ce polymère à partir de ses pics FTIR : 2915, 1715, 1450 cm-1.
Recherche des spectres de référence de polypropylène dans FTIR.fun.
```

---

## API REST

Appelez FTIR.fun depuis n'importe quel langage — Python, JavaScript, R, MATLAB, Go.

Référence complète : https://ftir.fun/api-docs/

### Vérification de l'état (sans clé)

```bash
curl https://ftir.fun/health
# → {"status":"ok","service":"ftirfun-api"}
```

### Identifier un spectre inconnu — pics

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

Supporte 28+ formats : Thermo `.spa`/`.spc`, Bruker `.opus`, PerkinElmer `.sp`, JCAMP-DX, CSV, Excel, etc.

---

## Outils (Tools)

| Outil | Description |
|-------|-------------|
| `parse_ftir_spectrum` | Analyse un fichier instrument encodé en base64 |
| `analyze_ftir_spectrum` | Recherche des correspondances pour un spectre inconnu |
| `submit_ftir_report` | Soumet un spectre au workflow tri-axial complet |
| `get_ftir_report_status` | Interroge l'état d'un rapport soumis |
| `explain_peaks` | Explique un ou plusieurs pics sans recherche complète |
| `find_spectra` | Trouve des spectres de référence par nom, CAS ou mots-clés |
| `fetch_result` | Récupère un résultat historique par numéro de rapport |

---

## Auto-hébergement (proxy local)

```bash
export FTIRFUN_API_KEY="your-ftirfun-api-key"
pip install ftirfun-mcp
ftirfun-mcp
```

---

## Liens

| Ressource | URL |
|-----------|-----|
| Site web | https://ftir.fun |
| Guide de configuration | https://ftir.fun/ai-integration/ |
| Documentation API | https://ftir.fun/api-docs/ |
| Point de terminaison MCP | https://ftir.fun/mcp |
| Smithery | https://smithery.ai/servers/hlin2097/ftirfun |
| PyPI | https://pypi.org/project/ftirfun-mcp/ |
