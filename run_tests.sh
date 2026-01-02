#!/bin/bash
# Run tests in parallel
pytest -n 2
# Generate Allure HTML report
allure generate allure-results --clean -o allure-report
echo "Allure report generated at ./allure-report"