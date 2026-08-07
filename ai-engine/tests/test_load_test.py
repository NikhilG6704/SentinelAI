from validation.load_test import load_tester


def test_load_test():

    report = load_tester.run()

    assert report.total_requests > 0
    assert report.throughput >= 0
    assert report.average_latency >= 0
    assert report.max_latency >= 0
    assert 0 <= report.error_rate <= 1