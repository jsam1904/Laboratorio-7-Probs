# ⚽🃏 Simulación Monte Carlo: Álbum de Figuritas (Laboratorios 7 y 8)

**MM3014 · Teoría de Probabilidades | Universidad del Valle de Guatemala (UVG)**  
**Integrantes:**  
* 👤 **Javier Alvarado** - Carné 24546  
* 👤 **Hugo Méndez** - Carné 241265  

---

## 📝 Descripción del Proyecto

Este repositorio contiene la implementación y el análisis de una **Simulación de Monte Carlo** para modelar el proceso de completar un álbum de figuritas coleccionables. El estudio se divide en **tres etapas** distribuidas en dos laboratorios, y está disponible tanto en formato interactivo (**Jupyter Notebook**) como en script de Python ejecutable (**Script**).

### Parámetros del Problema
* **$N = 100$**: Total de figuritas distintas que componen el álbum.
* **$S = 7$**: Figuritas por sobre. Es muy importante destacar que las figuritas dentro de un mismo sobre son **únicas** (muestreo sin reemplazo al abrir un sobre).
* **$R = 10,000$**: Número de simulaciones independientes realizadas para asegurar la convergencia estadística (Estabilidad de Monte Carlo).
* **Precio por sobre (Etapa 3):** Q 9.50
* **Presupuesto total (Etapa 3):** Q 1 000

| Laboratorio | Etapas | Archivos |
| :---: | :--- | :--- |
| **Lab 7** | Etapa 1 — Distribución del nº de sobres | `Lab 7/lab7.py`, `Lab 7/lab7.ipynb` |
| **Lab 7** | Etapa 2 — Probabilidad en función del nº de sobres | `Lab 7/lab7.py`, `Lab 7/lab7.ipynb` |
| **Lab 8** | Etapa 3 — Incorporación del presupuesto y costo | `Lab 8/lab8.py`, `Lab 8/lab8.ipynb` |
| **Lab 8** | Etapa 4 — Efecto del intercambio de repetidas | `Lab 8/lab8.py`, `Lab 8/lab8.ipynb` |

---

## 🛠️ Metodología de la Simulación

La simulación modela la compra secuencial de sobres hasta que se marca como "adquirida" cada una de las $N=100$ figuritas. Para cada una de las $10,000$ repeticiones:
1. Se inicializa un vector booleano de tamaño $100$ en `False` (álbum vacío).
2. Se genera un ciclo que simula la compra de un sobre usando un muestreo aleatorio sin reemplazo (`np.random.choice(N, S, replace=False)`), garantizando que las $S=7$ figuritas dentro del sobre sean distintas.
3. Se actualiza el álbum y se contabilizan las figuritas repetidas (aquellas que ya habían sido marcadas como `True`).
4. El ciclo se detiene cuando todas las posiciones del vector son `True` (álbum completo).
5. Se registran la cantidad de sobres totales comprados y la cantidad de figuritas repetidas obtenidas.

---

## 📊 Resultados Generales (Etapa 1)

