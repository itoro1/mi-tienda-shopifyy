# AUDITORÍA TÉCNICA — ITorostore (Copia de Dawn — PRO)
**Tema:** `gid://shopify/OnlineStoreTheme/200413446469`  
**Rol:** UNPUBLISHED (preview) — seguro para trabajar  
**Fecha:** 2026-06-08

---

## 1. MAPA DEL REPOSITORIO

### Layout (2 ficheros)
| Archivo | Tamaño | Función |
|---------|--------|---------|
| `layout/theme.liquid` | 24 KB | Raíz HTML: head, fuentes, CSS global, scripts, dark-mode toggle, back-to-top, WhatsApp |
| `layout/password.liquid` | 14 KB | Página de contraseña (Dawn estándar) |

### Templates (10 ficheros JSON)
| Template | Secciones configuradas |
|----------|----------------------|
| `index.json` | 12 secciones custom itoro (hero-premium, features, categorias, finder, urgencia, packs, como-funciona, comparador, faq, compra-banner, banner) |
| `product.json` | main-product (Dawn) + it-trust-product + it-product-extras |
| `collection.json` | main-collection-product-grid (Dawn) |
| `cart.json` | main-cart-items + main-cart-footer (Dawn) |
| `page.json` / `page.contact.json` | Páginas estándar |
| `404.json`, `blog.json`, `article.json`, `search.json` | Dawn estándar |

### Secciones custom ITORO (confirmadas)
| Sección | Tamaño | Función |
|---------|--------|---------|
| `sections/it-announcement-bar.liquid` | 1.8 KB | Barra superior con scroll infinito (mensajes clave) |
| `sections/it-hero.liquid` | 2.9 KB | Hero simple v1 (posiblemente obsoleto) |
| `sections/it-faq.liquid` | 3.2 KB | FAQ con acordeones JS inline |
| `sections/it-reviews.liquid` | 7.0 KB | Grid de reseñas (avatares externos!) |
| `sections/it-popup-email.liquid` | 4.2 KB | Popup captación email |

### Secciones Dawn (sin modificar)
`header.liquid` (22 KB), `footer.liquid` (20 KB), `main-product.liquid` (113 KB), `main-collection-product-grid.liquid` (14 KB), `featured-collection.liquid` (18 KB), `image-banner.liquid` (18 KB), `rich-text.liquid` (12 KB), `main-cart-*.liquid`, `announcement-bar.liquid`

### Snippets custom ITORO
| Snippet | Tamaño | Función |
|---------|--------|---------|
| `buy-buttons.liquid` | Variable | Botones CTA con bifurcación bajo-pedido/normal |
| `itoro-reservar.liquid` | Variable | Botón Reservar 50 € + envío + trust |
| `it-whatsapp.liquid` | 1.5 KB | Botón flotante WhatsApp |
| `it-theme-bar.liquid` | 1.5 KB | Toggle claro/oscuro persistido en localStorage |
| `it-schema-org.liquid` | 1.7 KB | JSON-LD Product + Organization |
| `meta-tags.liquid` | 1.7 KB | Canonical, hreflang, OG |

### Snippets Dawn
`card-product.liquid` (34 KB), `product-media-gallery.liquid` (14 KB), `product-variant-picker.liquid` (3.4 KB), `price.liquid` (5.5 KB) y ~15 más.

### Assets CSS custom ITORO
| Archivo | Tamaño | Carga | Función |
|---------|--------|-------|---------|
| `itoro-dark-mode.css` | 7.6 KB | **Crítico (head)** | Design tokens `--it-*`, dark mode global, botones, FAQ, reviews |
| `itoro-trust-extras.css` | 13 KB | **Crítico (head)** | Trust badges, secciones de garantías |
| `itoro-collection.css` | 6.1 KB | **Crítico (head)** | Tarjetas catálogo, filtros, tokens `--ico-*` |
| `itoro-mobile.css` | 8.9 KB | **Crítico (head)** | Responsive overrides para todos los componentes |
| `itoro-hero-v2.css` | 13.6 KB | Bajo demanda | Hero con tabs (tokens `--ih-*`) |
| `itoro-hero.css` | 6.6 KB | Bajo demanda(?) | Hero v1 — ¿en uso? |
| `itoro-pack-selector.css` | 6.8 KB | Bajo demanda | Selector de packs (tokens `--ips-*`) |
| `itoro-trade-in.css` | 13.8 KB | Bajo demanda | Trade-in |
| `itoro-trust.css` | 1 KB | Por snippet | Widget envío + trust row (PDP) |

