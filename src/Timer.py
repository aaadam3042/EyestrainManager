from typing import overload

class Timer():
    def __init__(self) -> None:
        self.states = ['Initialising', 'Waiting', 'Work', 'WorkOvertime', 'Break', 'BreakOverTime']
        self.currentState = 0

    def get_currentState(self) -> str:
        return self.states[self.currentState]
        
    @overload
    def set_state(self, state: str): ...

    @overload
    def set_state(self, state: int): ...

    def set_state(self, state: int | str) -> bool:
        '''
        Returns true if state exists and succesfull, otherwise false.
        '''

        if isinstance(state, int):
            if state > len(self.states) -1:
                return False
            self.currentState = state
            return True
        elif isinstance(state, str):
            try:
                self.currentState = self.states.index(state)
                return True
            except:
                return False
        else:
            raise TypeError("Something has gone terribly wrong!")
        