## Execution

Include your open source articles in the "entryData" folder in the appropriate format or use the example ones.
Run the full analysis:

python script/xmlAnalyzer.py

After execution the following files are generated:

analysisResult/keyword_cloud.png  
analysisResult/figures_per_paper.png  
analysisResult/links_per_paper.txt

Two tests are included:
1. Check the correct input format
2. Check that output documents exist

run the next command in your terminal:

python -m pytest
