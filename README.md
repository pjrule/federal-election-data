# Federal Election Data
This project is an attempt to aggregate state-level federal election data in an easily readable open format for use in machine learning experiments and perhaps gerrymandering research. The Federal Election Commission has published statistics over the years in inconsistent formats—paper reports, generated HTML pages, and Excel files, each with varying schemas from year to year—which presents a barrier to entry to processing and manipulating the data in a programmatic way.

## Available formats
All processed data is currently available as CSV files in the "results" directory. Currently available:
  - 1992 Senate results

## Adding data and reporting issues
While modern OCR is quite good, the processed data from elections before 1996 may not be entirely accurate. If you find an obvious inconsistency, please verify it against the raw data and submit a pull request. :) Ideally, all processed data should be generated repeatedly and programatically, but there are cases where it might make sense to correct the CSV files manually.

Additional official sources of data are welcome.

## Other election data
The FEC (Federal Election Commission) has an API for campaign finance data called OpenFEC. Their documentation is here: https://api.open.fec.gov/developers/

## Licensing
All raw documents created by the government, and thus the election statistics, are in the public domain. Processing scripts are governed by the MIT License. Processed data is in the public domain.
