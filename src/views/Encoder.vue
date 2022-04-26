<template>
  <v-container>
    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
    />

    <StepFileDrop
      stepTitle="File Selection"
      stepNumber="1"
      @files="batchEvaluateMetadataAndStore"
    />
    <StepFileCheck
      stepTitle="Adjust Non-Numerical Columns"
      stepNumber="2"
      :filePipeline="FilePipeline"
    />
    <StepFileRow
      stepTitle="Handle Missing Values"
      stepNumber="3"
      :filePipeline="FilePipeline"
    />    


  </v-container>

</template>

<script>
//packages
// import FileDownload from 'js-file-download'
// import JSZip from 'jszip'

//support code
import FilePipeline from '@/FilePipeline.js'

//components
import MenuBar from '@/components/MenuBar'
import StepFileDrop from '@/components/v2/StepFileDrop'
import StepFileCheck from '@/components/v2/StepFileCheck'
import StepFileRow from '@/components/v2/StepFileRow'

export default {
  name: 'Encoder',
  components: {
    MenuBar,
    StepFileDrop,
    StepFileCheck,
    StepFileRow
  },
  props: [],
  created() {

  },
  data() {
    return {
      FilePipeline: null,
      toggle_exclusive: null

    }
  },
  computed: {




  },
  methods: {
    //Step 1
    batchEvaluateMetadataAndStore(data) {
      
      this.FilePipeline = FilePipeline.newFilePipeline()
      this.FilePipeline.setInitialFiles(data.files, data.target)
      this.FilePipeline.evaluateMetadataAndStore()
      


    },
    // batchDummyEncodeNonNumericColumns() {
    //   let batch = []
    //   this.filePipelines.forEach(fp => {
    //     batch.push(fp.dummyEncodeNonNumericColumns())
    //   })
    //   Promise.all(batch).then(() => {
    //     let zip = new JSZip();

    //     this.filePipelines.forEach(fp => {
    //       zip.file(fp.metadata.filename + '.csv', fp.csv)
    //     })

    //     zip.generateAsync({type:"blob"})
    //     .then(function(content) {
    //         // Force down of the Zip file
    //         FileDownload(content, "encoder_combined_files.zip");
    //     });
    //     //Show download UI
    //     this.$store.commit('FileProcessingDialogOpenSet', true)                

        
    //   })
  }
}
</script>
