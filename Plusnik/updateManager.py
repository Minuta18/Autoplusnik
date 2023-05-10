# Autoplusnik Copyright (C) 2023 Igor Samsonov

import enum
import datetime
import sys

from . import update
from .readToken import readStepikToken, readGoogleToken
from .sheets import load_to_sheet, get_worksheet

WORK_SHEET = 'Инфо Силаэдр 2022-23'

class UpdateQueue():
    def __init__(self):
        self.queue = []

    def pop_first(self):
        '''Deletes first element'''
        try:
            self.queue.pop(0)
        except IndexError as e:
            raise Exception('No elements to delete')

    def append(self, task):
        # TODO: add isinstance assertion
        self.queue.append(task)

    def get(self, tid):
        '''Returns task with given id. Raise ValueError if task does not exist'''
        task = None
        for task_ in self.queue:
            if task.klass_id == tid:
                task = task_
        if task == None:
            raise ValueError(f'No task with id {tid}')
        return task

    def get_all(self) -> list:
        '''Returns all tasks'''
        return self.queue

    def get_tasks_info(self) -> list:
        '''Returns info of all tasks'''
        info = []
        for task_ in self.queue:
            info.append(task_.get_task_info())
        return info

    def get_first(self):
        if len(self.queue) == 0:
            raise Exception('No tasks')
        return self.queue[0]
    
    def get_last(self):
        if len(self.queue) == 0:
            raise Exception('No tasks')
        return self.queue[-1]

class TaskStatus(enum.Enum):
    '''Status of a task'''
    queued = 0
    running = 1
    cancelled = 2
    updated = 3

class UpdateTask():
    def __init__(
            self, 
            queue: UpdateQueue, 
            klass_id: int, 
            sheet_name: str, 
            stepik_token: dict,
            google_token: dict,
            loop: int=None, 
        ):
        '''
        ARGS:
        queue: UpdateQueue - queue to insert task
        klass_id: int - ID of the class in Stepik
        sheet_name: str - name of google sheet to write record
        loop: int|None - loop (in seconds). If None, loop won't be used
        '''
        try:
            self.tid = queue.get_last().get_tid() + 1
        except Exception as e:
            self.tid = 0
        self.status = TaskStatus.queued
        self.klass_id = klass_id
        self.sheet_name = sheet_name
        self.loop = loop
        self.stepik_token = stepik_token
        self.google_token = google_token
        self.last_update = datetime.datetime.utcnow()

    def get_task_info(self) -> dict:
        '''Gets task information'''
        return {
            'task_id': self.tid,
            'status': self.status,
            'class_id': self.klass_id,
            'sheet_name': self.sheet_name,
            'loop_time': self.loop,
            'last_update': self.last_update,
        }

    def get_tid(self) -> None:
        '''Returns the task id'''
        return self.tid

    def run(self) -> None:
        '''Updates klass'''
        update(self.stepik_token[0], self.stepik_token[1], self.klass_id)
        load_to_sheet(get_worksheet(WORK_SHEET, self.sheet_name, self.google_token), './last_report.xlsx')

task_queue = UpdateQueue()
stepik_token = readStepikToken('./Plusnik/stepik_token.json')
google_token = readGoogleToken('./Plusnik/google_token.json')

def add_task(klass_id: int, sheet_name: str) -> None:
    '''Adds task to update queue'''
    global task_queue, stepik_token, google_token
    
    task_queue.append(UpdateTask(
        task_queue,
        klass_id,
        sheet_name,
        stepik_token,
        google_token,
        None,
    ))

def run():
    '''Run update process'''
    global task_queue

    while True:
        if len(task_queue.get_all()) > 0:
            try:
                task = task_queue.get_first()
                task_queue.pop_first()
                task.status = TaskStatus.running
                task.run()
            except Exception as e:
                print(f'Failed to update task\nError occurred: {e}\n')