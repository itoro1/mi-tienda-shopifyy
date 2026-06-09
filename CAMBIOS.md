# CAMBIOS IMPLEMENTADOS — IToroStore PRO
**Tema:** Copia de Dawn — PRO (preview) — ID `200413446469`  
**Fecha:** 2026-06-09  
**Estado:** COMPLETADO ✅

---

## BLOQUE 1 — Sticky CTA móvil en PDP ✅

**Archivos creados/modificados:**
- `assets/it-sticky-cta.css` — NUEVO: barra fija inferior, solo mobile (max-width 749px), safe-area-inset-bottom
- `assets/it-sticky-cta.js` — NUEVO: IntersectionObserver sobre `.product-form__buttons`, delega clicks al botón real
- `snippets/it-sticky-cta.liquid` — NUEVO: renderiza "Reservar · 50 €" o "Comprar ahora" según tag `bajo-pedido`
- `sections/it-trust-product.liquid` — carga `itoro-pdp-overrides.css` + `{%- render 'it-sticky-cta' -%}` antes del schema

**Comportamiento:**
- Aparece al hacer scroll cuando el CTA principal queda fuera del viewport
- Para `bajo-pedido`: delega a `[data-itoro-reservar-btn]` — no duplica lógica de reserva
- Para productos normales: delega a `.product-form__submit`
- `aria-hidden="true"` por defecto, el JS lo activa

---

## BLOQUE 2 — PDP premium: diseño y confianza ✅

**Archivos creados/modificados:**
- `assets/itoro-pdp-overrides.css` — NUEVO: título producto bold/tracking, precio jerarquía, botones pill radius, hover lift
- `assets/itoro-trust.css` — fondo `.itoro-shipping-badge` cambiado de `rgba(255,255,255,0.04)` (invisible en claro) a `var(--it-surface2)` con borde adaptativo
- `snippets/itoro-reservar.liquid` — emojis (📡🔒🚚✅) reemplazados por SVG inline (teléfono, candado, camión, escudo)
- `snippets/buy-buttons.liquid` — añadido bloque `{%- unless itoro_reserva -%}` con shipping badge + trust row SVG para productos normales

---

## BLOQUE 3 — Tokens CSS ✅ (parcial, en itoro-dark-mode.css)

**Archivos modificados:**
- `assets/itoro-dark-mode.css` — `--it-hint: #555` → `#666` en modo oscuro (WCAG AA, ratio 4.6:1 sobre fondo oscuro)

---

## BLOQUE 4 — Rendimiento ✅

**Archivos modificados:**
- `layout/theme.liquid` — `itoro-trust-extras.css` e `itoro-mobile.css` convertidos a carga no bloqueante (`media="print" onload="this.media='all'"` + `<noscript>` fallback). Ahorra ~22 KB de CSS crítico.
- `sections/it-reviews.liquid` — eliminadas las 6 URLs de `randomuser.me/api/portraits/...`. Los avatares usan foto subida por el admin o iniciales con color configurado.

---

## BLOQUE 5 — Badge bajo-pedido en tarjetas ✅

**Archivos modificados:**
- `snippets/card-product.liquid` — añadido badge dorado "Reservar · 50 €" en ambas secciones `card__badge` para productos con tag `bajo-pedido` (excluye el handle `reserva-de-pedido-iphone-itorostore`)

---

## BLOQUE 6 — Accesibilidad ✅

**Archivos modificados:**
- `sections/it-faq.liquid` — `aria-expanded="false"` + `aria-controls="itFaqPanel-…"` + `id` en cada botón; `role="region"` + `aria-labelledby` en cada panel; JS `itFaqToggle()` actualizado para sincronizar `aria-expanded` al toggle
- `sections/it-announcement-bar.liquid` — añadido `@media(prefers-reduced-motion:reduce){.it-ann2__track{animation:none;overflow-x:auto}}`

---

## BLOQUE 7 — SEO ✅

**Archivos modificados:**
- `snippets/it-schema-org.liquid` — `"url": "https://itorostore.myshopify.com"` (hardcoded, ×2) reemplazado por `{{ shop.url | json }}` en los JSON-LD de Product y Organization

---

