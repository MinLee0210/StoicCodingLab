"""
    Find effective release time and effective deadline.
"""

class Job:
    def __init__(self, name, release_time, deadline):
        self.name = name
        self.release_time = release_time
        self.deadline = deadline
        self.next = []
        self.prev = []

    def description(self):
        message = f'Job: {self.name}\n'\
                f'>>> Release time: {self.release_time}\n'\
                f'>>> Relative Deadline: {self.deadline}\n'\
                f'>>> Predecessors: {[job.name for job in self.prev]}\n'\
                f'>>> Successors: {[job.name for job in self.next]}\n'\
                '======================================'
        print(message)

class Effective:
    def __init__(self):
        pass

    def get_release_time(self, value:list):
        result = max(value)
        return result
    
    def get_deadline(self, value:list):
        result = min(value)
        return result

class PredecessorGraph:
    def __init__(self, init_job:list[Job]):
        if len(init_job) == 0:
            raise ValueError('Please init job')
        # self.initJob = initJob
        self.effective = Effective()
        self.job_dict = {job.name: job for job in init_job}

    def append(self, predecessor:str, job:Job):
        if job.name not in self.job_dict.keys():
            self.job_dict[job.name] = job
        new_job = self.job_dict[job.name]
        pred_job = self.job_dict[predecessor]
        pred_job.next.append(new_job)
        new_job.prev.append(pred_job)

    def description(self):
        for job_name in self.job_dict.keys():
            self.job_dict[job_name].description()

    def get_effective(self):
        for job_name in self.job_dict.keys():
            current_job = self.job_dict[job_name]
            prev_job = [job for job in current_job.prev]
            next_job = [job for job in current_job.next]
            if  len(prev_job) != 0:
                current_job.release_time = self.effective.get_release_time([job.release_time for job in prev_job])
            if len(next_job) != 0:
                current_job.deadline = self.effective.get_deadline([job.deadline for job in next_job])