# loglit

Lightweight logging for Python. One import, no boilerplate.

## The idea

You already know `print()`. Now use `log()` to write to a file, or `printlog()` to write to console **and** file. 

```
  print  →  console only
+ log    →  file only
= printlog → console + file
```

That's it.

**Without loglit** — the standard way:

```python
import logging
import os
from datetime import datetime

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%d-%m-%Y %H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(
    os.path.join(log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("Hello World")
```

**With loglit:**

```python
from loglit import log, printlog

printlog("Hello World")
```

Same result. Zero setup.

## When to use loglit

- Small scripts, bots, automation
- Quick prototyping and debugging
- Projects where setup should be zero

## When NOT to use loglit

- Large applications with multiple modules and a central logger
- Complex logging pipelines (filtering, routing, multiple sinks)
- Centralized logging systems (ELK, Datadog, etc.)

For those cases, use Python's built-in `logging` module directly.

## Installation

```bash
pip install loglit
```

## Usage

```python
from loglit import log, printlog

log("Only written to the log file.")
printlog("Written to console and log file.")
```

- `log()` → writes to log file only (silent)
- `printlog()` → writes to console **and** log file

Log files are created automatically with a timestamp per session.

## Configure (optional)

Call `configure()` before the first `log()` or `printlog()` to customize behavior:

```python
import logging
from loglit import configure, log, printlog

configure(
    log_dir="my_logs",           # where log files are stored (default: loglit/logs/)
    file_prefix="myapp_",        # filename prefix (default: loglit_)
    file_suffix="_debug",        # filename suffix before extension (default: "")
    file_extension="txt",        # file extension (default: log)
    log_format="%(asctime)s [%(levelname)s] %(message)s",
    date_format="%Y-%m-%d %H:%M:%S",
    log_level=logging.DEBUG,
    encoding="utf-8",
)

log("Only in file.", level=logging.DEBUG)
printlog("App started.")
printlog("Disk almost full.", level=logging.WARNING)
```

| Option | Default | Description |
|---|---|---|
| `log_dir` | `loglit/logs/` | Directory for log files |
| `file_prefix` | `loglit_` | Filename prefix |
| `file_suffix` | `""` | Filename suffix (before extension) |
| `file_extension` | `log` | File extension |
| `file_timestamp` | `%d-%m-%Y_%H-%M-%S` | Timestamp format in filename |
| `log_format` | `%(asctime)s - %(message)s` | Log line format |
| `date_format` | `%d-%m-%Y %H:%M:%S` | Timestamp format in log lines |
| `log_level` | `logging.DEBUG` | Minimum log level |
| `encoding` | `utf-8` | Log file encoding |

Log files are named automatically, e.g. `myapp_07-04-2026_14-32-01_debug.txt`.

## Workflow

Building a new function? Use `printlog()` — see what's happening live in your console while everything gets saved to the log file.

Function runs stable? Switch to `log()` — keeps your console clean, the log file still catches everything silently.

Quick debugging? Just use `print()` — throw it in, check your loop counter, remove it when you're done.

```python
printlog("Connecting to API...")       # developing — I want to see this
log("Connecting to API...")            # stable — just save it quietly
print("i =", i)                        # debugging — temporary, delete later
```

One word changes. No extra imports, no handler setup, no config files. Just swap the function name and move on.

## Configuration

Configuration is optional. Only call `configure()` if you want to change something:

```python
from loglit import configure, log

configure(log_dir="my_logs", file_prefix="myapp_", file_extension="txt")

log("Done.")
# → Log file: my_logs/myapp_22-03-2026_12-00-00.txt
```

The filename is built from these parts:

```
{file_prefix}{file_timestamp}{file_suffix}.{file_extension}
 myapp_       22-03-2026_12-00-00              .txt
```

All options with their defaults:

| Option             | Default                     | Description                       |
|--------------------|-----------------------------|-----------------------------------|
| `log_dir`          | `loglit/logs/`              | Directory for log files           |
| `encoding`         | `utf-8`                     | Log file encoding                 |
| `log_level`        | `logging.DEBUG`             | Minimum log level                 |
| `log_format`       | `%(asctime)s - %(message)s` | Log line format                   |
| `date_format`      | `%d-%m-%Y %H:%M:%S`        | Timestamp format in log lines     |
| `file_prefix`      | `loglit_`                   | Filename prefix                   |
| `file_suffix`      | `""`                        | Filename suffix (after timestamp) |
| `file_extension`   | `log`                       | File extension                    |
| `file_timestamp`   | `%d-%m-%Y_%H-%M-%S`        | Timestamp format in filename      |

## Log Levels

Standard Python log levels work out of the box:

```python
import logging
from loglit import log, printlog

log("Debug info", level=logging.DEBUG)           # file only
printlog("Something happened", level=logging.INFO)  # file + console
printlog("Watch out", level=logging.WARNING)         # file + console
printlog("Something broke", level=logging.ERROR)     # file + console
```

## Examples

See the [examples/](examples/) folder for ready-to-run scripts:

- [basic.py](examples/basic.py) — minimal usage, no configuration
- [configured.py](examples/configured.py) — all options customized

## License

[MIT](LICENSE)

---

**Author:** FMJ
