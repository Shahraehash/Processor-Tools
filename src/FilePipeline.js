import axios from 'axios'
import FileDownload from 'js-file-download'
import JSZip from 'jszip'

export default {
  newFilePipeline() {
    return {
      initialFiles: [],
      target: null,
      uploading: false,
      metadata: null,
      columnAdjust: null,
      rowHandling: null,
      rowOption: 0, //0: remove, 1: impute

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
              'target': this.target,
            }
          }).then((response) => {
            console.log(response.data)
            this.columnAdjust = response.data        
          })
        }
      },
      handleRows(includeIndexes) {
        if (this.metadata != null) {

          return axios.post('/preprocessor_api/encoder/manage_rows', this.metadata, {
              headers: {
              'Content-Type': 'application/json',
              'target': this.target,
              'rowOption': this.rowOption,
              'includeIndexes': includeIndexes,
            }
          }).then((response) => {
            console.log(response.data)
            let zip = new JSZip();

            for (let file in response.data.files) {
              console.log(file)
              zip.file(file, response.data.files[file])            
            }
            zip.generateAsync({type:"blob"})
            .then(function(content) {
                // Force down of the Zip file
                FileDownload(content, "encoder.zip");
            });            
          })
        }        

      }

    }
  }

}
