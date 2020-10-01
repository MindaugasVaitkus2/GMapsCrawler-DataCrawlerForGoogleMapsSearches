
class StateMachine():
    def __init__(self, init_state, init_inputs):
        self.curr_state = init_state
        self.inputs = init_inputs
    def process(self):
        self.inputs = self.curr_state.run(self.inputs)
        self.curr_state = self.curr_state.next(self.inputs)

class State():
    def run(self):
        pass
    def next(self, input):
        pass
