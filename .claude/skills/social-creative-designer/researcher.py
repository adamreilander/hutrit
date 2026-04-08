import pandas as pd
from pathlib import Path

def generar_estrategia_hutrit():
    """Analiza los prospectos y decide la mejor forma de venderles"""
    csv_path = Path(__file__).parent.parent.parent.parent / "research" / "seguimiento_hutrit.csv"
    
    if not csv_path.exists():
        return "No hay datos de prospectos para analizar."
    
    df = pd.read_csv(csv_path)
    
    # Lógica de Auto-Research:
    sin_pixel = df[df['Meta_Pixel'] == 'No'].shape[0]
    total = df.shape[0]
    
    reporte = f"""
    --- REPORTE DEL CEO DE HUTRIT ---
    Total agencias analizadas: {total}
    Oportunidades por falta de Pixel (Paid Media): {sin_pixel}
    
    ESTRATEGIA RECOMENDADA:
    1. Para las {sin_pixel} agencias sin Pixel: Enviar mensaje enfocado en 'Pérdida de Dinero por falta de Tracking'.
    2. Para el resto: Enfocarse en 'Escalabilidad con talento LATAM full-time (1200€)'.
    """
    return reporte

if __name__ == "__main__":
    print(generar_estrategia_hutrit())