pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Login to AWS and auth Docker client') {
            steps {
                script {
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'f7049708-5e10-4e8c-a7aa-5d8e89497f94',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        bat "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 017376638996.dkr.ecr.us-east-1.amazonaws.com"
                    }
                }
            }
        }
        stage('Clone repo') {
            steps {
                script {
                    bat "git pull https://github.com/akiioto/test_application.git"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t test_application ."
                }
            }
        }
        stage('Tag image') {
            steps {
                script {
                    bat "docker tag test_application:latest 017376638996.dkr.ecr.us-east-1.amazonaws.com/test_application:latest"
                }
            }
        }
        stage('Push image to AWS') {
            steps {
                script {
                    bat "docker push 017376638996.dkr.ecr.us-east-1.amazonaws.com/test_application:latest"
                }
            }
        }
        stage("Refresh image on ECS") {
            steps {
                script {
                    bat "aws ecs update-service --cluster clusterPD --service Hall --force-new-deployment --region us-east-1"
                }
            }
        }
    }
}