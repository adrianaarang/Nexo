#!/usr/bin/env bash
# Crea/actualiza el Kanban de NEXO (labels, milestones e issues epics) de forma idempotente.
# Se ejecuta en CI al mergear a dev (usa GITHUB_TOKEN, sin permisos extra) y tambien en local:
#   REPO=adrianaarang/Nexo gh auth login && bash scripts/setup-kanban.sh
#
# Comportamiento:
#   - Si un issue con el mismo titulo ya existe, se ACTUALIZA su cuerpo y labels (mantiene trazabilidad).
#   - Los issues de Sprint 2 se cierran solos al mergear el PR de integracion de cada grupo si este
#     incluye "Closes #<num>".
#   - Al crearse, los issues de Sprint 1 obsoletos (#41, #43, #44) se cierran con un comentario de
#     trazabilidad hacia su equivalente de Sprint 2.
set -o pipefail
REPO="${REPO:-adrianaarang/Nexo}"

LAST_ISSUE_NUM=""

label() {
  local name="$1" desc="$2" color="$3"
  gh label create "$name" --description "$desc" --color "$color" -R "$REPO" 2>/dev/null || true
}

milestone() {
  local title="$1" desc="$2"
  gh api "repos/$REPO/milestones" -f title="$title" -f description="$desc" >/dev/null 2>&1 || true
}

# Crea el issue si no existe; si existe, actualiza cuerpo+labels. Guarda el numero en LAST_ISSUE_NUM.
issue() {
  local title="$1" body="$2" labels="$3" ms="$4" assignee="$5" close="$6"
  local found existing
  found=$(gh issue list -R "$REPO" --state all --json number,title --jq "[.[] | select(.title==\"$title\")] | length" 2>/dev/null || echo 0)
  if [ -n "$found" ] && [ "$found" != "0" ]; then
    existing=$(gh issue list -R "$REPO" --state all --json number,title --jq "[.[] | select(.title==\"$title\")] | .[0].number" 2>/dev/null || true)
    LAST_ISSUE_NUM="$existing"
    # Actualiza para mantener trazabilidad (idempotente: no falla si no cambia).
    gh issue edit "$existing" -R "$REPO" -b "$body" -l "$labels" >/dev/null 2>&1 || true
    echo "skip (ya existe #${existing:-?}, actualizado): $title"
    return
  fi
  local cmd=(gh issue create -R "$REPO" -t "$title" -b "$body" -l "$labels")
  [ -n "$ms" ] && cmd+=(-m "$ms")
  [ -n "$assignee" ] && cmd+=(-a "$assignee")
  local out num
  out=$("${cmd[@]}" 2>&1)
  num=$(printf '%s' "$out" | grep -oE '/issues/[0-9]+' | head -1 | grep -oE '[0-9]+')
  LAST_ISSUE_NUM="$num"
  echo "creado #${num:-?}: $title"
  if [ "$close" = "closed" ] && [ -n "$num" ]; then
    gh issue close "$num" -R "$REPO" \
      -c "Cerrado automaticamente por setup-kanban: trabajo ya completado en su rama." >/dev/null 2>&1 || true
    echo "  -> cerrado (done)"
  fi
}

close_s1() {
  local num="$1" newnum="$2" mod="$3"
  [ -z "$newnum" ] && return
  gh issue close "$num" -R "$REPO" \
    -c "Sprint 1 obsoleto: el modulo pasa a **$mod** en Sprint 2. Trazabilidad -> issue #$newnum." \
    >/dev/null 2>&1 || true
  echo "cerrado S1 #$num -> #$newnum ($mod)"
}

# ---- Labels (sirven tambien como agrupacion por equipo en el tablero) ----
label "base-comun" "Base comun (pre-reparto)" "0E8A16"
label "equipo-1"   "Equipo 1 - Necesidades" "1F6FEB"
label "equipo-2"   "Equipo 2 - Alertas + activacion de crisis" "D93F0B"
label "equipo-3"   "Equipo 3 - Ayudas (donacion + voluntariado)" "6F42C1"
label "equipo-4"   "Equipo 4 - Mapa + Interfaz principal" "2088FF"
label "futuro"     "Horizonte futuro - Resilience OS" "BFD4F2"
label "kanban"     "Creado por setup-kanban (idempotente)" "CCCCCC"

