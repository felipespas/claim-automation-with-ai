# Step 1: Install the necessary tools
# You can install these tools from their respective websites or via package managers like pip (for Python) or brew (for Azure Functions Core Tools and Azure CLI).

# Step 2: Create a new Azure Functions project
# Still in the terminal, run:
func init func-sinistro --python

# Then, navigate to the project directory
cd func-sinistro

# Step 3: Create a virtual environment for Python
# Open a terminal and navigate to the directory where you want to create the project. Then run:

python3 -m venv .venv

# Then, activate the virtual environment
.\.venv\Scripts\activate

# install the requirements
pip install -r .\requirements.txt

# Step 4: Add a new function to the project
# Still in the terminal, run the command below
# and remember to choose function as the auth
func new --name gettext --template "HTTP trigger" --authlevel "function"

# Now add the second function
func new --name removehtml --template "HTTP trigger" --authlevel "function"

# Step 5: Test the function locally
# Run the function locally with:
func start