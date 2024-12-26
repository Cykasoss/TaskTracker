import pytest
from task_cli import TaskList, Task, TODO, IN_PROGRESS, DONE


@pytest.fixture()
def task():
    return Task(1, "Task 1", TODO)


@pytest.fixture()
def task_list():
    return TaskList(file_name="test_tasklist.json")


def test_should_create_task_list():
    assert TaskList() is not None


def test_should_create_task(task):
    assert task is not None


@pytest.mark.parametrize(
    ("index", "description", "status", "result"),
    (
        [1, "Task 1", TODO, 1],
        [2, "Task 2", IN_PROGRESS, 2],
        [3, "Task 3", DONE, 3]
    )
)
def test_should_return_indexes(index, description, status, result):
    assert Task(index, description, status).index == result


@pytest.mark.parametrize(
    ("index", "description", "status", "result"),
    (
        [1, "Task 1", TODO, "Task 1"],
        [2, "Task 2", IN_PROGRESS, "Task 2"],
        [3, "Task 3", DONE, "Task 3"]
    )
)
def test_should_return_descriptions(index, description, status, result):
    assert Task(index, description, status).description == result


@pytest.mark.parametrize(
    ("index", "description", "status", "result"),
    (
        [1, "Task 1", TODO, TODO],
        [2, "Task 2", IN_PROGRESS, IN_PROGRESS],
        [3, "Task 3", DONE, DONE]
    )
)
def test_should_return_status(index, description, status, result):
    assert Task(index, description, status).status == result


@pytest.mark.parametrize(
    ("index", "description", "status", "result"),
    (
        [1, "Task 1", TODO, "Task 1"],
        [2, "Task 2", IN_PROGRESS, "Task 2"],
        [3, "Task 3", DONE, "Task 3"]
    )
)
def test_should_compare_task_with_string(index, description, status, result):
    assert result == Task(index, description, status)


def test_should_return_string(task):
    assert str(task) == f"1: Task 1 (to do) [Created: {task.createdAt}, Last update: {task.updatedAt}]"


def test_should_return_repr(task):
    assert repr(task) == f"Task({task})"


def test_should_return_json_view(task):
    assert task.json_view() == {
        "index": task.index,
        "description": task.description,
        "status": task.status,
        "created_at": task.createdAt,
        "updated_at": task.updatedAt
    }


def test_should_add_task_to_task_list(task_list):
    task_list.add("Task 4")
    assert "Task 4" in task_list


def test_should_delete_task_from_task_list(task_list):
    task_list.delete(3)
    assert "Task 3" not in task_list


def test_should_update_task(task_list):
    task_list.update(2, "Task 5")
    assert "Task 5" in task_list


@pytest.mark.skip
def test_should_return_values(task_list):
    assert task_list.values() == task_list._task_list.values()


@pytest.mark.parametrize(
    "mark",
    [IN_PROGRESS, TODO, DONE]
)
def test_should_return_filtered_task_list(task_list, mark):
    assert task_list.list(mark) == [task for task in task_list.values() if task.status == mark]


def test_should_return_full_task_list(task_list):
    assert task_list.list() == [task for task in task_list.values()]


@pytest.mark.parametrize(
    ("index", "result"),
    (
        [1, "Task 1"],
        [2, "Task 2"],
        [3, "Task 3"]
    )
)
def test_should_get_task_from_task_list(task_list, index, result):
    assert task_list[index].description == result


@pytest.mark.parametrize(
    "mark",
    [IN_PROGRESS, TODO, DONE]
)
def test_should_mark_task(task_list, mark):
    task_list.mark(2, mark)
    assert task_list[2].status == mark
