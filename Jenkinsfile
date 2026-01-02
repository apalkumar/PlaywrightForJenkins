pipeline {
    agent any

    tools {
        allure 'allure'   // your global Allure CLI installation name
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/apalkumar/PlaywrightForJenkins.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'playwright install'
            }
        }

        stage('Run Tests in parallel') {
            steps {
                bat 'pytest -n auto --alluredir=allure-results'
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'pip --version'
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
