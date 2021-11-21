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


  </v-container>

</template>

<script>
//packages

//support code
import CustObjs from '@/CustomObjects.js'

//components
import MenuBar from '@/components/MenuBar'
import StepFileUploadMultiple from '@/components/StepFileUploadMultiple'

export default {
  name: 'FeatureSelector',
  components: {
    MenuBar,
    StepFileUploadMultiple
  },
  props: [],
  created() {
    this.file0 = CustObjs.newFileObject()
  },
  data() {
    return {
      file0: null,
      file1: null,
    }
  },
  methods: {
    resetStep1() {
      this.file0 = CustObjs.newFileObject()
      this.file1 = null
    },
    hasSecondFile(state) {
      if (state) {
        this.file1 = CustObjs.newFileObject()
      }
      else {
        this.file1 = null
      }
    }
  }
}
</script>
