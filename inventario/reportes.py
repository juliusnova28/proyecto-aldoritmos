"""
Módulo para generar el reporte de ventas con formato en consola.
"""
from typing import List
from datetime import datetime
from .modelos import Venta

class ReporteVentas:
    """Genera el reporte del día con columnas alineadas."""

    @staticmethod
    def generar(ventas: List[Venta]) -> str:
        """Filtra las ventas del día actual y devuelve un string formateado."""
        hoy = datetime.now().date()
        ventas_hoy = [v for v in ventas if v.fecha.date() == hoy]

        if not ventas_hoy:
            return "No hay ventas registradas hoy."

        resultado = f"\n{'Fecha':<21}{'Codigo':<9}{'Cant':>6}{'Total':>10}\n"
        resultado += "-" * 46 + "\n"
        
        total_dia = 0.0
        for v in ventas_hoy:
            fecha_str = v.fecha.strftime("%Y-%m-%d %H:%M:%S")
            resultado += f"{fecha_str:<21}{v.codigo_producto:<9}{v.cantidad:>6}{v.total:>10.2f}\n"
            total_dia += v.total
            
        resultado += "-" * 46 + "\n"
        resultado += f"{'Total del día':<36}{total_dia:>10.2f}\n"
        
        return resultado