import os
import json
import gzip
import argparse
from datetime import datetime
from typing import Dict, List, Any

# Define keys to be removed from JSON files during compaction
KEYS_TO_STRIP = ["description", "purpose", "date", "properties", "promotion_criteria", "approval_process", "usage", "id", "trigger"]

# Ultra-compact mode: Additional keys to strip for maximum compression
ULTRA_STRIP = KEYS_TO_STRIP + ["example", "notes", "comments", "documentation", "details", "explanation"]

# Common phrase dictionary for compression
COMMON_PHRASES = {
    "authenticity_validation": "AV",
    "memory_queries": "MQ", 
    "tool_testing": "TT",
    "session_cache": "SC",
    "user_correction": "UC",
    "verification_markers": "VM",
    "batch_operations": "BO",
    "token_optimization": "TO",
    "emergency_mode": "EM",
    "framework_components": "FC",
    "mcp_servers": "MS",
    "learning_integration": "LI",
    "safety_protocols": "SP",
    "hierarchical_learning": "HL"
}

# Files to exclude from compilation (to avoid recursive compilation)
EXCLUDE_FILES = ["autopilot-rules.json"]

def compact_json_recursively(data, ultra_mode=False, compress_phrases=False):
    """
    Recursively strips specified keys from a dictionary or list with advanced compression.
    """
    strip_keys = ULTRA_STRIP if ultra_mode else KEYS_TO_STRIP
    
    if isinstance(data, dict):
        # Create a new dictionary with only the desired keys
        new_dict = {}
        for key, value in data.items():
            if key not in strip_keys:
                # Compress key names if enabled
                compressed_key = compress_string(key) if compress_phrases else key
                new_dict[compressed_key] = compact_json_recursively(value, ultra_mode, compress_phrases)
        return new_dict
    elif isinstance(data, list):
        # Recursively process each item in the list
        return [compact_json_recursively(item, ultra_mode, compress_phrases) for item in data]
    elif isinstance(data, str) and compress_phrases:
        # Compress common phrases in strings
        return compress_string(data)
    else:
        # Return the value as is if it's not a dict or list
        return data

def compress_string(text: str) -> str:
    """
    Compress common phrases in strings using dictionary substitution.
    """
    compressed = text
    for phrase, abbrev in COMMON_PHRASES.items():
        compressed = compressed.replace(phrase, abbrev)
    return compressed

def decompress_string(text: str) -> str:
    """
    Decompress abbreviated phrases back to original form.
    """
    decompressed = text
    for phrase, abbrev in COMMON_PHRASES.items():
        decompressed = decompressed.replace(abbrev, phrase)
    return decompressed

def create_decompression_mapping() -> Dict[str, str]:
    """
    Create reverse mapping for decompression.
    """
    return {abbrev: phrase for phrase, abbrev in COMMON_PHRASES.items()}

def compact_directive_txt(file_path, ultra_mode=False):
    """
    Compacts a .txt directive file with advanced compression options.
    """
    if ultra_mode:
        # For ultra mode, return the ultra-compact version if it exists
        ultra_compact_path = file_path.replace('.txt', '-ultra-compact.txt')
        if os.path.exists(ultra_compact_path):
            with open(ultra_compact_path, 'r') as f:
                return f.read().strip()
    
    compacted_lines = []
    with open(file_path, 'r') as f:
        content = f.read()
        
    if ultra_mode:
        # Apply aggressive compression
        content = compress_string(content)
        # Remove extra whitespace and consolidate
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        # Keep only essential directive lines
        essential_keywords = ["PHASE", "MANDATORY", "ALWAYS", "NEVER", "TOKEN", "CACHE", "MEMORY", "TOOL", "AUTH"]
        compacted_lines = [line for line in lines if any(keyword in line.upper() for keyword in essential_keywords)]
    else:
        # Original compaction logic
        for line in content.split('\n'):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith("#"):
                continue
            
            if stripped_line.split('.')[0].isdigit() or any(keyword in stripped_line for keyword in ["MANDATORY", "ALWAYS", "FIRST", "DON'T", "STOP"]):
                processed_line = stripped_line.replace(":", "").replace("-", "").strip()
                compacted_lines.append(processed_line)
    
    return '\n'.join(compacted_lines) if ultra_mode else compacted_lines

def validate_compiled_rules(compiled_rules):
    """
    Validates the compiled rules to ensure essential data is preserved.
    """
    validation_errors = []

    # Check for essential components
    essential_components = [
        "prime_directive",
        "authenticity_controls",
        "safety_governance_system"
    ]

    for component in essential_components:
        if component not in compiled_rules:
            validation_errors.append(f"Missing essential component: {component}")

    # Check that prime directive has core commands
    if "prime_directive" in compiled_rules:
        pd = compiled_rules["prime_directive"]
        if not isinstance(pd, list) or len(pd) < 3:
            validation_errors.append("Prime directive appears incomplete")

    return validation_errors

