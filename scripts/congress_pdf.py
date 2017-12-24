import click
import pandas as pd
from scrubbing import *

@click.command()
@click.argument('infiles', nargs=-4)
@click.argument('year', type=int)
@click.argument('resultsfile')
@click.argument('totalsfile')
@click.option('--states', 'statesfile', help='Newline-separated file with list of states.', default='states.txt')
def parse(infiles, year, resultsfile, totalsfile, statesfile):
  district_prefix = "DISTRICT"

  # States
  all_states = set([])
  with open(statesfile) as f:
    for row in f:
      if len(row.strip()) > 0:
        all_states.add(row.strip().upper())
  
  state = ""
  lines = []
  for infile in infiles:
    with open(infile) as f:
      for row in f:
        # Find a state first
        if state == "":
          if row.strip() in all_states:
            state = row.strip()
          continue

        data_raw = row.split("  ") # it's a safe bet that columns will be separated by at least 2 spaces
        data = []
        for col in data_raw:
          if len(col.strip()) > 0:
            data.append(col.strip())
        lines.append(data)

  candidates = []
  parties = []
  districts = []
  votes = []
  states = []
  special = []
  runoffs = []
  total_states = []
  total_districts = []
  total_votes = []
  total_special = []
  total_runoff = []
  unexpired = False
  runoff = False
  district = ""
  
  for data in lines:
      if len(data) == 0:
        continue

      for c in data:
        if c in all_states:
          state = c
        elif c.lower().startswith("district"):
          if "columbia" not in (' '.join(data)):
            district = str(strip_int(' '.join(data)))
          else:
            state = "DISTRICT OF COLUMBIA"
            district = ""

      if ' '.join(data) in all_states:
        state = ' '.join(data)
      elif data[0].lower().startswith("unexpired") or data[0].lower().startswith("special"):
        unexpired = True
      elif data[0].lower().startswith("write") or data[0].lower().startswith("none"):
        candidates.append("")
        parties.append(clean_party_name(data[0]))
        votes.append(strip_int(data[1]))
        states.append(state)
        districts.append(district)
        special.append(unexpired)
        runoffs.append(runoff)
      # Some candidates ran under multiple parties.
      # In this case, we use their first party as a label and include the combined vote count.
      elif data[0].lower().startswith("combined parties"):
        votes[-1] = strip_int(data[-2])
      elif data[0].lower().startswith("runoff"):
        runoff = True
      elif "total votes" in ' '.join(data).lower():
        total_states.append(clean(state))
        total_districts.append(district)
        total_votes.append(strip_int(' '.join(data[1:])))
        total_special.append(unexpired)
        total_runoff.append(runoff)
        runoff = False
        unexpired = False

      elif len(data) >= 3 and year == 1992 and not data[0].startswith("CANDIDATE") and strip_int(data[2]) != None:
        candidates.append(data[0])
        parties.append(clean_party_name(data[1]))
        votes.append(strip_int(data[2]))
        states.append(state)
        districts.append(district)
        special.append(unexpired)
        runoffs.append(runoff)

      elif len(data) >= 4 and year < 1992 and not data[0].startswith("Last") and strip_int(data[3]) != None:
        candidates.append(data[0] + ", " + data[1])
        parties.append(clean_party_name(data[2]))
        votes.append(strip_int(data[3]))
        states.append(state)
        districts.append(district)
        special.append(unexpired)
        runoffs.append(runoff)
    # Ignores party names that wrap to next line
  
  # Senate data: no districts
  results_data = {"candidate": candidates, "party": parties, "votes": votes, "year": [year] * len(candidates), "state": states, "special": special, "runoff": runoffs}
  totals_data  = {"year": [year] * len(total_states), "state": total_states, "total_votes": total_votes, "special": total_special, "runoff": total_runoff}
  if district != "":
    results_data['district'] = districts
    totals_data['district'] =  total_districts
  results = pd.DataFrame(results_data)
  totals = pd.DataFrame(totals_data)
  # Validation
  totals_by_state = totals.groupby('state')['total_votes'].sum()
  for state, count in results.groupby('state')['votes'].sum().iteritems():
    if count != totals_by_state[state]:
      print("Warning: data for %s has a numerical inconsistency (%.0f, %.0f)." % (state, count, totals_by_state[state]))
  results.to_csv(resultsfile, index=False)
  totals.to_csv(totalsfile, index=False)
if __name__ == '__main__':
  parse()
