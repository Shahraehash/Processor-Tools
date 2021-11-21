<template>
  <v-container>
    <MenuBar
      title="Feature Selector"
      icon="mdi-select-all"
      description="This tool allows you to find the most important features in your data."
      @reset="resetStep1"
    />
    <StepFileUploadMultiple
      stepNumber="1"
      stepTitle="File Upload"
      :file0="file0"
      :file1="file1"
      fileName="Single File"
      @hasSecondFile="hasSecondFile"
    />
    <StepTargetSelection
      v-if="stepNumber >= 2"
      stepNumber="2"
      stepTitle="Select Target"
      :file0="file0"
    />
  </v-container>

</template>

<script>
//packages

//support code
import CustObjs from '@/CustomObjects.js'

//components
import MenuBar from '@/components/MenuBar'
import StepFileUploadMultiple from '@/components/StepFileUploadMultiple'
import StepTargetSelection from '@/components/StepTargetSelection'

export default {
  name: 'FeatureSelector',
  components: {
    MenuBar,
    StepFileUploadMultiple,
    StepTargetSelection
  },
  props: [],
  created() {
    this.file0 = CustObjs.newFileObject()
  },
  data() {
    return {
      file0: null,
      file1: null,
      secondFile: null
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
      if (
        this.file0.fileMetadata != null
        && this.secondFile == false
      ) {
        return true
      }
      else if (
        this.file0.fileMetadata != null
        && this.secondFile == true

        //Ensure the files are compatible and no errors
        // && (this.dataColumnsMatch.numberOfColumnsMatch && this.dataColumnsMatch.columnNamesMatch)
      ) {
        return true

      }
      else {
        return false
      }
    },
    stepStep3() {
      return false
    },
    stepStep4() {
      return false
    }

  },
  methods: {
    resetStep1() {
      this.file0 = CustObjs.newFileObject()
      this.file1 = null
    },
    hasSecondFile(state) {
      this.secondFile = state
      console.log('hassecondfile',state)
      if (state) {
        console.log('hassecondfile',state)
        this.file1 = CustObjs.newFileObject()
      }
      else {
        this.file1 = null
      }
    }
  }
}
</script>
