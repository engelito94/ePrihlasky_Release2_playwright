pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        EPRIHLASKY_RIADITEL = credentials('eprihlasky-riaditel')
        EPRIHLASKY_SEC_RIADITEL = credentials('eprihlasky-sec-riaditel')
        EPRIHLASKY_SPRACOVATEL = credentials('eprihlasky-spracovatel')
        EPRIHLASKY_ADMIN = credentials('eprihlasky-admin')
        EPRIHLASKY_ZZ = credentials('eprihlasky-zz')
        GMAIL_MAIN = credentials('gmail-main')
        GMAIL_SEC = credentials('gmail-sec')
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
if not exist reports mkdir reports

set EPRIHLASKY_TEST_URL=https://test-eprihlasky.iedu.sk/
set EPRIHLASKY_RIADITEL_USERNAME=%EPRIHLASKY_RIADITEL_USR%
set EPRIHLASKY_RIADITEL_PASSWORD=%EPRIHLASKY_RIADITEL_PSW%
set EPRIHLASKY_SEC_RIADITEL_USERNAME=%EPRIHLASKY_SEC_RIADITEL_USR%
set EPRIHLASKY_SEC_RIADITEL_PASSWORD=%EPRIHLASKY_SEC_RIADITEL_PSW%
set EPRIHLASKY_SPRACOVATEL_USERNAME=%EPRIHLASKY_SPRACOVATEL_USR%
set EPRIHLASKY_SPRACOVATEL_PASSWORD=%EPRIHLASKY_SPRACOVATEL_PSW%
set EPRIHLASKY_ADMIN_USERNAME=%EPRIHLASKY_ADMIN_USR%
set EPRIHLASKY_ADMIN_PASSWORD=%EPRIHLASKY_ADMIN_PSW%
set EPRIHLASKY_ZZ_USERNAME=%EPRIHLASKY_ZZ_USR%
set EPRIHLASKY_ZZ_PASSWORD=%EPRIHLASKY_ZZ_PSW%
set GMAIL_USERNAME=%GMAIL_MAIN_USR%
set GMAIL_APP_PASSWORD=%GMAIL_MAIN_PSW%
set GMAIL_SEC_USERNAME=%GMAIL_SEC_USR%
set GMAIL_SEC_APP_PASSWORD=%GMAIL_SEC_PSW%

.venv\\Scripts\\pytest -m spravaSkoly --junitxml=reports\\junit.xml --html=reports\\report.html --self-contained-html
'''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'

            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true

            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Pytest HTML Report',
                reportTitles: 'Pytest Report'
            ])
        }
    }
}