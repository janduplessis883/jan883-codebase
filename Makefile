install:
	@python -m pip install --upgrade pip
	@pip install -e .
	@echo "🌵 pip install -e . completed!"

clean:
	@rm -f */version.txt
	@rm -f .DS_Store
	@rm -f .coverage
	@rm -rf */.ipynb_checkpoints
	@rm -Rf build
	@rm -Rf */__pycache__
	@rm -Rf */*.pyc
	@echo "🧽 Cleaned up successfully!"

all: install clean

app:
	@streamlit run src/researchcrew_ai/streamlit_app.py

research:
	@python src/researchcrew_ai/research_eoi.py

git_merge:
	$(MAKE) clean
	@python src/researchcrew_ai/automation/git_merge.py
	@echo "👍 Git Merge (master) successfull!"

git_push:
	$(MAKE) clean
	@python src/researchcrew_ai/automation/git_push.py
	@echo "👍 Git Push (branch) successfull!"

test:
	@pytest -v tests

# Specify package name
lint:
	@black src/researchcrew_ai/