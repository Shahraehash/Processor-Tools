<template>
  <v-container>
    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
      @reset="resetStep1"
    />

    <StepFileDrop
      stepTitle="File Selection"
      stepNumber="1"
      @files="batchEvaluateMetadataAndStore"
    />
    <StepFileCheck
      stepTitle="Adjust Non-Numerical Columns"
      stepNumber="2"
      v-if="stepNumber >= 2"
      :filePipelines="filePipelines"
      @files="batchDummyEncodeNonNumericColumns"
    />


  </v-container>

</template>

<script>
//packages
import FileDownload from 'js-file-download'
import JSZip from 'jszip'

//support code
import FilePipeline from '@/FilePipeline.js'

//components
import MenuBar from '@/components/MenuBar'
import StepFileDrop from '@/components/v2/StepFileDrop'
import StepFileCheck from '@/components/v2/StepFileCheck'

export default {
  name: 'Encoder',
  components: {
    MenuBar,
    StepFileDrop,
    StepFileCheck
  },
  props: [],
  created() {

  },
  data() {
    return {
      filePipelines: [],
      toggle_exclusive: null

    }
  },
  computed: {
    stepNumber() {
      if (this.showStep4) {
        return 4
      }
      else if (this.showStep3) {
        return 3
      }
      else if (this.showStep2) {
        return 2
      }
      else {
        return 1
      }
    },
    showStep2() {
      if (this.filePipelines.length > 0) {
        if (this.filePipelines[0].metadata != null) {
          return true
        }
        else {
          return false
        }

      }
      else {
        return false
      }
    
    },
    showStep3() {
      return false

    },
    showStep4() {
      return false
    }


  },
  methods: {
    //Step 1
    batchEvaluateMetadataAndStore(data) {
      let batch = []
      data.files.forEach(file => {
        let fp = FilePipeline.newFilePipeline()

        fp.file = file //associate original file
        fp.target = data.target //note the target

        //queue up processing
        batch.push(fp.evaluateMetadataAndStore())

        //store file pipeline
        this.filePipelines.push(fp)
      })
      Promise.all(batch).then(() => {
        console.log('done')
      })

    },
    batchDummyEncodeNonNumericColumns() {
      let batch = []
      this.filePipelines.forEach(fp => {
        batch.push(fp.dummyEncodeNonNumericColumns())
      })
      Promise.all(batch).then(() => {
        let zip = new JSZip();

        this.filePipelines.forEach(fp => {
          zip.file(fp.metadata.filename + '.csv', fp.csv)
        })

        zip.generateAsync({type:"blob"})
        .then(function(content) {
            // Force down of the Zip file
            FileDownload(content, "encoder_combined_files.zip");
        });
        //Show download UI
        this.$store.commit('FileProcessingDialogOpenSet', true)                

        
      })

      

      
      //FileDownload(this.file0.columnReducerOutputFiles.output_file, this.file0.fileOutputName + '.csv')

      //generate file

    },

    resetStep1() {
    },
    resetStep2() {
    },
    resetStep3() {
    },
    resetStep4() {

    },


  }
}
</script>
