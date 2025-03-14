"""Endpoint File Management
"""
from typing import Dict, List
from constants import cmds

class EndpointFileManagement:
    """Endpoint File Management class
    """
    def __init__(self):
        """Initialize this class and set class member(s)
        """
        self.efm: Dict = {}

    def create(self, path: str) -> None:
        """Create

        Args:
            path (str)
        """
        current: Dict = self.efm
        path_parts: List = path.split('/')

        for path_part in path_parts:
            if path_part not in current:
                current[path_part] = {}
            current = current[path_part]

        print(f'CREATE {path_part}')

    def move(self, source: str, destination: str) -> None:
        """Move file and/or directory based on source and destination input

        Args:
            source (str)
            destination (str)
        """
        destination_parts = destination.split('/')
        source_parts = source.split('/')
        source_parent = self.__fetch_parent_directory(source_parts[:-1])

        if source_parent is None or source_parts[-1] not in source_parent:
            print(f'Error: Failed to move {source} - source does not exist')
            return

        destination_directory = self.__fetch_or_create_directory(destination_parts)
        destination_directory[source_parts[-1]] = source_parent.pop(source_parts[-1])

        print(f'MOVE {source} {destination}')

    def list_structure(self) -> None:
        """List current file and/or directory structure
        """
        print('LIST')
        self.__print_directory_structure(self.efm)

    def delete(self, path: str) -> None:
        """Delete file and/or directory

        Args:
            path (str)
        """
        path_parts: List = path.split('/')
        parent: Dict = self.__fetch_parent_directory(path_parts[:-1])

        if parent is None or path_parts[-1] not in parent:
            print(f"Error: Failed to delete {path} - {path_parts[-2] if len(path_parts) > 1 else 'root'} does not exist")
        else:
            del parent[path_parts[-1]]
            print(f'DELETE {path}')

    def sample_commands(self) -> None:
        """Print out sample commands
        """
        print('HELP')
        print(cmds)

    def __print_directory_structure(self, current: Dict, level: int = 0) -> None:
        """Print out file and/or directory structure

        Args:
            current (Dict)
            level (int, optional)
        """
        for name, content in sorted(current.items()):
            print('  ' * level + name)
            if isinstance(content, dict):
                self.__print_directory_structure(content, level + 1)

    def __fetch_parent_directory(self, path_parts: List) -> Dict:
        """Fetch parent directory

        Args:
            path_parts (List)

        Returns:
            Dict: parent's directory
        """
        current = self.efm

        for path_part in path_parts:
            if path_part not in current:
                return None
            current = current[path_part]

        return current

    def __fetch_or_create_directory(self, path_parts: List) -> Dict:
        """Fetch or create new directory

        Args:
            path_parts (List)

        Returns:
            Dict: current file/directory structure
        """
        current = self.efm

        for path_part in path_parts:
            if path_part not in current:
                current[path_part] = {}
            current = current[path_part]

        return current
