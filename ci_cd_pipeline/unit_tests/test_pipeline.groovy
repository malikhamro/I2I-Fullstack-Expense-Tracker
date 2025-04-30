pipeline {
    agent any

    // Stages of the pipeline
    stages {
        stage('Checkout') {
            steps {
                script {
                    // Checkout code from the repository
                    checkout scm
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    // Execute build script
                    sh './ci_cd_pipeline/build_scripts/docker_build.sh'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Execute test script
                    sh './ci_cd_pipeline/build_scripts/tests_run.sh'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Execute deployment script
                    sh './ci_cd_pipeline/deployment_scripts/deploy_docker.sh'
                }
            }
        }
    }

    // Post actions
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            script {
                // Execute rollback script in case of failure
                sh './ci_cd_pipeline/deployment_scripts/rollback_docker.sh'
                echo 'Pipeline failed and rollback executed.'
            }
        }
    }
}

// Test function for the pipeline
def pipeline_test() {
    def pipelineScript = new File('Jenkinsfile').text

    // Mock Jenkins environment for testing
    def mockJenkins = [
        'scm': 'mock_scm_data',
        checkout: { scmData -> assert scmData == 'mock_scm_data' },
        sh: { script -> 
            assert ['ci_cd_pipeline/build_scripts/docker_build.sh', 
                    'ci_cd_pipeline/build_scripts/tests_run.sh', 
                    'ci_cd_pipeline/deployment_scripts/deploy_docker.sh',
                    'ci_cd_pipeline/deployment_scripts/rollback_docker.sh'].contains(script)
        },
        echo: { message -> assert ['Pipeline completed successfully!', 'Pipeline failed and rollback executed.'].contains(message) }
    ]

    // Run pipeline using mock Jenkins environment
    Eval.me('jenkins', mockJenkins, pipelineScript)

    // Additional custom assertions can be added here
}

return this
