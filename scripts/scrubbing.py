def strip_int(s):
  stripped = ""
  for c in s:
    if c in "0123456789":
      stripped += c
  try:
    return int(stripped)
  except ValueError:
    return None

def clean(s):
  # Remove any non-alphabetic prefixes/suffixes
  stripped = ""
  first_letter_found = False
  for c in s:
    if c.isalpha():
      first_letter_found = True
    if first_letter_found:
      stripped += c

  pure = ""
  first_letter_found = False
  for c in reversed(stripped):
    if c.isalpha():
      first_letter_found = True
    if first_letter_found:
      pure += c
  # https://stackoverflow.com/questions/28632804/why-strreversed-doesnt-give-me-the-reversed-string
  return ''.join(reversed(pure))

def clean_party_name(s):
  if "write" in s.lower():
    return "Write-In"
  return clean(s)