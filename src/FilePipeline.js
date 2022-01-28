import axios from 'axios'

export default {
  newFilePipeline() {
    return {
      file: null,
      uploading: false,
      metadata: null,

      //methods
      evaluateMetadataAndStore() {
        if (this.file != null) {
          //this method uploads form data
          var formData = new FormData();
          //file name data stored in X-file header of post request
          formData.append("file", this.file);

          this.uploading = true

          return axios.post('/preprocessor_api/encoder/store', formData, {
              headers: {
              'Content-Type': 'multipart/form-data',
              'filename': this.file.name,
            }
          }).then((response) => {
            this.metadata = response.data
            this.metadata.describe = JSON.parse(this.metadata.describe)
            this.uploading = false
            return true
          })
        }
      }

    }
  }

}
