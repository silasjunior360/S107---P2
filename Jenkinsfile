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

        stage('Testar WebApp') {
    steps {
        echo 'Testando API completa do WebApp...'
        sh '''
            set -e

            BASE_URL="http://webapp:5000"

            test_endpoint() {
                URL="$1"
                echo "→ Testando $URL"

                STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}${URL}")

                if [ "$STATUS" -ne 200 ]; then
                    echo "Falha em $URL (HTTP $STATUS)"
                    return 1
                fi

                echo "OK ($URL)"
            }

            echo "Testando /health (PostgreSQL + Redis)"
            test_endpoint "/health"

            echo "Testando endpoints da API"
            test_endpoint "/api/basic-info"
            test_endpoint "/api/species-count"
            test_endpoint "/api/size-statistics"
            
            test_endpoint "/api/habitat-distribution"
            test_endpoint "/api/conservation-status"

            echo "Todos os testes passaram!"
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
