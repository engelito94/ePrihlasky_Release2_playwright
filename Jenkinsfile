pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    parameters {
        choice(
            name: 'RUN_MODE',
            choices: ['suite', 'single'],
            description: 'suite = spusti marker, single = spusti jeden konkretny test'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['regres1kolo', 'regres2kolo'],
            description: 'Vyber, ktory regresny marker sa ma spustit'
        )
        string(
            name: 'TEST_FILTER',
            defaultValue: '',
            description: 'Pri RUN_MODE=single zadaj presny nodeid testu alebo -k filter, napr. tests\\subor.py::test_nazov'
        )
        choice(
            name: 'SINGLE_MODE',
            choices: ['nodeid', 'kexpr'],
            description: 'nodeid = presna cesta k testu, kexpr = pytest -k filter'
        )
        string(
            name: 'EPRIHLASKY_TEST_URL_PARAM',
            defaultValue: 'https://test-eprihlasky.iedu.sk/',
            description: 'Cielova URL pre testy'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Spustit testy headless'
        )
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
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    script {
                        def pytestTarget = ""
                        def pytestSelector = ""

                        if (params.RUN_MODE == 'single') {
                            if (!params.TEST_FILTER?.trim()) {
                                error("RUN_MODE=single, ale TEST_FILTER je prazdny.")
                            }

                            if (params.SINGLE_MODE == 'nodeid') {
                                pytestTarget = params.TEST_FILTER.trim()
                            } else {
                                pytestSelector = "-k \"${params.TEST_FILTER.trim()}\""
                            }
                        } else {
                            pytestSelector = "-m \"${params.TEST_SUITE}\""
                        }

                        bat """
if exist reports\\screenshots rmdir /s /q reports\\screenshots
if not exist reports mkdir reports
if not exist reports\\screenshots mkdir reports\\screenshots

set EPRIHLASKY_TEST_URL=${params.EPRIHLASKY_TEST_URL_PARAM}
set HEADLESS=${params.HEADLESS}
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

.venv\\Scripts\\pytest ${pytestTarget} ${pytestSelector} --screenshot=only-on-failure --full-page-screenshot --junitxml=reports\\junit.xml
"""
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
        }
    }
}