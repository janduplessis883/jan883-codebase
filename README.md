# jan883-codebase

This is a collection of code snippets by myself, to use in local projects.

**Python Path**: Add your central codebase to the Python path in your projects so that you can import modules directly.

The following line of code is added to `~/.bash_profile` or `~/.zshrc` file:
```
export PYTHONPATH="/Users/janduplessis/code/janduplessis883/jan883-codebase:$PYTHONPATH"
```
### Codebase Structure
```
my_codebase/
├── README.md
├── utils/
│   ├── string_utils.py
│   ├── date_utils.py
├── data_processing/
│   ├── data_cleaning.py
│   ├── data_transformation.py
├── machine_learning/
│   ├── models/
│   │   ├── linear_regression.py
│   │   ├── random_forest.py
├── visualization/
│   ├── plot_helpers.py
└── tests/
    ├── test_string_utils.py
    ├── test_date_utils.py
```
