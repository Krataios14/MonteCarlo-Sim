# MonteCarlo-Sim

To use the Monte Carlo simulation, follow these steps:

---

## Installation

1. **Download the Source Code**:
   - Clone the repository or download the ZIP file and extract it to your desired location.

2. **Install Python and PIP**:
   - **Python**: Download and install Python from the [official website](https://www.python.org/downloads/).
     - Ensure Python is added to your system's PATH.
   - **PIP**: PIP usually comes installed with Python 3.4 and above. You can verify by running:
     ```bash
     pip --version
     ```
     - If PIP is not installed, follow the instructions [here](https://pip.pypa.io/en/stable/installation/).



## Running the Simulation

Open your terminal or command prompt, navigate to the project directory, and run:

For **Python 2**:
```bash
python main.py
```
For **Python 3**:
```bash
python3 main.py
```

## Config
All config options for the angle simulation are in the `angles.py`.

Open `angles.py` in a text editor to adjust simulation params:

- `num_simulations`: Number of simulations to run.
- `h_min`, `h_max`: Bounds for h
- `o_min`, `o_max`: Bounds for o

All config options for coin monte-carlo are available in the `config.py`.

Open `config.py` in a text editor to adjust simulation params:

- `num_simulations`: Number of simulations to run.
- `W`, `H`: Width and height of the simulation area.
- `N_slots`: Number of slots in the simulation.
- `slot_w`: Width of each slot.
- `R`: Radius of the coin.
- `S`: Number of sides to approximate the coin.
- `R_P`: % of the coin that has to be over the slot to fall in


