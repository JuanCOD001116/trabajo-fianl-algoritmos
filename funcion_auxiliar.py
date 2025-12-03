# Función auxiliar para obtener límite y unidad según variable y tipo de sistema
def obtener_limite_unidad(lmp, variable, tipo_sistema):
    """Retorna el límite y la unidad para una variable y tipo de sistema específico."""
    unidad = lmp["Unidad"][(lmp["Variable"] == variable)]
    
    # Intentar obtener límite para el tipo de sistema especificado
    limite = lmp["LMP_max"][(lmp["Variable"] == variable) & (lmp["TipoSistema"] == tipo_sistema)]
    
    # Si no existe, buscar alternativa (Rio o Residual)
    if limite.empty and tipo_sistema == "Potable":
        limite = lmp["LMP_max"][(lmp["Variable"] == variable) & (lmp["TipoSistema"] == "Rio")]
        if limite.empty:
            limite = lmp["LMP_max"][(lmp["Variable"] == variable) & (lmp["TipoSistema"] == "Residual")]
    
    return limite, unidad