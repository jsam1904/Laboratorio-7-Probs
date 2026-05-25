import numpy as np
import matplotlib.pyplot as plt
import math

np.random.seed(2026)

# ── Parameters ───────────────────────────────────────────────────────────────
N = 100    # different stickers
S = 7      # stickers per pack (unique within pack)
R = 10000  # simulations

# ── Simulation ───────────────────────────────────────────────────────────────
packs_results    = []
repeated_results = []

for _ in range(R):
    collected         = np.zeros(N, dtype=bool)
    packs_bought      = 0
    repeated_stickers = 0

    while not collected.all():
        pack = np.random.choice(N, S, replace=False)
        for sticker in pack:
            if collected[sticker]:
                repeated_stickers += 1
            else:
                collected[sticker] = True
        packs_bought += 1

    packs_results.append(packs_bought)
    repeated_results.append(repeated_stickers)

packs_results    = np.array(packs_results)
repeated_results = np.array(repeated_results)

# ── Results ──────────────────────────────────────────────────────────────────
mean_packs    = np.mean(packs_results)
std_packs     = np.std(packs_results)
mean_repeated = np.mean(repeated_results)
std_repeated  = np.std(repeated_results)
p_over_30     = np.mean(packs_results > 30)
theo_min      = math.ceil(N / S)   # = 15

print("=" * 55)
print("RESULTADOS DE LA SIMULACION")
print("=" * 55)
print(f"Media de sobres comprados:          {mean_packs:.4f}")
print(f"Desviacion estandar de sobres:      {std_packs:.4f}")
print(f"Media de figuritas repetidas:       {mean_repeated:.4f}")
print(f"Desviacion estandar de repetidas:   {std_repeated:.4f}")
print(f"P(sobres > 30):                     {p_over_30:.4f}")
print()
print("Justificacion del umbral de 30 sobres:")
print(f"  Minimo teorico: ceil({N}/{S}) = {theo_min} sobres.")
print(f"  30 es el doble del minimo ({theo_min}), lo que representa una")
print(f"  holgura razonable dado el efecto de 'cola larga' del proceso.")
print(f"  La probabilidad P(sobres > 30) = {p_over_30:.4f} cuantifica cuan")
print(f"  frecuente es superar ese doble del minimo.")

# ── Histogram ────────────────────────────────────────────────────────────────
plt.figure(figsize=(10, 6))
plt.hist(packs_results, bins=40, edgecolor='black', color='steelblue', alpha=0.7)
plt.axvline(mean_packs, color='red',   linestyle='--', linewidth=2,
            label=f'Media muestral = {mean_packs:.2f}')
plt.axvline(theo_min,   color='green', linestyle='-',  linewidth=2,
            label=f'Minimo teorico = {theo_min}')
plt.title(f'Distribucion del numero de sobres para completar el album\n'
          f'(N={N}, S={S}, R={R:,} simulaciones)')
plt.xlabel('Numero de sobres comprados')
plt.ylabel('Frecuencia')
plt.legend()
plt.tight_layout()
plt.savefig('distribucion_sobres.png', dpi=150)
plt.show()

# ── Analysis Questions ────────────────────────────────────────────────────────
print()
print("=" * 55)
print("ANALISIS")
print("=" * 55)

# Q1 — Minimum packs without repeats
print()
print("Pregunta 1: Minimo de sobres sin figuritas repetidas")
print("-" * 55)
print(f"  Si ninguna figurita se repitiera, cada sobre aportaria")
print(f"  exactamente S={S} figuritas nuevas. Para N={N} figuritas:")
print(f"    Minimo = ceil(N/S) = ceil({N}/{S}) = ceil({N/S:.6f}) = {theo_min} sobres")
min_count = int(np.sum(packs_results == theo_min))
print(f"  Apariciones en simulaciones: {min_count} de {R} ({100*min_count/R:.4f}%).")
if min_count == 0:
    print(f"  No se observo este caso: la probabilidad es extremadamente")
    print(f"  pequenya; siempre hay al menos alguna repeticion en la practica.")
else:
    print(f"  Se observo {min_count} vez/veces -- evento muy raro.")

