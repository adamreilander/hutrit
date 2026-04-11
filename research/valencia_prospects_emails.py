import os, sys
sys.path.insert(0, 'C:/Users/Admin/AppData/Local/Programs/Python/Python313/Lib/site-packages')

from resend import Resend

client = Resend(api_key="re_GbmKvVW9_BPZThHtWWSthWAage2CAhoFF")

emails = [
    {
        "company": "Quibim",
        "contact": "Equipo de Talento Quibim",
        "subject": "Quibim + LATAM: el siguiente paso en vuestra escala de ingeniería",
        "body": """Hola equipo de Quibim,

Acabo de ver que cerrasteis una ronda de $50M Series A en enero — enhorabuena. Ese tipo de crecimiento exige escalar el equipo de ingeniería a una velocidad que el mercado local en España difícilmente puede absorber.

Os escribo desde Hutrit.

Somos una plataforma que conecta empresas europeas con ingenieros y científicos de datos de LATAM — perfiles validados, con experiencia en Python, ML y pipelines de datos, listos para trabajar en remoto full-time.

Lo que hacemos en concreto:
→ Seleccionamos y validamos el perfil antes de presentarlo
→ Presentamos candidatos en menos de 72 horas
→ Acompañamos el onboarding para que la integración sea real

El coste de un senior de ML en LATAM es entre 40-60% menor que un perfil equivalente en España, sin sacrificar nivel técnico.

Si en los próximos meses necesitáis incorporar ingenieros de ML, data scientists o backend — o simplemente queréis ver qué perfiles tenemos ahora mismo —, estaré encantado de coordinar una llamada de 20 minutos.

Un saludo,
Adam Reilander
Hutrit
hutrit.com"""
    },
    {
        "company": "Imperia SCM",
        "contact": "Equipo de Talento Imperia",
        "subject": "Imperia SCM: Ingenieros listos para escalar con vosotros tras el Series A",
        "body": """Hola equipo de Imperia,

Seguís vuestro crecimiento de cerca — €10M para expandir operaciones en Europa es una señal clara de que el equipo de ingeniería necesita crecer pronto.

En Hutrit conectamos startups europeas con ingenieros de LATAM especializados en backend, cloud e infraestructura — exactamente el perfil que necesita un SaaS de supply chain en fase de escala.

Trabajamos con perfiles en C#, Python, Docker y cloud, con experiencia en entornos SaaS B2B.

Lo que nos diferencia:
→ No enviamos CVs — presentamos perfiles validados y filtrados
→ Match en menos de 72 horas
→ Onboarding acompañado para garantizar integración real

¿Tenéis previsión de incorporar ingenieros en los próximos 3 meses? Me encantaría contaros cómo lo hacemos en una llamada corta.

Un saludo,
Adam Reilander
Hutrit
hutrit.com"""
    },
    {
        "company": "Kimera Technologies",
        "contact": "Equipo de Kimera",
        "subject": "Kimera + LATAM: ingeniería de IA sin el coste de contratar localmente",
        "body": """Hola equipo de Kimera,

Con 19 personas y un producto ya desplegado en 40+ retailers, sé que cada incorporación cuenta — y que contratar un senior de IA en Valencia al precio de mercado local puede frenar el ritmo de producto.

En Hutrit trabajamos con startups en fase de escala que necesitan ingenieros de ML, computer vision y backend — sin pagar precios de Madrid o Barcelona.

Nuestros perfiles LATAM tienen experiencia en stacks de IA aplicada, integraciones con Shopify/Magento y entornos de ecommerce — exactamente el contexto en el que operáis.

Si tenéis alguna posición abierta o prevista, puedo presentaros candidatos en menos de 72 horas.

¿Hablamos esta semana?

Adam Reilander
Hutrit
hutrit.com"""
    },
    {
        "company": "Depa Finance",
        "contact": "Equipo de Depa",
        "subject": "Depa Finance: ingenieros backend y fintech desde LATAM",
        "body": """Hola equipo de Depa,

Operar infraestructura de pagos en 200+ países requiere un equipo de backend sólido, disponible y que entienda entornos regulados. Contratar ese perfil localmente en España es caro y lento.

En Hutrit conectamos fintechs europeas con ingenieros de LATAM especializados en backend, APIs e infraestructura fintech — con experiencia en TypeScript, Python y arquitecturas cloud-native.

Os presentamos perfiles validados en menos de 72 horas, al 40-60% del coste de un equivalente local.

Vuestra selección para Endeavor's Scaleup Spain Network confirma que estáis en la fase donde el equipo técnico es el cuello de botella. Podemos ayudaros a desbloquearlo.

¿Tenéis 20 minutos esta semana para una llamada?

Adam Reilander
Hutrit
hutrit.com"""
    },
    {
        "company": "MasLeads",
        "contact": "Equipo de MasLeads",
        "subject": "MasLeads: talento tech de LATAM para escalar sin frenar el producto",
        "body": """Hola equipo de MasLeads,

200+ clientes con 11 personas es una señal muy clara: necesitáis sumar capacidad técnica sin disparar la estructura de costes.

En Hutrit conectamos startups SaaS con ingenieros y perfiles de producto de LATAM — validados, listos para trabajar en remoto full-time y a un coste que tiene sentido para equipos en vuestra fase.

Trabajamos con perfiles en desarrollo, datos, UX y automatización — el tipo de talento que necesita un producto de lead gen basado en IA para seguir creciendo.

Match en 72 horas. Onboarding acompañado. Sin CV genéricos.

¿Os cuento cómo lo hacemos?

Adam Reilander
Hutrit
hutrit.com"""
    }
]

results = []
for e in emails:
    try:
        r = client.emails.send({
            "from": "onboarding@resend.dev",
            "to": ["adamreilander@gmail.com"],
            "subject": f"[PRUEBA - {e['company']}] {e['subject']}",
            "text": e["body"]
        })
        results.append(f"OK - {e['company']} - ID: {r.id}")
    except Exception as ex:
        results.append(f"ERROR - {e['company']}: {ex}")

for r in results:
    print(r)
