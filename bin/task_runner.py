from threading import Thread
import asyncio
import time
import os
import gc


class TaskThread(Thread):
    def __init__(self, task, task_id):
        Thread.__init__(self)
        self._id = task_id
        self._task = task
        self._task_finished = False
        self.runner_attributes = None

    def run(self, *args, **kwargs):
        print(f'Task {self._id} running')
        try:
            self._task(
                proc=self,
                attributes=self.runner_attributes,
                *args,
                **kwargs
            )
        except Exception as e:
            print(e)
        finally:
            print(f'Task {self._id} has ended.')
            self._task_finished = True

    def get_id(self):
        return self._id

    def is_task_finished(self):
        return self._task_finished


class TaskRunner:
    """
    This class will multithread any task passed in by user (via function)
    """

    def __init__(self, task, task_count=1, **attributes):
        self._wait = attributes.get('wait', lambda _: None)
        self._tasks = list()
        self._attributes = dict()
        attr_keys = attributes.keys()
        for k in attr_keys:
            self._attributes[k] = attributes.get(k, None)

        for count in range(task_count):
            t = TaskThread(task, count)
            t.runner_attributes = self._attributes  # Every task will have access to the task runner's attributes
            t.start()
            self._tasks.append(t)

    def __del__(self):
        try:
            for t in self._tasks:
                t.join()
        except Exception as e:
            print(e)
        finally:
            print(f'All tasks finished.')
            gc.collect()

    def all_tasks_finished(self):
        """ Returns if all tasks are finished
            :return: bool
        """
        all_finished = True
        for t in self._tasks:
            if all_finished:
                all_finished = t.is_task_finished()
            else:
                continue
        return all_finished

    def get_attributes(self, key=''):
        attr_copy = {**self._attributes}
        return attr_copy.get(key, None) if key else attr_copy

    async def _async_await_task_complete(self):
        while 1:
            if self.all_tasks_finished():
                break

    def await_task_complete(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_await_task_complete())
