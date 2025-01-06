class StateManager:
    def __init__(self):
        self.poison_reverse = False

    def set_poison_reverse(self, value):
        self.poison_reverse = value

    def get_poison_reverse(self):
        return self.poison_reverse
    
state_manager = StateManager()
