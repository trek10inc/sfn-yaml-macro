import copy
import json
import logging


def get_resources_of_type(resources, resource_type):
    result = {}
    for name, resource in resources.items():
        if resource['Type'] == resource_type:
            result[name] = resource
    return result


def convert_definition(definition, sub_mapping):
    new_definition = copy.deepcopy(definition)
    new_sub_mapping = copy.deepcopy(sub_mapping)

    for key, value in definition.items():
        if key == 'Ref' or key.startswith('Fn::'):
            sub_prefix = str(len(sub_mapping.keys())) # unique keys for sub map
            sub_key = sub_prefix + key.replace('::', '')
            new_sub_mapping[sub_key] = { key: value }
            new_definition = '${' + sub_key + '}'

        elif type(value) == list:
            new_definition[key] = []
            for element in definition[key]:
                if type(element) == dict:
                    new_element, given_sub_mapping = convert_definition(element, new_sub_mapping)
                    new_sub_mapping.update(given_sub_mapping)
                    new_definition[key].append(new_element)
                else:
                    new_definition[key].append(element)

        elif type(value) == dict:
            new_definition[key], given_sub_mapping = convert_definition(value, new_sub_mapping)
            new_sub_mapping.update(given_sub_mapping)

    return new_definition, new_sub_mapping


def process_template(template):
    new_template = copy.deepcopy(template)
    state_machines = get_resources_of_type(template['Resources'], 'AWS::StepFunctions::StateMachine')

    for name, resource in state_machines.items():
        if not new_template['Resources'][name]['Properties'].get('DefinitionString'):
            continue

        definition = new_template['Resources'][name]['Properties'].pop('DefinitionString')
        converted_definition, sub_mapping = convert_definition(definition, {})

        if sub_mapping:
            new_template['Resources'][name]['Properties']['DefinitionString'] = {
                'Fn::Sub': [ json.dumps(converted_definition, indent=2), sub_mapping ],
            }
        else:
            new_template['Resources'][name]['Properties']['DefinitionString'] = json.dumps(converted_definition, indent=2)

    return new_template


def handler(event, context):
    # print('Event', json.dumps(event, default=str))
    template = event['fragment']
    status = 'success'

    try:
        template = process_template(template)
    except Exception as e:
        logging.error(e, exc_info=True)
        status = 'failure'

    result = {
        'requestId': event['requestId'],
        'status': status,
        'fragment': template,
    }
    # print('Result', json.dumps(result, default=str))
    return result
