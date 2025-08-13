# Meal Planner GraphRAG

## Overview

This repository showcases the implementation of a **GraphRAG** (Graph-based Retriever-Augmented Generation) meal planning assistant. 
The project leverages a **Neo4j graph database**, **semantic search**, and **LLM-driven reasoning** to generate personalized recipe recommendations and shopping lists based on user preferences and dietary needs.

## Architecture
![Architecture](docs/images/architecture.png)

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- OpenAI API key (for LLM features)
- Neo4j (runs in Docker)

### Setup

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd meal-planner-graphrag
   ```

2. **Configure environment variables:**
  - Example environment files are provided as `.env.example` and `.env-docker.example` in the `app/` directory, and `.env.neo4j.example` in the `neo4j/` directory.
  - To configure your environment:
    1. Copy the example files to their active counterparts:
      ```sh
      cp app/.env.example app/.env
      cp app/.env-docker.example app/.env-docker
      cp neo4j/.env-docker.example neo4j/.env-docker
      ```
    2. Edit these files to set your API keys, database credentials, Neo4j settings, and other configuration as needed.
  - These files are required for both local development and Docker-based deployment.


3. **Start Neo4j and the app:**
   ```sh
   docker-compose up --build
   ```

4. **Access the application:**
   - The app will be available at `http://localhost:8501`
   - The neo4j database will be available at `http://localhost:7474`

### Development

- Main application logic is in [`app/app.py`](app/app.py).
- Prompts and LLM logic are in [`app/core/prompts.py`](app/core/prompts.py).
- Evaluation tools are in [`evaluation/`](evaluation/).

## Evaluation

- Use [`evaluation/eval.ipynb`](evaluation/eval.ipynb) to assess the quality of generated research plans and retrieval outputs.