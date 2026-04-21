class Context:
    def __init__(self):
        self.data = {}
        self.state = {}  

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def set_state(self, key, value):
        self.state[key] = value

    def get_state(self, key, default=None):
        return self.state.get(key, default)

    def clear_state(self):
        self.state = {}

    def clear_state_key(self, key):
        """Clear a specific conversation state key without wiping everything."""
        if key in self.state:
            del self.state[key]

    def debug(self):
        """Return current context for debugging/logging."""
        return {"data": self.data, "state": self.state}
