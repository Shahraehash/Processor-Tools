import axios from 'axios'

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
            this.uploading = false
          })
        }
      },
      validateTarget(column) {
        if (column != null ) {
          let payload = {
            target: column,
            storage_id: this.fileMetadata.storage_id
          }
          axios.post('/validate/target_column', payload, {
              headers: {
              'Content-Type': 'application/json',
              'X-inbound': 'validation'
            }
          }).then(result => {
            console.log(result)
            if(!result.data.validation) {
              this.target = null
            }
            this.featureList = []
            this.fileMetadata.column_names.forEach(item => {
              if (item != column) {
                this.featureList.push(item)
              }
            })
          })
        }
      },
      generateCorrelation() {
        if (this.target != null) {
          let payload = {
            target: this.target,
            storage_id: this.fileMetadata.storage_id
          }
          axios.post('/calc/cor', payload, {
              headers: {
              'Content-Type': 'application/json',
              'X-inbound': 'validation'
            }
          }).then(result => {
            this.correlation = result.data
          })
        }

      }

    }
  },


}
