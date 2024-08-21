import json
from jsonschema import validate, ValidationError, Draft202012Validator
from pathlib import Path
from referencing import Registry, Resource, Specification
from referencing.jsonschema import specification_with

def validate_json(data, schema, referenced_schemas):
    try:
        # Create a registry and register the referenced schemas
        registry = Registry()
        for uri, schema_content in referenced_schemas.items():
            registry = registry.with_resource(uri=uri, resource=Resource.from_contents(schema_content))

        # Create the validator with the registry containing multiple referenced schemas
        validator = Draft202012Validator(schema, registry=registry)

        validator.validate(data)

        return True
    except ValidationError as e:
        print(f"Invalid JSON: {e}")
        print("Failed at: ", e.absolute_path)  # Shows the path in the data where the validation failed
        print("Schema path: ", e.schema_path)  # Shows the path in the schema that triggered the error
        return False

# Load the schemas that are being referenced
with open("/schemas/S03P01_TiGR/JSONSchema_HeaderEvt.json") as header_schema_file:
    header_schema = json.load(header_schema_file)

with open("/schemas/S03P01_TiGR/JSONSchema_Codes.json") as another_schema_file:
    another_schema = json.load(another_schema_file)

# Store the referenced schemas in a dictionary with their URIs
referenced_schemas = {
    "JSONSchema_HeaderEvt.json": header_schema,
    "JSONSchema_Codes.json": another_schema,
}

########################################################################################

# Load the main JSON schema
with open('/schemas/S03P01_TiGR/JSONSchema_HeaderEvt_EventON.json', 'r') as schema_file:
    schema = json.load(schema_file)

# Load the JSON file you want to validate
payload_path = '/examples/S03P01_TiGR/HeaderEvt_EventON_TTS0.json'
with open(payload_path, 'r') as json_file:
    data = json.load(json_file)

# Validate the JSON
if validate_json(data, schema, referenced_schemas):
    print("PASS: " + payload_path)
