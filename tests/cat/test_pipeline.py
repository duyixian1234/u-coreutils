from u_coreutils.cat.pipeline import (
    ShowEnds,
    ShowTabs,
    ShowLineNumbers,
    ShowNotBlankLineNumbers,
    SqueezeBlankLines,
    Pipeline,
)


def test_pipeline():
    kwargs = dict(showLineNumberFlag=1, showEndFlag=False, showTabsFlag=False, squeezeBlankFlag=True)
    pipeline = Pipeline(**kwargs)
    assert len(pipeline.linePipeline) == 2
    assert [type(item) for item in pipeline.linePipeline] == [ShowLineNumbers, SqueezeBlankLines]
    assert pipeline.execute("a\n", 0) == "     1  a\n"

    kwargs["showAllFlag"] = True
    kwargs["showLineNumberFlag"] = 2
    pipeline = Pipeline(**kwargs)
    assert len(pipeline.linePipeline) == 4
    expect = [
        ShowNotBlankLineNumbers,
        ShowTabs,
        SqueezeBlankLines,
        ShowEnds,
    ]
    assert [type(item) for item in pipeline.linePipeline] == expect


def testShowEnds():
    showEnds = ShowEnds()
    assert showEnds.run("a\n") == "a$\n"


def testShowTabs():
    showTabs = ShowTabs()
    assert showTabs.run("\ta\t") == "^Ia^I"


def testShowLineNumbers():
    showLineNumbers = ShowLineNumbers()
    assert showLineNumbers.run("a\n", 1) == "     2  a\n"


def testShowNotBlankLineNumbers():
    showNotBlankLineNumbers = ShowNotBlankLineNumbers()
    assert showNotBlankLineNumbers.run("a\n") == "     1  a\n"
    assert showNotBlankLineNumbers.run("\n") == "\n"
    assert showNotBlankLineNumbers.run("b\n") == "     2  b\n"


def testSqueezeBlankLines():
    squeezeBlankLines = SqueezeBlankLines()
    assert squeezeBlankLines.run("a\n") == "a\n"
    assert squeezeBlankLines.run("\n") == ""
    assert squeezeBlankLines.run("\n", 2) == ""
    assert squeezeBlankLines.run("b\n", 3) == "b\n"
    assert squeezeBlankLines.run("c\n", 4) == "c\n"
