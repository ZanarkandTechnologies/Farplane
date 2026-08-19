#!/usr/bin/env bash
# Generated setup wizards copy this library, then replace only the section
# below SETUP_ADVISOR_STAGES. The library intentionally handles human gates;
# agent-operable setup belongs in the setup-advisor run that generated it.

set -euo pipefail

if [[ -t 1 ]] && command -v tput >/dev/null 2>&1 && [[ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]]; then
  WIZ_BOLD=$(tput bold)
  WIZ_DIM=$(tput dim)
  WIZ_RESET=$(tput sgr0)
  WIZ_BLUE=$(tput setaf 4)
  WIZ_GREEN=$(tput setaf 2)
  WIZ_YELLOW=$(tput setaf 3)
else
  WIZ_BOLD=""
  WIZ_DIM=""
  WIZ_RESET=""
  WIZ_BLUE=""
  WIZ_GREEN=""
  WIZ_YELLOW=""
fi

TOTAL_STAGES=0
WIZARD_STAGE_INDEX=0
WIZARD_CONFIGURED=()
WIZARD_SKIPPED=()

wizard_clear() {
  [[ -t 1 ]] || return 0
  if command -v tput >/dev/null 2>&1; then
    tput clear
  else
    printf '\033[2J\033[3J\033[H'
  fi
}

wizard_banner() {
  wizard_clear
  printf '\n%s%s%s%s\n' "$WIZ_BOLD" "$WIZ_BLUE" "$1" "$WIZ_RESET"
  printf '%s%s human-gated stage(s). Automatable setup was handled before this wizard.%s\n\n' \
    "$WIZ_DIM" "$TOTAL_STAGES" "$WIZ_RESET"
  wizard_pause "Press Enter to begin"
}

wizard_stage() {
  wizard_clear
  WIZARD_STAGE_INDEX=$((WIZARD_STAGE_INDEX + 1))
  printf '\n%s%sStage %s/%s: %s%s\n' \
    "$WIZ_BOLD" "$WIZ_BLUE" "$WIZARD_STAGE_INDEX" "$TOTAL_STAGES" "$1" "$WIZ_RESET"
}

wizard_say() { printf ' %s\n' "$1"; }
wizard_step() { printf ' %s•%s %s\n' "$WIZ_BLUE" "$WIZ_RESET" "$1"; }
wizard_note() { printf ' %s%s%s\n' "$WIZ_DIM" "$1" "$WIZ_RESET"; }
wizard_warn() { printf ' %s! %s%s\n' "$WIZ_YELLOW" "$1" "$WIZ_RESET"; }

wizard_open_url() {
  local url="$1"
  printf ' %sOpening%s %s\n' "$WIZ_GREEN" "$WIZ_RESET" "$url"
  if command -v wslview >/dev/null 2>&1; then
    wslview "$url" >/dev/null 2>&1 || true
  elif command -v explorer.exe >/dev/null 2>&1; then
    explorer.exe "$url" >/dev/null 2>&1 || true
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" >/dev/null 2>&1 || true
  elif command -v open >/dev/null 2>&1; then
    open "$url" >/dev/null 2>&1 || true
  else
    wizard_warn "Could not open a browser; visit the URL manually."
  fi
}

wizard_pause() {
  printf ' %s%s%s ' "$WIZ_DIM" "${1:-Press Enter to continue}" "$WIZ_RESET"
  read -r _ || true
}

wizard_confirm() {
  local reply=""
  printf ' %s? %s [y/N]%s ' "$WIZ_YELLOW" "$1" "$WIZ_RESET"
  read -r reply || true
  [[ "$reply" =~ ^[Yy]$ ]]
}

wizard_ask() {
  local variable_name="$1" prompt="$2" value=""
  printf ' %s%s%s ' "$WIZ_BOLD" "$prompt" "$WIZ_RESET"
  read -r value
  printf -v "$variable_name" '%s' "$value"
}

wizard_ask_secret() {
  local variable_name="$1" prompt="$2" value=""
  printf ' %s%s%s ' "$WIZ_BOLD" "$prompt" "$WIZ_RESET"
  read -rs value
  printf '\n'
  printf -v "$variable_name" '%s' "$value"
}

wizard_store_doppler_secret() {
  local name="$1" value="$2"
  if ! command -v doppler >/dev/null 2>&1; then
    WIZARD_SKIPPED+=("Doppler secret $name")
    wizard_warn "Doppler is unavailable; $name was not persisted."
    return 1
  fi
  if printf '%s' "$value" | doppler secrets set "$name" --silent >/dev/null; then
    WIZARD_CONFIGURED+=("Doppler secret $name")
    printf ' %s✓ stored%s Doppler secret %s\n' "$WIZ_GREEN" "$WIZ_RESET" "$name"
    return 0
  fi
  WIZARD_SKIPPED+=("Doppler secret $name")
  wizard_warn "Doppler rejected $name; no value was printed."
  return 1
}

wizard_store_github_secret() {
  local name="$1" value="$2"
  if ! command -v gh >/dev/null 2>&1 || ! gh auth status >/dev/null 2>&1; then
    WIZARD_SKIPPED+=("GitHub secret $name")
    wizard_warn "GitHub CLI is unavailable or unauthenticated; $name was not persisted."
    return 1
  fi
  if printf '%s' "$value" | gh secret set "$name" >/dev/null; then
    WIZARD_CONFIGURED+=("GitHub secret $name")
    printf ' %s✓ stored%s GitHub secret %s\n' "$WIZ_GREEN" "$WIZ_RESET" "$name"
    return 0
  fi
  WIZARD_SKIPPED+=("GitHub secret $name")
  wizard_warn "GitHub rejected $name; no value was printed."
  return 1
}

wizard_set_github_variable() {
  local name="$1" value="$2"
  if ! command -v gh >/dev/null 2>&1 || ! gh auth status >/dev/null 2>&1; then
    WIZARD_SKIPPED+=("GitHub variable $name")
    wizard_warn "GitHub CLI is unavailable or unauthenticated; $name was not persisted."
    return 1
  fi
  if printf '%s' "$value" | gh variable set "$name" >/dev/null; then
    WIZARD_CONFIGURED+=("GitHub variable $name")
    printf ' %s✓ stored%s GitHub variable %s\n' "$WIZ_GREEN" "$WIZ_RESET" "$name"
    return 0
  fi
  WIZARD_SKIPPED+=("GitHub variable $name")
  wizard_warn "GitHub rejected variable $name."
  return 1
}

wizard_finish() {
  wizard_clear
  printf '\n%s%sHuman-gated stages finished%s\n' "$WIZ_BOLD" "$WIZ_GREEN" "$WIZ_RESET"
  if (( ${#WIZARD_CONFIGURED[@]} )); then
    wizard_note "Configured names: ${WIZARD_CONFIGURED[*]}"
  fi
  if (( ${#WIZARD_SKIPPED[@]} )); then
    wizard_warn "Still unresolved:"
    local item
    for item in "${WIZARD_SKIPPED[@]}"; do
      wizard_note "- $item"
    done
    return 1
  fi
}

# SETUP_ADVISOR_STAGES
# Replace this placeholder in a generated copy. Do not edit the library above.
wizard_warn "This is the setup-advisor template, not an authored wizard."
exit 2