### Assets JS custom ITORO
| Archivo | Tamaño | Función |
|---------|--------|---------|
| `itoro-reservar.js` | 1.9 KB | Lógica reserva: mapeo variante → señal, POST cart/add, redirect checkout |
| `itoro-trade-in.js` | 17.4 KB | Calculadora trade-in |

---

## 2. AUDITORÍA POR ÁREAS

### A) Coherencia visual / Sistema de diseño — ⭐⭐ (2/5)

**Hallazgos:**
- ❌ **4 sistemas de tokens CSS distintos** coexisten sin jerarquía:
  - `--it-*` (itoro-dark-mode.css) — base global
  - `--ico-*` (itoro-collection.css) — colecciones
  - `--ih-*` (itoro-hero-v2.css) — hero v2
  - `--ips-*` (itoro-pack-selector.css) — packs
  - Los valores dorado son `#d4af37` en unos y `#d4af37` en otros — coincide por suerte, no por diseño
- ❌ **Dos sistemas de botones**: `.it-btn-primary / .it-btn-secondary` (custom) vs `.button.button--primary / .button.button--secondary` (Dawn). En la PDP se ven ambos.
- ❌ **Dos sistemas de dark mode**: `[data-theme="dark"]` (itoro) + `color-scheme--dark / [data-color-scheme="dark"]` (Dawn nativo) — el hero-v2 tiene 5 selectores distintos por si acaso.
- ❌ `itoro-hero.css` (v1, 6.6 KB) puede estar cargándose aunque no se use — CSS sin usar.
- ✅ Los tokens `--it-*` están bien definidos con fallback y cubren bg, text, border, accent, radius.
- ✅ El sistema de tipografía usa `clamp()` correctamente.

**Impacto:** ALTO — dificulta mantener consistencia y añade peso.

---

### B) Home / Hero — ⭐⭐⭐ (3/5)

**Hallazgos:**
- ✅ Estructura narrativa sólida: anuncio → hero → features → finder → urgencia → packs → cómo funciona → comparador → FAQ → compra/vende
- ✅ Hero premium con tabs Nuevo/Segunda Mano, precio, comparativa, 2 CTAs
- ✅ Barra de anuncios con scroll infinito y 5 mensajes clave
- ✅ FAQ con 7 preguntas reales y respuestas honestas
- ❌ **Rating "4.9 Google" en hero pills sin respaldo verificable** — roza Directiva Omnibus si no hay datos reales publicados
- ❌ Las 12 secciones son secciones *custom* definidas en `templates/index.json` — muchas apuntan a secciones (`it-slider-valor`, `it-hero-premium`, `it-features`, `it-categorias`, `it-finder`, `it-urgencia`, `it-packs-cargadores`, `it-como-funciona`, `it-comparador`, `it-compra-banner`, `it-banner`) que **no aparecen en la lista de archivos del tema** → esas secciones o bien están sin crear o no se pudieron listar. Si no existen, el home está roto.
- ❌ Hero v1 (`it-hero.liquid`) y CSS v1 (`itoro-hero.css`) posiblemente obsoletos pero cargando.

**Impacto:** CRÍTICO si las secciones custom faltan — el home estaría en blanco.

---

### C) Tarjetas de producto y colección — ⭐⭐⭐ (3/5)

**Hallazgos:**
- ✅ `itoro-collection.css` con sistema de tokens completo, dark mode, chips de filtro, etiquetas NEW/SALE
- ✅ `card-product.liquid` grande (34 KB) — probablemente Dawn extendido con overrides de precio, estado, etc.
- ❌ `card-product.liquid` no está modificado con lógica custom de "Reservar por 50 €" visible en tarjeta
- ❌ No hay indicador claro de "bajo pedido" vs "en stock" en las tarjetas de colección
- ❌ Sin lazy-load explícito en imágenes de colección (Dawn lo pone `loading="lazy"` por defecto — OK, pero srcset puede no estar optimizado)

**Impacto:** MEDIO — falta diferenciación clara de estado en tarjetas.

---

### D) Ficha de producto (PDP) — ⭐⭐⭐ (3/5)

