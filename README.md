# GGJ Game Repository

## Development Instructions

This game is developed with PyGame and Utilizing a Virtual Environment to standardize dependencies. the Pip package manager for python or another widely-used package manager will be needed for this.
### Windows:

Step 1: Installation

`pip install virtualenv`

Step 2: Initializing the virtual environment

`virtualenv venv`

or

`python -m venv venv`

Step 3: Activating the Virtual Environment

`venv\scripts\activate`

Step 4: Installing Required Dependencies

`pip install pygame==2.6.1 pyinstaller==6.11.1 flake8==7.1.1 pre-commit==4.0.1`

`pre-commit install`

Step 5 Deactivating the Virtual Environment

`deactivate`

### Mac/Linux:

Step 1: Installation

`pip install virtualenv`

Step 2: Initializing the virtual environment

`virtualenv venv`

or

`python -m venv venv`

Step 3: Activating the Virtual Environment

`source venv/bin/activate`

Step 4: Installing Required Dependencies

`pip install pygame==2.6.1 pyinstaller==6.11.1 pre-commit==4.0.1`
`pre-commit install`

Step 5: Deactivating the Virtual Environment

`deactivate`

---

## Build Instructions

To build the game executable:

1. Ensure you are in the `GameLib` directory:
   ```bash
   cd GameLib
   ```

2. Run the following command to create a standalone executable:
   ```bash
   pyinstaller --onefile --add-data "ball.png;." main.py
   ```

The built executable can be found in the `dist` directory. Copy all necessary files (like `ball.png`) to the same folder as the executable if needed for the game to function properly.