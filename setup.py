from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mini-agent",
    version="0.1.0",
    description="Lightweight agentic framework with ReAct, A-MEM memory system, and advanced reasoning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="aixiasang",
    author_email="aixiasang@163.com",
    url="https://github.com/aixiasang/mini-agent",
    packages=["core", "agent", "prompt"],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "httpx>=0.24.0",
        "numpy>=1.20.0",
        "chromadb>=0.4.0",
        "tenacity>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "all": [
            "pillow>=9.0.0",
        ],
    },
    keywords=["agent", "ai", "llm", "react", "reasoning", "memory", "a-mem", "multi-agent"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Source": "https://github.com/aixiasang/mini-agent",
        "Bug Reports": "https://github.com/aixiasang/mini-agent/issues",
        "Documentation": "https://github.com/aixiasang/mini-agent#readme",
    },
)
