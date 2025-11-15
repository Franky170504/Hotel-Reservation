pipeline{
    agent any

    stages{
        stage("Cloning github repo to jenkins"){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Franky170504/Hotel-Reservation.git']])
                }

            }
        }
    }
}