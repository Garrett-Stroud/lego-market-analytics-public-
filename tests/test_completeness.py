from pipeline.canonicalization.completeness import infer_completeness


def test_infer_completeness_complete():
    c, figs, box, instr = infer_completeness("LEGO 75192 COMPLETE with minifigs box instructions")
    assert c == "complete"
    assert figs is True
    assert box is True
    assert instr is True

def test_infer_completeness_minifigs_only():
    c, figs, box, instr = infer_completeness("Millennium Falcon minifigs only")
    assert c == "minifigs_only"
    assert figs is True
    assert box is False
    assert instr is False
