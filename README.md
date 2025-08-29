# buzzline-01-case

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)

This project introduces streaming data. 
The Python language includes generators - we'll use this feature to generate some streaming buzzline messages. 
As the code runs, it will continuously update the log file. 
We'll use a consumer to monitor the log file and alert us when a special message is detected. 

## Task 1. Set Up Your Machine & Sign up for GitHub

We practice professional Python. In each course that uses Python, we use a standard set of popular professional tools. 
This course uses advanced tools such as Apache Kafka that requires **Python 3.11**. 
You are encouraged to install and practice with multiple versions. 
If space is an issue, we only need Python 3.11 for this course. 

Follow instructions at [pro-analytics-01](https://github.com/denisecase/pro-analytics-01), **Part 1: Set Up Machine & Sign up for GitHub**.

**Setup is critical.** Follow all steps exactly and verify success before proceeding.  
Missing or incomplete setup steps can make the course impossible to complete.

## Task 2. Initialize a Project

Once your machine is ready, you'll copy this template repository into your own GitHub account  
and create your personal version of the project to run and explore. 
Name it **buzzline-01-yourname** (replace `yourname` with something unique to you).  

Follow instructions at [pro-analytics-01](https://github.com/denisecase/pro-analytics-01), **Part 2: Initialize a Project**.
This will get your project stored safely in the cloud - and ready for work on your machine. 

## Task 3. Generate Streaming Data (Terminal 1)

Now we'll generate some streaming data. 
By the way - you've done 90% of the hard work before we even look at code. 
Congratulations!

In VS Code, open a terminal.
Use the commands below to activate .venv, and run the generator as a module. 
To learn more about why we run our Python file as a module, see [PYTHON-PKG-IMPORTS](docs/PYTHON-PKG-IMPORTS.md) 

Windows PowerShell:

```shell
.venv\Scripts\activate
py -m producers.basic_producer_case
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m producers.basic_producer_case
```

## Task 4. Monitor an Active Log File (Terminal 2)

A common streaming task is monitoring a log file as it is being written. 
This project has a consumer that reads and processes our own log file as log messages arrive. 

In VS Code, open a NEW terminal in your root project folder. 
Use the commands below to activate .venv, and run the file as a module. 

Windows:
```shell
.venv\Scripts\activate
py -m consumers.basic_consumer_case
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m consumers.basic_consumer_case
```

## Task 5. Run the Pokémon Producer & Consumer

## Real-Time Analytics: Rolling Average of Message Length  (PART A)

The custom consumer performs a simple real-time analytic: a **rolling average of the message payload length (in characters)**. This provides a quick, noise-reduced signal about how the shape/size of messages is changing over time.

### What it does
- Tails `logs/project_log.log` as new lines are written by the producer.
- Extracts only the **payload** (text after the `" - "` separator added by the logger), so timestamps and levels don’t skew measurements.
- Maintains a fixed-size window (default: last **20** messages) of payload lengths.
- Reports the **rolling average** every **5** messages to reduce console noise.

You will see output lines such as:

2025-08-29 17:49:14.793 | INFO     | __main__:process_stream:67 - Rolling avg payload length (last 20): 56.2 chars

2025-08-29 17:49:26.796 | INFO     | __main__:process_stream:67 - Rolling avg payload length (last 20): 56.6 chars

### Why it’s useful
- **Smoother than a single reading:** A rolling average dampens random spikes and highlights trends.
- **Early drift detection:** If templates grow longer (e.g., added fields or richer text), the average rises; if messages become shorter or malformed, it drops.
- **Lightweight health check:** Gives immediate feedback that the stream is active and consistent without heavy metrics infrastructure.

### How to tune it
Open your custom consumer (e.g., `consumers/basic_consumer_pokemon.py`) and adjust the window size and reporting cadence:
```python
# Default values shown here; increase/decrease as needed
process_stream(str(log_file_path), window_size=20, report_every=5)
```

### Real-Time Alerts: Keyword/Pattern Matches (PART B)

The custom consumer also raises warnings when certain keywords appear in the message payload. By default, the alerts trigger on:
- **"Hyper Beam"**
- **"evolved"**

These matches are **case-insensitive** and tolerate minor spacing (for example, “HyperBeam” also triggers).

**Why this is useful**
- Highlights **business-significant events** immediately without heavy tooling.
- Complements the rolling average by surfacing **discrete signals** (e.g., evolutions or powerful moves).
- Easy to extend as your message schema evolves.

**How to customize**
Open `consumers/basic_consumer_pokemon.py` and edit the `KEYWORD_PATTERNS` list to add, remove, or adjust regular expressions:
```python
KEYWORD_PATTERNS = [
    re.compile(r"\bhyper\s*beam\b", re.IGNORECASE),
    re.compile(r"\bevolved\b", re.IGNORECASE),
    # re.compile(r"\bshiny\b", re.IGNORECASE),  # example
]
```


Windows: Terminal 1 (Producer)
```shell
.venv\Scripts\activate
py -m producers.basic_producer_pokemon
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m producers.basic_producer_pokemon
```

---

Windows: Terminal 2 (Consumer)
```shell
.venv\Scripts\activate
py -m consumers.basic_consumer_pokemon
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m consumers.basic_consumer_pokemon
```

## Save Space
To save disk space, you can delete the .venv folder when not actively working on this project.
We can always recreate it, activate it, and reinstall the necessary packages later. 
Managing Python virtual environments is a necessary and valuable skill. 
We will get a good amount of practice. 

## License
This project is licensed under the MIT License as an example project. 
You are encouraged to fork, copy, explore, and modify the code as you like. 
See the [LICENSE](LICENSE.txt) file for more.
