import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import os



def validate_json(data, schema):
    try:
        schema_resource = DRAFT202012.create_resource(schema)
        codes_resource = DRAFT202012.create_resource(load_json('schemas/S03P01_TiGR/JSONSchema_Codes.json'))
        header_resource = DRAFT202012.create_resource(load_json('schemas/S03P01_TiGR/JSONSchema_HeaderEvt.json'))
        registry = Registry().with_resource(uri="urn:schema", resource=schema_resource)
        registry = registry.with_resource(uri="urn:codes", resource=codes_resource)
        registry = registry.with_resource(uri="urn:header", resource=header_resource)
        
        
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
    if validate_json(example_data, schema):
        print("Valid JSON")
    else:
        print("Invalid JSON!!!")


print_result('examples/S03P01_TiGR/HeaderEvt_EventLT.json', 'schemas/S03P01_TiGR/JSONSchema_HeaderEvt_EventLT.json')
print_result('examples/S03P01_TiGR/HeaderEvt_EventOFF_NativeFault.json', 'schemas/S03P01_TiGR/JSONSchema_HeaderEvt_EventOFF.json')
print_result('examples/S03P01_TiGR/HeaderEvt_EventOFF_TTS0.json', 'schemas/S03P01_TiGR/JSONSchema_HeaderEvt_EventOFF.json')
print_result('examples/S03P01_TiGR/HeaderEvt_EventON_Extra_NativeFault.json', 'schemas/S03P01_TiGR/JSONSchema_HeaderEvt_EventON_Extra.json')
print_result('examples/S03P01_TiGR/HeaderEvt_EventON_TTS0.json', 'schemas/S03P01_TiGR/JSONSchema_HeaderEvt_EventON.json')
print_result('examples/S03P01_TiGR/HeaderEvt_EventTRK.json', 'schemas/S03P01_TiGR/JSONSchema_HeaderEvt_EventTRK.json')
print_result('examples/S03P01_TiGR/HeaderEvt.json', 'schemas/S03P01_TiGR/JSONSchema_HeaderEvt.json')