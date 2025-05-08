# Shed of Graphs

## Overview
`Shed of Graphs` is a Python tool that filters graphs based on specific edge conditions involving the sum of the degrees of the incident nodes. The tool processes graphs in the graph6 format, applies user-defined filtering rules, and outputs only those that satisfy the conditions. 

### Filter Conditions

The filter operates on graphs with a fixed number of vertices and supports conditions based on edge degree sums. Each rule includes:

* **Vertices**: All graphs are filtered based on a fixed number of vertices, as specified when generating graphs.
* **Degree Sum**: The sum of the degrees of the two nodes at each edge is evaluated.
* **Type**: The condition applied to the number of matching edges. Supported types:

  * **Minimum**: At least a given number of edges must meet the degree sum.
  * **Maximum**: At most a given number of edges may meet the degree sum.
  * **Exactly**: Exactly a given number of edges must meet the degree sum.
* **Count**: The number of edges required to satisfy the condition.

Each graph is tested against all specified rules and is kept only if it satisfies **all** of them.

Additionally, the tool tracks a **history of processed graphs** and stores key metadata like the number of graphs processed, the filter applied, and the 20 most recent passed graphs.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/JitseVDB/ShedOfGraphs
    cd ShedOfGraphs
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Building the `geng` tool from the included `nauty2_8_9` directory manually (required if not using Docker)

```bash
cd graph_processing/nauty2_8_9
./configure
make
cp geng /usr/local/bin  # Or another directory in your PATH
```

## Usage

### Running the Graph Filter

Once you’ve built `geng` and set up the environment, you can filter graphs using the provided shell scripts.

#### Sequential Filtering

Use `run_filter.sh` to generate and filter graphs sequentially:

```bash
./run_filter.sh <n> '<filter_rules>' [--export <folder>] [--image <format>]
```

**Example:**

```bash
./run_filter.sh 6 '[{"degree_sum": 6, "type": "exactly", "count": 4}]' --export ./graph_images --image png
```

This command generates all graphs with 6 nodes and filters them according to the specified rules. Matching graphs can optionally be exported as image files (e.g., png or svg) to the specified folder.

#### Parallel Filtering

To process graphs faster using multiple CPU cores, use the parallel version:

```bash
./run_filter_parallel.sh <n> '<filter_rules>' [--export <folder>] [--image <format>]
```

**Example:**

```bash
./run_filter_parallel.sh 6 '[{"degree_sum": 6, "type": "exactly", "count": 4}]' --export ./graph_images --image png
```

This functions the same as the sequential version but speeds up processing by distributing the workload.

The filtered graph information is logged in `graph_processing/history.txt`.

### Example of `history.txt` Format:

Each line in the `history.txt` file represents a batch of processed graphs:

```
<timestamp>	<inputNumber>	<outputNumber>	<filter>	<passedGraphList>
```

- `<timestamp>`: The time when the batch was processed.
- `<inputNumber>`: The total number of graphs generated.
- `<outputNumber>`: The number of graphs that passed the filter.
- `<filter>`: The filter string applied.
- `<passedGraphList>`: The 20 most recent passed graphs (graph6 strings).

## Setting up Automatic Backups

To set up automatic backups of the history file, follow these steps:

1. Ensure you have `python3` installed and the `backup_history.py` script is located at `/home/ShedOfGraphs/history_backup/backup_history.py`.

2. Add the following cron job to run the backup script every hour:
   ```bash
   crontab -e

Then add this line to the crontab file:

```bash
0 * * * * /usr/bin/python3 /home/ShedOfGraphs/history_backup/backup_history.py
```
### Restoring a Backup of History

If you want to restore a previous version of your `history.txt` file (e.g. after accidentally modifying or deleting it), you can use the `restore_history.py` script.

#### Steps:

1. Open a terminal.
2. Run the script:

   ```bash
   python3 graph_processing/restore_history.py
   ```
3. A list of available backups will be shown (these are located in `~/.filtered-graphs/` and named like `history_YYYYMMDD_HHMM.txt`).
4. Enter the number corresponding to the backup you want to restore.
5. The selected backup will replace the current `history.txt` file in `graph_processing/`.

#### Notes:

* Backups must exist in the `.filtered-graphs` folder for this to work.

### Running the Web Server

To start the web server for your project, you have two options: you can run it directly using Python or use Docker.

#### Option 1: Running with Python

1. Open a terminal.
2. Navigate to the `graph_processing` directory where the `webserver.py` script is located.
3. Run the web server with:

   ```bash
   python3 webserver.py
   ```
4. The web server will start and will be accessible at `http://localhost:5000/index`.

#### Option 2: Running with Docker

If you'd prefer to use Docker, follow these steps:

1. First, build the Docker image:

   ```bash
   docker build -t shed-of-graphs .
   ```
2. Then, run the container:

   ```bash
   docker run -p 5000:5000 shed-of-graphs
   ```
3. The web server will be available at `http://localhost:5000/index`.


### Continuous Integration (CI) Tests
The project includes a CI pipeline (configured via GitHub Actions) to run tests automatically whenever code is pushed to the repository ensuring everything works correctly.
