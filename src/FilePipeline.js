import axios from 'axios'
import FileDownload from 'js-file-download'
import JSZip from 'jszip'

export default {
  newFilePipeline() {
    return {
      initialFiles: [],
      target: null,
      targetMap: null,
      uploading: false,
      metadata: null,
      columnAdjust: null,
      rowHandling: null,
      rowOption: 0, //0: remove, 1: impute

      setInitialFiles(files) {
        //reset default state
        this.initialFiles =[]
        this.target = null
        //set values
        this.initialFiles = files
      }, 
      setTarget(target) {
        this.target = target
        this.metadata = null
      },   
      setTargetMap(targetMap) {
        this.targetMap = targetMap
      },
      setRowOption(option) {
        console.log('setRowOption', option)
        this.rowOption = option
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
              'target': this.target,              
            }
          }).then((response) => {
            this.metadata = response.data
            return true
          })
        }
      },
      evaluateColumns() {
        if (this.metadata != null) {        
          return axios.post('/preprocessor_api/encoder/evaluate_columns', this.metadata, {
              headers: {
                'Content-Type': 'application/json',
                'target': this.target,           
            }
          }).then((response) => {
            //this.columnAdjust = response.data
            console.log(response.data)
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
              'targetMap': JSON.stringify(this.targetMap),
            }
          }).then((response) => {
            console.log(response.data)
            this.columnAdjust = response.data
            //column array is deep enough needs secondary parse 
            // for (let i in this.columnAdjust.nan_columns) {
            //   this.columnAdjust.nan_columns[i] = JSON.parse(this.columnAdjust.nan_columns[i])
            // }
          })
        }
      },
      handleRows(includeIndexes) {
        if (this.metadata != null) {

          return axios.post('/preprocessor_api/encoder/manage_rows', this.metadata, {
              headers: {
              'Content-Type': 'application/json',
              'target': this.target,
              'targetMap': JSON.stringify(this.targetMap),              
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
