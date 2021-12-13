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
      <p>
        Identify the column containing your target variable to ensure it is maintain in the output.
      </p>
      <v-layout class="ma-5">

        <v-row wrap>
          <v-col cols="6">
            <v-autocomplete
              clearable
              outlined
              label="Target Column"
              v-model="fileObject.target"
              :items="fileObject.fileMetadata.column_names_reversed"
              @change="targetColumnChanged"
            ></v-autocomplete>
          </v-col>
        </v-row>
      </v-layout>
      <div v-if="fileObject.target != null" class="body-1">
        <div v-if="targetValid == true" >
          <v-icon color="green" >mdi-check-circle</v-icon> Valid target column.

        </div>
        <div v-if="targetValid == false" >
          <v-icon color="red" >mdi-alert-circle</v-icon> The selected target column is not valid. There must be two unique values.
        </div>
      </div>

      <div class="text-right">
        <v-btn
          color="primary"
          v-if="fileObject.target && fileObject.targetValid"
          dark
          rounded
          depressed
          @click="moveToNextStep"
          :disabled="confirmStep"
        >{{nextStepButtonText}}</v-btn>
      </div>

    </div>
  </v-card>


</template>

<script>
//packages

//support code


//components
import StepHeading from '@/components/StepHeading'

export default {
  name: 'StepTargetSelection',
  components: {
    StepHeading
  },
  props: [
    'fileObject',
    'stepNumber',
    'stepTitle',
    'nextStepFunction',
    'nextStepButtonText'
  ],
  data() {
    return {
      targetValid: null,
      confirmStep: false,
    }
  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
  },
  methods: {
    targetColumnChanged(target) {
      this.confirmStep = false
      this.$emit('nextStepState', this.confirmStep)
      if (target != null) {
        this.fileObject.validateTarget(target).then(() => {
          this.targetValid = this.fileObject.targetValid
        })
      }

    },
    moveToNextStep() {
      this.fileObject[this.nextStepFunction]()
      this.confirmStep = true
      this.$emit('nextStepState', this.confirmStep)

    }


  }
}
</script>
