# PLAN DE MEJORAS — IToroStore
**Tema:** Copia de Dawn — PRO (preview) — UNPUBLISHED  
**Fecha:** 2026-06-08  
**Estado:** Esperando aprobación antes de implementar

> **C1 RESUELTO:** Todas las secciones del home existen y el tema está operativo.

---

## PRINCIPIOS DE TRABAJO
- Un commit por bloque, mensajes descriptivos.
- Todos los cambios en el tema PREVIEW (`200413446469`). Nada en el tema MAIN (`198878757189`).
- El flujo de reserva (tag `bajo-pedido` → `itoro-reservar.liquid` → señal 50 €) no se toca salvo mejoras visuales explícitas.
- Apple Pay/pago dinámico permanece oculto en productos `bajo-pedido`.
- Cero escasez/reseñas/sellos falsos.

---

## BLOQUE 1 — Sticky CTA móvil en PDP 🔴
**Impacto:** CONVERSIÓN MÁXIMA · Tráfico TikTok = móvil · Sin esto, el botón desaparece al hacer scroll

### Qué hace
- Barra fija en la parte inferior del móvil que aparece cuando el botón principal queda fuera de viewport.
- Muestra: imagen miniatura del producto · título corto · precio · botón CTA.
- Para productos `bajo-pedido`: "Reservar · 50 €" → dispara el mismo flujo de `itoro-reservar.js`.
- Para productos normales: "Comprar ahora" → hace submit del formulario.
- Se oculta al volver arriba (cuando el botón original es visible).
- `padding-bottom: env(safe-area-inset-bottom)` para iPhone con notch.
- Solo en mobile (`max-width: 749px`), invisible en desktop.

### Archivos
| Acción | Archivo |
|--------|---------|
| CREAR | `snippets/it-sticky-cta.liquid` |
| CREAR | `assets/it-sticky-cta.css` |
| CREAR | `assets/it-sticky-cta.js` |
| EDITAR | `sections/main-product.liquid` — añadir `{%- render 'it-sticky-cta' -%}` al final del bloque `buy_buttons` |

### No se toca
`itoro-reservar.js`, lógica de reserva, Apple Pay.

---

## BLOQUE 2 — PDP premium: diseño y confianza 🔴
**Impacto:** CONVERSIÓN · La PDP es Dawn sin personalizar; visualmente no transmite "marca top"

### Qué hace
**2a — Trust badge visible en modo claro:**
- El fondo del shipping badge (`rgba(255,255,255,0.04)`) es casi invisible en claro. Se corrige con un fondo adaptativo (`var(--it-surface2)` en claro, el actual en oscuro).
- Trust row: sustituir emoji por SVG inline (candado, camión, escudo) — más premium y no depende de font emoji del sistema.

**2b — Descripción con acordeón:**
- La descripción del producto actualmente se muestra flat (todo el texto visible, sin estructura).
- Se añade un acordeón "Descripción" + "Especificaciones" que colapsa el contenido largo — la PDP queda más limpia y escaneable.

**2c — Tipografía y espaciado en main-product:**
- Aumentar el `letter-spacing` del título del producto (`--font-heading-scale` ya existe, pero los overrides del brand no están aplicados).
- Precio: tamaño y peso aumentados para jerarquía visual clara.
- Padding interno de la columna de info ajustado para más "aire" estilo Apple.

**2d — Galería:**
- Confirmar `object-fit: contain` (ya configurado en product.json) — las imágenes de iPhone no deben recortarse.
- Añadir fondo neutro (`var(--it-surface2)`) al área de galería cuando el producto tiene fondo blanco — mejora en dark mode.

### Archivos
| Acción | Archivo |
|--------|---------|
| EDITAR | `assets/itoro-trust.css` — fondo adaptativo, SVG trust icons |
| EDITAR | `snippets/itoro-reservar.liquid` — SVG icons en trust row |
| EDITAR | `snippets/buy-buttons.liquid` — añadir trust row para productos normales |
| EDITAR | `assets/section-main-product.css` — tipografía, espaciado, galería bg |

---

## BLOQUE 3 — Consolidación de tokens CSS 🟠
**Impacto:** MANTENIMIENTO · 4 sistemas de tokens imposibles de mantener coherentes

### Qué hace
- Añadir aliases en `itoro-dark-mode.css` que mapeen `--ico-*`, `--ih-*`, `--ips-*` a los valores `--it-*` correspondientes, sin romper nada.
- Así los componentes siguen usando sus tokens pero todos apuntan al mismo valor.
- Eliminar los valores duplicados en cada archivo (gold `#d4af37` repetido 4 veces).
- El resultado: cambiar el color dorado en un sitio lo cambia en toda la tienda.
- Verificar si `itoro-hero.css` (v1) sigue en uso; si no, marcar para eliminar.

### Archivos
| Acción | Archivo |
|--------|---------|
| EDITAR | `assets/itoro-dark-mode.css` — añadir aliases de tokens |
| EDITAR | `assets/itoro-collection.css` — simplificar tokens que ya existen en base |
| EDITAR | `assets/itoro-hero-v2.css` — simplificar tokens |
| EDITAR | `assets/itoro-pack-selector.css` — simplificar tokens |

---

## BLOQUE 4 — Rendimiento: CSS crítico y recursos pesados 🟠
**Impacto:** VELOCIDAD · LCP y FCP penalizados por ~143 KB CSS bloqueante

### Qué hace
**4a — Diferir CSS no crítico:**
- `itoro-mobile.css` y `itoro-trust-extras.css` se mueven a carga no bloqueante:
  ```html
  <link rel="stylesheet" href="..." media="print" onload="this.media='all'">
  ```
