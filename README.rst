Rtridz-tasks
==============

The package is a solution of some algorithmic problems.

Installation
--------------

- Install using python package

    .. code-block:: python

            pip install git+https://github.com/rtridz/rtridz-tasks

                Or directly cloning the repo:
            git clone https://github.com/rtridz/rtridz-tasks.git
            cd rtridz-tasks
            python3 setup.py install
            tasks.py -h

Usage Examples:
------------------
If you installed the package, then use the command tasks.py from anywhere

- Usage examples for first task

    .. code-block:: python

            tasks.py -t 1
            tasks.py -t 1 -v 4 1.5 3 6 1.5
            echo "4 1.5 3 6 1.5" | tasks.py -t 1
            cat ./INPUT_DATA.txt | tasks.py -t 1


- Usage examples for second task

    .. code-block:: python

            tasks.py -t 2
            cat ./data_in.txt | tasks.py -t 2


Command arguments:
------------------
tasks.py [-h] [-t TASK] [-v VALUES [VALUES ...]] [-d DEBUG] [-i INFO]

- Show help information

    .. code-block:: python

            tasks.py -h


- Show information about task

    .. code-block:: python

            tasks.py -t 1 -i 1
            tasks.py -t 2 -i 1

- Put values into argument

    .. code-block:: python

            tasks.py -t 1 -v 4 1.5 3 6 1.5


Python import:
------------------
- Use methods Tasks()

    .. code-block:: python

            python
            >>> from tasks import Tasks
            >>> tasks = Tasks()
            >>> help(tasks)


