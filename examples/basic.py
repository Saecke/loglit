"""Basic usage - no configuration needed."""
from loglit import log, printlog

print("Console only, nothing saved.")       #   print
log("Log file only, nothing printed.")      # + log
printlog("Console + log file.")             # = printlog
