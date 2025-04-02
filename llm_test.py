# This script runs the generate_response function with test data
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the generate_response function
from smp.generate_response import generate_response

def main():
    # Test data - example game actions
    actions_for_chat = [
        "GAME ENGINE [self.run]: Best Action = 62 roll",
        "GAME ENGINE [self.run]: Instruction given by the model = ()",
        "GAME ENGINE [self.run]: Action is valid",
        "GAME ENGINE [self.run]: Calls roll with no parameters"
    ]
    
    # Format the actions as a string
    formatted_actions = "\n".join(actions_for_chat)
    
    print("Sending actions to generate_response:")
    print(formatted_actions)
    print("-" * 50)
    
    # Call the generate_response function
    generate_response(formatted_actions)

if __name__ == "__main__":
    main()