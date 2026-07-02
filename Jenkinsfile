pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat '''
if not exist .venv (
    python -m venv .venv
)
.venv\\Scripts\\python -m pip install --upgrade pip
.venv\\Scripts\\pip install -r requirements.txt
.venv\\Scripts\\python -m playwright install
'''
            }
        }

        stage('Run tests') {
            steps {
                bat '''
.venv\\Scripts\\pytest -m spravaSkoly --html=reports\\report.html --self-contained-html
'''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
        }
    }
}