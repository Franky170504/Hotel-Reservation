pipeline {
    agent any

    environment{
        GCP_PROJECT = "mlops-1-476212"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk"
    }

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
                    . /opt/conda/etc/profile.d/conda.sh
                    
                    echo "--- Activating Conda Environment: ml-dl-env ---"
                    # I'm using 'ml-dl-env' since I saw it in your prompt
                    echo "--- Creating/Activating Environment ---"
                    # Since this is a fresh container, we might need to create the env first
                    # If env exists, this line skips. If not, it creates it.
                    conda create -n ml-dl-env python=3.9 -y || true

                    conda activate ml-dl-env
                    
                    # Ensure pip is installed
                    conda install pip -y
                    pip install -r requirements.txt
                                                            
                    echo "--- Running Project ---"
                    python --version
                    # Add your python run command here
                '''
            }
            
        }

        stage('Buidling and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key-hotel', variable: 'GOOGLE_APP_CREDENTIALS')]){
                    script{
                        echo 'Buidling and Pushing Docker Image to GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APP_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/mlops-1:latest .

                        docker push gcr.io/${GCP_PROJECT}/mlops-1:latest 


                        '''
                    }
                }
            }
        }

    }
}