import json
def load_config(file_path):
    """
    Lee la configuracion desde un .json

    Args:
         file_path (str): Ruta del fichero de configuracion.

        """
    with open(file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config
