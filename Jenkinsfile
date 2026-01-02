pipeline {
    agent any

    tools {
        // Assumes you configured Allure CLI in Jenkins global tools
        allure 'allure'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/your/repo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python and Playwright dependencies..."

                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'playwright install'
            }
        }

        stage('Run Tests in Parallel') {
            steps {
                echo "Running tests in parallel..."
                bat 'pytest -n auto --alluredir=allure-results'
            }
        }

        stage('Generate Allure HTML Report') {
            steps {
                echo "Generating Allure report..."
                bat 'allure generate allure-results --clean -o allure-report'
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                   reportDir: 'allure-report',
                   results: [[path: 'allure-results']]
        }
    }
}
