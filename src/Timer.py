import os
import multiprocessing
import time
from inputimeout import inputimeout, TimeoutOccurred
from playsound import playsound
from threading import Timer as ThreadTimer
from typing import overload

class Timer():
    def __init__(self) -> None:
        self.states = ['Initialising', 'Waiting', 'Work', 'WorkOvertime', 'Break', 'BreakOverTime'] # NOTE: at the moment not using overtime. Can be used to get analytics
        self.currentState = 0
        self.alarm_path = ""

        self.validUnits = ['second', 'minute']
        self.timings = {'Work': 20, 'Break': 20}
        self.isTiming = False
        self.timer = -1
        self.timingUnit = ""

        self.cycle = 1

    def load_alarm(self, path):
        self.alarm_path = path
        self.set_state("Waiting")

    def get_currentState(self) -> str:
        return self.states[self.currentState]
        
    @overload
    def set_state(self, state: str) -> bool: ...

    @overload
    def set_state(self, state: int) -> bool: ...

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
        
    def get_current_time(self) -> int:
        if self.timer < 0:
            raise RuntimeError("Something went wrong with timer - Returned a negative value.")
        return self.timer
    
    def set_timing_unit(self, unit: str) -> None:
        if unit not in self.validUnits:
            raise ValueError(f"Tried to set timer to an invalid unit '{unit}'.")
        self.timingUnit = unit

    def get_timing_unit(self) -> str:
        if self.timingUnit.strip() == "":
            raise RuntimeError("Attempted to access timing unit before it was set.")
        elif self.timingUnit.strip().lower() in self.validUnits:
            return self.timingUnit
        else:
            raise RuntimeError("Timing unit was set as an invalid value.")
        
    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def usage(self) -> None:
        print("Welcome to the eyestrain manager application.")
        print("Use ctrl + c at any time to exit the application.")
        print("To use this application just follow the prompts as they appear.")
        
    def display(self) -> None:
        print(f'''
############################################
                           
              
    You are one cycle {self.cycle}
    Current state is {self.get_currentState()}
    You have {self.get_current_time()} {self.get_timing_unit()}/s left
                           

############################################
              ''')
        
    def run(self):
        if self.get_currentState() != "Waiting":
            raise RuntimeError("Program has not correctly initialised the timer.")

        try:
            self.clear_screen()
            self.usage()
            input("\nPress enter to start the session: ")
            self.clear_screen()

            while True:
                self.set_state('Work')
                self.timeSession()
                self.set_state('Break')
                self.timeSession()
                self.cycle += 1

        except KeyboardInterrupt:
            print("\nSuccesfully exited the program!")

    def timeSession(self):
        self.timer = self.timings[self.get_currentState()]
        
        if self.get_currentState() == 'Work':
            self.set_timing_unit("minute")
        elif self.get_currentState() == 'Break':
            self.set_timing_unit("second")

        multiplier = 1
        if self.get_timing_unit() == "minute":
            multiplier = 60 

        while self.timer != 0:
            self.display()
            time.sleep(1 * multiplier)
            self.clear_screen()
            self.timer -= 1

        self.play_alarm_blocking()
            

    def play_alarm_blocking(self):
        while True:
            try:
                alarm = multiprocessing.Process(target=playsound, args=(self.alarm_path,))
                alarm.start()
                inputimeout("\nPress ENTER to start next session: ", 60) 
                alarm.terminate()
                break
            except TimeoutOccurred:
                self.clear_screen()
                print(f'Previous {self.get_currentState()} state has ended. Reminder to move to the next session!')
                continue

            raise RuntimeError("Program arrived at an unreachable state in alarm timer.")
        
def raiseTimeout():
    raise TimeoutError