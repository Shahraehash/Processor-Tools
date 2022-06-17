import axios from 'axios'
import FileDownload from 'js-file-download'
import JSZip from 'jszip'

export default {
  newFilePipeline() {
    return {
      initialFiles: [], //change to uploadFiles
      files: null,
      metadata: null,      
      target: null,
      targetMap: null,
      columnsToRemove: null,
      uploading: false,
      columnAdjust: null,
      rowHandling: null,
      rowOption: 0, //0: remove, 1: impute

      setInitialFiles(files) {
        //reset default state
        this.initialFiles =[]
        //set values
        this.initialFiles = files
      }, 
      setTarget(target) {
        this.target = target
      },   
      setTargetMap(targetMap) {
        this.targetMap = targetMap
      },
      setColumnsToRemove(columnsToRemove) {
        this.columnsToRemove = columnsToRemove
      },
      setRowOption(option) {
        this.rowOption = option
      },
      //methods
      evaluateMetadataAndStore() {
        if (this.initialFiles.length > 0) {
          //this method uploads form data
          var formData = new FormData();

          this.initialFiles.map((file) => {
            formData.append('files', file);
          });          

          return axios.post('/preprocessor_api/encoder/store', formData, {
              headers: {
              'Content-Type': 'multipart/form-data',
              'target': this.target,              
            }
          }).then((response) => {
            this.files = response.data.files
            this.metadata = response.data.metadata
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
          }).then(() => {
            return true
          })
        }
      },      
      applyTransforms() {
        if (this.files != null) {

          return axios.post('/preprocessor_api/encoder/apply_transforms', this.files, {
              headers: {
              'Content-Type': 'application/json',
              'target': this.target,
              'targetMap': JSON.stringify(this.targetMap),
              'columnsToRemove': JSON.stringify(this.columnsToRemove),
            }
          }).then((response) => {
            this.columnAdjust = response.data
          })
        }
      },
      handleRows(includeIndexes) {
        if (this.files != null) {

          return axios.post('/preprocessor_api/encoder/manage_rows', this.files, {
              headers: {
              'Content-Type': 'application/json',
              'target': this.target,
              'targetMap': JSON.stringify(this.targetMap),              
              'rowOption': this.rowOption,
              'columnsToRemove': JSON.stringify(this.columnsToRemove),
              'includeIndexes': includeIndexes,
            }
          }).then((response) => {
            let zip = new JSZip();

            for (let file in response.data.files) {
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