- `itoro-collection.css` permanece crítico (se usa en colecciones y posiblemente en home).
- `itoro-dark-mode.css` permanece crítico (tokens globales y dark mode).
- Esto reduce el CSS crítico de ~143 KB a ~115 KB.

**4b — Avatares de reseñas sin dependencias externas:**
- Eliminar URLs de `randomuser.me` del código de `it-reviews.liquid`.
- Usar iniciales con colores generados a partir del nombre (ya tiene lógica de fallback con `avatar-fallback`).
- El admin puede subir fotos reales via `avatar_image` (image_picker ya existe en el schema).

**4c — sparkle.gif:**
- Identificar dónde se usa y añadir `loading="lazy"` o convertir a CSS animation si es posible.

### Archivos
| Acción | Archivo |
|--------|---------|
| EDITAR | `layout/theme.liquid` — cambiar stylesheet_tag de itoro-mobile.css e itoro-trust-extras.css a carga diferida |
| EDITAR | `sections/it-reviews.liquid` — eliminar URLs randomuser.me |

---

## BLOQUE 5 — Tarjetas de colección: badge bajo-pedido 🟡
**Impacto:** EXPECTATIVAS · El cliente debe saber antes de entrar a la PDP que es bajo pedido

### Qué hace
- En `card-product.liquid`, si el producto tiene tag `bajo-pedido`, mostrar una etiqueta "Reservar · 50 €" en la tarjeta (debajo del precio o como badge superpuesto).
- Estilo coherente con el sistema `--ico-*` (fondo dorado o superficie oscura).
- Sin cambios en la lógica de precio ni inventario.

### Archivos
| Acción | Archivo |
|--------|---------|
| EDITAR | `snippets/card-product.liquid` — añadir badge condicional por tag |

---

## BLOQUE 6 — Accesibilidad: FAQ y animaciones 🟡
**Impacto:** LEGAL + UX · Requisito EN 301 549, lectores de pantalla

### Qué hace
- FAQ: convertir a `<details>`/`<summary>` nativo (accesible por defecto, sin JS extra) o añadir `aria-expanded` y `aria-controls` al `<button>` existente.
- Ticker de anuncios: añadir `@media (prefers-reduced-motion: reduce) { animation: none }`.
- Contraste modo oscuro: `--it-hint: #555` → `#666` (pasa AA) para textos de soporte.
- Focus visible: confirmar que los overrides custom no rompen el outline de Dawn.

### Archivos
| Acción | Archivo |
|--------|---------|
| EDITAR | `sections/it-faq.liquid` — aria-expanded + aria-controls |
| EDITAR | `sections/it-announcement-bar.liquid` — prefers-reduced-motion |
| EDITAR | `assets/itoro-dark-mode.css` — --it-hint a #666 en dark mode |

---

## BLOQUE 7 — SEO: AggregateRating y dominio 🟡
**Impacto:** TRÁFICO ORGÁNICO · Estrellas en resultados de Google

### Qué hace
- Añadir `AggregateRating` al JSON-LD Product en `it-schema-org.liquid` (solo cuando la puntuación configurada en la sección de reseñas sea un valor real que el admin haya introducido — no inventado).
- Cambiar la URL del seller en JSON-LD a `{{ shop.url }}` en lugar de `itorostore.myshopify.com`.
- Verificar que el alt text de las imágenes del hero premium use `{{ section.settings.heading | escape }}`.

### Archivos
| Acción | Archivo |
|--------|---------|
| EDITAR | `snippets/it-schema-org.liquid` — AggregateRating + shop.url |
| EDITAR | `sections/it-hero-premium.liquid` — alt text en imagen |

---

## RESUMEN VISUAL

```
BLOQUE   IMPACTO     TIEMPO EST.   RIESGO
──────────────────────────────────────────
B1  Sticky CTA       🔴 Crítico    2–3h    Bajo
B2  PDP premium      🔴 Crítico    3–4h    Bajo
B3  Tokens CSS       🟠 Alto       2h      Bajo
B4  Rendimiento      🟠 Alto       1–2h    Bajo
B5  Badge bajo-ped.  🟡 Medio      1h      Bajo
B6  Accesibilidad    🟡 Medio      1–2h    Bajo
B7  SEO              🟡 Medio      1h      Bajo
──────────────────────────────────────────
TOTAL                              ~12–15h
```

---

## LO QUE NO CAMBIA (nunca)
- `assets/itoro-reservar.js` — lógica de reserva
- `snippets/itoro-reservar.liquid` — estructura del flujo (solo mejoras visuales)
- El condicional `bajo-pedido` en `snippets/buy-buttons.liquid` — solo se extiende
- El producto `reserva-de-pedido-iphone-itorostore` — no se toca
- `sections/it-reviews.liquid` blocks — los datos de reseñas del admin se mantienen
- `assets/itoro-trade-in.*` — trade-in intacto
- Secciones del home ya configuradas (`it-hero-premium`, `it-finder`, etc.)

---

## CÓMO PROBAR CADA BLOQUE
1. Abrir el tema PREVIEW en el editor de Shopify: `Tiendas > Temas > Personalizar` en "Copia de Dawn — PRO (preview)".
2. Verificar móvil con DevTools → modo dispositivo (375px, iPhone SE).
3. Para el flujo de reserva: entrar a un producto con tag `bajo-pedido`, comprobar que el botón "Reservar ahora · señal 50 €" aparece y Apple Pay no.
4. Para sticky CTA: hacer scroll hacia abajo en PDP en móvil.

---

**¿Apruebas este plan? Puedo empezar por el Bloque 1 (sticky CTA) inmediatamente.**
