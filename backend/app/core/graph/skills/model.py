from pydantic import BaseModel, Field # type: ignore
from langchain.chat_models import AzureChatOpenAI # type: ignore
from langchain.tools import StructuredTool # type: ignore
from langchain.agents import initialize_agent, AgentType # type: ignore

# Definir el esquema de entrada usando Pydantic
class SchemaInput(BaseModel):
    text: str = Field(description="El texto del archivo de entrada")

# Definir el esquema de salida
class TemplateInfoOutput(BaseModel):
    Nombre_Empresa_Cliente: str
    Direccion_Cliente: str
    Representante_Cliente: str
    Nombre_Empresa_Ciberseguridad: str
    Direccion_Empresa_Ciberseguridad: str
    Representante_Ciberseguridad: str
    Duracion_Contrato: str
    Importe_Contrato: str
    Calendario_Pagos: str
    Preaviso_Terminacion: str
    Pais_Jurisdiccion: str
    Lugar_Firma: str
    Fecha_Firma: str
    Firma_Representante_Cliente: str
    Firma_Representante_Ciberseguridad: str

# Función que será utilizada por el agente para procesar el texto
def get_template_info(text: str) -> dict:
    """Lógica para extraer información del texto según las categorías"""
    prompt = f"""
    Extrae la siguiente información del texto proporcionado y devuélvela en formato JSON:

    - Nombre_Empresa_Cliente
    - Direccion_Cliente
    - Representante_Cliente
    - Nombre_Empresa_Ciberseguridad
    - Direccion_Empresa_Ciberseguridad
    - Representante_Ciberseguridad
    - Duracion_Contrato
    - Importe_Contrato
    - Calendario_Pagos
    - Preaviso_Terminacion
    - Pais_Jurisdiccion
    - Lugar_Firma
    - Fecha_Firma
    - Firma_Representante_Cliente
    - Firma_Representante_Ciberseguridad

    Texto:
    {text}
    """
    # Aqui ponemos un ejemplo para guiar al modelo 
    return {
        "Nombre_Empresa_Cliente": "ACME Corp",
        "Direccion_Cliente": "123 Calle Principal",
        "Representante_Cliente": "John Doe",
        "Nombre_Empresa_Ciberseguridad": "CyberSafe Ltd",
        "Direccion_Empresa_Ciberseguridad": "456 Calle Seguridad",
        "Representante_Ciberseguridad": "Jane Smith",
        "Duracion_Contrato": "1 año",
        "Importe_Contrato": "1.500 euros",
        "Calendario_Pagos": "Mensual",
        "Preaviso_Terminacion": "30 días",
        "Pais_Jurisdiccion": "España",
        "Lugar_Firma": "Madrid",
        "Fecha_Firma": "2024-01-01",
        "Firma_Representante_Cliente": "John Doe",
        "Firma_Representante_Ciberseguridad": "Jane Smith"
    }

get_template_info_tool = StructuredTool.from_function(
    func=get_template_info,
    name="get_template_info",
    description="Extrae información del texto según el esquema definido.",
    args_schema=SchemaInput,
    return_direct=True,
)

#### Hasta aqui el modelo ahora viene el test ####

import os
import dotenv

input_text = """
La empresa cliente es Ciberseguridad Global S.L., ubicada en Calle Falsa 123, 28000 Madrid, España. Su representante es Juan Pérez Gómez. La empresa de ciberseguridad es Seguridad Digital Pro S.L., situada en Avenida de la Innovación 45, 08000 Barcelona, España. La representante es Laura Martínez López.

El contrato tiene una duración de 12 meses y un importe total de 25,000 euros. Los pagos se hacen mensualmente, al final de cada mes.

Para terminar el contrato, se necesita un preaviso de 30 días.

La jurisdicción es en España.

El contrato se firmó en Madrid el 1 de noviembre de 2024.

Firmaron Juan Pérez Gómez por la empresa cliente y Laura Martínez López por la empresa de ciberseguridad. "
"""

# Load environment variables from .env file
dotenv.load_dotenv()

# Inicializar el LLM (asegúrate de configurar correctamente tus credenciales y endpoints)
llm = AzureChatOpenAI(
    openai_api_base=os.environ.get('openai_api_base'),
    openai_api_version=os.environ.get('openai_api_version'),
    deployment_name=os.environ.get('deployment_name'),
    openai_api_key=os.environ.get('openai_api_base'),
    openai_api_type="azure",
    temperature=0,
)

# Crear el agente con la herramienta
tools = [get_template_info_tool]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, #el agente no tiene memoria
    verbose=True,
)

# Texto de entrada para el agente
input_agent = "Por favor, extrae la información del siguiente texto: " + input_text

# Usar `invoke` para ejecutar el agente con el input proporcionado
resultado_agente = agent.run(input_agent)
print("Resultado del agente:")
print(resultado_agente)
