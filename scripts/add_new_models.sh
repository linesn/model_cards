#!/usr/bin/env bash
# Add model cards for slugs in model_slugs.txt that lack a card yet.
# Runs in GitLab CI (see .gitlab-ci.yml); locally set DRY_RUN=1 to skip the push.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

BOT_NAME="${BOT_NAME:-Model Card Bot}"
BOT_EMAIL="${BOT_EMAIL:-model-card-bot@users.noreply.gitlab.com}"
DRY_RUN="${DRY_RUN:-0}"

if [[ "$DRY_RUN" != "1" ]] && [[ -z "${CI_SERVER_HOST:-}" || -z "${CI_PROJECT_PATH:-}" ]]; then
    echo "ERROR: not running inside GitLab CI (CI_SERVER_HOST/CI_PROJECT_PATH unset). Local runs must set DRY_RUN=1." >&2
    exit 1
fi

SLUGS_FILE="model_slugs.txt"
if [[ ! -f "$SLUGS_FILE" ]]; then
    echo "ERROR: $SLUGS_FILE not found in $REPO_ROOT" >&2
    exit 1
fi

# --- 1. Diff: slugs without a card ---------------------------------------------
all_slugs=()
while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line#"${line%%[![:space:]]*}"}"   # trim leading whitespace
    line="${line%"${line##*[![:space:]]}"}"   # trim trailing whitespace
    if [[ -z "$line" || "$line" == \#* ]]; then
        continue
    fi
    all_slugs+=("$line")
done < "$SLUGS_FILE"

new_slugs=()
for slug in "${all_slugs[@]}"; do
    if [[ ! -f "${slug}/model_records.json" ]]; then
        new_slugs+=("$slug")
    fi
done

if [[ ${#new_slugs[@]} -eq 0 ]]; then
    echo "Nothing to do: all ${#all_slugs[@]} slugs already have cards."
    exit 0
fi

echo "New slugs to fetch: ${new_slugs[*]}"

# --- 3. Fetch -------------------------------------------------------------------
tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT
printf '%s\n' "${new_slugs[@]}" > "$tmp_file"

fetch_rc=0
python scripts/gather_models.py --models-file "$tmp_file" --output-dir "$REPO_ROOT" || fetch_rc=$?
if [[ $fetch_rc -ne 0 ]]; then
    echo "No models succeeded; not committing."
    exit 1
fi

# --- 4. Verify -------------------------------------------------------------------
declare -A fail_reason=()
verified=()
for slug in "${new_slugs[@]}"; do
    if [[ ! "$slug" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]]; then
        fail_reason[$slug]="invalid slug (expected maker/name)"
    else
        missing=()
        [[ -f "${slug}/model_records.json" ]] || missing+=("model_records.json")
        [[ -f "${slug}/README.txt" ]] || missing+=("README.txt")
        [[ -f "${slug}/model_card.pdf" ]] || missing+=("model_card.pdf")
        if [[ ${#missing[@]} -gt 0 ]]; then
            fail_reason[$slug]="no card produced (missing: ${missing[*]})"
        elif ! head -c 4 "${slug}/model_card.pdf" | grep -q '%PDF'; then
            fail_reason[$slug]="model_card.pdf is not a valid PDF"
        else
            verified+=("$slug")
        fi
    fi
done

# Remove the managed outputs of demoted slugs so the next run re-fetches them
# (without this, the diff step above would see model_records.json and skip).
for slug in "${new_slugs[@]}"; do
    if [[ -n "${fail_reason[$slug]:-}" ]]; then
        rm -f "${slug}/model_records.json" "${slug}/README.txt" "${slug}/model_card.pdf"
        rmdir "${slug}" 2>/dev/null || true
    fi
done

if [[ ${#verified[@]} -eq 0 ]]; then
    echo "No verified cards; not committing."
    exit 1
fi

# --- 5. Commit -------------------------------------------------------------------
git add "${verified[@]}"

names=""
for s in "${verified[@]}"; do
    if [[ -z "$names" ]]; then
        names="$s"
    else
        names="$names, $s"
    fi
done
git -c user.name="$BOT_NAME" -c user.email="$BOT_EMAIL" commit -m "Add ${#verified[@]} model cards: $names"

# --- 6. Push -------------------------------------------------------------------
if [[ "$DRY_RUN" == "1" ]]; then
    echo "DRY_RUN=1: skipping push; commit is local only."
else
    if [[ -n "${GITLAB_PUSH_TOKEN:-}" ]]; then
        push_url="https://oauth2:${GITLAB_PUSH_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git"
    elif [[ -n "${CI_JOB_TOKEN:-}" ]]; then
        push_url="https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git"
    else
        echo "ERROR: no push token available (set GITLAB_PUSH_TOKEN, or let CI_JOB_TOKEN be provided by GitLab)." >&2
        exit 1
    fi
    target_branch="${CI_DEFAULT_BRANCH:-$(git symbolic-ref --short HEAD)}"
    git push "$push_url" "HEAD:refs/heads/${target_branch}"
fi

# --- 7. Report -------------------------------------------------------------------
echo
echo "=== Report ==="
echo "Committed ${#verified[@]} card(s):"
for s in "${verified[@]}"; do
    echo "  OK: $s"
done
if [[ ${#fail_reason[@]} -gt 0 ]]; then
    echo "Failed ${#fail_reason[@]} slug(s):"
    for s in "${new_slugs[@]}"; do
        if [[ -n "${fail_reason[$s]:-}" ]]; then
            echo "  FAIL: $s - ${fail_reason[$s]}"
        fi
    done
fi
