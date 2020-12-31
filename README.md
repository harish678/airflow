# Airflow Tutorial

Airflow is platform to programmatically author, schedule and monitor workflows.

5 core components:

    1. Web Server
    2. Scheduler
    3. Metadata database
    4. Worker
    5. Executor

6 in distributed mode

    6. Queue

4 key concepts:

    1. DAG           - graph of operators and dependencies
    2. Operator      - define the task and what they do
    3. Task          - instance of operator
    4. Task Instance - Specific run of task: DAG + Task + Point in TIME
    5. workflow      - Mix of all the above

# DAG

1. DAG can not have any cycle.
2. Each node is a `TASK`
3. Each edge is a `DEPENDENCY`

<u> Properties: </u>

DAG's are defined in Python files placed in Airflow's DAG_FOLDER (default: ~/airflow/dags)

    dag_id              - unique id
    description         - description
    start_date          - when dag should start
    schedule_interval   - how often dag should run
    dependend_on_past   - based on previous dag run state
    default_args        - dict of variables used as constructor paramater when initializing operators

# Operators

1. Definition of a single task
2. Should be `idempotent` - operator should produce same result on every run
3. Task is created by instantiating an `Operator` class

<u>Types of Operators:</u>

    1. Action Operators
        1. BashOperator
        2. PythonOperator
        3. EmailOperator
        4. MySqlOperator, SqliteOperator, PostgreOperator ...
    2. Transfer Operators
        1. PrestoToMySqlOperator
        2. SftpOperator
    3. Sensor Operators

<br/>

> <u>**DAGBAG**</u> - checks for the dag configurations/dag directory refresh for every interval set in the configuration file

DAGBAG attributes in configuration file:

1. worker_refresh_interval (default: 30 secs)
2. dag_dir_list_interval (default: 300 secs)

# Scheduler

`schedule_interval` should be given as `CRON JOB` (str) or `date` (datetime.timedelta)

## Parallelism

Parallelism attributes in configuration file:

1. parallelism
2. max_active_runs_per_dag
3. dag_concurrency

# SubDAG

Implemented using `SubDagOperator` and `subdag_factory`

# Hooks

Hook is used as an interface to interact with external systems

# XCOM

1. Share data between tasks using XCOM's methods (`xcom_push`, `xcom_pull`)
2. XCOM with most recent `execution_date` will be pulled out in first if they both have the same key

# Branching

Allow DAG to choose different branch based on the result of a specific task (`BranchPythonOperator`).

> Not recommended to use `dependend_on_past`.

# SLA

1. Add to an operator using `sla=timedelta(seconds=5)` -> time based on the SLA
2. `Formula: execution_date + 2 schedule intervals ahead + sla.time < utcnow()` -> SLA missed
3. Checks for past execution task for calculating SLA

# Plugins

Create using `airflow.plugins_manager.AirflowPlugin`

## Extendable Components

    1. Operators    (BaseOperator)
    2. Sensors      (BaseSensor)
    3. Hooks        (BaseHook)
    4. Executors    (BaseExecutor)
    5. Admin Views  (flask_admin.BaseView)
    6. Blueprints   (flask.Blueprint)
    7. Menu Link    (flask_admin.base.MenuLink)

# Variables

`from airflow.models import Variable` -> `get`, `set` methods
