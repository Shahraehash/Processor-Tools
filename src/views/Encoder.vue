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
      @targetChange="FilePipeline.setTarget($event)"
      :disableNext="FilePipeline.metadata != null"
      @evaluateMetadata="evaluateMetadata"
      :backendFileDataProp="FilePipeline.files"
    />
    <StepTargetCheck
      v-if="FilePipeline.files != null"
      stepTitle="Target Column Audit"
      stepNumber="2"
      :filePipeline="FilePipeline"
      :disableNext="FilePipeline.targetMap != null"
    />
    <StepColumnRemoval
      v-if="FilePipeline.targetMap != null"
      stepTitle="Missing Data Audit"
      :filePipeline="FilePipeline"
      stepNumber="3"
      :disableNext="false"
      @nextStep="FilePipeline.setColumnsToRemove($event)"
    />        
    <StepFileCheck
      v-if="false"
      stepTitle="Adjust Non-Numerical Columns"
      stepNumber="3"
      :filePipeline="FilePipeline"
      :disableNext="FilePipeline.columnAdjust != null"
    />
    <StepFileRow
      v-if="false"
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
    },
    evaluateMetadata() {
      this.FilePipeline.evaluateMetadataAndStore()
    }
  }
}
</script>
