import axios from 'axios'

export default {

  newFileObject() {
    return {
      file: null,
      uploading: false,
      dataSet: null,
      tool: null,
      fileMetadata: null,
      fileValid: null,
      target: null,
      featureList: null,
      correlation: null,
      validateFile() {
        this.fileValid = true
      },
      validateTarget(col) {
        if (col != null ) {
          let payload = {
            target: col,
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
              if (item != col) {
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

  uploadFile(file, fileGroup) {
    if (file != null) {
      //this method uploads form data
      var formData = new FormData();
      //file name data stored in X-file header of post request
      formData.append("file", file);
      return axios.post('/data_file_upload', formData, {
          headers: {
          'Content-Type': 'multipart/form-data',
          'X-filename': file.name,
          'X-filegroup': fileGroup
        }
      }).then(result => {
        return result.data

      }).catch((err) => {
        return err
      })
    }
    else {
      Promise.resolve(null);
    }


  }
}
