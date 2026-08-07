from validation.benchmark import benchmark_runner


def test_benchmark_runner():

    report = benchmark_runner.run()

    assert report.iterations > 0

    assert report.startup_average >= 0
    assert report.load_average >= 0

    assert report.average_cpu >= 0
    assert report.average_memory >= 0