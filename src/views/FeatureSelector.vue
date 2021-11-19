<template>
  <v-container>
    <MenuBar
      title="Feature Selector"
      icon="mdi-select-all"
      description="This tool allows you to find the most important features in your data."
      @reset="resetStep1"
    />
    <FileUploadSingle
      stepNumber="1"
      stepTitle="File Upload"
      :fileObject="file"
      fileName="Single File"

    />


  </v-container>

</template>

<script>
//packages

//support code
import CustObjs from '@/CustomObjects.js'

//components
import MenuBar from '@/components/MenuBar'
import FileUploadSingle from '@/components/FileUploadSingle'

export default {
  name: 'FeatureSelector',
  components: {
    MenuBar,
    FileUploadSingle
  },
  props: [],
  created() {
    this.file = CustObjs.newFileObject()
  },
  data() {
    return {
      file: null

    }
  },
  methods: {
    resetStep1() {
      this.file = CustObjs.newFileObject()
    }
  }
}
</script>
