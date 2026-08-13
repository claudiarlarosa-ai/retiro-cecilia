# Formulario de reserva — cambios en el HTML

**Sitio:** dosagujasyuncrochet.com (Hostinger) · **Formulario:** `#form-registro`

> No reemplaces tu formulario entero: perderías el diseño. Son tres cambios puntuales sobre lo que ya tienes.

---

## Cambio 1 — La etiqueta `<form>`

**Antes:**
```html
<form id="form-registro" name="submit-to-google-sheet" method="get">
```

**Después:**
```html
<form id="form-registro" name="reserva" method="POST">
```

El `method="get"` era el motivo de que los datos se perdieran: recargaba la página y los dejaba en la barra de direcciones.

---

## Cambio 2 — Dos campos nuevos

Pégalos dentro del formulario, antes del botón de enviar. Conserva las clases CSS que uses en los otros campos para que se vean igual.

```html
<!-- Tipo de habitación -->
<label for="habitacion">Tipo de habitación</label>
<select id="habitacion" name="Habitacion" required>
  <option value="">Elige una opción</option>
  <option value="Individual">Individual</option>
  <option value="Doble">Doble (compartida)</option>
  <option value="Aún no lo decido">Aún no lo decido</option>
</select>

<!-- Origen: se llena solo, dice si llegó por la web o por WhatsApp -->
<input type="hidden" id="origen" name="Origen" value="Web">

<!-- Trampa antispam: invisible para las personas, la llenan los bots -->
<div style="position:absolute;left:-9999px;" aria-hidden="true">
  <label>No llenar este campo
    <input type="text" name="website" tabindex="-1" autocomplete="off">
  </label>
</div>
```

---

## Cambio 3 — Mensaje de confirmación

Justo **después** de cerrar el `</form>`, agrega:

```html
<div id="form-exito" role="status" style="display:none;">
  <p><strong>¡Recibimos tus datos! 🧶</strong></p>
  <p>Cecilia te escribirá por WhatsApp en las próximas horas con las
     instrucciones para el pago del 50% y confirmar tu vacante.</p>
</div>

<p id="form-error" role="alert" style="display:none;">
  Hubo un problema al enviar. Escríbenos por WhatsApp y lo resolvemos.
</p>
```

Dale los estilos que quieras — lo importante son los `id`.

---

## Cambio 4 — El script que conecta todo

Pégalo antes de `</body>`, y reemplaza la URL por la que te dé Apps Script.

```html
<script>
(function () {
  var URL_RESERVAS = 'PEGA_AQUI_LA_URL_DEL_APPS_SCRIPT';

  var form   = document.getElementById('form-registro');
  var exito  = document.getElementById('form-exito');
  var error  = document.getElementById('form-error');
  if (!form) return;

  // Si el link trae ?origen=whatsapp, lo registra. Si no, queda como "Web".
  var origen = new URLSearchParams(location.search).get('origen');
  if (origen) {
    document.getElementById('origen').value =
      origen.toLowerCase() === 'whatsapp' ? 'WhatsApp' : origen;
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    var boton = form.querySelector('[type="submit"]');
    var textoOriginal = boton ? boton.textContent : '';
    if (boton) { boton.disabled = true; boton.textContent = 'Enviando...'; }
    error.style.display = 'none';

    fetch(URL_RESERVAS, { method: 'POST', body: new FormData(form) })
      .then(function () {
        form.style.display = 'none';
        exito.style.display = 'block';
        exito.scrollIntoView({ behavior: 'smooth', block: 'center' });
      })
      .catch(function () {
        error.style.display = 'block';
        if (boton) { boton.disabled = false; boton.textContent = textoOriginal; }
      });
  });
})();
</script>
```

---

# Pasos en Google (10 minutos)

**1.** Crea una hoja nueva en Google Sheets. Nómbrala *Reservas Arte entre Puntadas*.

**2.** Renombra la pestaña de abajo a `Reservas` (por defecto dice "Hoja 1").

**3.** En la fila 1 escribe estos encabezados, uno por columna:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Fecha | Nombre | Correo | Teléfono | Habitación | Estado de pago | Notas |

Las dos últimas las llena Cecilia a mano — ahí lleva el control del 50% y del saldo del 20 de octubre.

**4.** Copia el ID de la hoja. Está en la URL, entre `/d/` y `/edit`:
`docs.google.com/spreadsheets/d/`**`ESTO_ES_EL_ID`**`/edit`

**5.** En la hoja: **Extensiones → Apps Script**. Borra lo que haya y pega el contenido de `reservas-apps-script.gs`.

**6.** Cambia las tres líneas de configuración del inicio: el ID de la hoja y el correo de Cecilia.

**7.** Guarda (💾) y ponle nombre al proyecto.

**8.** **Implementar → Nueva implementación**. Rueda dentada → **Aplicación web**. Configura:
- Ejecutar como: **Yo**
- Quién tiene acceso: **Cualquier usuario**

> Ese "cualquier usuario" es obligatorio: sin eso, el formulario de la web no puede escribir en la hoja. No expone la hoja — solo permite enviar datos, no leerlos.

**9.** Google pedirá autorización la primera vez. Avanzado → Ir al proyecto → Permitir.

**10.** Copia la URL que te da (termina en `/exec`) y pégala en `URL_RESERVAS` del script del HTML.

**11.** Sube el HTML actualizado a Hostinger.

---

# Prueba antes del lanzamiento

1. Abre la página y llena el formulario con datos tuyos.
2. Debe aparecer el mensaje de confirmación y desaparecer el formulario.
3. Revisa que la fila llegó a la hoja.
4. Revisa que el correo llegó a Cecilia.
5. Borra esa fila de prueba.

Si no llega nada: abre el Apps Script → **Ejecuciones**. Ahí se ve el error exacto.