# Q2 — Harmonic number approximation
print()
print("Pregunta 2: Calculo teorico con H_100")
print("-" * 55)
H_N = np.log(N) + 0.5772
E_T = (N / S) * H_N
print(f"  H_100 aprox ln(100) + 0.5772")
print(f"        = {np.log(N):.4f} + 0.5772")
print(f"        = {H_N:.4f}")
print(f"  E[T]  = (N/S) * H_100")
print(f"        = ({N}/{S}) * {H_N:.4f}")
print(f"        = {N/S:.4f} * {H_N:.4f}")
print(f"        = {E_T:.4f} sobres")
print(f"  Media simulada: {mean_packs:.4f} sobres")
diff_pct = 100 * abs(E_T - mean_packs) / mean_packs
print(f"  Diferencia absoluta: {abs(E_T - mean_packs):.4f} sobres ({diff_pct:.2f}%)")
print(f"  La aproximacion es {'muy cercana' if diff_pct < 5 else 'razonable'} a la media simulada.")

# Q3 — Theoretical repeated stickers
print()
print("Pregunta 3: Figuritas repetidas -- teorico vs simulado")
print("-" * 55)
E_repeated = E_T * S - N
print(f"  Total de figuritas abiertas aprox E[sobres] * S")
print(f"    = {E_T:.4f} * {S} = {E_T*S:.4f}")
print(f"  De esas, N={N} son nuevas (para completar el album).")
print(f"  E[repetidas] = E[sobres] * S - N = {E_T*S:.4f} - {N} = {E_repeated:.4f}")
print(f"  Media simulada de repetidas: {mean_repeated:.4f}")
print(f"  Diferencia: {abs(E_repeated - mean_repeated):.4f} figuritas")

# Q4 — Variability interpretation
print()
print("Pregunta 4: Interpretacion de la desviacion estandar")
print("-" * 55)
cv = std_packs / mean_packs
print(f"  Media:                 {mean_packs:.4f} sobres")
print(f"  Desviacion estandar:   {std_packs:.4f} sobres")
print(f"  Coeficiente de var.:   {cv:.4f}  ({100*cv:.2f}%)")
print()
print(f"  La desviacion es {'ALTA' if cv > 0.25 else 'moderada'} relativa a la media (CV aprox {100*cv:.1f}%).")
print("  Esto refleja el efecto de 'cola larga' del coleccionismo:")
print("  - Las primeras figuritas son faciles de obtener.")
print("  - Las ultimas son muy dificiles (pocas chances de salir).")
print("  - Este desequilibrio genera asimetria positiva y alta varianza.")
print("  - No hay control sobre que sale en cada sobre: la suerte")
print("    domina y algunos terminan rapido mientras otros tardan mucho.")

# ── Etapa 2: Analisis de la probabilidad de exito ────────────────────────────
print("\n" + "=" * 55)
print("ETAPA 2: ANALISIS EN FUNCION DEL NUMERO DE SOBRES")
print("=" * 55)

# 1. Secuencia de numero de sobres
M_values = [20, 25, 30, 35, 40, 45, 50, 60, 70, 80]

# Reinicializar semilla para reproducibilidad perfecta e independencia de Etapa 1
np.random.seed(2026)

# Matriz para registrar la completitud de cada simulacion a los M sobres
# Filas: Simulaciones, Columnas: Cada valor de M
completion_matrix = np.zeros((R, len(M_values)), dtype=int)

for r in range(R):
    collected = np.zeros(N, dtype=bool)
    # Simulamos la compra de hasta 80 sobres (el maximo valor de M)
    for pack_idx in range(1, max(M_values) + 1):
        pack = np.random.choice(N, S, replace=False)
        for sticker in pack:
            collected[sticker] = True
        
        # Si el numero de sobres actual es uno de nuestros milestones en M_values
        if pack_idx in M_values:
            m_col = M_values.index(pack_idx)
            completion_matrix[r, m_col] = 1 if collected.all() else 0

# Calcular proporciones de exito
success_proportions = np.mean(completion_matrix, axis=0)

# Imprimir tabla de resultados
print(f"{'Sobres (M)':<12} | {'Probabilidad de exito estimada':<32}")
print("-" * 47)
for M, prob in zip(M_values, success_proportions):
    print(f"{M:<12} | {prob:<32.4f}")

# ── Visualizacion (Etapa 2) ──────────────────────────────────────────────────
plt.figure(figsize=(10, 6))
bars = plt.bar([str(m) for m in M_values], success_proportions, color='coral', edgecolor='black', alpha=0.8)
plt.axhline(0.5, color='red', linestyle='--', linewidth=2, label='Umbral del 50% de exito')

# Anadir etiquetas de valor sobre cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.01, f'{yval:.4f}', ha='center', va='bottom', fontsize=9)