**Hallazgos:**
- ✅ Flujo de reserva intacto: tag `bajo-pedido` → `itoro-reservar.liquid` → señal 50 € → mapa a variante reserva → POST cart
- ✅ Apple Pay/pago dinámico oculto en productos `bajo-pedido` (el snippet no renderiza `payment_button`)
- ✅ Shipping badge y trust row recién añadidos en `itoro-reservar.liquid`
- ✅ JSON-LD Product correcto con precio, disponibilidad, condición y vendedor
- ✅ Bloques `it-trust-product` e `it-product-extras` después del producto
- ❌ **Sin sticky CTA en PDP móvil** — al hacer scroll el botón desaparece; oportunidad de conversión perdida
- ❌ `main-product.liquid` es el Dawn sin apenas modificar (112 KB) — tipografía, espaciados y colores del esquema de color genérico, no del brand premium
- ❌ El trust row usa emoji (🔒🚚✅) — funciona pero no es el nivel premium objetivo
- ❌ El badge de envío tiene fondo `rgba(255,255,255,0.04)` — apenas visible en modo claro (diseñado para dark)
- ❌ Sin acordeones para descripción / especificaciones técnicas en PDP — el campo `description` se muestra flat

**Impacto:** ALTO — PDP es la página de mayor conversión.

---

### E) Experiencia móvil — ⭐⭐⭐ (3/5)

**Hallazgos:**
- ✅ `itoro-mobile.css` con overrides completos para todos los componentes
- ✅ Prevención de zoom en inputs iOS (`font-size: 16px !important`)
- ✅ Touch targets mínimos `min-height: 44px` en botones
- ✅ Popup como bottom sheet en móvil (`border-radius: 16px 16px 0 0`)
- ✅ Back-to-top y WhatsApp reposicionados en móvil
- ❌ **Sin sticky CTA** en PDP (el punto más crítico en móvil)
- ❌ El toggle de dark mode (`it-theme-bar.liquid`) tiene `position: fixed; top: 12px; right: 14px` — colisiona con el menú hamburguesa en móvil
- ❌ `safe-area-inset-*` solo en popup, no en el sticky footer que deberíamos añadir
- ❌ El comparador tiene `overflow-x: auto` en móvil — scroll horizontal aceptable pero no ideal

**Impacto:** ALTO — el 70%+ del tráfico es móvil (TikTok).

---

### F) Navegación, búsqueda y carrito — ⭐⭐⭐ (3/5)

**Hallazgos:**
- ✅ Cart drawer activado con barra de envío gratis
- ✅ Búsqueda predictiva habilitada
- ❌ Header Dawn estándar (22 KB) — no revisado en profundidad, posiblemente sin personalización del brand
- ❌ Sin mega-menú configurado por modelos (iPhone 13, 14, 15, 16, 17)
- ❌ Menú en móvil: drawer de Dawn — funcional pero genérico

**Impacto:** MEDIO.

---

### G) Rendimiento — ⭐⭐ (2/5)

**CSS crítico cargado en `<head>` (bloquea render):**
```
base.css             107 KB  (Dawn base)
itoro-dark-mode.css    7.6 KB
itoro-trust-extras.css 13 KB
itoro-collection.css    6.1 KB
itoro-mobile.css        8.9 KB
─────────────────────────────
TOTAL CRÍTICO         ~143 KB  ← demasiado
```
**Hallazgos:**
- ❌ **~143 KB de CSS en `<head>`** sin diferir — primer byte pintado retrasado
- ❌ `itoro-hero.css` (6.6 KB) posiblemente cargado aunque hero v1 no esté activo
- ❌ **`sparkle.gif` de 179 KB** — probablemente en alguna sección; GIF pesado sin lazy
- ❌ **Avatares de reseñas desde `randomuser.me`** — requests externos a terceros por cada card (latencia, GDPR)
- ❌ `itoro-trust.css` cargado mediante `stylesheet_tag` dentro del snippet — genera un `<link>` por cada render del snippet si aparece más de una vez
- ❌ `global.js` (43.8 KB) con `defer` — OK, pero grande
- ❌ `main-product.liquid` (112 KB) — mucho Liquid que se parsea cada request
- ✅ Fuentes con `font-display: swap` y `preload`
- ✅ Imágenes con `loading="lazy"` (Dawn por defecto)
- ✅ Scripts con `defer="defer"`

