import numpy as np
import matplotlib.pyplot as plt
import math

# ── Parámetros ────────────────────────────────────────────────────────────────
N      = 100          # estampas distintas
S      = 7            # estampas por sobre (únicas dentro del sobre)
R      = 10_000       # simulaciones
PRICE  = 9.50         # precio por sobre (Q)
BUDGET = 1_000.0      # presupuesto total (Q)
SEED   = 2026


# ── Función auxiliar: simular n_packs sobres fijos ───────────────────────────
def simulate_packs(n_packs, seed=None):
    """Compra n_packs sobres por simulación.
    Retorna la proporción de simulaciones en que se completó el álbum."""
    if seed is not None:
        np.random.seed(seed)
    completed = 0
    for _ in range(R):
        collected = np.zeros(N, dtype=bool)
        for _ in range(n_packs):
            pack = np.random.choice(N, S, replace=False)
            collected[pack] = True
        if collected.all():
            completed += 1
    return completed / R


# ═══════════════════════════════════════════════════════════════════════════════
# ETAPA 3 — Incorporación del presupuesto y costo
# ═══════════════════════════════════════════════════════════════════════════════

np.random.seed(SEED)

completed_flag  = np.zeros(R, dtype=int)   # 1 = completó, 0 = no completó
packs_bought    = np.zeros(R, dtype=int)   # sobres comprados en cada simulación
distinct_failed = []                        # estampas distintas en sims. fallidas

for i in range(R):
    collected = np.zeros(N, dtype=bool)
    gasto  = 0.0
    sobres = 0

    # Comprar mientras se puede pagar otro sobre Y el álbum no está completo
    while (gasto + PRICE <= BUDGET) and (not collected.all()):
        pack = np.random.choice(N, S, replace=False)
        collected[pack] = True
        gasto  += PRICE
        sobres += 1

    packs_bought[i] = sobres

    if collected.all():
        completed_flag[i] = 1
    else:
        distinct_failed.append(int(np.sum(collected)))   # estampas únicas al quedarse sin presupuesto

distinct_failed      = np.array(distinct_failed)
prob_complete        = np.mean(completed_flag)
mean_packs_all       = np.mean(packs_bought)
mean_distinct_failed = (np.mean(distinct_failed) if len(distinct_failed) > 0
                        else float('nan'))
max_packs_possible   = int(BUDGET // PRICE)   # = 105

# ── Resultados principales ────────────────────────────────────────────────────
print("=" * 65)
print("ETAPA 3: INCORPORACIÓN DEL PRESUPUESTO Y COSTO")
print("=" * 65)
print(f"  N={N} | S={S} | R={R:,} | Precio=Q{PRICE} | Presupuesto=Q{BUDGET:.0f}")
print()
print(f"  P(completar álbum con Q{BUDGET:.0f}):              {prob_complete:.4f}  ({prob_complete*100:.2f}%)")
print(f"  Sobres esperados comprados (todas las sims.): {mean_packs_all:.4f}")
print(f"  Estampas distintas esperadas (sims. fall.):   {mean_distinct_failed:.4f}")
print(f"  Simulaciones exitosas:  {int(np.sum(completed_flag)):>6,} / {R:,}")
print(f"  Simulaciones fallidas:  {R - int(np.sum(completed_flag)):>6,} / {R:,}")

# ── Diagrama de barras: completó vs no completó ───────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
proportions = [prob_complete, 1.0 - prob_complete]
labels = [
    f'Completó\n(P = {prob_complete:.4f})',
    f'No completó\n(P = {1 - prob_complete:.4f})',
]
bars = ax.bar(labels, proportions, color=['steelblue', 'salmon'],
              edgecolor='black', alpha=0.85, width=0.5)
for b in bars:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width() / 2, h + 0.012, f'{h:.4f}',
            ha='center', va='bottom', fontsize=13, fontweight='bold')
ax.set_ylim(0, 1.25)
ax.set_ylabel('Proporción de simulaciones', fontsize=12)
ax.set_title(
    f'Completó vs no completó el álbum — Presupuesto Q{BUDGET:.0f}\n'
    f'N={N}, S={S}, precio/sobre=Q{PRICE}, R={R:,} simulaciones',
    fontsize=12
)
plt.tight_layout()
plt.savefig('proporcion_completar_budget.png', dpi=150)
plt.show()
print("\n  [Gráfico guardado: proporcion_completar_budget.png]")


