<template>
  <v-container>
    <MenuBar
      title="Multicollinearity Assessment & Removal Tool"
      icon="mdi-chart-bell-curve-cumulative"
      description="This tool allows you to detect covariance in datasets."
      @reset="resetStep1"
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
  props: []
  data() {
    return {

    }
  }
}
</script>
