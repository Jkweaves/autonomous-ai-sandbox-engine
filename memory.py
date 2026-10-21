import os
import time
import chromadb

class AgentMemory:
    def __init__(self, storage_directory: str = "./ai_memory"):
        """Initializes a persistent vector database inside your project directory."""
        self.storage_directory = storage_directory
        self.client = chromadb.PersistentClient(path=self.storage_directory)
        self.collection = self.client.get_or_create_collection(name="invented_tools")

    def save_tool(self, tool_name: str, problem_description: str, code_solution: str):
        """Saves an invented code fix or tool layout into long-term memory."""
        print(f"\n[💾 MEMORY DATABASE]: Committing code patch for '{tool_name}' to long-term storage...")
        
        # Generates a clean timestamp ID
        unique_id = f"tool_{int(time.time() * 1000)}"
        
        # ⚠️ CRUCIAL: Make sure all parameters sit inside these single parentheses!
        self.collection.add(
            ids=[unique_id],
            documents=[code_solution],  
            metadatas=[{"tool_name": tool_name, "context": problem_description}]
        )

    def search_memory(self, search_prompt: str, max_results: int = 1):
        """Searches past memory dynamically using structural concept matching."""
        print(f"\n[🔍 MEMORY DATABASE]: Searching past experiences for concepts related to: '{search_prompt}'...")
        return self.collection.query(query_texts=[search_prompt], n_results=max_results)
