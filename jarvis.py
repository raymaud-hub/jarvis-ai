#!/usr/bin/env python3
"""
JARVIS - AI Assistant (Inspired by Tony Stark)
Your personal AI that remembers everything and helps with tasks.
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
import sys

# Try to import required libraries
try:
    import openai
    from dotenv import load_dotenv
except ImportError:
    print("⚠️  Required packages missing. Run: pip install openai python-dotenv")
    sys.exit(1)

class JARVISMemory:
    """Memory system - stores all queries and actions"""
    
    def __init__(self):
        self.memory_dir = Path.home() / ".jarvis"
        self.memory_dir.mkdir(exist_ok=True)
        self.memory_file = self.memory_dir / "memory.json"
        self.load_memory()
    
    def load_memory(self):
        """Load existing memory from file"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {"queries": [], "tasks": [], "learned_patterns": []}
    
    def save_memory(self):
        """Save memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_query(self, query, response, category="general"):
        """Store a query and response"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "category": category
        }
        self.data["queries"].append(entry)
        self.save_memory()
    
    def recall_similar(self, query):
        """Find similar past queries"""
        results = []
        query_lower = query.lower()
        for q in self.data["queries"]:
            if any(word in q["query"].lower() for word in query_lower.split()):
                results.append(q)
        return results[-5:] if results else []

class JARVIS:
    """Main JARVIS Assistant"""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("❌ OPENAI_API_KEY not found in .env file")
            print("📝 Create a .env file with: OPENAI_API_KEY=your_key_here")
            sys.exit(1)
        
        openai.api_key = self.api_key
        self.memory = JARVISMemory()
        self.model = "gpt-3.5-turbo"
    
    def think(self, prompt):
        """Process user request with AI"""
        try:
            similar = self.memory.recall_similar(prompt)
            context = ""
            if similar:
                context = "\n\nPrevious similar queries:\n"
                for s in similar:
                    context += f"- {s['query']}\n  Response: {s['response'][:100]}...\n"
            
            enhanced_prompt = f"""You are JARVIS, an intelligent AI assistant inspired by Tony Stark's AI.
You are helpful, witty, and remember previous interactions.
{context}

User request: {prompt}

Provide a helpful, concise response."""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": enhanced_prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            self.memory.add_query(prompt, answer)
            return answer
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def show_status(self):
        """Show JARVIS status"""
        total_queries = len(self.memory.data["queries"])
        print(f"""
╔══════════════════════════════════════╗
║     JARVIS - AI ASSISTANT ACTIVE     ║
╚══════════════════════════════════════╝
🧠 Total queries remembered: {total_queries}
📁 Memory location: {self.memory.memory_file}
🤖 Model: {self.model}
✅ Status: Ready to assist
        """)
    
    def interactive_mode(self):
        """Interactive chat mode"""
        self.show_status()
        print("Type 'help' for commands, 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    print("JARVIS: Goodbye, sir. Until next time.")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                
                elif user_input.lower() == 'memory':
                    print(f"JARVIS: I've remembered {len(self.memory.data['queries'])} interactions.\n")
                
                else:
                    response = self.think(user_input)
                    print(f"JARVIS: {response}\n")
            
            except KeyboardInterrupt:
                print("\nJARVIS: Shutting down.")
                break
    
    def show_help(self):
        """Show available commands"""
        print("""
JARVIS Commands:
  help              - Show this help message
  memory            - Show memory statistics
  exit              - Exit JARVIS
  
Or just ask me anything naturally!
        """)

def main():
    jarvis = JARVIS()
    jarvis.interactive_mode()

if __name__ == "__main__":
    main()