Los resultados obtenidos mediante la simulación de Monte Carlo se comparan con las aproximaciones teóricas derivadas de la **Teoría del Coleccionista de Cupones** (*Coupon Collector's Problem*):

| Métrica | Valor Teórico (Aproximado) | Valor Simulado (Promedio) | Diferencia Absoluta / Error Relativo |
| :--- | :---: | :---: | :---: |
| **Sobres para completar ($E[T]$)** | $74.0348$ sobres (usando $H_{100}$) | **$72.2456$ sobres** | $1.7892$ sobres ($2.47\%$) |
| **Figuritas repetidas ($E[R]$)** | $418.2439$ figuritas | **$405.7192$ figuritas** | $12.5247$ figuritas ($3.08\%$) |
| **Mínimo teórico de sobres** | $15$ sobres ($\lceil 100/7 \rceil$) | **$15$ sobres** | $0.00\%$ (No observado en la simulación) |
| **Desviación estándar de sobres ($\sigma$)** | *N/A* | **$17.4715$ sobres** | *N/A* ($CV \approx 24.18\%$) |
| **Probabilidad de requerir $>30$ sobres** | $\approx 1.0000$ | **$1.0000$ (100%)** | $0.00\%$ |

> [!NOTE]
> La aproximación teórica utiliza el **Número Armónico $H_{100} \approx \ln(100) + 0.5772 \approx 5.1824$**. La fórmula para el valor esperado de sobres es $E[T] = \frac{N}{S} H_N$. La excelente coincidencia con los datos empíricos valida la precisión del modelo de simulación.

---

## 📈 Explicación Detallada de las Gráficas

Las simulaciones generan dos visualizaciones clave que describen detalladamente el comportamiento probabilístico del problema.

### 1. Distribución del Número de Sobres (`distribucion_sobres.png`)
Esta gráfica muestra la frecuencia (o probabilidad empírica) del número de sobres necesarios para completar el álbum a lo largo de las $10,000$ ejecuciones.

* **Eje X (Horizontal - Número de sobres comprados):** Representa la cantidad de sobres que le tomó a un coleccionista completar el álbum.
* **Eje Y (Vertical - Frecuencia):** Indica en cuántas de las $10,000$ simulaciones se requirió exactamente esa cantidad de sobres.
* **Línea Roja Discontinua (Media Muestral $\approx 72.25$ sobres):** Muestra el promedio de sobres necesarios.
* **Línea Verde Continua (Mínimo Teórico $= 15$ sobres):** El escenario utópico en el que nunca sale una sola figurita repetida. Nótese que la probabilidad de lograr esto es prácticamente cero; en las 10,000 simulaciones **ningún** caso logró completarse en 15 sobres.
* **Análisis de la Forma:** La distribución presenta una marcada **asimetría positiva (sesgo a la derecha)**. Esto ilustra el clásico fenómeno de la "cola larga" (*long-tail*): es sumamente fácil conseguir las primeras figuritas, pero las últimas requieren abrir decenas de sobres debido a la bajísima probabilidad de obtener justamente las faltantes. Algunos coleccionistas con "mala suerte" requirieron más de $120$ sobres.

<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/73572bec-846d-4240-b474-0d646ee4e2ba" />

---

### 2. Probabilidad de Éxito en función del Presupuesto (`probabilidad_completar.png`)
Esta gráfica de barras representa la probabilidad acumulada de haber completado el álbum tras comprar una cantidad fija $M$ de sobres.


* **Eje X (Horizontal - Sobres Comprados $M$):** Hitos discretos de sobres evaluados ($20, 25, 30, \dots, 80$).
* **Eje Y (Vertical - Probabilidad de Éxito):** La probabilidad empírica $P(\text{Completar} \mid M \text{ sobres})$.
* **Línea Roja Discontinua (Umbral del 50%):** Marca la probabilidad de "moneda al aire" (50% de probabilidad de éxito).
* **Análisis de las Barras:**
  * Para **$M \le 30$ sobres**, la probabilidad de completar el álbum es **prácticamente $0\%$**. Comprar el doble del mínimo teórico sigue siendo insuficiente.
  * Para **$M = 50$ sobres**, la probabilidad de éxito es muy baja, de apenas **$5.63\%$**.
  * El umbral de la mitad de probabilidad (50%) se supera por primera vez a los **$70$ sobres** (alcanzando un **$53.36\%$**).
  * A los **$80$ sobres**, un coleccionista tiene un **$73.26\%$** de probabilidad de haber terminado su álbum.

<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/ceb7c7fb-9843-41cc-9917-9c1fd8f3f2ac" />

---

## 🔍 Análisis Profundo (Etapa 2)

### 1. Relación entre la Mediana y el Hito de Éxito
La **mediana muestral** calculada en la simulación es de **$69$ sobres**. Por definición, la mediana es el valor que acumula exactamente el $50\%$ de la probabilidad. 
Como los hitos evaluados en la Etapa 2 se incrementan de forma discreta, **$M = 70$** es el primer valor evaluado que es mayor o igual a la mediana. Por ende, es matemáticamente consistente que $M = 70$ sea el primer hito en superar el umbral del $50\%$ de éxito ($53.36\%$).

### 2. Cota de la Unión para $M = 50$
La **Cota de la Unión** (*Union Bound*) nos provee un límite superior teórico para la probabilidad de fracaso (es decir, la probabilidad de que al menos una figurita quede sin colectar después de abrir $M$ sobres):

$$P(\text{Fracaso}) \le N \cdot e^{-\frac{M \cdot S}{N}}$$

Para un presupuesto de **$M = 50$** sobres:
* **Probabilidad de fracaso simulada:** $1 - P(\text{Éxito}) = 1 - 0.0563 = 0.9437$ ($94.37\%$).
* **Cota de la Unión teórica:** 
  $$100 \cdot e^{-\frac{50 \cdot 7}{100}} = 100 \cdot e^{-3.5} \approx 3.0197 \text{ (o } 301.97\% \text{)}$$

> [!WARNING]
> **Evaluación de Utilidad de la Cota:**  
> En este escenario, la Cota de la Unión **no es útil**. Debido a que cualquier probabilidad está acotada superiormente por $1$ ($100\%$) de forma trivial, una cota superior de $3.0197$ no aporta información relevante. 
>
> La Cota de la Unión asume que los eventos de que falte cada estampa individual son disjuntos (no se traslapan), lo cual es una pésima aproximación cuando $M$ es pequeño y las intersecciones de figuritas faltantes son muy grandes. Esta cota solo se vuelve matemáticamente útil (menor a $1$) cuando $M > \frac{N \ln(N)}{S}$, es decir, a partir de **$M = 66$ sobres**.

---

## 💰 Etapa 3 — Incorporación del Presupuesto y Costo (Lab 8)

En la Etapa 3 se agrega una restricción económica realista: cada sobre cuesta **Q 9.50** y el coleccionista cuenta con un presupuesto de **Q 1 000**. La simulación compra sobres mientras quede presupuesto y el álbum no esté completo.

### 📊 Resultados de la Simulación (Etapa 3)

| Métrica | Valor |
| :--- | :---: |
| **P(completar álbum con Q 1 000)** | **0.9488 (94.88%)** |
| Sobres esperados comprados (todas las sims.) | 71.61 |
| Estampas distintas esperadas en sims. fallidas | 98.96 |
| Simulaciones exitosas | 9 488 / 10 000 |
| Simulaciones fallidas | 512 / 10 000 |

> [!NOTE]
> La media de ~72 sobres es muy inferior al límite de 105 sobres comprables: la mayoría de los coleccionistas completa el álbum sin agotar el presupuesto. Las simulaciones fallidas quedan con ~99/100 estampas — les falta **apenas una** en promedio.

### 📈 Gráfica: Completó vs No Completó (`proporcion_completar_budget.png`)
<img width="1050" height="900" alt="image" src="https://github.com/user-attachments/assets/fc4b6128-6e7e-4068-a547-cb0a4c9b2840" />


Diagrama de barras que muestra la proporción de simulaciones en que se completó el álbum frente a las que se agotó el presupuesto antes de completarlo.

---

## 🔍 Análisis Profundo (Etapa 3)

### Pregunta 1 — ¿Los 105 sobres comprables alcanzan el mínimo teórico sin repetidos?

$$\text{Máximo comprables} = \left\lfloor \frac{Q\,1000}{Q\,9.50} \right\rfloor = 105 \text{ sobres}$$

$$\text{Mínimo teórico} = \left\lceil \frac{N}{S} \right\rceil = \left\lceil \frac{100}{7} \right\rceil = 15 \text{ sobres}$$

**Respuesta: SÍ** ($105 \ge 15$, con 90 sobres de holgura). El presupuesto es más que suficiente para el caso ideal. En la práctica, sin embargo, siempre hay repeticiones y la media de sobres necesarios es ~72.

---

### Pregunta 2 — Caja de 104 sobres (Q 975) vs sobres sueltos

La caja tiene un precio unitario de $Q\,975/104 \approx Q\,9.375$, más barato que el suelto ($Q\,9.50$). Con el mismo presupuesto de Q 975 en sueltos solo se obtienen $\lfloor 975/9.50 \rfloor = 102$ sobres.

| Modalidad | Sobres | Gasto | P(completar) |
| :--- | :---: | :---: | :---: |
| Sueltos con Q 975 (mismo presupuesto) | 102 | Q 969.00 | **0.9378** |
| **Caja de 104 sobres** | **104** | **Q 975.00** | **0.9468** |
| Sueltos con Q 1 000 (presupuesto completo) | 105 | Q 997.50 | 0.9488 |

La caja entrega **2 sobres más** con el mismo presupuesto y supera a los sueltos equivalentes en **+0.90 p.p.**

---

### Pregunta 3 — Estrategia mixta óptima dentro de Q 1 000

| Estrategia | Sobres | Gasto | P(completar) |
| :--- | :---: | :---: | :---: |
| Solo sueltos | 105 | Q 997.50 | 0.9488 |
| Solo caja | 104 | Q 975.00 | 0.9468 |
| **Caja + 2 sueltos ★** | **106** | **Q 994.00** | **0.9544** |

#### Mejor estrategia: 1 caja (104 sobres, Q 975) + 2 sobres sueltos (Q 19) = Q 994

La caja ahorra Q 13 frente a 104 sueltos. Esos Q 13 más Q 2.50 de vuelto de la estrategia de sueltos puros financian **2 sobres extra** (total: 106 sobres), logrando la mayor probabilidad de completar el álbum con **+0.56 p.p.** sobre solo sueltos, ahorrando además Q 3.50.

---

## 🔄 Etapa 4 — Efecto del intercambio de repetidas (Lab 8)

En la Etapa 4 se introduce un mecanismo de intercambio: cada $K$ estampas repetidas se pueden canjear por 1 estampa nueva (a elegir entre las que faltan). Se exploran los valores de $K \in \{1, 2, 5, 10\}$.

### 📊 Parte A: Simulación hasta completar el álbum

| Configuración | Media de Sobres | Desviación Estándar | Reducción vs. Sin Intercambio |
| :--- | :---: | :---: | :---: |
| **Sin intercambio** | ~72.25 sobres | 17.47 | - |
| **K = 10** | ~35.15 sobres | 2.45 | **51.35%** |
| **K = 5** | ~28.11 sobres | 1.44 | **61.09%** |
| **K = 2** | ~19.85 sobres | 0.54 | **72.53%** |
| **K = 1** | ~15.00 sobres | 0.00 | **79.24%** |

> [!NOTE]
> La disminución de K reduce drásticamente el número medio de sobres necesarios. La mejora no es lineal: pasar de $K=10$ a $K=5$ ofrece una mejora importante, pero los saltos hacia $K=2$ y $K=1$ presentan ganancias masivas.

### Gráfica Distribución de sobres necesarios para completar el álbum (`hist_intercambio.png`)

<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/91f08ac7-d203-4014-a95b-89c28cb72813" />

### 📈 Parte B: Probabilidad en función de M sobres

Se evaluaron secuencias fijas de $M$ sobres ($20, 25, 30, \dots, 70$) para determinar los puntos donde se alcanzan ciertas probabilidades clave:

| Configuración | Sobres para 50% | Sobres para 75% | Sobres para 90% |
| :--- | :---: | :---: | :---: |
| **Sin intercambio** | 70 | >70 | >70 |
| **K = 10** | 35 | 40 | 40 |
| **K = 5** | 30 | 30 | 30 |
| **K = 2** | 20 | 20 | 20 |
| **K = 1** | 20 | 20 | 20 |

### Gráfica Probabilidad de completar el álbum vs sobres comprados (`prob_vs_M_intercambio.png`)
<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/e61878c0-1400-4346-b87a-3f5a1e6e3e0d" />

---

## 🔍 Análisis Profundo (Etapa 4)

### 1. Ahorro monetario (K = 2)
Para $K = 2$, se ahorran en promedio **52.40 sobres** respecto al caso sin intercambio. Multiplicando por Q 9.50/sobre, esto representa un ahorro monetario sustancial de **Q 497.80**.

### 2. Rendimientos Decrecientes
Valores de $K$ más altos (por ejemplo, mayores a 10) ofrecen beneficios marginales muy reducidos. Con tasas exigentes, la mayoría de figuritas repetidas nunca alcanzan el umbral para canjearse y el efecto sobre la distribución se diluye fuertemente.

### 3. Costo Efectivo del Canje
Aunque las repetidas provienen de sobres ya pagados (costo hundido), su "costo de oportunidad" (inversión indirecta por cada estampa canjeada) es de $K \cdot (9.50 / 7)$ Quetzales. 
Por ejemplo, para $K = 2$ es de Q 2.71, y para $K = 10$ es de Q 13.57. $K = 1$ es la tasa más rentable pues transforma cada repetida inútil directamente en una estampa útil.

---

## 🚀 Cómo Ejecutar el Proyecto

### Clonar el repositorio
```bash
git clone https://github.com/hmndzzl/Laboratorio-8-Probs.git
```
### Ir a la carpeta

```bash
cd Laboratorio-8-Probs
```

### Requisitos Previos
Asegúrate de tener instalado Python y las bibliotecas necesarias:
```bash
pip install numpy matplotlib
```

### Lab 7 — Etapas 1 y 2

#### Lab 7 · Jupyter Notebook (interactivo)

```bash
jupyter notebook "Lab 7/lab7.ipynb"
```

#### Lab 7 · Script de consola

```bash
python "Lab 7/lab7.py"
```

### Lab 8 — Etapas 3 y 4

#### Lab 8 · Jupyter Notebook (interactivo)

```bash
jupyter notebook "Lab 8/lab8.ipynb"
```

#### Lab 8 · Script de consola

```bash
python "Lab 8/lab8.py"
```

El script imprimirá el análisis detallado y las respuestas a las preguntas directamente en la consola, y guardará los gráficos correspondientes (`proporcion_completar_budget.png`, `hist_intercambio.png`, `prob_vs_M_intercambio.png`) en el directorio de trabajo.
