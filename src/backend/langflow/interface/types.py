from langflow.interface.agents.base import agent_creator
from langflow.interface.chains.base import chain_creator
from langflow.interface.document_loaders.base import documentloader_creator
from langflow.interface.embeddings.base import embedding_creator
from langflow.interface.llms.base import llm_creator
from langflow.interface.memories.base import memory_creator
from langflow.interface.prompts.base import prompt_creator
from langflow.interface.text_splitters.base import textsplitter_creator
from langflow.interface.toolkits.base import toolkits_creator
from langflow.interface.tools.base import tool_creator
from langflow.interface.utilities.base import utility_creator
from langflow.interface.vector_store.base import vectorstore_creator
from langflow.interface.wrappers.base import wrapper_creator


def get_type_list():
    """Get a list of all langchain types"""
    all_types = build_langchain_types_dict()

    # all_types.pop("tools")

    for key, value in all_types.items():
        all_types[key] = [item["template"]["_type"] for item in value.values()]

    return all_types


def build_langchain_types_dict():  # sourcery skip: dict-assign-update-to-union
    """Build a dictionary of all langchain types"""

    all_types = {}

    creators = [
        chain_creator,
        agent_creator,
        prompt_creator,
        llm_creator,
        memory_creator,
        tool_creator,
        toolkits_creator,
        wrapper_creator,
        embedding_creator,
        vectorstore_creator,
        documentloader_creator,
        textsplitter_creator,
        utility_creator,
    ]

    all_types = {}
    for creator in creators:
        created_types = creator.to_dict()
        if created_types[creator.type_name].values():
            all_types.update(created_types)
    return all_types


def find_class_type(class_name, classes_dict):
    return next(
        (
            {"type": class_type, "class": class_name}
            for class_type, class_list in classes_dict.items()
            if class_name in class_list
        ),
        {"error": "class not found"},
    )


def build_langchain_template_custom_component(raw_code, function_args, function_return_type):
    type_list = get_type_list()
    type_and_class = find_class_type("Tool", type_list)

    # Field with the Python code to allow update
    code_field = {
        "code": {
            "required": True,
            "placeholder": "",
            "show": True,
            "multiline": True,
            "value": raw_code,
            "password": False,
            "name": "code",
            "advanced": False,
            "type": "code",
            "list": False
        }
    }

    # TODO: Add extra fields

    # TODO: Build template result
    template = chain_creator.to_dict()['chains']['ConversationChain']

    template.get('template')['code'] = code_field.get('code')

    return template
    # return globals()['tool_creator'].to_dict()[type_and_class['type']][type_and_class['class']]
    # return chain_creator.to_dict()['chains']['ConversationChain']
