"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import os
    import re
    import pandas as pd
    # 1. Definir la ruta dinámica al archivo
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "../files/input/clusters_report.txt")

    # Listas para almacenar los datos limpios
    data = []
    current_row = None

    # 2. Leer línea por línea
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        # Expresión regular para detectar el inicio de una fila (un número al principio)
        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+\s*%).*", line)

        if match:
            # Si teníamos una fila acumulada anterior, la guardamos
            if current_row:
                data.append(current_row)

            # Extraer las primeras 3 columnas usando regex
            cluster = int(match.group(1))
            cantidad = int(match.group(2))
            # Convertir porcentaje a float (ej: "15,9 %" -> 15.9)
            porcentaje = float(
                match.group(3).replace("%", "").replace(",", ".").strip()
            )

            # El resto de la línea son las palabras clave iniciales
            # Las extraemos sabiendo que las primeras columnas ocupan los primeros 40 caracteres
            keywords_start = line[40:].strip()

            current_row = [cluster, cantidad, porcentaje, keywords_start]
        else:
            # Si no empieza con número, es la continuación de las palabras clave de la fila actual
            # Verificamos que ya estemos procesando una fila y que no sea una línea vacía o decorativa
            if current_row and line.strip() and not line.startswith("---"):
                current_row[3] += " " + line.strip()

    # No olvidar añadir la última fila procesada después de salir del ciclo
    if current_row:
        data.append(current_row)

    # 3. Crear el DataFrame inicial
    columns = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]
    df = pd.DataFrame(data, columns=columns)

    # 4. Limpieza final de las palabras clave (quitar múltiples espacios sueltos y el punto final)
    def clean_keywords(text):
        # Reemplazar múltiples espacios o tabulaciones por un solo espacio
        text = re.sub(r"\s+", " ", text)
        # Eliminar el punto final si existe
        if text.endswith("."):
            text = text[:-1]
        # Asegurar espacio correcto después de cada coma
        text = ", ".join([w.strip() for w in text.split(",")])
        return text

    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(
        clean_keywords
    )

    return df