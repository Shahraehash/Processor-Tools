<template>
  <v-card
    outlined
    class="ma-3 pa-5"
    >
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    {{fileObject.featureSelectorResults}}
    <!-- Next Step -->
    <div class="text-right">
      <v-btn

        :disabled="confirmStep"
        color="primary"
        rounded
        dark
        @click="nexStep()"
        >
        Proceed to next step
      </v-btn>
    </div>




  </v-card>


</template>

<script>
//packages

//support code

//components
import StepHeading from '@/components/StepHeading'

export default {
  name: 'StepFeatureSelector',
  components: {
    StepHeading
  },
  props: [
    'stepNumber',
    'stepTitle',
    'fileObject'
  ],
  data() {
    return {
      confirmStep: false,

    }
  },

  methods: {

    nexStep() {
      this.confirmStep = true
      this.$emit('nextStep')

    },

  }
}
</script>
