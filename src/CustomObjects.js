import axios from 'axios'
import FileDownload from 'js-file-download'


export default {

  newFileObject() {
    return {
      file: null,
      uploading: false,
      dataSet: null,
      fileMetadata: null,
      fileValid: null,
      target: null,
      featureList: null,
      correlation: null,
      correlationThreshold: 0.85,
      correlationFeatureRemovalList: [],
      fileOutputName: '',

      filteredList() {
        if (this.correlation) {
          return this.correlation.list.filter(item => {return item.value > this.correlationThreshold})
        }
        else return []

      },
      toggleFeatureRemoval(feature) {
        !this.correlationFeatureRemovalList.includes(feature) ? this.correlationFeatureRemovalList.push(feature) : this.correlationFeatureRemovalList.splice(this.correlationFeatureRemovalList.indexOf(feature),1)
      },

      //upload file
      uploadFile() {
        if (this.file != null) {
          //this method uploads form data
          var formData = new FormData();
          //file name data stored in X-file header of post request
          formData.append("file", this.file);

          this.uploading = true

          return axios.post('/data_file_upload', formData, {
              headers: {
              'Content-Type': 'multipart/form-data',
              'X-filename': this.file.name,
              'X-filegroup': this.dataSet
            }
          }).then(result => {
            this.fileMetadata = result.data
            this.fileMetadata.describe = JSON.parse(this.fileMetadata.describe)
            this.uploading = false
            this.fileOutputName = this.file.name.split('.csv')[0]
          })
        }
      },
      validateTarget(column) {
        if (column != null ) {
          let payload = {
            target: column,
            storage_id: this.fileMetadata.storage_id
          }
          return axios.post('/validate/target_column', payload, {
              headers: {
              'Content-Type': 'application/json',
              'X-inbound': 'validation'
            }
          }).then(result => {
            this.featureList = []

            if(result.data.validation) {
              this.fileMetadata.column_names.forEach(item => {
                if (item != column) {
                  this.featureList.push(item)
                }
              })
              return true
            }
            else {
              this.target = null
              return Error('Invalid target column.')
            }
          })
        }
      },
      generateCorrelation() {
        if (this.target != null) {
          let payload = {
            target: this.target,
            storage_id: this.fileMetadata.storage_id
          }
          return axios.post('/calc/cor', payload, {
              headers: {
              'Content-Type': 'application/json',
              'X-inbound': 'validation'
            }
          }).then(result => {
            this.correlation = result.data
            return true
          }).catch(error => {
            return error
          })
        }
        else {
          return Promise.reject(Error('No target is selected.'))
        }

      },
      buildCorrelationFile() {
        let payload = {
          storage_id: this.fileMetadata.storage_id,
          feature_removal_list: this.correlationFeatureRemovalList
        }
        return axios.post('/calc/cor/process', payload, {
            headers: {
            'Content-Type': 'application/json',
          }
        }).then(response => {
          FileDownload(response.data.output, this.fileOutputName + '.csv')
          FileDownload(response.data.nan, this.fileOutputName + '_nan.csv')
          return true
        })
      },


    }
  },


}
