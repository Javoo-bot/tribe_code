import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field # type: ignore
from jinja2 import Environment, FileSystemLoader
from langchain.agents import initialize_agent, AgentType # type: ignore
from langchain.tools import StructuredTool # type: ignore
from langchain.chat_models import AzureChatOpenAI # type: ignore
from langchain.schema import HumanMessage # type: ignore

# Definir el esquema de entrada usando Pydantic
class SchemaInput(BaseModel):
    text: str = Field(description="El texto JSON del archivo de entrada")

class TemplateInfoOutput(BaseModel):
    pass

# Definir la función fill_template que incluye ejemplos y lógica unida
def fill_template(json_data: dict) -> str:
    """
    Lógica para sustituir la información del template usando Jinja2 y 
    educar al modelo con ejemplos de HumanMessage.
    """
    
    # Convertir el JSON en un diccionario
    template_data = json.loads(json_data)

    # Crear el prompt con las instrucciones específicas y ejemplos
    prompt_base = """
    A continuación tienes un contrato de ciberseguridad con marcadores en el formato **{{ }}**. Sustituye los valores de los siguientes marcadores en el template con los datos proporcionados en el JSON y proporciona solo el texto resultante, sin los marcadores originales ni sus nombres:

    Ejemplos de sustitución:
    - **{{ Nombre_Empresa_Cliente }}**: "Ciberseguridad Global S.L."
    - **{{ Nombre_Empresa_Cliente }}**: "Tech Innovators S.A."
    - **{{ Nombre_Empresa_Cliente }}**: "Data Security Corp."

    Sustituye los siguientes marcadores en el template:
    - **{{ Nombre_Empresa_Cliente }}**
    - **{{ Direccion_Cliente }}**
    - **{{ Representante_Cliente }}**
    - **{{ Nombre_Empresa_Ciberseguridad }}**
    - **{{ Direccion_Empresa_Ciberseguridad }}**
    - **{{ Representante_Ciberseguridad }}**
    - **{{ Duracion_Contrato }}**
    - **{{ Importe_Contrato }}**
    - **{{ Calendario_Pagos }}**
    - **{{ Preaviso_Terminacion }}**
    - **{{ Pais_Jurisdiccion }}**
    - **{{ Lugar_Firma }}**
    - **{{ Fecha_Firma }}**
    - **{{ Firma_Representante_Cliente }}**
    - **{{ Firma_Representante_Ciberseguridad }}**

    Texto a procesar:
    {json_data}
    """

    # Crear el mensaje en formato de chat usando HumanMessage
    prompt = prompt_base.format(json_data=json_data)
    messages = [HumanMessage(content=prompt)]

    # Ejecutar el LLM para obtener la respuesta (datos con sustituciones hechas)
    llm_response = llm(messages)

    # Renderizar el template con Jinja2 usando los datos proporcionados por el LLM
    env = Environment(loader=FileSystemLoader('./markers'))  # Configurar el entorno de Jinja2
    template = env.get_template('contrato.j2')  # Cargar el template

    # Si la respuesta del LLM ya es el texto final, simplemente se guarda
    output_text = llm_response.content.strip()  # Obtener el contenido como string

    return output_text

# Crear la herramienta estructurada
fill_template_tool = StructuredTool.from_function(
    func=fill_template,
    name="get_template_info",
    description="Sustituye la información del texto en el template usando LLM",
    args_schema=SchemaInput,
    return_direct=True,
)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Definir la cadena JSON de entrada
data_json = """
{
  "Nombre_Empresa_Cliente": "Ciberseguridad Global S.L.",
  "Direccion_Cliente": "Calle Falsa 123, 28000 Madrid, España",
  "Representante_Cliente": "Juan Pérez Gómez",
  "Nombre_Empresa_Ciberseguridad": "Seguridad Digital Pro S.L.",
  "Direccion_Empresa_Ciberseguridad": "Avenida de la Innovación 45, 08000 Barcelona, España",
  "Representante_Ciberseguridad": "Laura Martínez López",
  "Duracion_Contrato": "12 meses",
  "Importe_Contrato": "25,000 euros",
  "Calendario_Pagos": "mensualmente, al final de cada mes",
  "Preaviso_Terminacion": "30 días",
  "Pais_Jurisdiccion": "España",
  "Lugar_Firma": "Madrid",
  "Fecha_Firma": "1 de noviembre de 2024",
  "Firma_Representante_Cliente": "Juan Pérez Gómez",
  "Firma_Representante_Ciberseguridad": "Laura Martínez López"
}
"""

# Inicializar el LLM
llm = AzureChatOpenAI(
    openai_api_base=os.environ.get('openai_api_base'),
    openai_api_version=os.environ.get('openai_api_version'),
    deployment_name=os.environ.get('deployment_name'),
    openai_api_key=os.environ.get('openai_api_key'),
    openai_api_type="azure",
    temperature=0,
)

# Crear el agente con la herramienta
tools = [fill_template_tool]

# Inicializar el agente con los tools y el modelo de lenguaje
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # El agente no tiene memoria
    verbose=True,
)

# Utilizar el agente para ejecutar la lógica de sustitución
response = agent.run(data_json)

# Guardar el resultado en un archivo .txt
with open('output.txt', 'w') as output_file:
    output_file.write(str(response))  # response ya es un string

# Mostrar el resultado
print("Resultado generado por el agente:")
print(response)
