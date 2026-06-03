from pipeline.canonicalization.dates import parse_sold_timestamp


def test_parse_sold_timestamp_formats():
    assert isinstance(parse_sold_timestamp("May-28-24"), int)
    assert isinstance(parse_sold_timestamp("2024-05-28"), int)
    assert isinstance(parse_sold_timestamp("05/28/2024"), int)
    assert isinstance(parse_sold_timestamp("28 May 2024"), int)

def test_parse_sold_timestamp_empty():
    ts = parse_sold_timestamp("")
    assert isinstance(ts, int)
