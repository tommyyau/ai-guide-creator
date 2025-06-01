#!/usr/bin/env python
import json
import os
import re
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from guide_creator_flow.crews.content_crew.content_crew import ContentCrew
from guide_creator_flow.phoenix_config import setup_phoenix_observability, cleanup_phoenix

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual .env loading as fallback
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def create_filename(topic: str, audience: str, extension: str = "md") -> str:
    """
    Create a safe filename based on topic and audience.
    
    Args:
        topic: The guide topic
        audience: The target audience level
        extension: File extension (default: md)
        
    Returns:
        A safe filename string
    """
    # Clean the topic string for filename use
    safe_topic = re.sub(r'[^\w\s-]', '', topic.lower())  # Remove special chars
    safe_topic = re.sub(r'[-\s]+', '-', safe_topic)      # Replace spaces/hyphens with single hyphen
    safe_topic = safe_topic.strip('-')                    # Remove leading/trailing hyphens
    
    # Limit length to avoid filesystem issues
    if len(safe_topic) > 50:
        safe_topic = safe_topic[:50].rstrip('-')
    
    # Create filename
    filename = f"{safe_topic}-{audience}-guide.{extension}"
    return filename

# Define our models for structured data
class Section(BaseModel):
    title: str = Field(description="Title of the section")
    description: str = Field(description="Brief description of what the section should cover")

class GuideOutline(BaseModel):
    title: str = Field(description="Title of the guide")
    introduction: str = Field(description="Introduction to the topic")
    target_audience: str = Field(description="Description of the target audience")
    sections: List[Section] = Field(description="List of sections in the guide")
    conclusion: str = Field(description="Conclusion or summary of the guide")

# Define our flow state
class GuideCreatorState(BaseModel):
    topic: str = ""
    audience_level: str = ""
    guide_outline: GuideOutline = None
    sections_content: Dict[str, str] = {}

def clean_section_content(content: str) -> str:
    """Clean the section content to ensure proper markdown formatting"""
    
    # Remove markdown code block wrappers
    content = re.sub(r'^```markdown\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^```\s*\n', '', content, flags=re.MULTILINE)
    
    # Remove meta-comments (lines that start with common meta-comment patterns)
    meta_comment_patterns = [
        r'^This .*section.*maintains.*$',
        r'^This .*version.*enhances.*$', 
        r'^This .*content.*provides.*$',
        r'^This .*improved.*section.*$',
        r'^The .*section.*has been.*$',
        r'^Here.*improved.*version.*$',
        r'^This .*revision.*$'
    ]
    
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        is_meta_comment = False
        for pattern in meta_comment_patterns:
            if re.match(pattern, line.strip(), re.IGNORECASE):
                is_meta_comment = True
                break
        
        if not is_meta_comment:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Ensure the section starts with ## (level 2 heading)
    lines = content.strip().split('\n')
    if lines and lines[0].strip().startswith('# ') and not lines[0].strip().startswith('## '):
        # Convert level 1 heading to level 2
        lines[0] = '#' + lines[0]
    
    # Clean up excessive whitespace
    content = '\n'.join(lines)
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Replace multiple newlines with double newlines
    content = content.strip()
    
    return content

