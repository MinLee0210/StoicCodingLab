import time

from copy import deepcopy
from job import Job

"""
    A job is a unit of work that is scheduled and executed by a system. 
     A task is a set of related jobs which jointly provide some function.
"""

class Task:
    def __init__(self, period=None, execution_time=None, relative_deadline=None, absolute_deadline=None, name='Job'):
        # Temporal Parameters of a task.
        self.period = period
        self.execution_time = execution_time
        if relative_deadline == None:
            self.relative_deadline = relative_deadline
        self.relative_deadline = relative_deadline
        self.absolute_deadline = absolute_deadline

        self.job_list = []
        self.job_prototype_list = []
        self.job_dict = {job.name: job for job in self.job_list}
        self.name = name

    def build_job(self, job):
        job_copy = deepcopy(job)
        return job_copy
    
    def reset_job(self, job):
        self.build_job(job)

    def add_job(self, job:Job):
        self.job_list.append(job)

    def remove_job(self, job_name:str):
        del self.job_dict[job_name]

    def execute(self):
        tick = 0
        while True:
            for job in self.job_list:
                # if (job.relative_deadline - job.release_time) // job.period != tick:
                #     continue
                job.run()
                if job.is_avaiable_runtime() == False:
                    pass
            time.sleep(1)
            tick +=1
    
# class PeriodicTask(Task):
#     def __init__(self):
#         super().__init__()

# class AperiodicTask(Task):
#     def __init__(self):
#         super().__init__()

# class SporadicTask(Task):
#     def __init__(self):
#         super().__init__()


# class TaskState:
#     def __init__(self):
#         pass