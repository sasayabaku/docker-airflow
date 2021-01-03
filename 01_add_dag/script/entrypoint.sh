#!/bin/bash
exec /bin/bash -l -c "$*"
CMD="airflow" 
TRY_LOOP="20"
cd ${AIRFLOW_HOME}

export PATH=${HOME}/.local/bin:${PATH}
