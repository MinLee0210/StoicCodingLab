from enum import Enum

class JobState(Enum):
    ON = 1
    OFF = 0

class Job:
    def __init__(self, release_time=None, period=None, execution_time=None, relative_deadline=None, absolute_deadline=None, name='Job'):
        # Temporal Parameters of a Job.
        self.release_time = release_time
        self.period = period
        self.execution_time = execution_time
        self.relative_deadline = relative_deadline
        self.absolute_deadline = absolute_deadline

        self.run_time = self.execution_time - self.release_time

        # Parameters that giving informations about a job: current status and name 
        self.current_state = JobState.OFF
        self.name = name

    def description(self):
        message = f'Job: {self.name}\n'\
                f'>>> Release time: {self.release_time}\n'\
                f'>>> Execution time: {self.execution_time}\n'\
                f'>>> Relative Deadline: {self.relative_deadline}\n'\
                f'>>> Absolute Deadline: {self.absolute_deadline}\n'\
                f'>>> Current State: {self.current_state}\n'\
                '======================================'
        print(message)

    def in_feasible_interval(self, current_time):
        if current_time > self.relative_deadline and current_time <= self.absolute_deadline:
            return True
        return False
    
    def is_executable(self, current_time):
        sys_current_time = current_time % self.period
        if ((sys_current_time) >= self.release_time) and (sys_current_time < self.execution_time):
            print(f'Realtime at: {current_time} To server: At {sys_current_time} {self.name} is executing')
        #     return True
        # return False

    def is_deadline(self, current_time):
        sys_current_time = current_time % self.period
        # if sys_current_time in range(self.relative_deadline - self.execution_time):
        if (sys_current_time >= self.execution_time) and (sys_current_time < self.relative_deadline):
            print(f'Realtime at: {current_time} To server: At {sys_current_time} {self.name} is waiting to be executed.')

    def run(self, current_time):
        self.is_executable(current_time=current_time)
        # self.is_deadline(current_time=current_time)

    def update_execution(self):
        pass

    def is_available_runtime(self):
        if self.current_state != 0:
            return True
        self.current_state = JobState.OFF
        return False
 