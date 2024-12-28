import sys
import json
from datetime import datetime

ALL = "all"
TODO = "to do"
IN_PROGRESS = "in-progress"
DONE = "done"


class Task(object):
    def __init__(self, index: int, description: str, status: str = TODO,
                 created_at: str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), updated_at: str = None):
        self.index = index
        self.description = description
        self.status = status
        self.createdAt = created_at
        self.updatedAt = updated_at if updated_at else self.createdAt

    def __eq__(self, other: str):
        return self.description == other

    def __repr__(self):
        return f"Task({self})"

    def __str__(self):
        return (f"{self.index}: {self.description} ({self.status}) "
                f"[Created: {self.createdAt}, Last update: {self.updatedAt}]")

    def json_view(self):
        return {"index": self.index,
                "description": self.description,
                "status": self.status,
                "created_at": self.createdAt,
                "updated_at": self.updatedAt}


class TaskList:
    def __init__(self, file_name: str = "tasklist.json"):
        self._index = 1
        self.file_name = file_name
        try:
            self._task_list = {task["index"]: Task(**task) for task in self._load()}
            self._index = int(max(self._task_list.keys())) + 1
        except FileNotFoundError:
            self._task_list = {}
        except json.JSONDecodeError:
            self._task_list = {}

    def __setitem__(self, task):
        self._task_list[task.index] = task

    def __contains__(self, task: str):
        return task in self._task_list.values()

    def __getitem__(self, index: int):
        return self._task_list[index]

    def add(self, task: str):
        if task in self._task_list.values():
            raise ValueError("Task is already created")
        self._task_list[self._index] = Task(self._index, description=task)
        self._index += 1
        self.save()
        return self._index-1

    def delete(self, index: int):
        if index in self._task_list.keys():
            del self._task_list[index]
            self._save()
        else:
            raise ValueError("Task not found")

    def update(self, index: int, updated_task: str):
        if index in self._task_list.keys():
            self._task_list[index].description = updated_task
            self._task_list[index].updatedAt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            self._save()
        else:
            raise ValueError("Task not found")

    def _test_save(self):
        with open("save_" + self.file_name, "w") as f:
            json.dump([task.json_view() for task in self._task_list.values()], f)

    def _test_load(self):
        with open("load_" + self.file_name, "r") as f:
            return json.load(f)

    def _save(self):
        with open(self.file_name, "w") as f:
            json.dump([task.json_view() for task in self._task_list.values()], f)

    def _load(self):
        with open(self.file_name, "r") as f:
            return json.load(f)

    def mark(self, index: int, mark: str):
        if index in self._task_list.keys():
            self._task_list[index].status = mark
            self._save()
        else:
            raise ValueError("Task not found")

    def values(self):
        return self._task_list.values()

    def list(self, mark: str = ALL):
        if self._task_list == {}:
            return "Task list is empty"
        for index, task in self._task_list.items():
            if mark == ALL:
                print(task)
            elif task.status == mark:
                print(task)


if __name__ == "__main__":
    task_list = TaskList()
    command = sys.argv[1]

    if command == "add":
        user_task = sys.argv[2]
        new_index = task_list.add(user_task)
        print(f"Task added successfully (ID: {new_index})")

    if command == "update":
        user_task = int(sys.argv[2])
        user_updated_task = sys.argv[3]
        task_list.update(user_task, user_updated_task)

    if command == "delete":
        user_task = int(sys.argv[2])
        task_list.delete(user_task)

    if command == "mark-in-progress":
        user_task = int(sys.argv[2])
        task_list.mark(user_task, IN_PROGRESS)

    if command == "mark-done":
        user_task = int(sys.argv[2])
        task_list.mark(user_task, DONE)

    if command == "list":
        try:
            sort_mark = sys.argv[2]
        except IndexError:
            task_list.list()
        else:
            task_list.list(sort_mark)
