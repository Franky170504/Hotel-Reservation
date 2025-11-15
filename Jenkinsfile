pipeline {
    agent any

    stages {
        stage("Cloning github repo to jenkins") {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Franky170504/Hotel-Reservation.git']])
                }
            }
        }

        stage("Run project in Conda env") {
            steps {
                sh '''
                    #!/bin/bash
                    echo "--- Initializing Conda ---"
                    
                    # 1. UPDATE THIS PATH TO YOUR CONDA INSTALLATION
                    # This is the path you asked to be marked
                    source C:/Users/LaukikS/anaconda3/condabin/conda.sh
                    
                    echo "--- Activating Conda Environment: ml-dl-env ---"
                    # I'm using 'ml-dl-env' since I saw it in your prompt
                    conda activate ml-dl-env
                    
                    echo "--- Verifying Environment ---"
                    which python
                    python --version
                    
                    echo "--- Installing requirements ---"
                    # This command will now run inside your Conda env
                    pip install -r requirements.txt
                    
                    echo "--- Running Project Steps ---"
                    # Add any other build/test commands here
                    # For example: python your_script.py
                    
                    echo "--- Deactivating ---"
                    conda deactivate
                '''
            }
            
        }
        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

    }
}