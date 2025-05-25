// Jenkinsfile Otimizado
pipeline {
    agent {
        docker {
            image 'python:3.10-slim-buster'
            // Adiciona um volume para o cache do pip.
            // 'pip_cache' será um volume Docker gerenciado no host onde o agente roda.
            // Como estamos usando '-u root', o diretório de cache do pip para root é /root/.cache/pip
            args '-u root -v pip_cache:/root/.cache/pip'
        }
    }

    environment {
        VENV_DIR = 'venv'
        PATH = "${VENV_DIR}/bin:${env.PATH}"
        PYTHONPATH = '.'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Clonando o repositório (shallow clone)...'
                // Modificado para fazer um shallow clone (profundidade 1)
                checkout([
                    $class: 'GitSCM',
                    branches: scm.branches,
                    doGenerateSubmoduleConfigurations: scm.doGenerateSubmoduleConfigurations,
                    extensions: [[$class: 'CloneOption', depth: 1, noTags: true, shallow: true, timeout: 20]], // Shallow clone com timeout
                    userRemoteConfigs: scm.userRemoteConfigs
                ])
            }
        }

        stage('Setup Environment and Install Dependencies') {
            steps {
                echo 'Criando ambiente virtual e instalando dependências (usando cache do pip)...'
                sh 'python -m venv $VENV_DIR'
                // Removido --no-cache-dir para permitir que o pip use o cache montado
                sh "pip install -r requirements.txt" //
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Rodando testes com pytest (com paralelização)...'
                // Adicionado -n auto para paralelização com pytest-xdist
                // Certifique-se de adicionar 'pytest-xdist' ao seu requirements.txt
                sh 'pytest -vs --junitxml=test-results.xml -n auto'
            }
        }
    }

    post {
        always {
            echo 'Publicando resultados de testes...'
            junit 'test-results.xml'
        }
        success {
            echo '✅ Pipeline concluído com SUCESSO. Testes passaram.'
        }
        failure {
            echo '❌ Pipeline falhou. Testes NÃO passaram.'
        }
        unstable {
            echo '⚠️ Pipeline instável. Houve falhas em testes.'
        }
    }
}