**Impacto:** ALTO — Core Web Vitals penalizan LCP y CLS.

---

### H) SEO — ⭐⭐⭐ (3/5)

**Hallazgos:**
- ✅ `it-schema-org.liquid`: JSON-LD Product con precio, disponibilidad (`InStock`/`OutOfStock`), condición (`NewCondition`/`UsedCondition`), vendedor, marca Apple — **correcto y veraz**
- ✅ OG tags completos en `theme.liquid` (tipo, título, descripción, imagen, precio)
- ✅ Meta description desde `page_description` del admin
- ✅ Canonical URL con `{{ canonical_url }}`
- ✅ Hreflang delegado a `meta-tags.liquid`
- ❌ **Jerarquía H1/H2**: en la PDP el título del producto es H1 (bien), pero si las secciones del home usan H2 incorrectamente habrá problemas
- ❌ **Alt text** en imágenes de hero y secciones custom — sin verificar si las secciones lo pasan correctamente
- ❌ Las reseñas en `it-reviews.liquid` **no tienen JSON-LD AggregateRating** — se muestra "4.9 ★" visualmente pero Google no lo ve
- ❌ Rating "4.9 Google" en hero — sin datos estructurados verificables
- ❌ URL de la tienda en JSON-LD es `itorostore.myshopify.com` — debería ser el dominio personalizado real

**Impacto:** MEDIO — estructura base bien, faltan AggregateRating y revisión de alt text.

---

### I) Accesibilidad — ⭐⭐ (2/5)

**Hallazgos:**
- ✅ Skip-to-content link en `theme.liquid`
- ✅ `aria-label` en botón WhatsApp, back-to-top, tema toggle
- ✅ Botones de formulario con `type="submit"` y `name="add"` correctos
- ❌ **FAQ sin `aria-expanded`** — el accordion usa `onclick="itFaqToggle()"` pero no actualiza atributos ARIA, ni usa `<details>`/`<summary>`. Lectores de pantalla no saben si está abierto.
- ❌ **Toggle dark mode** con todos los estilos inline hardcodeados — difícil de auditar contraste; el ícono emoji (☀️/🌙) sin texto alternativo real
- ❌ **Carrusel de anuncios** sin pausa accesible (hay `animation-play-state:paused` en `:hover` pero no en focus ni con media `prefers-reduced-motion`)
- ❌ **Focus visible** no garantizado en elementos custom — Dawn tiene estilos de foco pero los overrides custom pueden romperlos
- ❌ `card-product.liquid` (Dawn) tiene foco pero los swatches custom pueden carecer de `aria-label` por color
- ❌ Contraste: modo claro usa `--it-muted: #636360` sobre `#f5f5f7` — ratio ~4.1:1, pasa AA para texto normal pero ajustado
- ❌ Contraste: modo oscuro usa `--it-hint: #555` sobre `#0d0d0b` — ratio ~3.8:1, **no pasa AA** para texto normal

**Impacto:** MEDIO-ALTO — requisito legal en España (RGPD + EN 301 549).

---

## 3. LISTA PRIORIZADA DE PROBLEMAS

### 🔴 CRÍTICO (bloquea conversión o está roto)

| # | Problema | Archivo(s) | Impacto |
|---|----------|------------|---------|
| C1 | **Secciones del home probablemente inexistentes** — 10 de las 12 secciones de `index.json` no aparecen en el listado del tema (`it-hero-premium`, `it-features`, `it-categorias`, `it-finder`, etc.) | `templates/index.json` | Home en blanco |
| C2 | **Sin sticky CTA en PDP móvil** — al hacer scroll el botón "Reservar" desaparece | Nuevo snippet necesario | Conversión móvil |
| C3 | **~143 KB CSS crítico** en `<head>` bloquea First Contentful Paint | `layout/theme.liquid` | LCP / velocidad |
| C4 | **Itoro-trust.css badge de envío** invisible en modo claro (fondo casi transparente) | `assets/itoro-trust.css` | UX producto |

### 🟠 ALTO (afecta experiencia de marca o conversión)

