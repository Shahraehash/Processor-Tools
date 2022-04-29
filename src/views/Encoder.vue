<template>
  <v-container>
    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
      @reset="reset()"
    />

    <StepFileDrop
      stepTitle="File Selection"
      stepNumber="1"
      @files="batchEvaluateMetadataAndStore"
    />
    <StepTargetCheck
      v-if="FilePipeline.metadata != null"
      stepTitle="Verify Target Column"
      stepNumber="2"
      :filePipeline="FilePipeline"
    />    
    <StepFileCheck
      stepTitle="Adjust Non-Numerical Columns"
      stepNumber="3"
      :filePipeline="FilePipeline"
    />
    <StepFileRow
      stepTitle="Handle Missing Values"
      stepNumber="4"
      :filePipeline="FilePipeline"
      @processStep="$store.commit('FileProcessingDialogOpenSet', true)"
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
import StepTargetCheck from '@/components/v2/StepTargetCheck'
import StepFileCheck from '@/components/v2/StepFileCheck'
import StepFileRow from '@/components/v2/StepFileRow'

export default {
  name: 'Encoder',
  components: {
    MenuBar,
    StepFileDrop,
    StepTargetCheck,
    StepFileCheck,
    StepFileRow
  },
  props: [],
  created() {
    this.FilePipeline = FilePipeline.newFilePipeline()

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
      
      
      this.FilePipeline.setInitialFiles(data.files, data.target)
      this.FilePipeline.evaluateMetadataAndStore()
      


    },
    reset() {
      return true
      //this.FilePipeline = FilePipeline.newFilePipeline()
    },
    showFinalUI() {
    }
  }
}
</script>
