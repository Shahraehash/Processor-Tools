<template>
  <v-container>
    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
      @reset="$refs.step1.reset()"
    />
    <StepFileDropUpload
      ref="step1"
      stepTitle="File Selection"
      stepNumber="1"
      @filesChange="filesChange"
      @targetChange="targetChange"
      :disableNext="FilePipeline.metadata != null"
      @nextStep="FilePipeline.evaluateMetadataAndStore()"
      :backendFileDataProp="FilePipeline.files"
    />
    <StepTargetCheck
      v-if="FilePipeline.files != null"
      stepTitle="Target Column Audit"
      stepNumber="2"
      @changeStep="changeStep2"
      :filePipeline="FilePipeline"
      :disableNext="FilePipeline.targetMap != null"
      @nextStep="FilePipeline.setTargetMap($event)"
    />
    <StepColumnRemoval
      v-if="FilePipeline.targetMap != null"
      stepTitle="Missing Data Audit"
      :filePipeline="FilePipeline"
      stepNumber="3"
      @changeStep="changeStep3"
      :disableNext="false"
      @nextStep="FilePipeline.setColumnsToRemove($event)"
      
    />        
    <StepFileCheck
      v-if="FilePipeline.columnsToRemove != null"
      stepTitle="Adjust Non-Numerical Columns"
      stepNumber="4"
      @changeStep="changeStep4"
      :filePipeline="FilePipeline"
      @nextStep="FilePipeline.applyTransforms()"
      :disableNext="FilePipeline.columnAdjust != null"
     
    />
    <StepFileRow
      v-if="FilePipeline.columnAdjust != null"
      stepTitle="Handle Missing Values and Output"
      stepNumber="4"
      :filePipeline="FilePipeline"
      @processStep="buildFiles($event)"
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
import StepFileDropUpload from '@/components/v2/StepFileDropUpload'
import StepColumnRemoval from '@/components/v2/StepColumnRemoval'
import StepTargetCheck from '@/components/v2/StepTargetCheck'
import StepFileCheck from '@/components/v2/StepFileCheck'
import StepFileRow from '@/components/v2/StepFileRow'

export default {
  name: 'Encoder',
  components: {
    MenuBar,
    StepFileDropUpload,
    StepColumnRemoval,
    StepTargetCheck,
    StepFileCheck,
    StepFileRow,
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
    filesChange(files) {
      this.FilePipeline = FilePipeline.newFilePipeline()
      this.FilePipeline.setInitialFiles(files)
      this.targetChange(null)
    },
    targetChange(target) {
      this.FilePipeline.setTarget(target)
      this.FilePipeline.metadata = null
      this.FilePipeline.files = null
    },
    changeStep2() {
      this.FilePipeline.targetMap = null
      this.changeStep3()
    },
    changeStep3() {
      this.FilePipeline.setColumnsToRemove(null)
      this.changeStep4()
    },
    changeStep4() {
      this.FilePipeline.columnAdjust = null

    },
    async buildFiles(includeIndexes) {
      const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

      console.log('includeIndexes',includeIndexes)
      this.$store.commit('FileProcessingDialogLoadingSet', true)
      this.$store.commit('FileProcessingDialogOpenSet', true)
      await this.FilePipeline.handleRows(includeIndexes) 
      await delay(1000);
      this.$store.commit('FileProcessingDialogLoadingSet', false)
           
    }
  }
}
</script>
