import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import os



def validate_json(data, schema, schema_dir):
    try:
        # The schemas $ref each other by file name, e.g. "JSONSchema_Codes.json#/properties/CODE"
        registry = Registry()
        for name in os.listdir(schema_dir):
            if name.endswith('.json'):
                resource = DRAFT202012.create_resource(load_json(os.path.join(schema_dir, name)))
                registry = registry.with_resource(uri=name, resource=resource)
        
        # Use the registry to validate the instance
        validator = Draft202012Validator(schema=schema, registry=registry)
        validator.validate(data)

        #print("Valid JSON!")
        return True
    except ValidationError as e:
        print(f"Invalid JSON: {e}")
        print("Failed at: ", e.absolute_path)  # Shows the path in the data where the validation failed
        print("Schema path: ", e.schema_path)  # Shows the path in the schema that triggered the error
        return False

def load_json(schema_path):
    with open(schema_path, 'r') as file:
        schema = json.load(file)
    return schema

def reject_constants(constant):
    """Reject invalid JSON constants like NaN, Infinity, -Infinity."""
    raise ValueError(f"Invalid constant: {constant}")

def load_json_data(data_path):
    with open(data_path, 'r') as file:
        data = json.load(file, parse_constant=reject_constants)
    return data



def print_result(example_path, schema_path):
    example_data = load_json_data(example_path)
    schema = load_json(schema_path)
    if validate_json(example_data, schema, os.path.dirname(schema_path)):
        print("Valid JSON  ", example_path)
    else:
        print("Invalid JSON!!!  ", example_path)


EXAMPLES = {
    'HeaderEvt.json': 'JSONSchema_HeaderEvt.json',
    'HeaderEvt_EventLT.json': 'JSONSchema_HeaderEvt_EventLT.json',
    'HeaderEvt_EventOFF_NativeFault.json': 'JSONSchema_HeaderEvt_EventOFF.json',
    'HeaderEvt_EventOFF_TTS0.json': 'JSONSchema_HeaderEvt_EventOFF.json',
    'HeaderEvt_EventOFF_FE01.json': 'JSONSchema_HeaderEvt_EventOFF.json',
    'HeaderEvt_EventOFF_ITS_SysDiag.json': 'JSONSchema_HeaderEvt_EventOFF_ITS_SysDiag.json',
    'HeaderEvt_EventON_Extra_NativeFault.json': 'JSONSchema_HeaderEvt_EventON_Extra.json',
    'HeaderEvt_EventON_Extra_FE01.json': 'JSONSchema_HeaderEvt_EventON_Extra.json',
    'HeaderEvt_EventON_Extra_ITS.json': 'JSONSchema_HeaderEvt_EventON_Extra_ITS.json',
    'HeaderEvt_EventON_ITS_SysDiag.json': 'JSONSchema_HeaderEvt_EventON_ITS_SysDiag.json',
    'HeaderEvt_EventON_TTS0.json': 'JSONSchema_HeaderEvt_EventON.json',
    'HeaderEvt_EventTRK.json': 'JSONSchema_HeaderEvt_EventTRK.json',
}
ENERGIES = ['diesel', 'electric', 'gas', 'hybrid', 'hybrid_plugin', 'hydrogen']

for energy in ENERGIES:
    for example, schema in EXAMPLES.items():
        if not os.path.exists(f'examples/S03P01_TiGR_{energy}/{example}'):
            continue  # e.g. no FE01 alternator examples for electric and hydrogen
        print_result(f'examples/S03P01_TiGR_{energy}/{example}', f'schemas/S03P01_TiGR_{energy}/{schema}')
