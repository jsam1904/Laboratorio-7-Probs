# ⚽🃏 Simulación Monte Carlo: Álbum de Figuritas (Laboratorios 7, 8 y 9)

**MM3014 · Teoría de Probabilidades | Universidad del Valle de Guatemala (UVG)**  
**Integrantes:**  
* 👤 **Javier Alvarado** - Carné 24546  
* 👤 **Hugo Méndez** - Carné 241265  

---

## 📝 Descripción del Proyecto

Este repositorio contiene la implementación y el análisis de una **Simulación de Monte Carlo** para modelar el proceso de completar álbumes de figuritas coleccionables. El estudio se divide en **cinco etapas** distribuidas en tres laboratorios, y está disponible tanto en formato interactivo (**Jupyter Notebook**) como en script de Python ejecutable (**Script**).

| Laboratorio | Etapas | Parámetros clave | Archivos |
| :---: | :--- | :--- | :--- |
| **Lab 7** | Etapa 1 — Distribución del nº de sobres | N=100, S=7, R=10 000 | `Lab 7/lab7.py`, `Lab 7/lab7.ipynb` |
| **Lab 7** | Etapa 2 — Probabilidad en función del nº de sobres | N=100, S=7, R=10 000 | `Lab 7/lab7.py`, `Lab 7/lab7.ipynb` |
| **Lab 8** | Etapa 3 — Incorporación del presupuesto y costo | N=100, S=7, R=10 000 | `Lab 8/lab8.py`, `Lab 8/lab8.ipynb` |
| **Lab 8** | Etapa 4 — Efecto del intercambio de repetidas | N=100, S=7, R=10 000 | `Lab 8/lab8.py`, `Lab 8/lab8.ipynb` |
| **Lab 9** | Etapa 5 — Álbum del Mundial 2026 (5 preguntas) | N=980, S=7, R=2 000 | `Lab 9/simulaciones_mundial2026.py`, `Lab 9/lab9.ipynb` |

---

## 🛠️ Metodología de la Simulación

La simulación modela la compra secuencial de sobres hasta que se marca como "adquirida" cada una de las $N$ figuritas. Para cada repetición:
1. Se inicializa un vector booleano de tamaño $N$ en `False` (álbum vacío).
2. Se genera un ciclo que simula la compra de un sobre usando un muestreo aleatorio (`np.random.randint(0, N, S)`).
3. Se actualiza el álbum y se contabilizan las figuritas repetidas.
4. El ciclo se detiene cuando todas las posiciones del vector son `True` (álbum completo).
5. Se registran la cantidad de sobres totales comprados y la cantidad de figuritas repetidas obtenidas.

---

## 📊 LABORATORIO 7 — Etapas 1 y 2

### Parámetros
* **$N = 100$**: Total de figuritas distintas.
* **$S = 7$**: Figuritas por sobre (únicas dentro del sobre — sin reemplazo).
* **$R = 10{,}000$**: Simulaciones independientes.

### Resultados Generales (Etapa 1)