# ═══════════════════════════════════════════════════════════════════════════════
# PREGUNTAS DE ANÁLISIS — ETAPA 3
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("PREGUNTAS DE ANÁLISIS — ETAPA 3")
print("=" * 65)


# ── Pregunta 1 ────────────────────────────────────────────────────────────────
theo_min = math.ceil(N / S)   # = 15

print("\nPregunta 1: ¿Con Q1000 se puede comprar al menos el mínimo teórico")
print("            de sobres sin estampas repetidas?")
print("-" * 65)
print(f"  Máximo de sobres comprables con Q{BUDGET:.0f}:")
print(f"    floor(Q{BUDGET:.0f} / Q{PRICE}) = floor({BUDGET / PRICE:.6f}) = {max_packs_possible} sobres")
print()
print(f"  Mínimo teórico sin ninguna estampa repetida:")
print(f"    ceil(N / S) = ceil({N} / {S}) = ceil({N / S:.6f}) = {theo_min} sobres")
print()
if max_packs_possible >= theo_min:
    print(f"  Respuesta: SI  ({max_packs_possible} >= {theo_min})")
    print(f"  Con Q{BUDGET:.0f} se pueden comprar hasta {max_packs_possible} sobres, lo que supera")
    print(f"  el minimo teorico de {theo_min} en {max_packs_possible - theo_min} sobres de holgura.")
    print(f"  En el escenario ideal, donde cada sobre aporta {S} estampas")
    print(f"  completamente distintas a las anteriores, bastarian {theo_min} sobres")
    print(f"  para completar el album. Sin embargo, ese escenario es practicamente")
    print(f"  imposible: con {N} estampas y {S} por sobre, las repeticiones son")
    print(f"  inevitables. La simulacion (media ~ {mean_packs_all:.0f} sobres) lo confirma.")
else:
    print(f"  Respuesta: NO  ({max_packs_possible} < {theo_min})")
    print(f"  El presupuesto es insuficiente incluso en el caso sin repeticiones.")