| # | Problema | Archivo(s) | Impacto |
|---|----------|------------|---------|
| A1 | **4 sistemas de tokens CSS** — mantenimiento imposible a largo plazo | Todos los `itoro-*.css` | Coherencia |
| A2 | **PDP Dawn sin personalizar** — espaciados, tipografía y colores genéricos | `sections/main-product.liquid` | Brand premium |
| A3 | **Avatares externos `randomuser.me`** en reseñas — GDPR + rendimiento | `sections/it-reviews.liquid` | Legal + velocidad |
| A4 | **`sparkle.gif` de 179 KB** — GIF pesado sin lazy-load optimizado | `assets/sparkle.gif` | LCP |
| A5 | **FAQ sin `aria-expanded`** — accesibilidad rota para lectores de pantalla | `sections/it-faq.liquid` | Accesibilidad |
| A6 | **Toggle dark mode** posiciona sobre menú hamburguesa en móvil | `snippets/it-theme-bar.liquid` | UX móvil |
| A7 | **Sin JSON-LD AggregateRating** — las reseñas no son visibles para Google | `snippets/it-schema-org.liquid` | SEO |
| A8 | **Contraste `--it-hint: #555`** no pasa AA en modo oscuro | `assets/itoro-dark-mode.css` | Accesibilidad |

### 🟡 MEDIO (mejora notable)

| # | Problema | Archivo(s) | Impacto |
|---|----------|------------|---------|
| M1 | **Ningún indicador "bajo pedido" en tarjetas** de colección | `snippets/card-product.liquid` | Expectativas |
| M2 | **Descripción del producto sin acordeones** en PDP | `sections/main-product.liquid` | UX |
| M3 | **URL en JSON-LD** apunta a `myshopify.com` en lugar del dominio real | `snippets/it-schema-org.liquid` | SEO |
| M4 | **`itoro-hero.css` posiblemente sin usar** (6.6 KB CSS extra) | `assets/itoro-hero.css` | Rendimiento |
| M5 | **`prefers-reduced-motion`** sin respetar en animaciones del ticker | `sections/it-announcement-bar.liquid` | Accesibilidad |
| M6 | **Cart drawer** — no revisado en profundidad; barra de envío gratis a confirmar | `sections/main-cart-*.liquid` | Carrito |
| M7 | **Alt text** en imágenes de secciones custom sin verificar | Varias secciones | SEO + accesibilidad |

### 🟢 BAJO (pulido)

| # | Problema | Archivo(s) | Impacto |
|---|----------|------------|---------|
| B1 | Trust row con emoji en lugar de SVG inline — menos premium | `snippets/itoro-reservar.liquid` | Estética |
| B2 | Mega-menú por modelos no configurado | `sections/header.liquid` | Navegación |
| B3 | Búsqueda predictiva sin customización de resultados | `assets/predictive-search.js` | UX búsqueda |

---

## 4. REGLAS INNEGOCIABLES — ESTADO ACTUAL

| Regla | Estado |
|-------|--------|
| Rama de preview, no publicar en vivo | ✅ Tema UNPUBLISHED |
| Flujo de reserva intacto (`itoro-reservar.liquid`, `itoro-reservar.js`, tag `bajo-pedido`) | ✅ Funcional y documentado |
| Apple Pay oculto en productos `bajo-pedido` | ✅ El snippet `itoro-reservar` no renderiza `payment_button` |
| Producto señal `reserva-de-pedido-iphone-itorostore` intacto | ✅ Referenciado en JS, no modificar |
| Sin escasez/reseñas/sellos falsos | ✅ Las reseñas están como datos de bloque (editables en admin) |
| Sin tocar precios/inventario | ✅ No tocado |
| Secciones propias itoro: mantenidas | ✅ |

---

## 5. PRÓXIMO PASO

**¿Procedo con el PLAN de mejoras?**

Orden propuesto de bloques:
1. **Diagnóstico C1** — confirmar qué secciones del home faltan y si el home está roto
2. **Sticky CTA móvil** (C2) — máximo impacto de conversión
3. **CSS crítico** — diferir itoro-mobile.css e itoro-trust-extras.css (C3)
4. **Consolidar tokens** — unificar en un solo sistema (A1)
5. **PDP premium** — tipografía, espaciado, acordeones descripción (A2)
6. **Reseñas** — eliminar avatares externos, usar iniciales o imágenes subidas (A3)
7. **Accesibilidad** — aria-expanded FAQ, contraste, prefers-reduced-motion (A5, A8, M5)
8. **SEO** — AggregateRating, URL dominio real (A7, M3)

**Esperando tu aprobación para escribir el PLAN detallado.**
