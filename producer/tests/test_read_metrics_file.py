from producer.metrics_generator import read_metrics


def test_metrics():
    metrics = read_metrics()
    assert ["metadata"] == list(metrics[0].keys())
    assert isinstance(list(metrics[0].values())[0], str)