class GuideCreatorFlow(Flow[GuideCreatorState]):
    """Flow for creating a comprehensive guide on any topic"""

    @start()
    def get_user_input(self):
        """Get input from the user about the guide topic and audience"""
        print("\n=== Create Your Comprehensive Guide ===\n")

        # Get user input
        self.state.topic = input("What topic would you like to create a guide for? ")

        # Get audience level with validation
        while True:
            audience = input("Who is your target audience? (beginner/intermediate/advanced) ").lower()
            if audience in ["beginner", "intermediate", "advanced"]:
                self.state.audience_level = audience
                break
            print("Please enter 'beginner', 'intermediate', or 'advanced'")

        print(f"\nCreating a guide on {self.state.topic} for {self.state.audience_level} audience...\n")
        return self.state

    @listen(get_user_input)
    def create_guide_outline(self, state):
        """Create a structured outline for the guide using a direct LLM call"""
        print("Creating guide outline...")

        # Initialize the LLM
        llm = LLM(model="openai/gpt-4o-mini", response_format=GuideOutline)

        # Create the messages for the outline
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"""
            Create a detailed outline for a comprehensive guide on "{state.topic}" for {state.audience_level} level learners.

            The outline should include:
            1. A compelling title for the guide
            2. An introduction to the topic
            3. 4-6 main sections that cover the most important aspects of the topic
            4. A conclusion or summary

            For each section, provide a clear title and a brief description of what it should cover.
            """}
        ]

        # Make the LLM call with JSON response format
        response = llm.call(messages=messages)

        # Parse the JSON response
        outline_dict = json.loads(response)
        self.state.guide_outline = GuideOutline(**outline_dict)

        # Ensure output directory exists before saving
        os.makedirs("output", exist_ok=True)

        # Create dynamic filename for outline
        outline_filename = create_filename(state.topic, state.audience_level, "json")
        outline_path = f"output/{outline_filename.replace('-guide.json', '-outline.json')}"

        # Save the outline to a file with dynamic name
        with open(outline_path, "w") as f:
            json.dump(outline_dict, f, indent=2)

        print(f"Guide outline created with {len(self.state.guide_outline.sections)} sections")
        print(f"Outline saved to: {outline_path}")
        return self.state.guide_outline

    @listen(create_guide_outline)
    def write_and_compile_guide(self, outline):
        """Write all sections and compile the guide"""
        print("Writing guide sections and compiling...")
        completed_sections = []

        # Process sections one by one to maintain context flow
        for section in outline.sections:
            print(f"Processing section: {section.title}")

            # Build context from previous sections
            previous_sections_text = ""
            if completed_sections:
                previous_sections_text = "# Previously Written Sections\n\n"
                for title in completed_sections:
                    previous_sections_text += f"## {title}\n\n"
                    previous_sections_text += self.state.sections_content.get(title, "") + "\n\n"
            else:
                previous_sections_text = "No previous sections written yet."

            # Run the content crew for this section
            result = ContentCrew().crew().kickoff(inputs={
                "section_title": section.title,
                "section_description": section.description,
                "audience_level": self.state.audience_level,
                "previous_sections": previous_sections_text,
                "draft_content": ""
            })

            # Clean the content before storing
            cleaned_content = clean_section_content(result.raw)
            self.state.sections_content[section.title] = cleaned_content
            completed_sections.append(section.title)
            print(f"Section completed: {section.title}")

        # Compile the final guide
        guide_content = f"# {outline.title}\n\n"
        guide_content += f"## Introduction\n\n{outline.introduction}\n\n"

        # Add each section in order
        for section in outline.sections:
            section_content = self.state.sections_content.get(section.title, "")
            guide_content += f"{section_content}\n\n"

        # Add conclusion
        guide_content += f"## Conclusion\n\n{outline.conclusion}\n\n"

        # Create dynamic filename for the guide
        guide_filename = create_filename(self.state.topic, self.state.audience_level)
        guide_path = f"output/{guide_filename}"

        # Save the guide with dynamic filename
        with open(guide_path, "w") as f:
            f.write(guide_content)

        print(f"\nComplete guide compiled and saved to {guide_path}")
        return f"Guide creation completed successfully. File saved as: {guide_path}"

def kickoff():
    """Run the guide creator flow"""
    # Setup Phoenix observability
    phoenix_enabled = setup_phoenix_observability()
    
    try:
        result = GuideCreatorFlow().kickoff()
        print("\n=== Flow Complete ===")
        print("Your comprehensive guide is ready in the output directory.")
        
        if phoenix_enabled:
            print("\n🔍 Check your Phoenix dashboard for observability data:")
            print("   https://app.phoenix.arize.com")
            
    finally:
        # Cleanup Phoenix instrumentation
        if phoenix_enabled:
            cleanup_phoenix()

def plot():
    """Generate a visualization of the flow"""
    flow = GuideCreatorFlow()
    flow.plot("guide_creator_flow")
    print("Flow visualization saved to guide_creator_flow.html")

if __name__ == "__main__":
    kickoff()