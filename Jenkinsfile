pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    environment {
        GIT_REPOSITORY = 'https://github.com/akiioto/test_application.git'
        APP_NAME = 'test_application'
        REGION =  'us-east-1'
        USR_ECR = '017376638996'
        CLUSTER_NAME = 'clusterPD'
        CLUSTER_SERVICE_NAME = 'Hall'
    }
    stages {
        stage('Login to AWS and auth Docker client') {
            steps {
                script {
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'f7049708-5e10-4e8c-a7aa-5d8e89497f94',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        bat "aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${USR_ECR}.dkr.ecr.${REGION}.amazonaws.com"
                    }
                }
            }
        }
        stage('Clone repo') {
            steps {
                script {
                    bat "git pull ${GIT_REPOSITORY}"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${APP_NAME} ."
                }
            }
        }
        stage('Tag image') {
            steps {
                script {
                    bat "docker tag ${APP_NAME}:latest ${USR_ECR}.dkr.ecr.${REGION}.amazonaws.com/${APP_NAME}:latest"
                }
            }
        }
        stage('Push image to AWS') {
            steps {
                script {
                    bat "docker push ${USR_ECR}.dkr.ecr.${REGION}.amazonaws.com/${APP_NAME}:latest"
                }
            }
        }
        stage("Refresh image on ECS") {
            steps {
                script {
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'f7049708-5e10-4e8c-a7aa-5d8e89497f94',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        bat "aws ecs update-service --cluster ${CLUSTER_NAME} --service ${CLUSTER_SERVICE_NAME} --force-new-deployment --region ${REGION}"
                    }
                }
            }
        }
    }
}