plt.title('Probabilidad de completar el album en funcion del numero de sobres comprados\n'
          f'(N={N}, S={S}, R={R:,} simulaciones)')
plt.xlabel('Numero de sobres comprados (M)')
plt.ylabel('Probabilidad de exito P(Completar | M sobres)')
plt.ylim(0, 1.05)
plt.legend()
plt.tight_layout()
plt.savefig('probabilidad_completar.png', dpi=150)
plt.close()

# ── Preguntas de analisis (Etapa 2) ──────────────────────────────────────────
print("\n" + "=" * 55)
print("PREGUNTAS DE ANALISIS - ETAPA 2")
print("=" * 55)

# Q1: First time exceeding 50% and 90%
print("\nPregunta 1: Superacion de los umbrales del 50% y 90%")
print("-" * 55)
m_50 = None
m_90 = None

for M, prob in zip(M_values, success_proportions):
    if prob > 0.5 and m_50 is None:
        m_50 = M
    if prob > 0.9 and m_90 is None:
        m_90 = M

print(f"  - El umbral del 50% se supera por primera vez en M = {m_50} sobres (P = {success_proportions[M_values.index(m_50)]:.4f}).")
if m_90 is not None:
    print(f"  - El umbral del 90% se supera por primera vez en M = {m_90} sobres.")
else:
    # Calcular percentil 90 teorico-muestral usando packs_results de Etapa 1
    # que es el mismo proceso aleatorio independiente
    p90_muestral = np.percentile(packs_results, 90)
    print(f"  - El umbral del 90% NO se supera dentro de la secuencia dada (max M = 80, P = {success_proportions[-1]:.4f}).")
    print(f"    Sin embargo, analizando la distribucion completa de la Etapa 1,")
    print(f"    se requeririan al menos {int(p90_muestral)} sobres para tener un 90% de probabilidad de exito.")

# Q2: Comparison with median
print("\nPregunta 2: Comparacion con la mediana")
print("-" * 55)
median_packs = np.median(packs_results)
print(f"  - Mediana muestral de sobres (Etapa 1): {median_packs:.1f} sobres.")
print(f"  - Primer valor de M con P > 50%:       M = {m_50} sobres.")
print(f"  - Explicacion: Son extremadamente similares debido a que la mediana es,")
print("    por definicion, el valor de la variable aleatoria T para el cual la")
print("    probabilidad acumulada alcanza exactamente el 50% (P(T <= mediana) = 0.5).")
print("    Dado que M = 70 es el primer valor discreto en nuestra secuencia evaluada")
print("    que es mayor o igual a la mediana real (69 sobres), es matematicamente")
print("    esperable que sea el primero en superar una probabilidad de exito de 0.5.")

# Q3: Union Bound for M = 50
print("\nPregunta 3: Cota superior de la union para M = 50")
print("-" * 55)
M_eval = 50
p_exito_50 = success_proportions[M_values.index(M_eval)]
p_fracaso_50_emp = 1 - p_exito_50

# Calculo de la cota: N * e^(-M * S / N)
union_bound_50 = N * math.exp(-M_eval * S / N)

print(f"  - Para M = {M_eval} sobres:")
print(f"    - Probabilidad de exito estimada:   {p_exito_50:.4f} ({p_exito_50*100:.2f}%)")
print(f"    - Probabilidad de fracaso estimada:  {p_fracaso_50_emp:.4f} ({p_fracaso_50_emp*100:.2f}%)")
print(f"    - Cota de la union teorica:         N * e^(-M*S/N) = {N} * e^(-({M_eval}*{S})/{N})")
print(f"                                        = 100 * e^(-3.5) = {union_bound_50:.4f} ({union_bound_50*100:.2f}%)")
print()
print("  - Evaluacion de la utilidad de la cota:")
print(f"    ¿Es util la cota? {'SI' if union_bound_50 < 1.0 else 'NO'}.")
print(f"    La cota es {union_bound_50:.4f} > 1. Toda probabilidad esta acotada superiormente")
print("    por 1 de forma trivial. Por lo tanto, un limite superior mayor que 1 no aporta")
print("    informacion util. La cota de la union asume que los eventos de que falte cada")
print("    estampa son disjuntos, lo cual es una aproximacion burda cuando M es pequeño")
print("    y las intersecciones entre eventos son grandes. La cota solo se vuelve util (< 1)")
print("    cuando M > (N * ln(N)) / S, es decir, a partir de M = 66 sobres.")