# ---- Milestones ----
milestone "Sprint 1 (MVP)" "MVP end-to-end demo"
milestone "Sprint 2" "Reparto final 27/08: Necesidades, Alertas, Ayudas, Mapa"

# ---- Issues (epics) Sprint 2 ----
issue "Equipo 1 - Necesidades" \
"Frontend pages/mapa.html (formulario) + js/core/mapa-necesidades/ + geocodificacion.js. Backend modules/necesidades/ (services.py, categorias, direccion, intensidad).
- [ ] Categorias (8): agua, alimentos, parafarmacia, ropa, higiene, refugio, transporte, otros
- [ ] Estados: abierta -> cubierta (se retiro en_proceso)
- [ ] Campo direccion (texto legible geocodificado) + latitud/longitud
- [ ] Intensidad por conteo (verde/naranja/rojo) en el mapa
- [ ] Contrato JSON hacia el mapa: {id, type, latitude, longitude, status, direccion}
- [ ] pytest + JS tests verdes
- [ ] Detalle en docs/equipos/grupo1-tareas.md
Al mergear el PR de integracion del grupo, incluir 'Closes #<num>' para cerrar este issue." \
"equipo-1,kanban" "Sprint 2" "SiR0N"
E1="$LAST_ISSUE_NUM"

issue "Equipo 2 - Alertas + activacion de crisis" \
"Backend modules/alertas/ (Juan) + frontend alertas-oficiales (Javi) + crisis.js/mapa (Luis) + integraciones GDACS/Proteccion Civil (Vanessa).
- [ ] Backend gestor: crear, activar, alto-riesgo, desactivar (rama alerts, Juan)
- [ ] Contrato mapa: {id, risk_level, status, zone}
- [ ] ALTO RIESGO desbloquea necesidades/ayudas en la zona
- [ ] Frontend alertas.html + crisis.js (activacion)
- [ ] Integracion GDACS + Proteccion Civil
- [ ] Detalle en docs/equipos/grupo2-tareas.md
Al mergear el PR de integracion del grupo, incluir 'Closes #<num>'." \
"equipo-2,kanban" "Sprint 2" "juandelaf1"
E2="$LAST_ISSUE_NUM"

issue "Equipo 3 - Ayudas (donacion + voluntariado)" \
"Frontend donaciones.html/voluntariado.html + js/core/voluntariado-donaciones/. Backend modules/donaciones/ + modules/voluntariado/.
- [ ] Unificar en modulo 'Ayudas': 3 tipos (recursos, servicios, tiempo/voluntariado con nombre+DNI)
- [ ] Contrato JSON hacia el mapa: {id, type, category, latitude, longitude, status}
- [ ] Reusar logica de voluntariado/donaciones de Sprint 1
- [ ] pytest + JS tests verdes
- [ ] Detalle en docs/equipos/grupo3-tareas.md
Al mergear el PR de integracion del grupo, incluir 'Closes #<num>'." \
"equipo-3,kanban" "Sprint 2" "LauraSilRu"
E3="$LAST_ISSUE_NUM"

issue "Equipo 4 - Mapa + Interfaz principal" \
"Frontend pages/mapa.html + js/core/mapa-necesidades/mapaNecesidades.js (consumo de alertas y necesidades). Interfaz principal.
- [ ] Consumir alertas (risk_level/status/zone) y necesidades (type/status) via contratos
- [ ] Resaltar zona de alerta ALTO RIESGO en el mapa
- [ ] Intensidad por conteo (verde/naranja/rojo)
- [ ] Interfaz principal/navegacion
- [ ] Detalle en docs/equipos/grupo4-tareas.md
Al mergear el PR de integracion del grupo, incluir 'Closes #<num>'." \
"equipo-4,kanban" "Sprint 2" "Isabela-Tellez"
E4="$LAST_ISSUE_NUM"

issue "Futuro - Resilience OS" \
"Horizonte 'A definir' (manifiesto §7): simulador what-if, indice de resiliencia, puntos de fallo, presupuesto, stress tests, equidad, Resilience API / Climate OS." \
"futuro,kanban" "" ""

# Cierre con trazabilidad de los issues de Sprint 1 obsoletos.
close_s1 41 "$E1" "Equipo 1 - Necesidades"
close_s1 43 "$E3" "Equipo 3 - Ayudas (donacion + voluntariado)"
close_s1 44 "$E4" "Equipo 4 - Mapa + Interfaz principal"

echo "Kanban: issues procesados."