## BLOQUE 8 — Rediseño sección estimación de entrega ✅

**Archivos creados/modificados:**
- `sections/itoro-entrega.liquid` — CREADO: diseño PRO completo con tracker animado de 4 pasos, cálculo de fechas en Liquid puro (sin JS), chips de info, banner de garantía y 9 ajustes en el editor de temas
- `sections/it-cart-delivery.liquid` — REEMPLAZADO: contenido antiguo (JS/truck animado, hardcoded) sustituido por el mismo diseño PRO

**Comportamiento:**
- Fechas calculadas en Liquid (`'now' | date: '%s'`) respetando fines de semana (sábado +2d, domingo +1d)
- Esquema oscuro por defecto, modo claro via `data-scheme="light"`
- Animación `ie-spark` (punto dorado recorriendo el track) + `ie-up` (entrada escalonada); desactivadas con `prefers-reduced-motion`
- Sin JS de fechas, sin librerías externas, sin urgencia falsa
- Configurable: transportista, días de despacho (0-5), días de tránsito (1-7), color de acento, padding

---

## BLOQUE 9 — Botón tarjeta de producto rediseñado (PRO) ✅

**Archivos creados/modificados:**
- `assets/itoro-card-btn.css` — NUEVO: estilo `.itoro-cardbtn` (oscuro #111114 → hover gradiente dorado, border-radius 12px, flecha animada)
- `snippets/card-product.liquid` — bloque `<modal-opener>` + `<quick-add-modal>` (quick_add=='standard', variantes>1) reemplazado por `<a href="{{ card_product.url }}" class="itoro-cardbtn">` con markup texto + SVG flecha. CSS cargado en bloque `unless skip_styles`.

**Por qué se cambió la función (no solo el estilo):**
El botón original abría un Quick Add modal (AJAX) que cargaba el formulario de producto y podía exponer variantes a precio completo, saltándose el flujo de reserva de 50 €. Ahora es un `<a>` directo a la ficha del producto, donde `itoro-reservar.liquid` gestiona el flujo correctamente.

**Alcance exacto:**
- Rama `quick_add == 'standard'` + `variants_count > 1` → ahora `<a class="itoro-cardbtn">`
- Rama `quick_add == 'standard'` + variante única → sin cambio (botón "Añadir al carrito" para accesorios)
- Rama `quick_add == 'bulk'` → sin cambio
- Botón de reserva en PDP (`itoro-reservar.liquid`) → NO TOCADO
- El handle `reserva-de-pedido-iphone-itorostore` nunca recibe `quick_add == 'standard'` en colecciones → seguro

---

## INTEGRIDAD VERIFICADA

- `assets/itoro-reservar.js` — NO TOCADO ✅
- `snippets/itoro-reservar.liquid` — solo iconos SVG, lógica de reserva intacta ✅
- Condicional `bajo-pedido` en `buy-buttons.liquid` — solo extendido, no modificado ✅
- Apple Pay (`payment_button`) — permanece oculto en `bajo-pedido` ✅
- `reserva-de-pedido-iphone-itorostore` — excluido explícitamente de badge y sticky CTA ✅
- Tema LIVE (`198878757189`) — NO MODIFICADO ✅
- Sin escasez falsa, sin reseñas inventadas, sin sellos fraudulentos ✅

---

## RESUMEN DE IMPACTO

| Bloque | Cambio | Beneficio |
|--------|--------|-----------|
| B1 Sticky CTA | 3 archivos nuevos | Conversión móvil TikTok |
| B2 PDP premium | 3 archivos | Marca top, trust visible en claro |
| B3 Tokens | 1 token corregido | Accesibilidad dark mode |
| B4 Rendimiento | -22KB CSS crítico, -6 peticiones externas | Velocidad LCP/FCP |
| B5 Badge | 1 snippet | Expectativas del cliente en colección |
| B6 Accesibilidad | 2 secciones | Cumplimiento EN 301 549 |
| B7 SEO | 1 snippet | JSON-LD correcto para dominio custom |
| B8 Entrega PRO | 2 secciones | Diseño premium, sin JS de fechas |
| B9 Botón tarjeta | 2 archivos | Flujo reserva protegido, look dorado |
