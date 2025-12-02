pipeline {

    agent any

    stages{
        stage('Build'){

            steps {
                echo 'Building...'
                sh "python3 --version"
                sh "pip3 --version"
                sh '''
                   python3 -m venv venv
                   . venv/bin/activate
                   pip install -r requirements.txt
                   ls
                   '''

            }
        }

        stage('Teste'){

            steps {
                echo 'Testando'
                sh '''
                   export PYTHONPATH=$PYTHONPATH:$(pwd)/src
                   ./venv/bin/pytest -v
                   '''

            }
        }

        stage('Testar WebApp'){

            steps {
                echo 'Testando conexão com WebApp, PostgreSQL e Redis...'
                sh '''
                   curl -f http://webapp:5000/health || exit 1
                   echo " WebApp respondendo!"
                '''
                
            }
        }

        stage('Endpoints'){

            steps {
                echo 'Testando endpoints da API...'
                sh '''
                   echo "=== Testando Switch Case 1: Basic Info ==="
                   curl -f http://webapp:5000/api/basic-info || echo "Endpoint não encontrado"
                   
                   echo "\n=== Testando Switch Case 2: Species Count ==="
                   curl -f http://webapp:5000/api/species-count || echo "Endpoint não encontrado"
                   
                   echo "\n=== Testando Switch Case 3: Size Statistics ==="
                   curl -f http://webapp:5000/api/size-statistics || echo "Endpoint não encontrado"
                   
                   echo "\n=== Testando Switch Case 4: Weight Statistics ==="
                   curl -f http://webapp:5000/api/weight-statistics || echo "Endpoint não encontrado"
                   
                   echo "\n=== Testando Switch Case 5: Habitat Distribution ==="
                   curl -f http://webapp:5000/api/habitat-distribution || echo "Endpoint não encontrado"
                   
                   echo "\n=== Testando Switch Case 6: Conservation Status ==="
                   curl -f http://webapp:5000/api/conservation-status || echo "Endpoint não encontrado"
                   
                   echo "\n=== Testando Cache Redis ==="
                   curl -f http://webapp:5000/api/basic-info || echo "Testando cache..."
                   curl -f http://webapp:5000/api/basic-info || echo "Cache funcionando"
                '''
                
            }
        }

        stage('Send Notification') {
            steps {
                echo 'Enviando notificação de conclusão...'
                
                sh '''
                    cd scripts
                    python3 send_email.py
                '''
            }
        }

    }
    
}
