pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage("POR FAVOR FUNCIONA"){
            steps{
                echo 'PFV'
            }
        }
    
        stage('Build'){

            steps {
                
                echo 'Construindo o projeto...'
                bat 'echo "Build concluído."'

            }
        }
        stage('Setup') {
            steps {
                echo 'Configurando ambiente...'
                sh '''
                   docker rm -f projeto_python || true
                   docker run -d --name projeto_python -v $PWD:/app -w /app python:3.9-slim tail -f /dev/null
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Instalando dependências...'
                sh '''
                   docker exec projeto_python pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Executando testes...'
                sh '''
                   docker exec projeto_python pytest test_crocodile_analyzer.py -v --junitxml=test-results.xml --cov --cov-report=html --cov-report=term
                '''
            }
        }

        stage('Archive Results') {
            steps {
                echo 'Arquivando resultados...'
                sh '''
                   docker cp projeto_python:/app/htmlcov ./htmlcov || true
                   docker cp projeto_python:/app/test-results.xml ./test-results.xml || true
                '''
                archiveArtifacts artifacts: 'htmlcov/**', allowEmptyArchive: true
                junit 'test-results.xml'
            }
        }
    }

    post {
        success {
            echo '✅ Testes passaram com sucesso!'
        }
        failure {
            echo '❌ Testes falharam!'
        }
    }
}
