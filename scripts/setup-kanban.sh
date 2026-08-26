#!/usr/bin/env bash
# Crea el Kanban de NEXO (labels, milestones e issues epics) de forma idempotente.
# Se ejecuta en CI al mergear a dev (usa GITHUB_TOKEN, sin permisos extra).
# Tambien es ejecutable en local:  REPO=adrianaarang/Nexo gh auth login && bash scripts/setup-kanban.sh
set -o pipefail
REPO="${REPO:-adrianaarang/Nexo}"

label() {
  local name="$1" desc="$2" color="$3"
  gh label create "$name" --description "$desc" --color "$color" -R "$REPO" 2>/dev/null || true
}

milestone() {
  local title="$1" desc="$2"
  gh api "repos/$REPO/milestones" -f title="$title" -f description="$desc" >/dev/null 2>&1 || true
}

issue() {
  local title="$1" body="$2" labels="$3" ms="$4" assignee="$5" close="$6"
  local n
  n=$(gh issue list -R "$REPO" --search "$title" --state all --json number --jq 'length' 2>/dev/null || echo 0)
  if [ -n "$n" ] && [ "$n" != "0" ]; then
    echo "skip (ya existe): $title"
    return
  fi
  local cmd=(gh issue create -R "$REPO" -t "$title" -b "$body" -l "$labels")
  [ -n "$ms" ] && cmd+=(-m "$ms")
  [ -n "$assignee" ] && cmd+=(-a "$assignee")
  local out num
  out=$("${cmd[@]}" 2>&1)
  num=$(printf '%s' "$out" | grep -oE '/issues/[0-9]+' | head -1 | grep -oE '[0-9]+')
  echo "creado #${num:-?}: $title"
  if [ "$close" = "closed" ] && [ -n "$num" ]; then
    gh issue close "$num" -R "$REPO" \
      -c "Cerrado automaticamente por setup-kanban: trabajo ya completado en su rama." >/dev/null 2>&1 || true
    echo "  -> cerrado (done)"
  fi
}

# ---- Labels (sirven tambien como agrupacion por equipo en el tablero) ----
label "base-comun" "Base comun (pre-reparto)" "0E8A16"
label "equipo-1"   "Equipo 1 - Mapa de necesidades" "1F6FEB"
label "equipo-2"   "Equipo 2 - Alertas oficiales" "D93F0B"
label "equipo-3"   "Equipo 3 - Voluntariado y donaciones" "6F42C1"
label "equipo-4"   "Equipo 4 - Personas y modo offline" "2088FF"
label "futuro"     "Horizonte futuro - Resilience OS" "BFD4F2"
label "kanban"     "Creado por setup-kanban (idempotente)" "CCCCCC"

# ---- Milestones ----
milestone "Sprint 1 (MVP)" "MVP end-to-end demo"
milestone "Sprint 2" "Decisiones + offline + cache + Proteccion Civil"

# ---- Issues (epics) ----
issue "Base comun - revision previa al reparto" \
"Revisar antes del reparto (manifiesto docs/manifiesto.md):
- [ ] index.html, menu, logo, estilos generales
- [ ] apiClient.js (cliente comun de API)
- [ ] main.py/config.py + BD (necesidades, voluntarios, donaciones, personas)
- [ ] seed.py
- [ ] Visto bueno de 1 persona por equipo (sin PR todavia)" \
"base-comun,kanban" "Sprint 1 (MVP)" "adrianaarang" "closed"

issue "Equipo 1 - Mapa de necesidades" \
"Frontend pages/mapa.html + js/core/mapa-necesidades/. Backend modules/necesidades/ (crear, listar, estado abierta->cubierta).
- [ ] Pagina mapa.html + estilos base
- [ ] Mapa, tarjeta de necesidad, llamadas API
- [ ] Backend CRUD + cambio de estado
- [ ] pytest verde + integrado en dev
- [ ] Decision: prioridad de necesidad; filtro por tipo" \
"equipo-1,kanban" "Sprint 1 (MVP)" "SiR0N"

issue "Equipo 2 - Alertas oficiales" \
"Frontend pages/alertas.html + js/core/alertas-oficiales/. Backend modules/alertas/ + integrations/ (GDACS + fallback mock).
- [ ] Backend GDACS + fallback (Sprint 1 casi listo en feature/alerts)
- [ ] Frontend alertas.html + alerts.js (crearTarjeta) + alertsApi.js
- [ ] PR feature/alerts -> dev
- [ ] Decision (Sprint 2): vacio sin alertas; cache GDACS
- [ ] Hueco Proteccion Civil (TODO)" \
"equipo-2,kanban" "Sprint 1 (MVP)" "juandelaf1" "closed"

issue "Equipo 3 - Voluntariado y donaciones" \
"Frontend voluntariado.html, donaciones.html + js/core/voluntariado-donaciones/. Backend modules/voluntariado/ + modules/donaciones/.
- [ ] Paginas voluntariado y donaciones
- [ ] Backend voluntariado/ y donaciones/
- [ ] pytest verde + integrado
- [ ] Decision: marcar donacion cubierta; auto-asignacion de voluntario" \
"equipo-3,kanban" "Sprint 1 (MVP)" "LauraSilRu"

issue "Equipo 4 - Personas y modo offline" \
"Frontend personas.html, estoy-bien.html + js/siguiente/ (registro + offline). Backend modules/personas/ + sync/.
- [ ] Backend registro + endpoint estoy-bien (Sprint 1)
- [ ] Frontend registro + offline
- [ ] Decision (Sprint 2): duplicados persona desaparecida; probar offline (modo avion)" \
"equipo-4,kanban" "Sprint 1 (MVP)" "Isabela-Tellez"

issue "Futuro - Resilience OS" \
"Horizonte 'A definir' (manifiesto §7): simulador what-if, indice de resiliencia, puntos de fallo, presupuesto, stress tests, equidad, Resilience API / Climate OS." \
"futuro,kanban" "" ""

echo "Kanban: issues procesados."
