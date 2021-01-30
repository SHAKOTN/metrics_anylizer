# Metrics Analyzer
![Test](https://github.com/SHAKOTN/metrics_anylizer/workflows/Test/badge.svg)

| [Latest Test Runs](https://github.com/SHAKOTN/metrics_anylizer/actions?query=workflow%3ATest) |

---

## Overview

### Technologies
python:3.8.3, kafka, zookeeper, postgres

### Docker
There are 5 different compose services + kafka:
1. `consume` Kafka consumer which consumes data from kafka and saves it to postgres
2. `produce` Kafka producer which reads and sends data to kafka
3. `db` - postgres instance where all metrics are stored
4. `migrate` - "dependency" service to be executed before running `consume` service. Needed to ensure db schema
5. `hist` - checks postgres and collects statistic over certain metrics. After that it is building "histograms"


---

## Tests
docker-compose-ci.yml is used for testing. In this case, it is not needed to install kafka and zookeeper, which makes
tests env faster and smaller.

To run tests locally:

```
$ make tests
```

---

## How to run:
### GitHub actions:
[Simply check this Action executed and it's printing all histograms](https://github.com/SHAKOTN/metrics_anylizer/actions/runs/523328768)

### Local run
```
$ make build
$ make full_run
```
