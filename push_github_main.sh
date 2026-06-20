#!/usr/bin/env bash
set -euo pipefail

REMOTE="${1:-origin}"
BRANCH="${2:-main}"
COMMIT_MESSAGE="${3:-chore: sync ftirfun-mcp changes}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}"
DEFAULT_SHARED_ENV="/home/bob/projects/ftirfun/.env"
ENV_FILE="${GITHUB_ENV_FILE:-${REPO_ROOT}/.env}"

if [[ ! -f "${ENV_FILE}" ]]; then
  if [[ -f "${DEFAULT_SHARED_ENV}" ]]; then
    ENV_FILE="${DEFAULT_SHARED_ENV}"
  else
    echo "Missing env file: ${ENV_FILE}" >&2
    echo "Shared fallback env also missing: ${DEFAULT_SHARED_ENV}" >&2
    exit 1
  fi
fi

set -a
source "${ENV_FILE}"
set +a

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "GITHUB_TOKEN is not set in ${ENV_FILE}" >&2
  exit 1
fi

cd "${REPO_ROOT}"

if ! git diff --quiet || ! git diff --cached --quiet; then
  git add -A -- .
  if ! git diff --cached --quiet; then
    git commit -m "${COMMIT_MESSAGE}"
  else
    echo "No staged changes after add; skipping commit."
  fi
else
  echo "No local changes to commit."
fi

ASKPASS_FILE="$(mktemp)"
cleanup() {
  rm -f "${ASKPASS_FILE}"
}
trap cleanup EXIT

cat > "${ASKPASS_FILE}" <<'EOF'
#!/usr/bin/env bash
case "$1" in
  *Username*) printf '%s\n' "x-access-token" ;;
  *Password*) printf '%s\n' "${GITHUB_TOKEN}" ;;
  *) printf '\n' ;;
esac
EOF
chmod 700 "${ASKPASS_FILE}"

GIT_ASKPASS="${ASKPASS_FILE}" GIT_TERMINAL_PROMPT=0 git push "${REMOTE}" "${BRANCH}"
