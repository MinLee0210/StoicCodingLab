import time
from job import Job

job1 = Job(release_time=0, period=3, execution_time=2, relative_deadline=4, absolute_deadline=None, name='Job1')
job2 = Job(release_time=1, period=10, execution_time=4, relative_deadline=9, absolute_deadline=None, name='Job2')
job3 = Job(release_time=5, period=5, execution_time=1, relative_deadline=2, absolute_deadline=None, name='Job3')

# job1.description()

tick = 0
while True:
    job1.run(tick)
    job2.run(tick)
    job3.run(tick)

    # Update after each second
    time.sleep(1)
    tick += 1