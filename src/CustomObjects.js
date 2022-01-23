import axios from 'axios'



export default {
  queryFileList() {
    let payload = {
      user_id: 'ui000001' //replace in future
    }
    return axios.post('/query/all_files', payload, {
        headers: {
        'Content-Type': 'application/json',
      }
    }).then(response => {
      return response
    }).catch(error => {
      throw error
    })
  },


  newFileObject() {
    return {
      //core properties
      file: null, //actual file
      uploading: false, //for UI
      dataSet: 'combined', //default is combined hidden for now //type of data set (training, test, combined, etc.)
      fileMetadata: null, //calculated as part of the data_file_upload() method
      fileValidation: null,
      target: null, //set by calling validateTarget() to validate_target_column()
      targetValid: null,
      featureList: null, //set by validateTarget()

      //sizeRules
      defaultMaxRows: 20000,
      defaultMaxFeatures: 2000,

      correlationMaxFeatures: 50,

      //output
      fileOutputName: '',

      //tool specific



      //upload file
      dataFileUpload() {
        if (this.file != null) {
          //this method uploads form data
          var formData = new FormData();
          //file name data stored in X-file header of post request
          formData.append("file", this.file);

          this.uploading = true

          return axios.post('/preprocessor_api/shared/data_file_upload', formData, {
              headers: {
              'Content-Type': 'multipart/form-data',
              'X-filename': this.file.name,
              'X-filegroup': this.dataSet
            }
          }).then(result => {
            this.fileMetadata = result.data

            //fileMetadata that needs further parsing
            this.fileMetadata.describe = JSON.parse(this.fileMetadata.describe)

            //UI changes post upload
            this.uploading = false

            //filename extraction with successful upload
            this.fileOutputName = this.file.name.split('.csv')[0]
          })
        }
      },
      validateTarget(column) {
        //reset downstream properities if value changes
        this.correlation = null

        //based on column

        if (column != null ) {
          let payload = {
            target: column,
            storage_id: this.fileMetadata.storage_id
          }
          return axios.post('/preprocessor_api/shared/validate_target_column', payload, {
              headers: {
              'Content-Type': 'application/json',
              'X-inbound': 'validation'
            }
          }).then(result => {
            this.featureList = []
            this.targetValid = result.data.validation

            if(result.data.validation) {
              this.fileMetadata.column_names.forEach(item => {
                if (item != column) {
                  this.featureList.push(item)
                }
              })
              return true
            }

          })
        }
      },
      customFileOutputSuffix(suffix) {
        this.fileOutputName = this.file.name.split('.csv')[0] + suffix
      },

      //NEW SECTION
      //Correlation Calculations
      correlation: null,
      correlationThreshold: 0.85,
      correlationFeatureRemovalList: [],
      correlationOutputFiles: null,

      allowCorrelationGraph() {
        if (this.fileMetadata != null) {
          return this.fileMetadata.columns - 1 <= this.correlationMaxFeatures
        }
        else {
          throw new Error('Missing file metadata')
        }

      },
      correlationTimeWarning() {
        return true
        //return this.fileMetadata.columns > 30 || this.fileMetadata.rows > 1000
      },

      correlationFilteredList() {
        if (this.correlation) {
          return this.correlation.list.filter(item => {return item.value > this.correlationThreshold})
        }
        else return []
      },
      toggleFeatureRemoval(feature) {
        !this.correlationFeatureRemovalList.includes(feature) ? this.correlationFeatureRemovalList.push(feature) : this.correlationFeatureRemovalList.splice(this.correlationFeatureRemovalList.indexOf(feature),1)
      },
      generateCorrelation() {
        if (this.target != null) {
          let payload = {
            target: this.target,
            storage_id: this.fileMetadata.storage_id
          }
          return axios.post('/preprocessor_api/colinearity/generate', payload, {
              headers: {
              'Content-Type': 'application/json',
              'X-inbound': 'validation'
              },
          }).then(response => {
            console.log(response.data)
            console.log(typeof(response.data))

            this.correlation = response.data

            return true
          }).catch(error => {
            return error
          })
        }
        else {
          return Promise.reject(Error('No target is selected.'))
        }
      },
      buildCorrelationFiles() {
        let payload = {
          storage_id: this.fileMetadata.storage_id,
          feature_removal_list: this.correlationFeatureRemovalList
        }
        return axios.post('/preprocessor_api/colinearity/build', payload, {
            headers: {
            'Content-Type': 'application/json',
          }
        }).then(response => {
          this.correlationOutputFiles = response.data

          return response.data //two files (output and nan)
        })
      },

      //NEW SECTION
      //Feature Selector
      featureSelectorResults: null,
      featureSelectorColumns: null,
      featureSelectorOutputFiles: null,

      generateFeatureSelection() {
        if (this.target != null) {
          let payload = {
            target: this.target,
            storage_id: this.fileMetadata.storage_id
          }
          return axios.post('/preprocessor_api/feature_selector/generate', payload, {
              headers: {
              'Content-Type': 'application/json',
              'X-inbound': 'validation'
              }
          }).then(response => {
            this.featureSelectorResults = response.data
            return true
          }).catch(error => {
            return error
          })
        }
        else {
          return Promise.reject(Error('No target is selected.'))
        }
      },
      buildFeatureSelectorFiles() {
        let payload = {
          target: this.target,
          storage_id: this.fileMetadata.storage_id,
          feature_selector_columns: this.featureSelectorColumns
        }
        return axios.post('/preprocessor_api/feature_selector/build', payload, {
            headers: {
            'Content-Type': 'application/json',
          }
        }).then(response => {
          this.featureSelectorOutputFiles = response.data
          return response.data //two files (output and nan)
        })
      },

      //NEW SECTION
      //Column Reducer
      columnReducerSelectedColumns: [],
      columnReducerErrorColumns: [],
      columnReducerOutputFiles: null,

      buildColumnReducerFiles() {
        this.columnReducerOutputFiles = null
        let payload = {
          target: this.target,
          storage_id: this.fileMetadata.storage_id,
          selected_columns: this.columnReducerSelectedColumns,
        }
        return axios.post('/preprocessor_api/column_reducer/build', payload, {
          headers: {
          'Content-Type': 'application/json',
          }
        }).then(response => {
          this.columnReducerOutputFiles = response.data
          return response.data
        })
      },

    }
  },


}
