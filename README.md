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
Or if you want to run it by youself:
- Navigate to `Actions`
- Under `Workflows` click `Run Services`
- Then click `Run workflow` and check logs


### Local run
```
$ make build
$ make full_run
```

### Histograms:
1. Most frequent alerts
```
| Most Frequent Alerts
| +----------+-------------+
| | alert id | alert count |
| +----------+-------------+
| | 9175114  |     346     |
| +----------+-------------+
| |    0     |     327     |
| +----------+-------------+
| | 9175147  |     192     |
| +----------+-------------+
```
2. Top affected nodes
```
| Top 5 most affected nodes
| +---------+----------------+
| |  node   | times affected |
| +---------+----------------+
| | LX00016 |       41       |
| +---------+----------------+
| | LX0002  |       39       |
| +---------+----------------+
| | LX00017 |       38       |
| +---------+----------------+
| | LX0008  |       36       |
| +---------+----------------+
| | LX00015 |       36       |
| +---------+----------------+
```
3. ERA015 timeserier perH
```
| ERA015 generated per hour
| +---------------------+-------+
| |        date         | count |
| +---------------------+-------+
| | 2020-01-25 05:00:00 |  19   |
| +---------------------+-------+
| | 2020-01-25 04:00:00 |  80   |
| +---------------------+-------+
| | 2020-01-25 00:00:00 |   1   |
| +---------------------+-------+
| | 2020-01-24 22:00:00 |  10   |
| +---------------------+-------+
| | 2020-01-24 21:00:00 |  19   |
| +---------------------+-------+
| | 2020-01-24 09:00:00 |  34   |
| +---------------------+-------+
| | 2020-01-24 02:00:00 |   3   |
| +---------------------+-------+
| | 2020-01-24 01:00:00 |   1   |
```