import os
import json
import argparse

# Define keys to be removed from JSON files during compaction
KEYS_TO_STRIP = ["description", "purpose", "date", "properties", "promotion_criteria", "approval_process", "usage", "id", "trigger"]

def compact_json_recursively(data):
    """
    Recursively strips specified keys from a dictionary or list.
    """
    if isinstance(data, dict):
        # Create a new dictionary with only the desired keys
        new_dict = {}
        for key, value in data.items():
            if key not in KEYS_TO_STRIP:
                new_dict[key] = compact_json_recursively(value)
        return new_dict
    elif isinstance(data, list):
        # Recursively process each item in the list
        return [compact_json_recursively(item) for item in data]
    else:
        # Return the value as is if it's not a dict or list
        return data

def compact_directive_txt(file_path):
    """
    Compacts a .txt directive file by extracting core commands.
    - Converts lines to uppercase
    - Replaces spaces with underscores
    - Strips leading/trailing whitespace
    - Ignores comments and empty lines
    """
    compacted_lines = []
    with open(file_path, 'r') as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith("#"):
                continue
            
            # Heuristic to identify actionable lines (those starting with a number or specific keywords)
            if stripped_line.split('.')[0].isdigit() or any(keyword in stripped_line for keyword in ["MANDATORY", "ALWAYS", "FIRST", "DON'T", "STOP"]):
                # Further process the line to make it more compact
                processed_line = stripped_line.replace(":", "").replace("-", "").strip()
                compacted_lines.append(processed_line)
    return compacted_lines

def main():
    """
    Main function to compile the framework rules.
    """
    parser = argparse.ArgumentParser(description="Compile human-readable AI-MCP framework rules into a compact, machine-optimized format.")
    parser.add_argument("--output", default="framework/autopilot-rules.json", help="Path to save the compiled autopilot ruleset.")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    framework_dir = os.path.join(project_root, "framework")
    output_path = os.path.join(project_root, args.output)

    if not os.path.isdir(framework_dir):
        print(f"Error: Framework directory not found at {framework_dir}")
        return

    compiled_rules = {}

    print(f"Reading source rules from: {framework_dir}")

    for filename in os.listdir(framework_dir):
        file_path = os.path.join(framework_dir, filename)
        rule_name = os.path.splitext(filename)[0].replace("-v2", "").replace("-", "_")

        if filename.endswith(".json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # The top-level key in the JSON is usually the most important one
                    if len(data) == 1:
                        key = list(data.keys())[0]
                        compacted_data = compact_json_recursively(data[key])
                        compiled_rules[key] = compacted_data
                    else:
                        # Fallback for unexpected JSON structure
                        compiled_rules[rule_name] = compact_json_recursively(data)
                print(f"  - Compiled JSON: {filename}")
            except json.JSONDecodeError as e:
                print(f"\n\nError decoding JSON from file: {filename}")
                print(f"Error: {e}\n\n")
                raise

        elif filename.endswith(".txt"):
            compiled_rules[rule_name] = compact_directive_txt(file_path)
            print(f"  - Compiled TXT: {filename}")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(compiled_rules, f, indent=2)

    print(f"\nSuccessfully compiled framework rules to: {output_path}")
    print(f"Original file count: {len(os.listdir(framework_dir))}, Compiled rule sets: {len(compiled_rules)}")

if __name__ == "__main__":
    main()
