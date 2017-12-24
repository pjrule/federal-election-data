# Historical Election Data
This project is an attempt to aggregate state-level federal election data from presidential and Congressional elections that's been published throughout the years in inconsistent formats on various government websites in an easily readable open format for use in machine learning experiments and perhaps gerrymandering research. The Federal Election Commission has published statistics over the years in paper reports, generated HTML pages, and Excel files, which presents a barrier to entry to processing and manipulating the data in a programmatic way.

## Available formats
All processed data is currently available as tab-separated CSV files in the "processed" directory. Currently available:
  - 1992 Senate results

## Adding data and reporting issues
While modern OCR is quite good, the processed data from elections before 1996 may not be entirely accurate. If you find an obvious inconsistency, please verify it against the raw data and submit a pull request. :) Ideally, all processed data should be generated repeatedly and programatically, but there are cases where it might make sense to correct the CSV files manually.

Additional official sources of data are welcome.

## Licensing
All raw documents created by the government, and thus the election statistics, are in the public domain. Processing scripts are governed by the MIT License.
