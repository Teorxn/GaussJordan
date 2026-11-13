EXPLANATIONS = {
	"unique": "El rango de A coincide con el rango de [A | b] y con el número de incógnitas. El sistema tiene una única solución.",
	"infinite": "El rango de A es igual al rango de [A | b], pero menor que el número de incógnitas. Hay variables libres y, por tanto, infinitas soluciones.",
	"inconsistent": "El rango de A es menor que el rango de [A | b]. Aparece una fila del tipo 0 = c con c ≠ 0, así que el sistema no tiene solución.",
	"rank": "El rango es la cantidad de filas no nulas en la forma escalonada (o de pivotes de la matriz).",
	"rank_aug": "El rango de la matriz ampliada permite comparar la consistencia del sistema con el rango de A.",
	"gauss": "La eliminación gaussiana transforma la matriz en forma escalonada por filas. Después se resuelve con sustitución regresiva.",
	"gauss-jordan": "La eliminación de Gauss-Jordan continúa hasta la forma escalonada reducida por filas (RREF). La solución se lee directamente.",
	"pivot": "Un pivote es el primer coeficiente no nulo de una fila en la forma escalonada.",
}


def get_explanation(key: str) -> str:
	return EXPLANATIONS.get(key, "")
