# send_test_outreach.py
# Hutrit Intelligence OS — Test Outreach via Resend
# MODO SEGURO: todos los emails van exclusivamente a adamreilander@gmail.com

import os
from dotenv import load_dotenv
import resend

load_dotenv()

resend.api_key = os.environ.get("RESEND_API_KEY")

TEST_RECIPIENT = "adamreilander@gmail.com"
FROM_EMAIL = "onboarding@resend.dev"  # Dominio de prueba universal de Resend

emails = [
    {
        "to": [TEST_RECIPIENT],
        "from": FROM_EMAIL,
        "subject": "[TEST — Holded] Talento Paid Media LATAM — una idea concreta",
        "html": """
        <p>Hola [nombre],</p>
        <p>Vi que Holded está en una etapa interesante de crecimiento — más mercados, más competencia,
        más presión sobre el canal paid para mantener el CAC bajo mientras escalan.</p>
        <p>Te escribo desde <strong>Hutrit</strong>. Conectamos empresas europeas con Paid Media Buyers
        de LATAM ya validados — perfiles con experiencia real gestionando presupuesto en Google Ads,
        Meta Ads, TikTok y LinkedIn Ads, en remoto desde <strong>$700–$1.000 USD al mes</strong>.</p>
        <p>Para un SaaS como Holded, donde el paid media es uno de los motores principales de
        adquisición, tener a alguien full-time y dedicado puede reducir el CAC de forma visible
        en las primeras 8 semanas.</p>
        <p>No es una propuesta de agencia. Es un perfil que trabaja con vosotros, en vuestras cuentas.</p>
        <p>¿Tienes 20 minutos esta semana?</p>
        <p>Un saludo,<br><strong>Hutrit</strong> — hutrit.com</p>
        <p><em>--- MODO SEGURO: Email de prueba — destinatario real sería contacto de Holded ---</em></p>
        """,
    },
    {
        "to": [TEST_RECIPIENT],
        "from": FROM_EMAIL,
        "subject": "[TEST — Factorial HR] Expandiendo a 4 mercados — ¿cómo está el paid?",
        "html": """
        <p>Hola [nombre],</p>
        <p>Sigo la expansión de Factorial con mucho interés — España, Francia, México, Brasil en
        paralelo es ambicioso y el equipo lo está ejecutando bien.</p>
        <p>Te escribo desde <strong>Hutrit</strong> porque ese tipo de expansión multi-mercado pone
        mucha presión sobre el equipo de paid: mismos recursos, cuatro veces más de segmentaciones,
        idiomas, plataformas y benchmarks distintos por país.</p>
        <p>Lo que conectamos son Paid Media Buyers de LATAM ya validados — perfiles senior con
        experiencia en Google Ads, Meta y LinkedIn, inglés fluido, gestión multi-idioma en remoto.
        Desde <strong>$700–$1.000 USD al mes</strong>.</p>
        <p>Una forma de sumar capacidad de ejecución real sin añadir estructura fija.</p>
        <p>¿Hablamos 20 minutos esta semana?</p>
        <p>Un saludo,<br><strong>Hutrit</strong> — hutrit.com</p>
        <p><em>--- MODO SEGURO: Email de prueba — destinatario real sería contacto de Factorial HR ---</em></p>
        """,
    },
    {
        "to": [TEST_RECIPIENT],
        "from": FROM_EMAIL,
        "subject": "[TEST — Cobee] La batalla por el decision-maker de RRHH — propuesta concreta",
        "html": """
        <p>Hola [nombre],</p>
        <p>En el mercado de beneficios para empleados hay varios jugadores fuertes compitiendo por
        el mismo perfil de cliente: el HR Director o CEO de empresa mediana. Y en ese contexto,
        el paid media — especialmente LinkedIn Ads — es uno de los pocos canales donde se puede
        ganar visibilidad de forma consistente y medible.</p>
        <p>Te escribo desde <strong>Hutrit</strong>. Conectamos empresas como Cobee con Paid Media
        Buyers de LATAM ya validados, con experiencia en campañas B2B SaaS en LinkedIn Ads y
        Google Ads, alineados con ciclos de venta consultiva.</p>
        <p>Disponibles en remoto, desde <strong>$700–$1.000 USD al mes</strong>.</p>
        <p>Si el objetivo es bajar el coste por demo cualificada, este perfil puede ser la
        pieza que falta.</p>
        <p>¿Tienes 20 minutos esta semana?</p>
        <p>Un saludo,<br><strong>Hutrit</strong> — hutrit.com</p>
        <p><em>--- MODO SEGURO: Email de prueba — destinatario real sería contacto de Cobee ---</em></p>
        """,
    },
]


def send_test_emails():
    print("=" * 60)
    print("Hutrit Intelligence OS -- MODO SEGURO")
    print(f"Destinatario de prueba: {TEST_RECIPIENT}")
    print(f"Remitente: {FROM_EMAIL}")
    print("=" * 60)

    success_count = 0
    for i, email in enumerate(emails, 1):
        empresa = ["Holded", "Factorial HR", "Cobee"][i - 1]
        try:
            response = resend.Emails.send(email)
            print(f"[OK] Email {i}/3 ({empresa}) enviado -- ID: {response['id']}")
            success_count += 1
        except Exception as e:
            print(f"[ERROR] Email {i}/3 ({empresa}): {str(e)}")

    print("=" * 60)
    print(f"Resultado: {success_count}/3 emails enviados correctamente")
    if success_count == 3:
        print("Test completado. Revisa la bandeja de adamreilander@gmail.com.")
    print("=" * 60)


if __name__ == "__main__":
    send_test_emails()
