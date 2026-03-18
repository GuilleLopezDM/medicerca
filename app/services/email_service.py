"""
app/services/email_service.py
==============================
EmailService adaptado de Chargeway → MediCerca.
Misma infraestructura SMTP, nuevos métodos de verificación.
"""

import os
import ssl
import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        email_user: str,
        email_password: str,
        *,
        from_name: str      = "MediCerca",
        use_ssl: bool       = True,
        enabled: bool       = True,
        timeout_seconds: int = 12,
        support_email: str  = "soporte@medicerca.com",
        app_url: str        = "http://localhost:5000",
    ):
        self.smtp_server     = smtp_server
        self.smtp_port       = smtp_port
        self.email_user      = email_user
        self.email_password  = email_password
        self.from_name       = from_name
        self.use_ssl         = use_ssl
        self.enabled         = enabled
        self.timeout_seconds = timeout_seconds
        self.support_email   = support_email
        self.app_url         = app_url

    # ─────────────────────────────────────────
    # CONEXIÓN
    # ─────────────────────────────────────────
    def _open_smtp(self):
        if self.smtp_port == 465:
            self.use_ssl = True

        if self.use_ssl:
            verify = os.getenv("EMAIL_SSL_VERIFY", "true").lower() == "true"
            ctx = ssl.create_default_context() if verify else ssl._create_unverified_context()
            print(f"🔐 SMTP_SSL → {self.smtp_server}:{self.smtp_port}")
            return smtplib.SMTP_SSL(self.smtp_server, self.smtp_port,
                                    timeout=self.timeout_seconds, context=ctx)

        print(f"🔐 SMTP+TLS → {self.smtp_server}:{self.smtp_port}")
        srv = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.timeout_seconds)
        srv.ehlo(); srv.starttls(context=ssl.create_default_context()); srv.ehlo()
        return srv

    def _send(self, msg: MIMEMultipart) -> tuple[bool, str]:
        if not self.enabled:
            print("⚠️  EMAIL_ENABLED=false — no se envía")
            return False, "EMAIL_ENABLED=false"
        try:
            print(f"📧 Enviando a {msg['To']} …")
            with self._open_smtp() as srv:
                srv.login(self.email_user, self.email_password)
                srv.send_message(msg)
            print(f"✅ Enviado a {msg['To']}")
            return True, "ok"
        except smtplib.SMTPAuthenticationError as e:
            return False, f"Auth error: {e}"
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {e}"
        except ssl.SSLError as e:
            return False, f"SSL error: {e}"
        except Exception as e:
            import traceback; traceback.print_exc()
            return False, f"Error inesperado: {e}"

    # ─────────────────────────────────────────
    # PLANTILLA BASE
    # ─────────────────────────────────────────
    def _html(self, titulo: str, cuerpo: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{titulo}</title></head>
<body style="margin:0;padding:0;background:#F2F2F2;font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0">
  <tr><td align="center" style="padding:40px 20px;">
    <table width="560" cellpadding="0" cellspacing="0"
           style="background:#fff;border-radius:16px;overflow:hidden;
                  box-shadow:0 2px 12px rgba(0,0,0,0.08);">

      <tr><td style="background:linear-gradient(135deg,#8BF57A,#7af5c0);
                     padding:28px 32px;text-align:center;">
        <p style="margin:0;font-size:26px;">🩺</p>
        <h1 style="margin:6px 0 0;font-size:20px;font-weight:700;color:#252529;">
          MediCerca
        </h1>
      </td></tr>

      <tr><td style="padding:32px;">{cuerpo}</td></tr>

      <tr><td style="padding:20px 32px;border-top:1px solid #f1f5f9;text-align:center;">
        <p style="margin:0;font-size:12px;color:#9ca3af;">
          ¿Problemas? Escribinos a
          <a href="mailto:{self.support_email}"
             style="color:#205ea6;text-decoration:none;">{self.support_email}</a>
        </p>
        <p style="margin:6px 0 0;font-size:11px;color:#d1d5db;">
          MediCerca · Médicos verificados en Paraguay
        </p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body></html>"""

    # ─────────────────────────────────────────
    # 1a. BIENVENIDA PACIENTE
    # ─────────────────────────────────────────
    def enviar_bienvenida(self, email: str, nombre: str) -> tuple[bool, str]:
        cuerpo = f"""
        <h2 style="margin:0 0 8px;font-size:22px;font-weight:700;color:#252529;">
          ¡Bienvenido/a a MediCerca, {nombre}! 🎉
        </h2>
        <p style="margin:0 0 16px;font-size:15px;color:#6b7280;line-height:1.6;">
          Tu cuenta fue creada exitosamente. Ya podés acceder a todos los servicios
          de MediCerca: encontrá médicos verificados cerca tuyo, leé reseñas y
          encontrá consultorios de forma rápida y segura.
        </p>

        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;
                    padding:18px 20px;margin-bottom:24px;">
          <p style="margin:0 0 8px;font-size:13px;font-weight:700;color:#166534;">
            ¿Qué podés hacer en MediCerca?
          </p>
          <p style="margin:0;font-size:13px;color:#15803d;line-height:1.8;">
            🔍 Buscar médicos por especialidad y zona<br/>
            ⭐ Ver reseñas de otros pacientes<br/>
            📍 Ver ubicación de consultorios en el mapa<br/>
            👤 Gestionar tu perfil personal
          </p>
        </div>

        <p style="margin:0;font-size:13px;color:#9ca3af;text-align:center;">
          Si no creaste esta cuenta, ignorá este mensaje.
        </p>"""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "🎉 ¡Bienvenido/a a MediCerca!"
        msg["From"]    = formataddr((self.from_name, self.email_user))
        msg["To"]      = email
        msg.attach(MIMEText(self._html("Bienvenido/a a MediCerca", cuerpo), "html"))
        return self._send(msg)

    # ─────────────────────────────────────────
    # 1b. BIENVENIDA MÉDICO
    # ─────────────────────────────────────────
    def enviar_bienvenida_medico(self, email: str, nombre: str) -> tuple[bool, str]:
        cuerpo = f"""
        <h2 style="margin:0 0 8px;font-size:22px;font-weight:700;color:#252529;">
          ¡Bienvenido/a a MediCerca, Dr/a. {nombre}! 👨‍⚕️
        </h2>
        <p style="margin:0 0 16px;font-size:15px;color:#6b7280;line-height:1.6;">
          Tu cuenta médica fue creada exitosamente. El próximo paso es completar
          tu perfil profesional para aparecer en el directorio y en el mapa de MediCerca.
        </p>

        <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;
                    padding:18px 20px;margin-bottom:24px;">
          <p style="margin:0 0 8px;font-size:13px;font-weight:700;color:#1e40af;">
            Pasos para activar tu perfil
          </p>
          <p style="margin:0;font-size:13px;color:#1d4ed8;line-height:1.8;">
            1️⃣ Iniciá sesión con tu correo y contraseña<br/>
            2️⃣ Completá tu perfil médico (especialidad, matrícula, hospital)<br/>
            3️⃣ Marcá tu consultorio en el mapa<br/>
            4️⃣ Esperá la verificación del equipo de MediCerca ✅
          </p>
        </div>

        <div style="background:#fefce8;border:1px solid #fde68a;border-radius:12px;
                    padding:14px 16px;margin-bottom:24px;">
          <p style="margin:0;font-size:13px;color:#92400e;line-height:1.6;">
            ⚠️ <strong>Importante:</strong> tu perfil no será visible en el directorio
            hasta que completes la información y sea verificado por nuestro equipo.
          </p>
        </div>

        <p style="margin:0;font-size:13px;color:#9ca3af;text-align:center;">
          Si no creaste esta cuenta, ignorá este mensaje o contactanos a
          <a href="mailto:{self.support_email}" style="color:#3B82F6;">{self.support_email}</a>
        </p>"""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "👨‍⚕️ Tu cuenta médica en MediCerca está lista"
        msg["From"]    = formataddr((self.from_name, self.email_user))
        msg["To"]      = email
        msg.attach(MIMEText(self._html("Bienvenido/a a MediCerca — Médico", cuerpo), "html"))
        return self._send(msg)

    # ─────────────────────────────────────────
    # 2. RECUPERAR CONTRASEÑA
    # ─────────────────────────────────────────
    def enviar_reset_contrasena(self, email: str, nombre: str, token: str) -> tuple[bool, str]:
        url = f"{self.app_url}/auth/nueva-contrasena/{token}"
        cuerpo = f"""
        <h2 style="margin:0 0 8px;font-size:20px;font-weight:700;color:#252529;">
          Restablecer contraseña
        </h2>
        <p style="margin:0 0 24px;font-size:15px;color:#6b7280;line-height:1.6;">
          Hola <strong>{nombre}</strong>, recibimos una solicitud para cambiar tu contraseña.
        </p>
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr><td align="center" style="padding:8px 0 28px;">
            <a href="{url}"
               style="display:inline-block;background:#205ea6;color:#fff;
                      font-size:15px;font-weight:700;text-decoration:none;
                      padding:14px 32px;border-radius:12px;">
              Cambiar contraseña →
            </a>
          </td></tr>
        </table>
        <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;
                    padding:14px 16px;margin-bottom:20px;">
          <p style="margin:0 0 4px;font-size:11px;font-weight:600;color:#9ca3af;
                    text-transform:uppercase;letter-spacing:.05em;">O copiá este enlace</p>
          <p style="margin:0;font-size:12px;color:#6b7280;word-break:break-all;">{url}</p>
        </div>
        <p style="margin:0;font-size:13px;color:#9ca3af;">
          ⏱ Expira en <strong>1 hora</strong>.
          Si no solicitaste el cambio, ignorá este mensaje.
        </p>"""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "🔑 Restablecé tu contraseña — MediCerca"
        msg["From"]    = formataddr((self.from_name, self.email_user))
        msg["To"]      = email
        msg.attach(MIMEText(self._html("Restablecer contraseña", cuerpo), "html"))
        return self._send(msg)


# ─────────────────────────────────────────────────
# FACTORY — lee .env
# ─────────────────────────────────────────────────
def get_email_service() -> EmailService:
    return EmailService(
        smtp_server     = os.getenv("SMTP_SERVER", ""),
        smtp_port       = int(os.getenv("SMTP_PORT", 465)),
        email_user      = os.getenv("EMAIL_USER", ""),
        email_password  = os.getenv("EMAIL_PASSWORD", ""),
        from_name       = os.getenv("EMAIL_FROM_NAME", "MediCerca"),
        use_ssl         = os.getenv("EMAIL_USE_SSL",  "true").lower() == "true",
        enabled         = os.getenv("EMAIL_ENABLED",  "true").lower() == "true",
        timeout_seconds = int(os.getenv("EMAIL_TIMEOUT_SECONDS", "12")),
        support_email   = os.getenv("SUPPORT_EMAIL", "soporte@medicerca.com"),
        app_url         = os.getenv("APP_URL", "http://localhost:5000"),
    )