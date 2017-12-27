#!/bin/bash
# To use this script, just type bash fetch_finances.sh in the scripts directory
# Made by InnovativeInventor, MIT license applies

year=1980 # Starting year
current_year=$(date +%Y)

echo "The current year is $current_year"
# If the election data do not exist yet, nothing will be fetched

while [[ $year -lt $current_year ]]; do
    echo "Gathering data for the year $year"
    last_two_digits=${year:(-2)}
    mkdir -p ../raw/$year/compressed

    echo "Getting Committee Master File for $year"
    curl -L ftp://ftp.fec.gov/FEC/$year/cm$last_two_digits.zip -o ../raw/$year/compressed/cn$last_two_digits.zip

    echo "Getting Candidate Master File for $year"
    curl -L ftp://ftp.fec.gov/FEC/$year/cn$last_two_digits.zip -o ../raw/$year/compressed/cn$last_two_digits.zip

    echo "Getting Any Transaction from One Committee to Another for $year"
    curl -L ftp://ftp.fec.gov/FEC/$year/oth$last_two_digits.zip -o ../raw/$year/compressed/oth$last_two_digits.zip

    echo "Getting Contributions to Candidates (and other expenditures) from Committees for $year"
    curl -L ftp://ftp.fec.gov/FEC/$year/pas2$last_two_digits.zip -o ../raw/$year/compressed/pas2$last_two_digits.zip

    echo "Getting Contributions by individuals for $year"
    curl -L ftp://ftp.fec.gov/FEC/$year/indiv$last_two_digits.zip -o ../raw/$year/compressed/indiv_$last_two_digits.zip

    # Only fetching these if they exist
    echo "Getting Candidate Committee Linkage File and Operating Expenditures for $year, if they exist"
    curl -Lf ftp://ftp.fec.gov/FEC/$year/ccl$last_two_digits.zip -o ../raw/$year/compressed/ccl$last_two_digits.zip
    curl -Lf ftp://ftp.fec.gov/FEC/$year/oppexp$last_two_digits.zip -o ../raw/$year/compressed/oppexp$last_two_digits.zip

    unzip "../raw/$year/compressed/*.zip" -d "../raw/$year/"
    ((year+=2))
    echo && echo
done
