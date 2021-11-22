<template>
  <v-card
    outlined
    class="ma-3 pa-5"
  >
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />

    <div>
      <FileUploadSingle
        :fileObject="file0"
        fileName="First File"
      />
      <Decision
        v-if="file0.fileMetadata != null"
        :decision="hasSecondFile"
        @decide="setSecondFileState"
        message="Do you have a second file?"
        trueVal="Yes"
        falseVal="No"
      />
      <FileUploadSingle
        v-if="hasSecondFile && file1 != null"
        :fileObject="file1"
        fileName="Second File"
      />
      <FilesCrossValidation
        v-if="file1 != null && file1.fileMetadata != null"
        :file0="file0"
        :file1="file1"
      />
    </div>
  </v-card>



</template>

<script>
//packages

//support code

//components
import StepHeading from '@/components/StepHeading'
import FileUploadSingle from '@/components/FileUploadSingle'
import Decision from '@/components/Decision'
import FilesCrossValidation from '@/components/FilesCrossValidation'

export default {
  name: 'StepFileUploadMultiple',
  components: {
    StepHeading,
    FileUploadSingle,
    Decision,
    FilesCrossValidation
  },
  props: [
    'stepNumber',
    'stepTitle',
    'file0',
    'file1'
  ],
  data() {
    return {
      hasSecondFile: null,
    }
  },
  created() {

  },
  computed: {
  },
  methods: {
    setSecondFileState(state) {
      console.log('decide', state)
      this.$emit('hasSecondFile', state)
      this.hasSecondFile = state
    },

  }
}
</script>
