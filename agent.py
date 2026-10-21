import os
import time
from openai import OpenAI
from sandbox import CodeSandbox
from memory import AgentMemory  # Imports your local vector database module

class MetaCognitiveAgent:
    def __init__(self):
        # Initializes connection to ChatGPT using your funded Windows environment key
        self.client = OpenAI()
        
        # Connects directly to your functional Docker execution sandbox
        self.sandbox = CodeSandbox()
        
        # Initializes your persistent vector database layer
        self.memory = AgentMemory()

    def get_critic_ai_feedback(self, broken_code: str, error_logs: str, iteration: int) -> str:
        """
        Calls ChatGPT to act as the Critic. It dynamically diagnoses the 
        sandbox crash log and writes a real, unscripted code patch.
        """
        print(f"\n[🧠 REAL CHATGPT CRITIC]: Analyzing failure on loop {iteration}...")
        
        prompt = f"""
        You are a highly advanced Critic Agent in a meta-cognitive execution system.
        The previous code block failed inside an isolated Docker container.
        
        BROKEN CODE SUBMITTED:
        ```python
        {broken_code}
        ```
        
        SANDBOX RUNTIME ERROR ENCOUNTERED:
        {error_logs}
        
        YOUR MISSION:
        Diagnose why the code crashed. Write a brand new, fully functional Python script 
        that resolves the error completely and produces a clean console output.
        Return ONLY valid python source code. Do not include markdown code blocks or talk.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",  # High-performance reasoning model
            messages=[
                {"role": "system", "content": "You are a code generation and debugging engine. Output raw executable python string content only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        corrected_code = response.choices[0].message.content.strip()
        
        # Clean any accidental markdown code blocks if the model includes them
        if corrected_code.startswith("```python"):
            corrected_code = corrected_code.split("```python")[1].split("```")[0].strip()
        elif corrected_code.startswith("```"):
            corrected_code = corrected_code.split("```")[1].split("```")[0].strip()
            
        return corrected_code

    def run_task(self, task_goal: str, initial_code: str, max_attempts: int = 3):
        """Runs the unscripted self-correction loop checking memory layouts first."""
        print("\n====================================================")
        print("🚀 RUNNING LIVE CHATGPT EVO-LOOP WITH LOCAL MEMORY 🚀")
        print("====================================================")
        
        # STEP A: Check Database to see if the AI already solved a similar issue in the past!
                # STEP A: Check Database to see if the AI already solved a similar issue in the past!
        past_results = self.memory.search_memory(task_goal)
        
        # Verify the database returned actual documents before indexing them
        if past_results and "documents" in past_results and past_results["documents"] and len(past_results["documents"][0]) > 0:
            print("\n[💡 MEMORY FLASH]: Found a highly relevant solution in the vector database! Running...")
            past_solution = past_results["documents"][0][0]  # Safely extracts the raw text string
            current_code = past_solution
        else:
            print("\n[❔ DATABASE CHECK]: No past tool matches this criteria. Proceeding with initial file execution.")
            past_solution = None
            current_code = initial_code

        
        # STEP B: Core Evaluation Loop
        for attempt in range(1, max_attempts + 1):
            print(f"\n[🎬 ACTOR AGENT (Attempt {attempt})]: Injecting code string into Sandbox...")
            
            # Execute inside your active Docker platform
            result = self.sandbox.execute(current_code)
            
            if result["success"]:
                print(f"\n[🎉 SYSTEM TRANSCENDED]: Task solved on attempt {attempt}!")
                print(f"[📊 LIVE SANDBOX OUTPUT]:\n{result['output'].strip()}")
                
                # STEP C: Commit to Persistent Memory if it was an unscripted fix
                if not past_solution:
                    self.memory.save_tool(
                        tool_name=task_goal,
                        problem_description=f"Resolved error state: {result['output'].strip()}",
                        code_solution=current_code
                    )
                print("====================================================")
                return True
            else:
                print(f"[❌ SANDBOX RUNTIME ERROR]: Exit Code {result['exit_code']}")
                print(f"[📋 TRAPPED STACK TRACE]:\n{result['output'].strip()}")
                
                if attempt < max_attempts:
                    current_code = self.get_critic_ai_feedback(
                        broken_code=current_code, 
                        error_logs=result["output"], 
                        iteration=attempt
                    )
                else:
                    print("\n[⚠️ SYSTEM FAIL-SAFE]: Maximum loop safety boundaries reached.")
                    print("====================================================")
                    return False

if __name__ == "__main__":
    agent = MetaCognitiveAgent()
    
    # Define our test variables
    task_goal = "Fix math calculation bounds"
    initial_broken_logic = """
def calculate_ratio(val_a, val_b):
    return val_a / val_b

# This will trigger a ZeroDivisionError dynamically in your Docker sandbox!
print(calculate_ratio(100, 0))
"""
    
    # Launch the complete framework
    agent.run_task(task_goal, initial_broken_logic)
