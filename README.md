# AccessAnalysisResultComparator

This project provides scripts to compare two results of the [Haskalladio analysis](https://github.com/KASTEL-SCBS/haskalladio) for [Confidentiality4CBSE](https://github.com/KASTEL-SCBS/Confidentiality4CBSE) models.

The python scripts are located in the **python** folder.

The script **AccessAnalysisResultComparator.py** compares two access analysis results and provides the common and different entries in separate files. 

When UUIDs are used as input for the Access Analysis, the UUIDs are represented as byte-arrays in the pretty printed output file. The script **AccessAnalysisResultUUIDConverter.py** takes this format and replaces the byte-arrays in the ouput with corresponding UUIDs. 

