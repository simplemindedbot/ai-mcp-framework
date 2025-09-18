#!/usr/bin/env python3
"""
Knowledge Graph Importer for AI MCP Framework

This script imports framework components into MCP memory systems.
It can work with different memory server implementations.

Usage:
    python knowledge-graph-importer.py [--source SOURCE] [--memory-server URL]
"""

import json
import argparse
from pathlib import Path

def load_knowledge_graph_export(source_path):
    """Load knowledge graph export from JSON file"""
    with open(source_path, 'r') as f:
        return json.load(f)

def create_memory_entities(knowledge_graph):
    """Convert framework components to memory system entities"""
    entities = []
    
    # Extract entities from knowledge graph
    for component_name, component_data in knowledge_graph.get("components", {}).items():
        entity = {
            "name": component_name.replace("_", " ").title(),
            "type": "framework_component",
            "framework_version": knowledge_graph.get("version", "2.0"),
            "component_data": component_data
        }
        entities.append(entity)
    
    return entities

def create_memory_relations(entities):
    """Create relationships between framework entities"""
    relations = []
    
    # Create hierarchical relationships
    prime_directive = next((e for e in entities if "prime directive" in e["name"].lower()), None)
    
    if prime_directive:
        for entity in entities:
            if entity != prime_directive:
                relation = {
                    "from": prime_directive["name"],
                    "to": entity["name"],
                    "type": "incorporates" if "control" in entity["name"].lower() 
                           else "governed_by" if "safety" in entity["name"].lower()
                           else "enhanced_by"
                }
                relations.append(relation)
    
    return relations

def generate_import_script(entities, relations, memory_server_type="generic"):
    """Generate import script for specific memory server type"""
    
    if memory_server_type == "mcp_memory":
        # Generate MCP memory server import
        import_data = {
            "entities": [
                {
                    "name": entity["name"],
                    "entityType": entity["type"],
                    "observations": [
                        f"Framework component: {entity['name']}",
                        f"Version: {entity['framework_version']}",
                        f"Data: {json.dumps(entity['component_data'])}"
                    ]
                }
                for entity in entities
            ],
            "relations": [
                {
                    "from": rel["from"],
                    "to": rel["to"], 
                    "relationType": rel["type"]
                }
                for rel in relations
            ]
        }
        
        return json.dumps(import_data, indent=2)
    
    else:
        # Generic format
        return json.dumps({
            "entities": entities,
            "relations": relations,
            "import_instructions": [
                "Adapt this data to your memory system format",
                "Ensure hierarchical relationships are preserved",
                "Set Prime Directive as highest priority",
                "Verify all components are accessible after import"
            ]
        }, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Import AI MCP Framework to knowledge graph")
    parser.add_argument("--source", type=Path,
                       default=Path(__file__).parent.parent / "examples" / "knowledge-graph-export.json",
                       help="Source knowledge graph export file")
    parser.add_argument("--output", type=Path,
                       default=Path(__file__).parent.parent / "framework-import.json",
                       help="Output import file")
    parser.add_argument("--memory-server", choices=["mcp_memory", "generic"],
                       default="mcp_memory",
                       help="Target memory server type")
    
    args = parser.parse_args()
    
    print("📥 AI MCP Framework Knowledge Graph Importer")
    print("=" * 50)
    
    # Load source data
    print(f"📖 Loading knowledge graph from: {args.source}")
    knowledge_graph = load_knowledge_graph_export(args.source)
    
    # Create entities and relations
    print("🔧 Processing framework components...")
    entities = create_memory_entities(knowledge_graph)
    relations = create_memory_relations(entities)
    
    print(f"✅ Created {len(entities)} entities and {len(relations)} relations")
    
    # Generate import script
    print(f"🎯 Generating import for {args.memory_server} memory server...")
    import_script = generate_import_script(entities, relations, args.memory_server)
    
    # Save import file
    with open(args.output, 'w') as f:
        f.write(import_script)
    
    print(f"💾 Import file saved to: {args.output}")
    
    # Display next steps
    print("\n📋 Next steps:")
    if args.memory_server == "mcp_memory":
        print("1. Use your MCP memory server's import function with the generated file")
        print("2. Example: memory.import_knowledge_graph('framework-import.json')")
    else:
        print("1. Adapt the generated data to your memory system's format")
        print("2. Import entities and relations preserving hierarchical structure")
    
    print("3. Verify framework components are accessible in your AI system")
    print("4. Test automatic tool usage and authenticity validation")
    
    print("\n🔍 Verification commands:")
    print("- Query for 'Enhanced MCP Server Exploration Prime Directive'")
    print("- Search for 'Self-Audit Questions'")
    print("- Confirm 'Safety Protocols' are accessible")

if __name__ == "__main__":
    main()