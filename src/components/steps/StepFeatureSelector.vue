<template>
  <v-card
    outlined
    class="ma-3 pa-5"
    >
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <v-row>
      <v-col cols="6">
        <v-select
          outlined
          dense
          label="Method"
          v-model="method"
          :items="methodItems"
          item-text="text"
          item-value="value"
        ></v-select>
      </v-col>
      <v-col cols="6">
        <v-select
          outlined
          dense
          label="Percentile"
          v-model="percentile"
          :items="percentileItems"
          item-text="text"
          item-value="value"
        ></v-select>
      </v-col>
    </v-row>
    <div v-if="method == null">
      Pick your method and percentile.
    </div>
    <v-card v-for="(item, key) in selectedColumns" :key="key"> {{item}} </v-card>


    <!-- Next Step -->
    <div class="text-right">
      <v-btn
        :disabled="confirmStep"
        color="primary"
        rounded
        dark
        depressed
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
      method: null,
      methodItems: [
        {'text': 'Select Percentile', value: 'select_percentile'},
        {'text': 'Random Forrest', value: 'rf'}
      ],
      percentile: 1.0,
      percentileItems: [
        {'text': '25%', value: 0.25},
        {'text': '50%', value: 0.50},
        {'text': '75%', value: 0.75},
        {'text': '100%', value: 1.0},
      ]


    }
  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
  },
  computed: {
    selectedColumns() {
      if (this.fileObject.featureSelectorResults == null && this.method != null && this.percentile != null) {
        return []
      }
      else {
        // let length = this.fileObject.featureSelectorResults.feature_number

        return this.fileObject.featureSelectorResults[this.method]
      }
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
