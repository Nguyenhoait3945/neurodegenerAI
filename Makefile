.PHONY: help setup lint test build up down demo clean install-dev

# Default target
help: ## Show this help message
	@echo "Neuro-Trends Suite - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup development environment
	@echo "Setting up development environment..."
	poetry install
	poetry run pre-commit install
	@echo " Setup complete!"

install-dev: ## Install development dependencies
	poetry install --with dev

lint: ## Run linting (ruff, black, mypy)
	@echo "Running linters..."
	poetry run ruff check .
	poetry run black --check .
	poetry run mypy .
	@echo "Linting complete!"

format: ## Format code (black, ruff)
	@echo "Formatting code..."
	poetry run black .
	poetry run ruff check --fix .
	@echo "Formatting complete!"

test: ## Run tests with coverage
	@echo "Running tests..."
	poetry run pytest
	@echo "Tests complete!"

test-coverage: ## Run tests and generate coverage report
	@echo "Running tests with coverage..."
	poetry run pytest --cov-report=html
	@echo "Coverage report generated in htmlcov/"

build: ## Build Docker images
	@echo "Building Docker images..."
	docker-compose build
	@echo "Docker build complete!"

up: ## Start all services
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Services started!"
	@echo "Neuro UI: http://localhost:8501"
	@echo "Trends UI: http://localhost:8502"
	@echo "Hub UI: http://localhost:8503"

down: ## Stop all services
	@echo "Stopping all services..."
	docker-compose down
	@echo "Services stopped!"

demo: ## Run demo mode (no API keys or data required)
	@echo "Starting demo mode..."
	cp env.example .env
	docker-compose -f docker-compose.yml -f docker-compose.demo.yml up --build
	@echo " Demo mode started!"
	@echo "Neuro UI: http://localhost:8501"
	@echo "Trends UI: http://localhost:8502"
	@echo "Hub UI: http://localhost:8503"

clean: ## Clean up Docker containers and volumes
	@echo "Cleaning up..."
	docker-compose down -v --remove-orphans
	docker system prune -f
	@echo "Cleanup complete!"

logs: ## Show logs from all services
	docker-compose logs -f

logs-neuro: ## Show logs from NeuroDegenerAI services
	docker-compose logs -f neuro-api neuro-ui

logs-trends: ## Show logs from Trend Detector services
	docker-compose logs -f trends-api trends-ui

# Individual service commands
neuro-train: ## Train NeuroDegenerAI models (demo mode)
	cd neurodegenerai && make train_tabular train_mri

neuro-eval: ## Evaluate NeuroDegenerAI models
	cd neurodegenerai && make eval

neuro-api: ## Run NeuroDegenerAI API only
	docker-compose up neuro-api

neuro-ui: ## Run NeuroDegenerAI UI only
	docker-compose up neuro-ui

trends-api: ## Run Trend Detector API only
	docker-compose up trends-api

trends-ui: ## Run Trend Detector UI only
	docker-compose up trends-ui

trends-seed: ## Seed Trend Detector with mock data
	cd trend-detector && make seed_mock

# Development commands
dev-neuro: ## Run NeuroDegenerAI in development mode
	cd neurodegenerai && poetry run streamlit run src/app/streamlit_app.py --server.port 8501

dev-trends: ## Run Trend Detector in development mode
	cd trend-detector && poetry run streamlit run src/app/streamlit_app.py --server.port 8502

dev-hub: ## Run unified hub in development mode
	poetry run streamlit run hub_app.py --server.port 8503

# CI/CD helpers
ci: lint test build ## Run CI pipeline locally
	@echo "CI pipeline complete!"

deploy-check: ## Check deployment readiness
	@echo "Checking deployment readiness..."
	@test -f .env || (echo "❌ .env file missing" && exit 1)
	@echo "Deployment check complete!"

# Documentation
docs: ## Generate documentation
	@echo "Generating documentation..."
	poetry run python -c "import shared; print('Shared library loaded successfully')"
	@echo "Documentation check complete!"

# Database commands
db-reset: ## Reset all databases
	rm -f trend-detector/trends.db
	rm -rf neurodegenerai/models/*
	@echo "Databases reset!"

# Health checks
health: ## Check health of all services
	@echo "Checking service health..."
	@curl -f http://localhost:9001/health || echo "❌ Neuro API not responding"
	@curl -f http://localhost:9002/health || echo "❌ Trends API not responding"
	@echo "Health check complete!"
