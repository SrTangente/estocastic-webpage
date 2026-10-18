/**
 * Recoge los correos del formulario de estocastic.xyz en una hoja de Google.
 *
 * PASOS (5 min, con la cuenta de Google del colectivo):
 * 1. Crea una hoja de cálculo nueva (sheets.new). Ponle de nombre "Correos esτocasτic".
 * 2. Extensiones -> Apps Script. Borra lo que haya y pega este código entero. Guarda.
 * 3. Implementar -> Nueva implementación -> tipo "Aplicación web".
 *      Ejecutar como: Yo   |   Quién tiene acceso: Cualquier usuario
 *    Autoriza los permisos (Google avisará de "app no verificada": es tuya, es normal).
 * 4. Copia la URL que acaba en /exec y pásamela (o pégala en site.json -> "endpoint").
 *    Esa URL no da acceso a la hoja: solo permite AÑADIR filas.
 * 5. Si cambias el código más adelante: Implementar -> Gestionar implementaciones -> editar -> Nueva versión.
 *
 * Columnas de la hoja: Fecha | Email | Origen | Consentimiento
 */
function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    var data = JSON.parse(e.postData.contents);
    var email = String(data.email || "").trim().toLowerCase();
    var ok = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) && email.length < 255 && data.consent === true;
    if (!ok) return out_({ ok: false });

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (sheet.getLastRow() === 0) sheet.appendRow(["Fecha", "Email", "Origen", "Consentimiento"]);

    var last = sheet.getLastRow();
    var existing = last > 1 ? sheet.getRange(2, 2, last - 1, 1).getValues().map(function (r) { return String(r[0]).toLowerCase(); }) : [];
    if (existing.indexOf(email) === -1) {
      sheet.appendRow([new Date(), email, String(data.source || "").slice(0, 200), "Sí (casilla marcada en la web)"]);
    }
    return out_({ ok: true });
  } catch (err) {
    return out_({ ok: false });
  } finally {
    lock.releaseLock();
  }
}
function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
