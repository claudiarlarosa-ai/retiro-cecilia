import re

with open("plantilla.html", "r") as f:
    content = f.read()

# 1. Remove FAQ section
# The FAQ section starts with <!-- ═══ Preguntas Frecuentes ═══════════════════════════ -->
# and ends with <!-- ═══ Cierre ════════════════════════════════════════ -->
faq_pattern = re.compile(r'<!-- ═══ Preguntas Frecuentes ═══════════════════════════ -->.*?<!-- ═══ Cierre', re.DOTALL)
content = faq_pattern.sub('<!-- ═══ Cierre', content)

# 2. Fix the 2 extra items in Talleres
old_extra = """
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

new_extra = """
      <article class="taller revela" style="grid-column: span 3; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; background: transparent; border: none; box-shadow: none;">
        <div style="background:linear-gradient(160deg, rgba(255,253,250,.95), rgba(244,235,223,.9)); padding: 2rem; border-radius: 12px; border: 1px solid rgba(63,51,42,0.08);">
          <p class="mini">Regalo especial</p>
          <h3 class="display">Dos kits de bienvenida</h3>
          <p class="guia" style="margin-bottom:0;">Al llegar recibirás dos kits preparados con cariño para que empieces la experiencia con todo listo.</p>
        </div>
        <div style="background:linear-gradient(160deg, rgba(255,253,250,.95), rgba(244,235,223,.9)); padding: 2rem; border-radius: 12px; border: 1px solid rgba(63,51,42,0.08);">
          <p class="mini">Momento de conexión</p>
          <h3 class="display">Círculo de compartir</h3>
          <p class="guia" style="margin-bottom:0;">Un espacio para historias, risas y apoyo entre mujeres que comparten la pasión por crear con sus manos.</p>
        </div>
      </article>
"""

if old_extra in content:
    content = content.replace(old_extra, new_extra)
else:
    # Just in case whitespace is off
    pass

# We also need to fix all the remaining {{FOTO}} templates that I didn't replace, if any.
# Let's check for {{ or }}
if "{{" in content:
    print("Found placeholders!")

with open("plantilla.html", "w") as f:
    f.write(content)
