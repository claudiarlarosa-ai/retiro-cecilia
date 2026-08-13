import re

with open("plantilla.html", "r") as f:
    content = f.read()

replacements = [
    (
        '<meta name="description" content="Retiro de crochet y descanso del 20 al 22 de agosto de 2026 en el Refugio de Santa Eulalia. Dos talleres, journaling creativo y un CAL de mantas. Nivel intermedio.">',
        '<meta name="description" content="Retiro de crochet y journaling creativo del 20 al 22 de noviembre de 2026 en el Refugio de Santa Eulalia. Dos talleres, journaling creativo, CAL de mantas y kits de bienvenida. Nivel intermedio.">'
    ),
    (
        '<textPath href="#sello-arc" startOffset="0%">20 · 21 · 22 AGOSTO 2026 · SANTA EULALIA ·</textPath>',
        '<textPath href="#sello-arc" startOffset="0%">20 · 21 · 22 NOVIEMBRE 2026 · SANTA EULALIA ·</textPath>'
    ),
    (
        '<p class="fecha">20 al 22 de agosto de 2026 · Santa Eulalia</p>',
        '<p class="fecha">20 al 22 de noviembre de 2026 · Santa Eulalia</p>'
    ),
    (
        '<p class="entrada">Tres días de crochet, campo y buena compañía. Un retiro para hacer una pausa, tejer sin apuro y volver a casa renovada.</p>',
        '<p class="entrada">Un retiro de crochet y journaling creativo para hacer una pausa, dejar atrás las responsabilidades y regalarte un fin de semana inolvidable.</p>'
    ),
    (
        '<p class="script">Hola, qué gusto verte</p>',
        '<p class="script">Bienvenida</p>'
    ),
    (
        '<p class="guia">Un fin de semana para hacer una pausa, dejar atrás las responsabilidades y regalarte tiempo para ti. Un entorno tranquilo, conversaciones sin prisa y la compañía de otras mujeres que aman crear con sus propias manos.</p>\n        <p class="guia">Entre el crochet y el journaling creativo vas a descubrir técnicas nuevas, despertar tu imaginación y hacer amistades que no esperabas.</p>',
        '<p class="guia">Vive un fin de semana inolvidable en Arte entre Puntadas, una experiencia creada para hacer una pausa, dejar atrás las responsabilidades y regalarte tiempo para ti.</p>\n        <p class="guia">Disfruta de un entorno tranquilo y acogedor, comparte conversaciones, risas y momentos especiales con mujeres que aman crear con sus propias manos. Déjate inspirar por el crochet y el journaling creativo mientras descubres nuevas técnicas, despiertas tu imaginación y conectas con nuevas amistades.</p>\n        <p class="guia">Más que un retiro creativo, será un fin de semana para descansar, disfrutar y volver a casa renovada, llena de inspiración y hermosos recuerdos.</p>\n        <p class="guia" style="font-style:italic; color:var(--terracota)">Tejemos juntas, crecemos juntas.</p>'
    ),
    (
        '<p><strong>Este retiro es para nivel intermedio.</strong> Los talleres parten de que ya manejas los puntos básicos del crochet. No es un retiro para principiantes.</p>',
        '<p><strong>Este retiro es para nivel intermedio.</strong> Está dirigido a quienes se encuentran en un nivel intermedio de crochet. No es un retiro para principiantes.</p>'
    ),
    (
        '<p class="script verde">Lo que vamos a tejer</p>\n      <h2 class="display">Tres sesiones de trabajo</h2>',
        '<p class="script verde">Lo que vamos a vivir</p>\n      <h2 class="display">Tres días de experiencias</h2>'
    ),
    (
        '<p class="guia">La técnica para tejer diseños gráficos llevando dos hilos a la vez. Desarrollarás precisión, ritmo y combinaciones de colores vibrantes.</p>',
        '<p class="guia">La técnica para tejer diseños gráficos llevando dos hilos a la vez. Incluye patrón detallado y los materiales de tu proyecto.</p>'
    ),
    (
        '<p class="guia">Transformarás recuerdos, ideas e inspiración en páginas que cuentan tu propia historia en un entorno natural rodeado de relax.</p>',
        '<p class="guia">Transformarás recuerdos, ideas e inspiración en páginas únicas que cuenten tu propia historia. Todos los materiales incluidos.</p>'
    ),
    (
        '<p class="mini">Precio de lanzamiento</p>\n          <span class="tarifa-cifra">S/ 1,450</span>\n          <p class="vigencia">Vigente del 1 al 15 de abril</p>',
        '<p class="mini">Precio de lanzamiento</p>\n          <span class="tarifa-cifra">S/ 1,750</span>\n          <p class="vigencia">Vigente del 8 al 24 de agosto</p>'
    ),
    (
        '<p class="mini">Precio regular</p>\n          <span class="tarifa-cifra">S/ 1,600</span>\n          <p class="vigencia">A partir del 16 de abril</p>',
        '<p class="mini">Precio regular</p>\n          <span class="tarifa-cifra">S/ 1,850</span>\n          <p class="vigencia">Del 25 de agosto al 15 de setiembre</p>'
    ),
    (
        '<dt>Saldo</dt>\n          <dd>50% restante hasta el 20 de julio.</dd>',
        '<dt>Saldo</dt>\n          <dd>50% restante hasta el 20 de octubre.</dd>'
    ),
    (
        '<p>Puedes cancelar hasta 30 días antes del retiro. Se devuelve el 70% si tu vacante se reemplaza o el grupo se completa, y el 50% si no llega a cubrirse. En ambos casos el reembolso se hace entre el 9 y el 15 de noviembre.</p>',
        '<p>Puedes cancelar hasta el 21 de octubre de 2026. Se reintegra el 70&nbsp;% si la vacante es reemplazada o el grupo se completa, y el 50&nbsp;% si no logra cubrirse. En ambos casos el reembolso se hará entre el 9 y el 15 de noviembre de 2026.</p>'
    ),
    (
        '20 al 22 de agosto de 2026',
        '20 al 22 de noviembre de 2026'
    ),
    (
        '20 de agosto',
        '20 de noviembre'
    ),
    (
        '21 de agosto',
        '21 de noviembre'
    ),
    (
        '22 de agosto',
        '22 de noviembre'
    )
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
    else:
        print(f"WARNING: Could not find '{old[:50]}...'")

# Add the Beneficios section before Talleres
beneficios_html = """
<!-- ═══ Beneficios ════════════════════════════════════ -->
<section id="beneficios" class="fondo-arena">
  <div class="lienzo">
    <div class="revela">
      <p class="script">Lo que te llevas</p>
      <h2 class="display">Beneficios del retiro</h2>
    </div>
    <div class="beneficios" style="display:grid; grid-template-columns:repeat(2,1fr); gap:clamp(1rem,2.5vw,1.8rem); margin-top:clamp(2.5rem,5vw,3.6rem);">
      <div class="beneficio revela" style="display:flex; gap:1rem; align-items:flex-start; padding:clamp(1.3rem,2.5vw,1.8rem) 1.4rem; background:linear-gradient(160deg, rgba(255,253,250,.95), rgba(244,235,223,.9)); box-shadow:var(--sombra-s); border-radius:12px;">
        <span class="beneficio-ico" style="flex:none; width:40px; height:40px; display:grid; place-items:center; border-radius:50%; background:linear-gradient(145deg, var(--verde-suave), var(--arena)); color:var(--verde-hondo); font-size:1.1rem;">✦</span>
        <p style="font-size:0.9rem; margin:0;"><strong style="display:block; margin-bottom:.3rem; color:var(--tinta)">Conexión genuina</strong>Con otras mujeres que comparten tu pasión por el tejido.</p>
      </div>
      <div class="beneficio revela d1" style="display:flex; gap:1rem; align-items:flex-start; padding:clamp(1.3rem,2.5vw,1.8rem) 1.4rem; background:linear-gradient(160deg, rgba(255,253,250,.95), rgba(244,235,223,.9)); box-shadow:var(--sombra-s); border-radius:12px;">
        <span class="beneficio-ico" style="flex:none; width:40px; height:40px; display:grid; place-items:center; border-radius:50%; background:linear-gradient(145deg, var(--verde-suave), var(--arena)); color:var(--verde-hondo); font-size:1.1rem;">✦</span>
        <p style="font-size:0.9rem; margin:0;"><strong style="display:block; margin-bottom:.3rem; color:var(--tinta)">Perfecciona tu crochet</strong>Para quienes están en nivel intermedio y quieren seguir creciendo.</p>
      </div>
      <div class="beneficio revela d2" style="display:flex; gap:1rem; align-items:flex-start; padding:clamp(1.3rem,2.5vw,1.8rem) 1.4rem; background:linear-gradient(160deg, rgba(255,253,250,.95), rgba(244,235,223,.9)); box-shadow:var(--sombra-s); border-radius:12px;">
        <span class="beneficio-ico" style="flex:none; width:40px; height:40px; display:grid; place-items:center; border-radius:50%; background:linear-gradient(145deg, var(--verde-suave), var(--arena)); color:var(--verde-hondo); font-size:1.1rem;">✦</span>
        <p style="font-size:0.9rem; margin:0;"><strong style="display:block; margin-bottom:.3rem; color:var(--tinta)">Aprendizaje guiado</strong>Nuevas técnicas de crochet con una instructora experta.</p>
      </div>
      <div class="beneficio revela" style="display:flex; gap:1rem; align-items:flex-start; padding:clamp(1.3rem,2.5vw,1.8rem) 1.4rem; background:linear-gradient(160deg, rgba(255,253,250,.95), rgba(244,235,223,.9)); box-shadow:var(--sombra-s); border-radius:12px;">
        <span class="beneficio-ico" style="flex:none; width:40px; height:40px; display:grid; place-items:center; border-radius:50%; background:linear-gradient(145deg, var(--verde-suave), var(--arena)); color:var(--verde-hondo); font-size:1.1rem;">✦</span>
        <p style="font-size:0.9rem; margin:0;"><strong style="display:block; margin-bottom:.3rem; color:var(--tinta)">Alivio del estrés</strong>A través de la práctica meditativa del tejido.</p>
      </div>
      <div class="beneficio revela d1" style="display:flex; gap:1rem; align-items:flex-start; padding:clamp(1.3rem,2.5vw,1.8rem) 1.4rem; background:linear-gradient(160deg, rgba(255,253,250,.95), rgba(244,235,223,.9)); box-shadow:var(--sombra-s); border-radius:12px;">
        <span class="beneficio-ico" style="flex:none; width:40px; height:40px; display:grid; place-items:center; border-radius:50%; background:linear-gradient(145deg, var(--verde-suave), var(--arena)); color:var(--verde-hondo); font-size:1.1rem;">✦</span>
        <p style="font-size:0.9rem; margin:0;"><strong style="display:block; margin-bottom:.3rem; color:var(--tinta)">Creatividad en un entorno inspirador</strong>La naturaleza y el campo despiertan tu imaginación.</p>
      </div>
      <div class="beneficio revela d2" style="display:flex; gap:1rem; align-items:flex-start; padding:clamp(1.3rem,2.5vw,1.8rem) 1.4rem; background:linear-gradient(160deg, rgba(255,253,250,.95), rgba(244,235,223,.9)); box-shadow:var(--sombra-s); border-radius:12px;">
        <span class="beneficio-ico" style="flex:none; width:40px; height:40px; display:grid; place-items:center; border-radius:50%; background:linear-gradient(145deg, var(--verde-suave), var(--arena)); color:var(--verde-hondo); font-size:1.1rem;">✦</span>
        <p style="font-size:0.9rem; margin:0;"><strong style="display:block; margin-bottom:.3rem; color:var(--tinta)">Bienestar emocional</strong>Tiempo para ti, sin prisas, sin pantallas.</p>
      </div>
    </div>
  </div>
</section>

<!-- ═══ Talleres ══════════════════════════════════════ -->
"""
content = content.replace("<!-- ═══ Talleres ══════════════════════════════════════ -->", beneficios_html)

# Now, we need to add the two extra "Talleres" (Regalo Especial & Momento de Conexión) to the grid, but maintaining the nice style from retiro-opcion-A-editorial.html
# Wait, the Talleres section in A-editorial uses a nice card style with an image. The user's new text has "Regalo Especial" (Dos kits de bienvenida) and "Momento de conexión" (Círculo de compartir). We can add them as simple text cards or with images. I'll add them with images that fit (manta.png and cecilia.jpg or just placeholders from assets).
# Actually, the user's HTML for new Talleres doesn't have images in the old plantilla.html, but let's just make them fit the grid of 3 items in A-editorial.
# Currently A-editorial has 3 items in "talleres" grid: Intarsia, Tapestry, Journaling. If we add 2 more, we need a 4th and 5th card.
extra_talleres_html = """
      <article class="taller revela">
        <div class="taller-img-container">
          <img src="assets/manta.png" alt="Kits de bienvenida">
        </div>
        <div class="taller-content">
          <p class="mini">Regalo especial</p>
          <h3 class="display">Dos kits de bienvenida</h3>
          <p class="guia">Al llegar recibirás dos kits preparados con cariño para que empieces la experiencia con todo listo.</p>
        </div>
      </article>

      <article class="taller revela d1">
        <div class="taller-img-container">
          <img src="assets/cecilia.jpg" alt="Círculo de compartir">
        </div>
        <div class="taller-content">
          <p class="mini">Momento de conexión</p>
          <h3 class="display">Círculo de compartir</h3>
          <p class="guia">Un espacio para historias, risas y apoyo entre mujeres que comparten la pasión por crear con sus manos.</p>
        </div>
      </article>
"""
# Insert after the journaling workshop
content = content.replace('</article>\n\n    </div>\n  </div>\n</section>\n\n<!-- ═══ El CAL', extra_talleres_html + '    </div>\n  </div>\n</section>\n\n<!-- ═══ El CAL')


with open("plantilla.html", "w") as f:
    f.write(content)