def main():
    """
    Main function to compile the framework rules.
    """
    parser = argparse.ArgumentParser(description="Compile human-readable AI-MCP framework rules into a compact, machine-optimized format.")
    parser.add_argument("--output", default="framework/autopilot-rules.json", help="Path to save the compiled autopilot ruleset.")
    parser.add_argument("--validate", action="store_true", help="Validate compiled rules for completeness.")
    parser.add_argument("--metrics-only", action="store_true", help="Show compression metrics without recompiling.")
    parser.add_argument("--ultra-compact", action="store_true", help="Enable ultra-compact mode for maximum compression.")
    parser.add_argument("--compress-phrases", action="store_true", help="Enable phrase compression using dictionary substitution.")
    parser.add_argument("--gzip", action="store_true", help="Apply gzip compression to output.")
    parser.add_argument("--generate-decompressor", action="store_true", help="Generate decompression utility.")
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

    source_file_sizes = []
    processed_files = []

    for filename in os.listdir(framework_dir):
        # Skip excluded files (like existing autopilot-rules.json)
        if filename in EXCLUDE_FILES:
            continue
        file_path = os.path.join(framework_dir, filename)
        rule_name = os.path.splitext(filename)[0].replace("-v2", "").replace("-", "_")

        if filename.endswith(".json"):
            try:
                file_size = os.path.getsize(file_path)
                source_file_sizes.append(file_size)

                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # The top-level key in the JSON is usually the most important one
                    if len(data) == 1:
                        key = list(data.keys())[0]
                        compacted_data = compact_json_recursively(data[key], args.ultra_compact, args.compress_phrases)
                        compiled_rules[key] = compacted_data
                    else:
                        # Fallback for unexpected JSON structure
                        compiled_rules[rule_name] = compact_json_recursively(data, args.ultra_compact, args.compress_phrases)
                print(f"  - Compiled JSON: {filename} ({file_size:,} bytes)")
                processed_files.append(filename)
            except json.JSONDecodeError as e:
                print(f"\n\nError decoding JSON from file: {filename}")
                print(f"Error: {e}\n\n")
                raise

        elif filename.endswith(".txt"):
            file_size = os.path.getsize(file_path)
            source_file_sizes.append(file_size)

            compiled_rules[rule_name] = compact_directive_txt(file_path, args.ultra_compact)
            print(f"  - Compiled TXT: {filename} ({file_size:,} bytes)")
            processed_files.append(filename)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Add compilation metadata
    compilation_metadata = {
        "_meta": {
            "compiled_at": datetime.now().isoformat(),
            "source_files": processed_files,
            "compilation_version": "1.1",
            "compiler": "AUTOPILOT Framework Compiler"
        }
    }

    # Merge metadata with compiled rules
    final_output = {**compilation_metadata, **compiled_rules}
    
    # Add decompression mapping if phrase compression was used
    if args.compress_phrases:
        final_output["_decompression_map"] = create_decompression_mapping()

    # Write output with optional compression
    if args.gzip:
        output_path_gz = output_path + '.gz'
        with gzip.open(output_path_gz, 'wt') as f:
            json.dump(final_output, f, indent=None, separators=(',', ':'))
        print(f"✅ Gzip compressed output: {output_path_gz}")
        
        # Also create uncompressed version
        with open(output_path, 'w') as f:
            json.dump(final_output, f, indent=2)
    else:
        indent = None if args.ultra_compact else 2
        separators = (',', ':') if args.ultra_compact else (',', ': ')
        with open(output_path, 'w') as f:
            json.dump(final_output, f, indent=indent, separators=separators)

    # Calculate compression metrics
    compiled_size = os.path.getsize(output_path)
    total_source_size = sum(source_file_sizes)
    reduction_percent = ((total_source_size - compiled_size) / total_source_size * 100) if total_source_size > 0 else 0
    
    # Check for gzipped version
    gzip_size = 0
    if args.gzip and os.path.exists(output_path + '.gz'):
        gzip_size = os.path.getsize(output_path + '.gz')

    print(f"\n=== AUTOPILOT Compilation Results ===")
    print(f"✅ Successfully compiled to: {output_path}")
    if args.gzip:
        print(f"✅ Gzip version created: {output_path}.gz")
    print(f"📁 Source files processed: {len(processed_files)}")
    print(f"📊 Source files total size: {total_source_size:,} bytes")
    print(f"📦 Compiled file size: {compiled_size:,} bytes")
    if gzip_size > 0:
        gzip_reduction = ((total_source_size - gzip_size) / total_source_size * 100)
        print(f"🗜️  Gzip compressed size: {gzip_size:,} bytes")
        print(f"🗜️  Total compression: {gzip_reduction:.1f}%")
        print(f"⚡ Gzip compression ratio: {total_source_size/gzip_size:.1f}x")
    if reduction_percent > 0:
        print(f"🗜️  Standard reduction: {reduction_percent:.1f}%")
        print(f"⚡ Standard compression ratio: {total_source_size/compiled_size:.1f}x")
    else:
        print(f"📈 Size increase: {abs(reduction_percent):.1f}% (expected for first compilation)")
    
    # Show optimization features used
    optimizations = []
    if args.ultra_compact:
        optimizations.append("ultra-compact")
    if args.compress_phrases:
        optimizations.append("phrase-compression")
    if args.gzip:
        optimizations.append("gzip")
    
    if optimizations:
        print(f"🚀 Optimizations applied: {', '.join(optimizations)}")
    print(f"🚀 Framework rule sets: {len(compiled_rules)}")
    print(f"\n🎯 AUTOPILOT optimization ready for deployment!")

    # Validation if requested
    if args.validate:
        print(f"\n=== Validation Results ===")
        validation_errors = validate_compiled_rules(compiled_rules)
        if validation_errors:
            print(f"⚠️  Validation warnings:")
            for error in validation_errors:
                print(f"  - {error}")
        else:
            print(f"✅ All essential components validated successfully")

if __name__ == "__main__":
    main()