Los resultados se comparan con la **Teoría del Coleccionista de Cupones** (*Coupon Collector's Problem*):

| Métrica | Valor Teórico | Valor Simulado | Error Relativo |
| :--- | :---: | :---: | :---: |
| **Sobres para completar ($E[T]$)** | $74.03$ sobres | **$72.25$ sobres** | $2.47\%$ |
| **Figuritas repetidas ($E[R]$)** | $418.24$ figuritas | **$405.72$ figuritas** | $3.08\%$ |
| **Mínimo teórico de sobres** | $15$ sobres | **$15$ sobres** | $0.00\%$ |
| **Desviación estándar de sobres ($\sigma$)** | *N/A* | **$17.47$ sobres** | *CV ≈ 24.18%* |
| **P(requerir > 30 sobres)** | $\approx 1.0000$ | **$1.0000$ (100%)** | $0.00\%$ |

> [!NOTE]
> La aproximación teórica usa el **Número Armónico $H_{100} \approx \ln(100) + 0.5772$**. La fórmula es $E[T] = \frac{N}{S} H_N$. La coincidencia con los datos empíricos valida la precisión del modelo.

### Gráficas

#### 1. Distribución del Número de Sobres (`distribucion_sobres.png`)
<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/73572bec-846d-4240-b474-0d646ee4e2ba" />

La distribución presenta una marcada **asimetría positiva (sesgo a la derecha)**, el clásico fenómeno de la "cola larga": las primeras figuritas son fáciles de conseguir, pero las últimas requieren decenas de sobres adicionales.

---

#### 2. Probabilidad de Éxito en función del nº de Sobres (`probabilidad_completar.png`)
<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/ceb7c7fb-9843-41cc-9917-9c1fd8f3f2ac" />

| Sobres ($M$) | P(Completar) |
| :---: | :---: |
| ≤ 30 | ≈ 0% |
| 50 | 5.63% |
| **70** | **53.36%** *(primer hito ≥ 50%)* |
| 80 | 73.26% |

### Análisis Profundo (Etapa 2)

**Mediana vs hito de éxito:** La mediana muestral es **69 sobres**. El primer hito discreto evaluado que la supera es $M = 70$ (53.36%), lo cual es matemáticamente consistente.

**Cota de la Unión para $M = 50$:**

$$P(\text{Fracaso}) \le N \cdot e^{-\frac{M \cdot S}{N}} = 100 \cdot e^{-3.5} \approx 301.97\%$$

> [!WARNING]
> La cota supera el 100%, por lo que **no es útil** en este escenario. Solo se vuelve informativa cuando $M > \frac{N \ln(N)}{S} \approx 66$ sobres.

---

## 💰 LABORATORIO 8 — Etapas 3 y 4

### Etapa 3 — Incorporación del Presupuesto y Costo

**Precio por sobre:** Q 9.50 | **Presupuesto total:** Q 1 000 | **Máximo comprables:** 105 sobres

| Métrica | Valor |
| :--- | :---: |
| **P(completar álbum con Q 1 000)** | **94.88%** |
| Sobres esperados comprados | 71.61 |
| Estampas distintas en sims. fallidas | 98.96 / 100 |
| Simulaciones exitosas | 9 488 / 10 000 |

<img width="1050" height="900" alt="image" src="https://github.com/user-attachments/assets/fc4b6128-6e7e-4068-a547-cb0a4c9b2840" />

**Estrategia óptima con Q 1 000:**

| Estrategia | Sobres | Gasto | P(completar) |
| :--- | :---: | :---: | :---: |
| Solo sueltos | 105 | Q 997.50 | 94.88% |
| Solo caja | 104 | Q 975.00 | 94.68% |
| **Caja + 2 sueltos ★** | **106** | **Q 994.00** | **95.44%** |

✅ **Mejor opción:** 1 caja (Q 975) + 2 sueltos (Q 19) = **Q 994**, que entrega 106 sobres y la mayor probabilidad de completar el álbum.

---

### Etapa 4 — Efecto del Intercambio de Repetidas

Cada $K$ estampas repetidas se canjean por 1 nueva (de las faltantes). Se exploran $K \in \{1, 2, 5, 10\}$.

| Configuración | Media de Sobres | Desv. Estándar | Reducción vs. Sin Intercambio |
| :--- | :---: | :---: | :---: |
| Sin intercambio | ~72.25 | 17.47 | — |
| **K = 10** | ~35.15 | 2.45 | **51.35%** |
| **K = 5** | ~28.11 | 1.44 | **61.09%** |
| **K = 2** | ~19.85 | 0.54 | **72.53%** |
| **K = 1** | ~15.00 | 0.00 | **79.24%** |

<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/91f08ac7-d203-4014-a95b-89c28cb72813" />

<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/e61878c0-1400-4346-b87a-3f5a1e6e3e0d" />

**Análisis financiero (K = 2):** Ahorro de ~52.40 sobres → **Q 497.80** respecto al caso sin intercambio.

---

## ⚽ LABORATORIO 9 — Etapa 5: Álbum del Mundial 2026

### Parámetros

| Parámetro | Valor |
| :--- | :---: |
| N — estampas totales | **980** |
| S — estampas por sobre | 7 |
| Precio sobre suelto | Q 9.50 |
| Precio caja (104 sobres) | Q 975.00 |
| Simulaciones por pregunta | 2 000 |
| Semilla aleatoria | 42 |

> Las estampas se eligen **uniformemente al azar con reemplazo** dentro del sobre (pueden existir duplicados dentro de un mismo sobre).

---

### P1 — Puntos de Corte de Completitud

**Objetivo:** Determinar cuántos sobres y repetidas se necesitan en promedio para completar el 75%, 90% y 100% del álbum.

| Umbral | Media de sobres | IC 95% | Repetidas promedio |
| :--- | :---: | :---: | :---: |
| **75%** (735 estampas) | 194.3 | (194.1, 194.6) | 624.7 |
| **90%** (882 estampas) | 322.4 | (321.8, 322.9) | 1 374.2 |
| **100%** (980 estampas) | 1 053.5 | (1 045.6, 1 061.5) | 6 394.6 |

<img src="Lab 9/p1_curva_completitud.png" alt="Curva de completitud Lab 9" width="800"/>

> **Interpretación:** El tramo 0%→90% requiere ~322 sobres, mientras que el tramo 90%→100% requiere ~731 sobres adicionales — casi el **doble** del camino previo. El fenómeno del coleccionista de cupones se acentúa dramáticamente con N=980.

---

### P2 — Presupuesto Óptimo por Tramos

**Objetivo:** Determinar el presupuesto mínimo para 50%, 75% y 90% de probabilidad de completar el álbum, comparando sobres sueltos vs. cajas.

| Objetivo | Sobres (percentil) | Sueltos (Q) | Cajas | Cajas (Q) | Conviene |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **50%** | 1 021 | Q 9 699.50 | 10 | Q 9 750.00 | **Sueltos** |
| **75%** | 1 142 | Q 10 849.00 | 11 | Q 10 725.00 | **Cajas** |
| **90%** | 1 294 | Q 12 293.00 | 13 | Q 12 675.00 | **Sueltos** |

<img src="Lab 9/p2_presupuesto_optimo.png" alt="Presupuesto óptimo Lab 9" width="800"/>

> **Nota:** Los sobres sueltos permiten granularidad de Q 9.50, mientras que las cajas obligan a comprar en bloques de Q 975 (104 sobres), lo que puede generar un excedente forzado. La curva de cajas es **escalonada**: dentro de un bloque de Q 975 ningún aumento de presupuesto mejora la probabilidad.

---

### P3 — Análisis Comparativo de Tasas de Intercambio (K = 3, 5, 7)

**Objetivo:** Cuantificar el ahorro en quetzales al completar el álbum según la tasa de intercambio K (K repetidas → 1 estampa nueva faltante).

**Línea base (sin intercambio):** Q 9 859.77 promedio para completar el álbum.

| K | Sobres (media) | Costo total (Q) | Ahorro (Q) | Ahorro % |
| :--- | :---: | :---: | :---: | :---: |
| **Sin intercambio** | 1 037.9 | Q 9 859.77 | — | — |
| **K = 3** | 230.8 | Q 2 192.47 | **Q 7 667.30** | **77.8%** |
| **K = 5** | 281.2 | Q 2 671.79 | **Q 7 187.98** | **72.9%** |
| **K = 7** | 317.5 | Q 3 016.34 | **Q 6 843.43** | **69.4%** |

**Rendimiento marginal decreciente:**
- K=7 → K=5: Δahorro = **−Q 344.55**
- K=5 → K=3: Δahorro = **−Q 479.33**

<img src="Lab 9/p3_tasas_intercambio.png" alt="Tasas de intercambio Lab 9" width="800"/>

> **Conclusión:** K más pequeño siempre ahorra más, pero el salto de K=7 a K=5 ya representa un ahorro masivo (~Q 344 más). Un sistema con K=5 ofrece excelente relación ahorro/complejidad para el editor.

---

### P4 — Distribución para Alcanzar el 95% del Álbum

**Objetivo:** Caracterizar la distribución del número de sobres para obtener **931 estampas** (95% de 980) y calcular P(sobres ≤ 1040), equivalente a 10 cajas.

| Estadístico | Valor |
| :--- | :---: |
| Media | 418.3 sobres |
| Percentil 50 (Mediana) | 418 sobres |
| Percentil 75 | 430 sobres |
| Percentil 95 | 448 sobres |
| **P(sobres ≤ 1040)** | **100.0%** |

<img src="Lab 9/p4_dist_95pct.png" alt="Distribución 95% Lab 9" width="800"/>

> **Resultado clave:** 10 cajas (1 040 sobres) son **más que suficientes** para alcanzar el 95% del álbum en prácticamente el 100% de los casos. La distribución es aproximadamente normal con leve sesgo a la derecha.

---

### P5 — Valor Económico Real por Estampa Única (S = 6, 7, 8)

**Objetivo:** Comparar el costo por estampa única y el porcentaje de dinero "desperdiciado" en repetidas para S = 6, 7 y 8.

| S | Sobres (media) | Costo total (Q) | Q por estampa única | % desperdiciado |
| :---: | :---: | :---: | :---: | :---: |
| **6** | 1 221.2 | Q 11 601.86 | Q 11.839 | 86.25% |
| **7** | 1 044.3 | Q 9 921.14 | Q 10.124 | 86.24% |
| **8** | 916.5 | Q 8 707.22 | Q 8.885 | 86.28% |

<img src="Lab 9/p5_valor_economico.png" alt="Valor económico Lab 9" width="800"/>

> **Hallazgo notable:** El **porcentaje desperdiciado en repetidas** es prácticamente idéntico (~86.2%) para todos los valores de S. Sin embargo, el **costo por estampa única** disminuye con S mayor, ya que sobres con más láminas requieren menos compras totales para cubrir el álbum. Desde la perspectiva del comprador, **mayor S siempre es más eficiente económicamente**.

---

## 🔍 Conclusiones Generales

| Pregunta | Hallazgo principal |
| :--- | :--- |
| **P1 (Cortes de completitud)** | El tramo 90%→100% cuesta casi el doble que 0%→90%. Con N=980 el fenómeno del coleccionista es extremo. |
| **P2 (Presupuesto óptimo)** | Sueltos vs. cajas depende del objetivo: 50% y 90% → sueltos; 75% → cajas. |
| **P3 (Intercambios K)** | K=3 ahorra un 77.8% del costo. Hay rendimientos decrecientes pero todos los valores de K son muy beneficiosos. |
| **P4 (Distribución 95%)** | 10 cajas (1 040 sobres) garantizan el 95% del álbum con probabilidad del 100%. |
| **P5 (Valor por estampa)** | S más grande → menor costo por estampa única; el % de desperdicio se mantiene constante (~86%). |

---

## 🚀 Cómo Ejecutar el Proyecto

### Clonar el repositorio
```bash
git clone https://github.com/jsam1904/Laboratorio-7-Probs.git
cd Laboratorio-7-Probs
```

### Requisitos Previos
```bash
pip install numpy matplotlib jupyter
```

### Lab 7 — Etapas 1 y 2

```bash
jupyter notebook "Lab 7/lab7.ipynb"
# o bien
python "Lab 7/lab7.py"
```

### Lab 8 — Etapas 3 y 4

```bash
jupyter notebook "Lab 8/lab8.ipynb"
# o bien
python "Lab 8/lab8.py"
```

### Lab 9 — Etapa 5 (Álbum Mundial 2026)

```bash
jupyter notebook "Lab 9/lab9.ipynb"
# o bien
python "Lab 9/simulaciones_mundial2026.py"
```

> Los scripts generan automáticamente los gráficos correspondientes en su carpeta de laboratorio:
> - **Lab 7:** `distribucion_sobres.png`, `probabilidad_completar.png`
> - **Lab 8:** `proporcion_completar_budget.png`, `hist_intercambio.png`, `prob_vs_M_intercambio.png`
> - **Lab 9:** `p1_curva_completitud.png`, `p2_presupuesto_optimo.png`, `p3_tasas_intercambio.png`, `p4_dist_95pct.png`, `p5_valor_economico.png`
