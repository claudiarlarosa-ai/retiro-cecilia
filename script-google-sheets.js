/**
 * Arte entre Puntadas — Recepción de reservas (Versión Landing Page)
 * Guarda cada reserva en la hoja y avisa por correo.
 *
 * ANTES DE USAR, cambia el CORREO_AVISO por el tuyo.
 */

// ─── CONFIGURACIÓN ───────────────────────────────────────────
const ID_HOJA   = '1ZyyvFLiOuhV-hqgLPxWQT5SwyE6njJHz7C_szJZweYM';   // Tu ID de hoja actual
const NOMBRE_HOJA = 'Reservas';                                     // Nombre de la pestaña de la hoja
const CORREO_AVISO = 'tu-correo@ejemplo.com';                       // PON TU CORREO AQUÍ
// ─────────────────────────────────────────────────────────────

function doPost(e) {
  try {
    // Trampa antispam: si el campo oculto "website" viene lleno, es un bot.
    if (e.parameter.website) {
      return responder({ ok: true });
    }

    const hoja = SpreadsheetApp.openById(ID_HOJA).getSheetByName(NOMBRE_HOJA);

    // Estos nombres coinciden con los "name" del formulario en index.html
    const nombre     = (e.parameter.Nombre     || '').trim();
    const correo     = (e.parameter.Correo     || '').trim();
    const telefono   = (e.parameter.Telefono   || '').trim();
    const habitacion = (e.parameter.Habitacion || '').trim();

    // Verificamos campos mínimos
    if (!nombre || !telefono || !correo) {
      return responder({ ok: false, error: 'Faltan datos (nombre, correo o teléfono)' });
    }

    // Agregamos la fila a Google Sheets
    hoja.appendRow([
      new Date(),   // Columna A: Fecha de registro
      nombre,       // Columna B: Nombre
      correo,       // Columna C: Correo
      telefono,     // Columna D: Teléfono / WhatsApp
      habitacion,   // Columna E: Tipo de habitación
      ''            // Columna F: Estado de pago (lo llenas tú)
    ]);

    // Enviamos el correo de aviso
    MailApp.sendEmail({
      to: CORREO_AVISO,
      subject: '🧶 Nueva reserva desde la Landing Page — ' + nombre,
      body:
        'Nueva solicitud de reserva para Arte entre Puntadas:\n\n' +
        'Nombre:     ' + nombre + '\n' +
        'Correo:     ' + correo + '\n' +
        'Teléfono:   ' + telefono + '\n' +
        'Habitación: ' + habitacion + '\n\n' +
        'Siguiente paso: Escribirle para enviarle las instrucciones para el pago.\n\n' +
        'Ver todas las reservas aquí: https://docs.google.com/spreadsheets/d/' + ID_HOJA
    });

    return responder({ ok: true });

  } catch (err) {
    console.error(err);
    return responder({ ok: false, error: String(err) });
  }
}

// Sirve para comprobar desde el navegador que el script está publicado
function doGet() {
  return responder({ ok: true, mensaje: 'Recepción de reservas activa (Landing Page)' });
}

function responder(objeto) {
  return ContentService
    .createTextOutput(JSON.stringify(objeto))
    .setMimeType(ContentService.MimeType.JSON);
}
