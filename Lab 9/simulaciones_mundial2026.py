"""
simulaciones_mundial2026.py
===========================
Simulaciones Monte Carlo — Álbum del Mundial 2026
Laboratorio 9 · MM3014 Teoría de Probabilidades
Universidad del Valle de Guatemala

Ejecución directa:  python simulaciones_mundial2026.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time

matplotlib.rcParams.update({
    'font.family':  'DejaVu Sans',
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
})

# ─── Constantes globales ──────────────────────────────────────────────────────
N            = 980      # Estampas totales en el álbum
S            = 7        # Estampas por sobre
PRECIO_SOBRE = 9.50     # Q  — sobre suelto
PRECIO_CAJA  = 975.00   # Q  — caja de 104 sobres
SOBRES_CAJA  = 104      # Sobres por caja
NUM_SIM      = 2000     # Iteraciones Monte Carlo por pregunta
SEED         = 42

np.random.seed(SEED)


# ─── Utilidades ───────────────────────────────────────────────────────────────

def ic95(datos):
    """
    Intervalo de confianza al 95 % (z = 1.96 para n grande).
    Devuelve (límite_inferior, límite_superior).
    """
    datos = np.asarray(datos, dtype=float)
    n     = len(datos)
    media = datos.mean()
    se    = datos.std(ddof=1) / np.sqrt(n)
    margen = 1.96 * se
    return media - margen, media + margen


def _comprar_sobre(n=N, s=S):
    """Devuelve un array con los índices de las s estampas del sobre."""
    return np.random.randint(0, n, s)


# ─── PREGUNTA 1 ───────────────────────────────────────────────────────────────

def simular_pregunta1(n_sim=NUM_SIM, n=N, s=S):
    """
    Calcula cuántos sobres se necesitan para completar el 75 %, 90 % y 100 %
    del álbum, junto con las estampas repetidas acumuladas en cada corte.

    Devuelve:
        dict con claves 0.75, 0.90, 1.00  →  {media_sobres, ic, media_rep, datos}
        curva_prom: array con estampas únicas promedio por sobre comprado
    """
    print("\n" + "=" * 62)
    print("  PREGUNTA 1 — Puntos de corte de completitud")
    print("=" * 62)

    cortes_sobres = {0.75: [], 0.90: [], 1.00: []}
    cortes_rep    = {0.75: [], 0.90: [], 1.00: []}
    todas_curvas  = []

    for _ in range(n_sim):
        album     = np.zeros(n, dtype=bool)
        sobres    = 0
        rep       = 0
        alcanzado = {0.75: False, 0.90: False, 1.00: False}
        curva     = []

        while not album.all():
            nuevas = _comprar_sobre(n, s)
            sobres += 1
            for e in nuevas:
                if album[e]:
                    rep += 1
                else:
                    album[e] = True

            unicas = int(album.sum())
            curva.append(unicas)

            for pct in (0.75, 0.90, 1.00):
                if not alcanzado[pct] and unicas >= int(n * pct):
                    cortes_sobres[pct].append(sobres)
                    cortes_rep[pct].append(rep)
                    alcanzado[pct] = True

        todas_curvas.append(curva)

    # ── Estadísticas ──
    resultados = {}
    print(f"\n  {'%':>6}  {'Media sobres':>14}  {'IC 95%':>24}  {'Repetidas (media)':>19}")
    print("  " + "-" * 70)
    for pct in (0.75, 0.90, 1.00):
        datos = np.array(cortes_sobres[pct])
        media = datos.mean()
        lo, hi = ic95(datos)
        mrep   = np.mean(cortes_rep[pct])
        resultados[pct] = dict(media_sobres=media, ic=(lo, hi),
                               media_rep=mrep, datos=datos)
        print(f"  {int(pct*100):>5}%  {media:>14.1f}  ({lo:.1f}, {hi:.1f})  {mrep:>19.1f}")

    # ── Curva promedio hasta P90 de sobres totales ──
    max_x = int(np.percentile(cortes_sobres[1.00], 90))
    acum  = np.zeros(max_x)
    cnt   = np.zeros(max_x)
    for curva in todas_curvas:
        top = min(len(curva), max_x)
        acum[:top] += curva[:top]
        cnt[:top]  += 1
    curva_prom = np.divide(acum, cnt, where=cnt > 0)

    # ── Gráfica ──
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(1, max_x + 1)
    ax.plot(x, curva_prom, color='steelblue', lw=2, label='Estampas únicas promedio')

    estilos = {0.75: ('orange',    '--'), 0.90: ('crimson', '--'), 1.00: ('darkgreen', '-.')}
    for pct, (col, ls) in estilos.items():
        xc = resultados[pct]['media_sobres']
        yc = int(n * pct)
        ax.axvline(xc, color=col, ls=ls, alpha=0.85,
                   label=f'{int(pct*100)}% → {xc:.0f} sobres')
        ax.axhline(yc, color=col, ls=':', alpha=0.4)

    ax.set_xlabel('Sobres comprados')
    ax.set_ylabel('Estampas únicas acumuladas')
    ax.set_title(f'Curva de Completitud del Álbum — Mundial 2026\n(N={n}, S={s}, {n_sim} simulaciones)')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('p1_curva_completitud.png', dpi=130)
    plt.show()

    return resultados, curva_prom


# ─── PREGUNTA 2 ───────────────────────────────────────────────────────────────

def simular_pregunta2(n_sim=NUM_SIM, objetivos=(0.50, 0.75, 0.90), n=N, s=S):
    """
    Calcula el presupuesto mínimo (en quetzales) para tener una probabilidad
    del 50 %, 75 % y 90 % de completar el álbum completo, comparando:
      · Estrategia SUELTOS : sobres sueltos a Q9.50 c/u
      · Estrategia CAJAS   : cajas de 104 sobres a Q975.00

    También genera la curva P(completar álbum) vs presupuesto para ambas.
    """
    print("\n" + "=" * 62)
    print("  PREGUNTA 2 — Presupuesto óptimo por tramos")
    print("=" * 62)

    # ── 1) Simular sobres necesarios para completar el 100 % ──
    print(f"\n  Simulando {n_sim} completaciones del álbum...")
    sobres_sim = []
    for _ in range(n_sim):
        album = np.zeros(n, dtype=bool)
        cnt   = 0
        while not album.all():
            album[_comprar_sobre(n, s)] = True
            cnt += 1
        sobres_sim.append(cnt)
    sobres_sim = np.array(sobres_sim)

    # ── 2) Presupuesto mínimo por objetivo ──
    resultados = {}
    print(f"\n  {'Objetivo':>10}  {'Sueltos (Q)':>14}  {'Cajas (Q)':>12}  {'Conviene'}")
    print("  " + "-" * 58)
    for obj in objetivos:
        pct = int(obj * 100)
        # El percentil obj*100 de sobres_sim da el mínimo de sobres
        # para garantizar la probabilidad objetivo.
        q_sobres = int(np.ceil(np.percentile(sobres_sim, pct)))

        presup_sueltos = float(q_sobres * PRECIO_SOBRE)
        cajas_nec      = int(np.ceil(q_sobres / SOBRES_CAJA))
        presup_cajas   = float(cajas_nec * PRECIO_CAJA)
        conviene       = "Sueltos" if presup_sueltos <= presup_cajas else "Cajas"

        resultados[obj] = dict(
            presup_sueltos   = presup_sueltos,
            presup_cajas     = presup_cajas,
            conviene         = conviene,
            sobres_percentil = q_sobres,
        )
        print(f"  {pct:>9}%  {presup_sueltos:>14.2f}  {presup_cajas:>12.2f}  {conviene}")

    # ── 3) Curva P(completar álbum) vs presupuesto ──
    p_max_sobres = int(sobres_sim.max())

    # Sobres sueltos: barre presupuesto continuo
    presup_s = np.linspace(0, p_max_sobres * PRECIO_SOBRE * 1.05, 800)
    prob_s   = np.array([
        float(np.mean(sobres_sim <= int(p // PRECIO_SOBRE)))
        for p in presup_s
    ])

    # Cajas: curva escalonada (solo múltiplos de PRECIO_CAJA importan)
    max_cajas = int(np.ceil(p_max_sobres / SOBRES_CAJA)) + 2
    presup_c  = np.arange(0, max_cajas * PRECIO_CAJA + 1, PRECIO_CAJA)
    prob_c    = np.array([
        float(np.mean(sobres_sim <= int(q // PRECIO_CAJA) * SOBRES_CAJA))
        for q in presup_c
    ])

    # ── Gráfica ──
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.plot(presup_s / 1_000, prob_s * 100,
            color='steelblue', lw=2.5, label='Sobres sueltos (Q9.50 c/u)')
    ax.step(presup_c / 1_000, prob_c * 100,
            color='darkorange', lw=2.5, where='post',
            label=f'Cajas (Q{PRECIO_CAJA:.0f} / {SOBRES_CAJA} sobres)')

    colores_obj = {0.50: '#2ca02c', 0.75: '#d62728', 0.90: '#9467bd'}
    for obj, r in resultados.items():
        col = colores_obj[obj]
        ax.axhline(obj * 100, color=col, ls=':', lw=1.2, alpha=0.6)
        ax.scatter([r['presup_sueltos'] / 1_000], [obj * 100],
                   color=col, marker='o', s=90, zorder=6)
        ax.scatter([r['presup_cajas'] / 1_000], [obj * 100],
                   color=col, marker='s', s=90, zorder=6,
                   label=(f"{int(obj*100)}%: "
                          f"Q{r['presup_sueltos']:.0f} sueltos  /  "
                          f"Q{r['presup_cajas']:.0f} cajas  → {r['conviene']}"))

    ax.set_xlabel('Presupuesto (miles de Q)')
    ax.set_ylabel('Probabilidad de completar el álbum (%)')
    ax.set_title('Probabilidad de Completar el Álbum vs Presupuesto\n'
                 f'Comparativa Sobres Sueltos vs Cajas  (N={n}, S={s}, {n_sim} sim.)')
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('p2_presupuesto_optimo.png', dpi=130)
    plt.show()

    return resultados, sobres_sim, presup_s, prob_s, presup_c, prob_c


# ─── PREGUNTA 3 ───────────────────────────────────────────────────────────────

def simular_pregunta3(n_sim=NUM_SIM, valores_k=(3, 5, 7), n=N, s=S):
    """
    Compara el ahorro en quetzales al completar el álbum con tasas de
    intercambio K = 3, 5 y 7  (K repetidas → 1 estampa nueva aleatoria
    que aún no tienes).

    Identifica el punto de rendimiento marginal decreciente entre valores
    consecutivos de K.
    """
    print("\n" + "=" * 62)
    print("  PREGUNTA 3 — Análisis comparativo de tasas de intercambio")
    print("=" * 62)

    def _sin():
        album = np.zeros(n, dtype=bool)
        cnt   = 0
        while not album.all():
            album[_comprar_sobre(n, s)] = True
            cnt += 1
        return cnt

    def _con(K):
        album  = np.zeros(n, dtype=bool)
        sobres = 0
        rep    = 0
        while not album.all():
            nuevas = _comprar_sobre(n, s)
            sobres += 1
            for e in nuevas:
                if album[e]: rep += 1
                else:        album[e] = True
            while rep >= K:
                faltantes = np.where(~album)[0]
                if len(faltantes) == 0:
                    rep = 0; break
                album[np.random.choice(faltantes)] = True
                rep -= K
        return sobres

    # ── Base: sin intercambio ──
    print(f"\n  Simulando {n_sim} × SIN intercambio (línea base)...")
    sobres_sin = np.array([_sin() for _ in range(n_sim)])
    costo_sin  = sobres_sin * PRECIO_SOBRE
    media_sin  = costo_sin.mean()

    # ── Por cada K ──
    resultados     = {}
    ahorros_medios = []
    print(f"\n  {'K':>4}  {'Sobres (media)':>16}  {'Costo (Q)':>12}  "
          f"{'Ahorro (Q)':>12}  {'Ahorro %':>10}")
    print("  " + "-" * 62)

    for K in valores_k:
        print(f"  Simulando {n_sim} × K={K}...")
        sobres_con = np.array([_con(K) for _ in range(n_sim)])
        costo_con  = sobres_con * PRECIO_SOBRE
        ahorro     = costo_sin - costo_con

        m_con = costo_con.mean()
        m_ah  = ahorro.mean()
        p_ah  = m_ah / media_sin * 100

        resultados[K] = dict(
            media_sobres = sobres_con.mean(),
            media_costo  = m_con,
            ahorro_medio = m_ah,
            pct_ahorro   = p_ah,
            costo_con    = costo_con,
        )
        ahorros_medios.append(m_ah)
        print(f"  {K:>4}  {sobres_con.mean():>16.1f}  {m_con:>12.2f}"
              f"  {m_ah:>12.2f}  {p_ah:>10.1f}%")

    # ── Análisis de rendimiento marginal ──
    print(f"\n  Línea base sin intercambio → media Q{media_sin:.2f}")
    print("\n  Ahorro marginal al disminuir K (K menor = intercambio más generoso):")
    for i in range(1, len(valores_k)):
        K_prev, K_curr = valores_k[i-1], valores_k[i]
        delta = ahorros_medios[i] - ahorros_medios[i-1]
        print(f"    K={K_prev} → K={K_curr}: Δahorro = Q{delta:+.2f}")

    # ── Gráficas ──
    Ks  = list(valores_k)
    ahs = [resultados[K]['ahorro_medio'] for K in Ks]

    fig, axes = plt.subplots(1, 2, figsize=(13, 6))

    # a) Línea de ahorro vs K
    axes[0].plot(Ks, ahs, 'o-', color='steelblue', lw=2.5, ms=9, zorder=3)
    for K, ah in zip(Ks, ahs):
        axes[0].annotate(f'Q{ah:,.0f}',
                         xy=(K, ah), xytext=(0, 12),
                         textcoords='offset points',
                         ha='center', fontweight='bold', fontsize=10)

    # Ahorro marginal (eje derecho)
    if len(Ks) > 1:
        ax2    = axes[0].twinx()
        K_mids = [(Ks[i] + Ks[i+1]) / 2 for i in range(len(Ks) - 1)]
        deltas = [ahs[i+1] - ahs[i]      for i in range(len(ahs) - 1)]
        ax2.bar(K_mids, deltas, width=0.55, alpha=0.30,
                color='tomato', label='Ahorro marginal (Δ)')
        ax2.set_ylabel('Ahorro marginal (Q)', color='tomato')
        ax2.tick_params(axis='y', labelcolor='tomato')
        ax2.legend(loc='lower left')

    axes[0].set_xlabel('Tasa de intercambio K')
    axes[0].set_ylabel('Ahorro promedio vs sin intercambio (Q)', color='steelblue')
    axes[0].tick_params(axis='y', labelcolor='steelblue')
    axes[0].set_xticks(Ks)
    axes[0].set_title('Ahorro Promedio vs Tasa de Intercambio K\n(+ Rendimiento Marginal)')
    axes[0].legend(['Ahorro promedio'], loc='upper right')
    axes[0].grid(alpha=0.3)

    # b) Boxplot comparativo
    data_bx   = [costo_sin] + [resultados[K]['costo_con'] for K in Ks]
    labels_bx = ['Sin\nintercambio'] + [f'K={K}' for K in Ks]
    bp = axes[1].boxplot(data_bx, labels=labels_bx,
                         patch_artist=True, notch=False,
                         medianprops=dict(color='black', lw=2))
    colores_bx = ['#5b9bd5', '#ed7d31', '#70ad47', '#ffc000']
    for box, col in zip(bp['boxes'], colores_bx[:len(bp['boxes'])]):
        box.set_facecolor(col)
    axes[1].set_ylabel('Costo total para completar el álbum (Q)')
    axes[1].set_title('Distribución del Costo Total\npor Tasa de Intercambio K')
    axes[1].grid(axis='y', alpha=0.3)

    plt.suptitle('Ahorro según Tasa de Intercambio K — Álbum Mundial 2026',
                 fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig('p3_tasas_intercambio.png', dpi=130)
    plt.show()

    return dict(resultados=resultados, media_sin=media_sin, costo_sin=costo_sin)


# ─── PREGUNTA 4 ───────────────────────────────────────────────────────────────

def simular_pregunta4(n_sim=NUM_SIM, pct_meta=0.95, limite_sobres=1040, n=N, s=S):
    """
    Distribuye el número de sobres para alcanzar el 95 % del álbum (931 est.).
    Calcula P(sobres ≤ 1040) y los percentiles 50, 75, 95.

    Devuelve dict con estadísticos y el array de sobres simulados.
    """
    print("\n" + "=" * 62)
    print("  PREGUNTA 4 — Distribución para el 95 % del álbum")
    print("=" * 62)

    meta = int(n * pct_meta)   # 931
    print(f"  Meta: {meta} estampas ({int(pct_meta*100)} % de {n})")

    sobres_lista = []
    for _ in range(n_sim):
        album  = np.zeros(n, dtype=bool)
        sobres = 0
        while album.sum() < meta:
            album[_comprar_sobre(n, s)] = True
            sobres += 1
        sobres_lista.append(sobres)

    arr = np.array(sobres_lista)

    prob   = float(np.mean(arr <= limite_sobres))
    p50    = float(np.percentile(arr, 50))
    p75    = float(np.percentile(arr, 75))
    p95    = float(np.percentile(arr, 95))
    media  = float(arr.mean())

    print(f"\n  Sobres necesarios — media: {media:.1f}")
    print(f"    Percentil 50:  {p50:.0f}")
    print(f"    Percentil 75:  {p75:.0f}")
    print(f"    Percentil 95:  {p95:.0f}")
    print(f"  P(sobres ≤ {limite_sobres} | 10 cajas) = {prob:.4f}  ({prob*100:.1f} %)")

    # ── Histograma ──
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(arr, bins=55, color='steelblue', edgecolor='white', alpha=0.80, density=True)

    for label, val, color in [('P50', p50, '#ff7f0e'),
                               ('P75', p75, '#d62728'),
                               ('P95', p95, '#9467bd')]:
        ax.axvline(val, color=color, ls='--', lw=2, label=f'{label}: {val:.0f} sobres')

    # El límite 1040 queda fuera del rango de datos; se anota en el gráfico
    xmax = ax.get_xlim()[1]
    ax.annotate(
        f'Límite {limite_sobres} sobres (10 cajas)\nP(≤{limite_sobres}) = {prob*100:.1f} %',
        xy=(xmax * 0.98, ax.get_ylim()[1] * 0.88),
        ha='right', va='top', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', fc='lightyellow', ec='black', alpha=0.8)
    )

    ax.set_xlabel(f'Sobres para alcanzar {meta} estampas ({int(pct_meta*100)} %)')
    ax.set_ylabel('Densidad de probabilidad')
    ax.set_title(f'Distribución de Sobres Necesarios para el {int(pct_meta*100)} % del Álbum\n'
                 f'(N={n}, S={s}, meta={meta} estampas, {n_sim} simulaciones)')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('p4_dist_95pct.png', dpi=130)
    plt.show()

    return dict(media=media, p50=p50, p75=p75, p95=p95,
                prob_limite=prob, datos=arr, meta=meta)


# ─── PREGUNTA 5 ───────────────────────────────────────────────────────────────

def simular_pregunta5(n_sim=NUM_SIM, valores_s=(6, 7, 8), n=N):
    """
    Compara S = 6, 7, 8 estampas por sobre (N=980 fijo).

    Métricas clave:
      · Costo por estampa única (Q_total / N) — precio real de cada lámina
      · Porcentaje "desperdiciado" en repetidas
        = (estampas_repetidas / estampas_totales_compradas) × 100

    Devuelve dict {s → estadísticos}.
    """
    print("\n" + "=" * 62)
    print("  PREGUNTA 5 — Valor económico real por estampa única")
    print("=" * 62)

    resultados = {}
    for sv in valores_s:
        sims_sobres = []
        sims_rep    = []
        for _ in range(n_sim):
            album  = np.zeros(n, dtype=bool)
            sobres = 0
            rep    = 0
            while not album.all():
                nuevas = np.random.randint(0, n, sv)
                sobres += 1
                for e in nuevas:
                    if album[e]: rep += 1
                    else:        album[e] = True
            sims_sobres.append(sobres)
            sims_rep.append(rep)

        arr_sob   = np.array(sims_sobres, dtype=float)
        arr_rep   = np.array(sims_rep,    dtype=float)
        arr_tot   = arr_sob * sv                      # estampas totales compradas
        arr_costo = arr_sob * PRECIO_SOBRE            # gasto total (Q)

        costo_x_unica = arr_costo / n                # Q por lámina única
        pct_desper    = arr_rep / arr_tot * 100       # % "desperdiciado"
        lo, hi        = ic95(arr_sob)

        resultados[sv] = dict(
            media_sobres    = arr_sob.mean(),
            std_sobres      = arr_sob.std(),
            ic              = (lo, hi),
            media_costo     = arr_costo.mean(),
            costo_x_unica   = costo_x_unica.mean(),
            pct_desperdicio = pct_desper.mean(),
            datos_sobres    = arr_sob,
        )

    # ── Tabla comparativa ──
    print(f"\n  {'S':>3}  {'Sobres':>8}  {'Costo total (Q)':>16}  "
          f"{'Q/estampa única':>17}  {'% desperdiciado':>17}")
    print("  " + "-" * 70)
    for sv, r in resultados.items():
        print(f"  {sv:>3}  {r['media_sobres']:>8.1f}  {r['media_costo']:>16.2f}"
              f"  {r['costo_x_unica']:>17.4f}  {r['pct_desperdicio']:>16.2f}%")

    # ── Gráfica de barras agrupadas ──
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    xs       = np.arange(len(valores_s))
    width    = 0.35
    colors   = ['#4878d0', '#ee854a', '#6acc65']
    labels_x = [f'S={sv}' for sv in valores_s]

    # Panel 1 — Costo por estampa única
    vals_cpu = [resultados[sv]['costo_x_unica'] for sv in valores_s]
    bars1    = axes[0].bar(xs, vals_cpu, color=colors, edgecolor='black', width=0.5)
    for bar, val in zip(bars1, vals_cpu):
        axes[0].text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 0.01,
                     f'Q{val:.3f}', ha='center', va='bottom', fontweight='bold')
    axes[0].set_xticks(xs); axes[0].set_xticklabels(labels_x)
    axes[0].set_ylabel('Costo promedio por estampa única (Q)')
    axes[0].set_title(f'Costo por Estampa Única Obtenida\nN={n}')
    axes[0].grid(axis='y', alpha=0.3)

    # Panel 2 — % desperdiciado en repetidas
    vals_des = [resultados[sv]['pct_desperdicio'] for sv in valores_s]
    bars2    = axes[1].bar(xs, vals_des, color=colors, edgecolor='black', width=0.5)
    for bar, val in zip(bars2, vals_des):
        axes[1].text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 0.3,
                     f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
    axes[1].set_xticks(xs); axes[1].set_xticklabels(labels_x)
    axes[1].set_ylabel('Porcentaje "desperdiciado" en repetidas (%)')
    axes[1].set_title('Dinero Desperdiciado en Repetidas\npor Configuración de S')
    axes[1].grid(axis='y', alpha=0.3)

    plt.suptitle(f'Valor Económico Real por Estampa Única — N={n}', fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig('p5_valor_economico.png', dpi=130)
    plt.show()

    return resultados


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    """Ejecuta todas las simulaciones y muestra un resumen en consola."""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Simulaciones Monte Carlo — Álbum Mundial 2026         ║")
    print("║   MM3014 · Universidad del Valle de Guatemala            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\nParámetros: N={N}, S={S}, Q_sobre=Q{PRECIO_SOBRE}, Q_caja=Q{PRECIO_CAJA}")
    print(f"Simulaciones por pregunta: {NUM_SIM}\n")

    t0 = time.time()

    r1, _  = simular_pregunta1()
    r2, *_ = simular_pregunta2()
    r3     = simular_pregunta3()
    r4     = simular_pregunta4()
    r5     = simular_pregunta5()

    print("\n\n" + "=" * 62)
    print("  RESUMEN FINAL")
    print("=" * 62)
    print(f"  P1 · Sobres para completar 100 %:   {r1[1.00]['media_sobres']:.0f} (promedio)")
    print(f"  P2 · Presupuesto mínimo (50 %):     "
          f"Q{r2[0.50]['presup_sueltos']:.0f} sueltos  /  Q{r2[0.50]['presup_cajas']:.0f} cajas")
    best_k = min(r3['resultados'], key=lambda K: K)   # K=3 tiene mayor ahorro
    print(f"  P3 · Ahorro con K={best_k}:              "
          f"Q{r3['resultados'][best_k]['ahorro_medio']:.2f} "
          f"({r3['resultados'][best_k]['pct_ahorro']:.1f} %)")
    print(f"  P4 · P(≤1040 sobres para 95 %):     {r4['prob_limite']*100:.1f} %")
    mejor5 = min(r5.keys(), key=lambda sv: r5[sv]['costo_x_unica'])
    print(f"  P5 · S con menor Q/estampa única:   "
          f"S={mejor5}  (Q{r5[mejor5]['costo_x_unica']:.3f}/lámina)")
    print(f"\n  Tiempo total: {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