# ── Pregunta 2 ────────────────────────────────────────────────────────────────
BOX_PACKS           = 104
BOX_PRICE           = 975.0
loose_with_box_bgt  = int(BOX_PRICE // PRICE)        # 102  (= floor(975/9.50))
box_unit_price      = BOX_PRICE / BOX_PACKS           # ≈ 9.375 Q/sobre
savings_vs_loose    = BOX_PACKS * PRICE - BOX_PRICE   # 104*9.50 - 975 = Q 13.00

print("\nPregunta 2: Caja de 104 sobres (Q975) vs sobres sueltos")
print("-" * 65)
print("  Simulando... (puede tardar unos segundos)")

prob_box       = simulate_packs(BOX_PACKS,          seed=SEED)  # caja → 104 sobres
prob_loose_102 = simulate_packs(loose_with_box_bgt, seed=SEED)  # sueltos con Q975 → 102 sobres

print()
print(f"  Precio unitario — sobre suelto:  Q{PRICE:.2f}")
print(f"  Precio unitario — caja:          Q{box_unit_price:.4f}  (ahorro Q{savings_vs_loose:.2f} total vs 104 sueltos)")
print()
print(f"  {'Modalidad':<42} {'Sobres':>7}  {'Gasto':>8}  {'P(completar)':>13}")
print(f"  {'-'*42} {'-'*7}  {'-'*8}  {'-'*13}")
print(f"  {'Sueltos con Q975 (mismo presupuesto que caja)':<42} {loose_with_box_bgt:>7}  {f'Q{loose_with_box_bgt * PRICE:.2f}':>8}  {prob_loose_102:>13.4f}")
print(f"  {'Caja de 104 sobres':<42} {BOX_PACKS:>7}  {f'Q{BOX_PRICE:.0f}':>8}  {prob_box:>13.4f}")
print(f"  {'Sueltos con Q1000 (presupuesto completo)':<42} {max_packs_possible:>7}  {f'Q{max_packs_possible * PRICE:.2f}':>8}  {prob_complete:>13.4f}")
print()
print(f"  Conclusión:")
print(f"  Con el mismo presupuesto de Q{BOX_PRICE:.0f}, la caja entrega {BOX_PACKS - loose_with_box_bgt}")
print(f"  sobres más que comprando sueltos ({BOX_PACKS} vs {loose_with_box_bgt}), porque el precio")
print(f"  unitario es más barato (Q{box_unit_price:.4f} vs Q{PRICE:.2f} por sobre).")
print(f"  Esto se traduce directamente en una mayor probabilidad de completar")
print(f"  el álbum: la caja supera a los sueltos equivalentes en")
print(f"  dif = {prob_box - prob_loose_102:+.4f} ({(prob_box - prob_loose_102)*100:+.2f}p.p.).")


# ── Pregunta 3 ────────────────────────────────────────────────────────────────
extra_loose = int((BUDGET - BOX_PRICE) // PRICE)   # floor(25/9.50) = 2
mixed_total = BOX_PACKS + extra_loose              # 106
mixed_cost  = BOX_PRICE + extra_loose * PRICE      # 975 + 19 = Q 994.00

print("\nPregunta 3: Estrategia mixta (caja + sueltos) que maximice P(completar)")
print("-" * 65)
print("  Enumerando estrategias factibles dentro de Q1000...")
print()

# Estrategia 0: sólo sueltos (prob_complete ya calculada, no requiere resimular)
# Estrategia 1: sólo caja    (prob_box ya calculada)
# Estrategia 2: caja + sueltos adicionales

print("  [Simulando estrategia mixta...]")
prob_mixed = simulate_packs(mixed_total, seed=SEED)   # 104 caja + 2 sueltos = 106

print()
print(f"  {'Estrategia':<42} {'Sobres':>7}  {'Gasto':>9}  {'P(completar)':>13}")
print(f"  {'-'*42} {'-'*7}  {'-'*9}  {'-'*13}")
print(f"  {'Solo sueltos':<42} {max_packs_possible:>7}  {f'Q{max_packs_possible * PRICE:.2f}':>9}  {prob_complete:>13.4f}")
print(f"  {'Solo caja':<42} {BOX_PACKS:>7}  {f'Q{BOX_PRICE:.0f}':>9}  {prob_box:>13.4f}")
mixed_label = f'Caja + {extra_loose} sueltos  [OPTIMA]'
print(f"  {mixed_label:<42} {mixed_total:>7}  {f'Q{mixed_cost:.2f}':>9}  {prob_mixed:>13.4f}")
print()

best_prob = max(prob_complete, prob_box, prob_mixed)

print(f"  >> Mejor estrategia: caja ({BOX_PACKS} sobres, Q{BOX_PRICE:.0f})")
print(f"    + {extra_loose} sobres sueltos (Q{extra_loose * PRICE:.2f})")
print(f"    = {mixed_total} sobres en total por Q{mixed_cost:.2f}")
print(f"    P(completar) = {prob_mixed:.4f}  ({prob_mixed*100:.2f}%)")
print()
print(f"  Por que es optima?")
print(f"  - La caja cuesta Q{BOX_PRICE:.0f} por {BOX_PACKS} sobres = Q{box_unit_price:.4f}/sobre.")
print(f"    Comprar {BOX_PACKS} sueltos costaria Q{BOX_PACKS * PRICE:.2f}: la caja ahorra Q{savings_vs_loose:.2f}.")
print(f"  - Con el ahorro de Q{savings_vs_loose:.2f} + Q{BUDGET - max_packs_possible * PRICE:.2f} de vuelto de")
print(f"    la estrategia de sueltos puros, se financian {extra_loose} sobres adicionales.")
print(f"  - Resultado: {mixed_total} sobres vs {max_packs_possible} de sueltos puros -> 1 sobre mas,")
print(f"    mayor probabilidad.")
print()
print(f"  Ganancia vs solo sueltos:  {prob_mixed - prob_complete:+.4f}  ({(prob_mixed - prob_complete)*100:+.2f}p.p.)")
print(f"  Ganancia vs solo caja:     {prob_mixed - prob_box:+.4f}  ({(prob_mixed - prob_box)*100:+.2f}p.p.)")
print(f"  Dinero ahorrado vs sueltos: Q{max_packs_possible * PRICE - mixed_cost:.2f}")
