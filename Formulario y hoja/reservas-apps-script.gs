/**
 * Arte entre Puntadas — Recepción de reservas
 * Guarda cada reserva en la hoja y avisa a Cecilia por correo.
 *
 * ANTES DE USAR, cambia las tres líneas de CONFIGURACIÓN de abajo.
 */

// ─── CONFIGURACIÓN ───────────────────────────────────────────
const ID_HOJA   = 'PEGA_AQUI_EL_ID_DE_LA_HOJA';   // está en la URL de tu Sheet
const NOMBRE_HOJA = 'Reservas';                    // la pestaña, tal cual se llama
const CORREO_AVISO = 'correo-de-cecilia@ejemplo.com';
// ─────────────────────────────────────────────────────────────


function doPost(e) {
  try {
    // Trampa antispam: si el campo oculto viene lleno, es un bot.
    // Respondemos ok para que no reintente, pero no guardamos nada.
    if (e.parameter.website) {
      return responder({ ok: true });
    }

    const hoja = SpreadsheetApp.openById(ID_HOJA).getSheetByName(NOMBRE_HOJA);

    const nombre     = (e.parameter.Nombre     || '').trim();
    const correo     = (e.parameter.Correo     || '').trim();
    const telefono   = (e.parameter.Telefono   || '').trim();
    const habitacion = (e.parameter.Habitacion || '').trim();
    const origen     = (e.parameter.Origen     || 'Web').trim();

    if (!nombre || !telefono) {
      return responder({ ok: false, error: 'Faltan nombre o teléfono' });
    }

    hoja.appendRow([
      new Date(),   // Fecha
      nombre,       // Nombre
      correo,       // Correo
      telefono,     // Teléfono
      habitacion,   // Habitación
      origen,       // Origen: Web o WhatsApp
      '',           // Estado de pago  ← lo llena Cecilia
      ''            // Notas           ← lo llena Cecilia
    ]);

    MailApp.sendEmail({
      to: CORREO_AVISO,
      subject: '🧶 Nueva reserva — ' + nombre,
      body:
        'Nueva solicitud de reserva para Arte entre Puntadas:\n\n' +
        'Nombre:     ' + nombre + '\n' +
        'Correo:     ' + correo + '\n' +
        'Teléfono:   ' + telefono + '\n' +
        'Habitación: ' + (habitacion || 'no indicó') + '\n' +
        'Llegó por:  ' + origen + '\n\n' +
        'Siguiente paso: enviarle las instrucciones para el pago del 50%.\n\n' +
        'Todas las reservas: https://docs.google.com/spreadsheets/d/' + ID_HOJA
    });

    return responder({ ok: true });

  } catch (err) {
    // Si algo falla, queda registrado en Ejecuciones del Apps Script
    console.error(err);
    return responder({ ok: false, error: String(err) });
  }
}


// Sirve para comprobar desde el navegador que el script está publicado.
function doGet() {
  return responder({ ok: true, mensaje: 'Recepción de reservas activa' });
}


function responder(objeto) {
  return ContentService
    .createTextOutput(JSON.stringify(objeto))
    .setMimeType(ContentService.MimeType.JSON);
}
