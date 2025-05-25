// meu_projeto_flask/Jenkinsfile
pipeline {
    agent {
        // Define o ambiente de execução como um contêiner Docker com Python 3.10
        docker {
            image 'python:3.10-slim-buster' // Imagem Python leve para agilidade
            args '-u root' // Executa como root no contêiner para evitar problemas de permissão na instalação de libs
        }
    }

    environment {
        // Define uma variável de ambiente para a pasta do ambiente virtual
        VENV_DIR = 'venv'
        // Adiciona a pasta bin do ambiente virtual ao PATH para que os comandos sejam encontrados
        PATH = "${VENV_DIR}/bin:${env.PATH}"
        // Adiciona o diretório de trabalho atual ao PYTHONPATH, garantindo que módulos como 'app.py' sejam encontrados.
        // Isso complementa o pytest.ini.
        PYTHONPATH = '.'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // 'checkout scm' é uma instrução padrão para pipelines multibranch.
                // O Jenkins clonará automaticamente a branch da PR que acionou o build.
                checkout scm
            }
        }

        stage('Setup Environment and Install Dependencies') {
            steps {
                echo 'Criando ambiente virtual e instalando dependências...'
                sh 'python -m venv $VENV_DIR' // Cria o ambiente virtual
                sh 'pip install --no-cache-dir -r requirements.txt' // Instala as dependências do requirements.txt
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Rodando testes com pytest...'
                // Executa os testes. -v para verbose, -s para mostrar print's
                // --junitxml=test-results.xml gera um relatório JUnit para o Jenkins
                sh 'pytest -vs --junitxml=test-results.xml'
            }
        }
    }

    post {
        // Bloco 'always' é executado sempre, independentemente do resultado do stage
        always {
            echo 'Publicando resultados de testes...'
            // Publica os resultados dos testes JUnit para o Jenkins
            // Requer o plugin "JUnit Plugin" instalado no Jenkins
            junit 'test-results.xml'
        }
        // Bloco 'success' é executado se todos os stages passarem
        success {
            echo '✅ Pipeline concluído com SUCESSO. Testes passaram.'
        }
        // Bloco 'failure' é executado se qualquer stage falhar
        failure {
            echo '❌ Pipeline falhou. Testes NÃO passaram.'
        }
        // Bloco 'unstable' é executado se o build for instável (ex: testes falharam, mas o pipeline continuou)
        unstable {
            echo '⚠️ Pipeline instável. Houve falhas em testes.'
        }
    }
}