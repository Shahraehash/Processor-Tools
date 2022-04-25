import axios from 'axios'
import FileDownload from 'js-file-download'

export default {
  newFilePipeline() {
    return {
      initialFiles: [],
      target: null,
      uploading: false,
      metadata: null,
      csv: null,

      setInitialFiles(files, target) {
        //reset default state
        this.initialFiles =[]
        this.target = null
        //set values
        this.initialFiles = files
        this.target = target
      },
      //methods
      evaluateMetadataAndStore() {
        if (this.initialFiles.length > 0) {
          //this method uploads form data
          var formData = new FormData();

          this.initialFiles.map((file, index) => {
            console.log(index)
            formData.append('files', file);
          });          

          return axios.post('/preprocessor_api/encoder/store', formData, {
              headers: {
              'Content-Type': 'multipart/form-data',
            }
          }).then((response) => {
            this.metadata = response.data
            return true
          })
        }
      },


      applyTransforms() {
        if (this.metadata != null) {

          return axios.post('/preprocessor_api/encoder/apply_transforms', this.metadata, {
              headers: {
              'Content-Type': 'application/json',
            }
          }).then((response) => {
            for (let file in response.data) {
              FileDownload(response.data[file], file)
            }
          })
        }
      }

    }
  }

}
