# Shed of Graphs

## Overview
`Shed of Graphs` is a Python tool that filters graphs based on specific edge conditions involving the sum of the degrees of the incident nodes. The tool processes graphs in the graph6 format, applies user-defined filtering rules, and outputs only those that satisfy the conditions. 

### Filter Conditions:
- **Minimum**: At least a given number of edges where the sum of the degrees of the incident nodes is a specific value.
- **Maximum**: At most a given number of edges where the sum of the degrees of the incident nodes is a specific value.
- **Exactly**: Exactly a given number of edges where the sum of the degrees of the incident nodes is a specific value.

Additionally, the tool tracks a **history of processed graphs** and stores key metadata like the number of graphs processed, the filter applied, and the 20 most recent passed graphs.

## Features
- **Graph Filtering**: Filters graphs based on degree-sum edge conditions.
- **Flexible Rules**: Supports rules with `min`, `max`, and `exactly` edge count conditions.
- **History Tracking**: Stores metadata for each filtering session in `history.txt`, including timestamps and processed graphs.
- **Extensible**: The program can be extended to support more complex filtering logic or additional features.

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

## Usage

To use the filter, you can run the provided **Bash script**, `run_filter.sh`, which simplifies the process of generating graphs and filtering them.

### Usage with the `run_filter.sh` script:

The `run_filter.sh` script generates graphs of a specified order and filters them according to the given rules. The filtering history is saved automatically in `history.txt`.

```bash
./run_filter.sh 6 '[{"degree_sum": 6, "type": "min", "count": 3}]'
```
The `run_filter_parallel.sh` script generates graphs of a specified order and filters them according to the given rules. The filtering history is saved automatically in `history.txt`.

```bash
./run_filter_parallel.sh 6 '[{"degree_sum": 6, "type": "exactly", "count": 4}]' --export ./graph_images --image png
```

This command will:
- Generate all graphs with 6 vertices.
- Filter the graphs with at least 3 edges where the sum of the degrees of the incident nodes is 6.
- Print the filtered graph6 strings to the console.
- Save the history of this session, including the timestamp and filter applied, to `history.txt`.

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

## **Setting Up Plantri**

To use the graph generation and filtering scripts in this project, you need to install **Plantri**. Below is a step-by-step guide to set it up.

### **1. Download Plantri**

1. **Visit the Plantri website** or use the following link: [Plantri GitHub or official site](http://www.maths.qmul.ac.uk/~pjc/plantri/).
2. Download the **tar.gz** file for Plantri (e.g., `plantri55.tar.gz`).

### **2. Extract the Files**

Once the **tar.gz** file is downloaded, follow these steps to extract it:

```bash
tar -xzvf plantri55.tar.gz
```

This will extract the contents into a folder named `plantri55`.

### **3. Compile Plantri**

Navigate to the extracted folder and run the `make` command to compile Plantri:

```bash
cd plantri55
make
```

This will generate the `plantri` executable.

### **4. Move Plantri to a Global Directory (Optional)**

If you want to run `plantri` from anywhere on your system, move it to a directory in your `PATH` (e.g., `/usr/local/bin/`):

```bash
sudo mv plantri /usr/local/bin/
```

### **5. Test Plantri**

To verify that Plantri is installed correctly, run:

```bash
plantri
```

This should display the Plantri command-line interface, confirming that it’s working properly.

### **6. Usage Example**

You can now use Plantri to generate graphs. For example, to generate graphs with 6 vertices and the symmetry `res=0 mod=4`, run:

```bash
plantri 6 0 4
```

You can also output the graphs to a file:

```bash
plantri 6 0 4 output.g6
```
