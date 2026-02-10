class ActionRegistry:
    def __init__(self):
        self._actions = {}

    def register(self, name: str, handler, action_type: str):
        self._actions[name] = {
            "handler": handler,
            "type": action_type,
        }

    def get(self, name):
        if name not in self._actions:
            raise ValueError(f"Action '{name}' is not registered.")
        return self._actions[name]


action_registry = ActionRegistry()