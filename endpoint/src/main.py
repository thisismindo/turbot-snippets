from typing import List
from services.endpointfilemanagement import EndpointFileManagement

def run_it():
    efm_obj: EndpointFileManagement = EndpointFileManagement()
    exit_cmds: List = ['exit', 'quit']
    commands_map = {
        'create': lambda args: efm_obj.create(args[0]) if len(args) == 1 else print('Error: Invalid number of arguments for CREATE'),
        'delete': lambda args: efm_obj.delete(args[0]) if len(args) == 1 else print('Error: Invalid number of arguments for DELETE'),
        'move': lambda args: efm_obj.move(args[0], args[1]) if len(args) == 2 else print('Error: Invalid number of arguments for MOVE'),
        'list': lambda args: efm_obj.list_structure() if len(args) == 0 else print('Error: LIST does not require arguments'),
        'help': lambda args: efm_obj.sample_commands() if len(args) == 0 else print('Error: HELP does not require arguments'),
    }

    while True:
        command = input('> ').strip()
        if command.lower() in exit_cmds:
            print('Goodbye 👋')
            break

        command_parts = command.split()
        if len(command_parts) == 0:
            continue

        cmd = command_parts[0].lower()
        args = command_parts[1:]

        if cmd in commands_map:
            commands_map[cmd](args)
        else:
            print('Error: Your command is not valid. Valid input should start with CREATE {{args0}}, DELETE {{args0}}, MOVE {{args0}} {{args1}}, DELETE {{args0}} or LIST.')

if __name__ == '__main__':
    run_it()
