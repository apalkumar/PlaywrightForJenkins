pipeline {
    agent any

    tools {
        allure 'allure'   // your global Allure CLI installation name
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/apalkumar/PlaywrightForJenkins.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'playwright install'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest -n auto --alluredir=allure-results'
            }
        }
    }

    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }
    }
}
