"""
AI Guide Creator - An AI-powered guide creation system using CrewAI

This package provides a complete solution for generating comprehensive guides
on any topic using AI agents with observability through Arize Phoenix.
"""

__version__ = "1.0.0"
__author__ = "AI Guide Creator"
__email__ = "contact@example.com"

from .main import kickoff, plot
from .phoenix_config import setup_phoenix_observability, cleanup_phoenix

__all__ = [
    "kickoff",
    "plot", 
    "setup_phoenix_observability",
    "cleanup_phoenix",
]
