pipeline {
  agent any
  stages {
    stage('Get excel and python script') {
      steps {
        echo 'Getting the excel and python files'
        sh '''ls -la
chmod 754 CSV_formatter.py
chmod 754 prod_mp_delete_rules.py
chmod 754 prod_mp_delete_validation.py 
'''
      }
    }

    stage('Running formatter') {
      steps {
        echo 'Running CSV formatter and generating CSV files'
        sh 'python3 CSV_formatter.py'
        sh 'ls -la'
      }
    }

    stage('Delete Rules') {
      steps {
        echo 'Start Delete validation'
        script {
          if (fileExists('delete-prod-test-upload.csv')) {
            sh 'echo "uploading games rules"'
            sh 'python3 prod_mp_delete_validation.py delete-prod-test-upload.csv'
          }
        }

      }
    }

    stage('Testing All Redirects') {
      steps {
        echo 'Testing the deleted rules'
        script {
          if (fileExists('delete-prod-test-upload.csv')) {
            sh 'echo "testing uploaded general rules"'
            sh 'python3 prod_mp_delete_validation.py delete-prod-test-upload.csv'
          }
        }

      }
    }

    stage('Delete environment') {
      steps {
        cleanWs(cleanWhenAborted: true, cleanWhenFailure: true, cleanWhenNotBuilt: true, cleanWhenSuccess: true)
      }
    }

  }
}
