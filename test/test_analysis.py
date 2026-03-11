import os
import pytest

entradaDir = "entryData"
resultsDir = "analysisResult"

def test_input_files_exist():
    files = os.listdir(entradaDir)
    assert len(files) > 0, "No XML files found in entryData"
    for f in files:
        assert f.endswith(".xml"), f"{f} is not an XML file"


def test_results_exist():
    assert os.path.exists(os.path.join(resultsDir, "keyword_cloud.png")), "Word cloud not generated"
    assert os.path.exists(os.path.join(resultsDir, "figures_per_paper.png")), "Figures histogram not generated"
    assert os.path.exists(os.path.join(resultsDir, "links_per_paper.txt")), "Links txt not generated"