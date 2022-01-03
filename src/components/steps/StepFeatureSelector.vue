<template>
  <v-card
    outlined
    class="ma-3 pa-5"
    >
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />

    <!-- Data Loading View -->
    <div v-if="fileObject.featureSelectorResults == null">
      <v-progress-circular color="blue" size="50" width="10" indeterminate></v-progress-circular>
    </div>
    <!-- Data Gathered View -->
    <div v-if="fileObject.featureSelectorResults != null">
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

      <FeatureSelectorDonutGraphs
        :input="selectedColumns"
      />
      <v-data-table
        :headers="tableHeaders"
        :items="selectedColumns"
        :items-per-page="100"
        >
      </v-data-table>



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
    </div>
  </v-card>


</template>

<script>
//packages

//support code

//components
import StepHeading from '@/components/StepHeading'
import FeatureSelectorDonutGraphs from '@/components/FeatureSelectorDonutGraphs'

export default {
  name: 'StepFeatureSelector',
  components: {
    StepHeading,
    FeatureSelectorDonutGraphs
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
        {'text': 'Random Forrest Feature Importance', value: 'rf'}
      ],
      percentile: 0.75,
      percentileItems: [
        {'text': '25%', value: 0.25},
        {'text': '50%', value: 0.50},
        {'text': '75%', value: 0.75},
      ],
      tableHeaders: [
        { 'text': 'Feature', value: 'feature'},
        { 'text': 'Raw Score', value: 'score'},
        { 'text': 'Relative Contribution of Selected Features (%)', value: 'selectedPercentage'},
        { 'text': 'Total Contribution to All Features (%)', value: 'totalPercentage'}
      ]


    }
  },
  mounted() {
    //automatically jump to bottom of screen
    window.scrollTo(0,document.body.scrollHeight);
  },
  watch: {
    method() {
      this.confirmStep = false
      this.$emit('selectPercentileMode', this.method + '_' + this.percentile)
    },
    percentile() {
      this.confirmStep = false
      this.$emit('selectPercentileMode', this.method + '_' + this.percentile)
    }
  },
  computed: {

    selectedColumns() {
      if (this.fileObject.featureSelectorResults != null && this.method != null && this.percentile != null) {
        let number = this.fileObject.featureSelectorResults.feature_number
        let finalColumnIndex = Math.round(number * this.percentile)
        let reducedFeatures = this.fileObject.featureSelectorResults[this.method].slice(0,finalColumnIndex)
        let selectedTotalScore = reducedFeatures.reduce((s, f) => s + f.score, 0);
        let totalTotalScore = this.fileObject.featureSelectorResults[this.method].reduce((s, f) => s + f.score, 0);
        reducedFeatures.forEach(item => {
          item.selectedPercentage = Math.round((item.score / selectedTotalScore) * 100)
          item.totalPercentage = Math.round((item.score / totalTotalScore) * 100)
        })
        return reducedFeatures
      }
      else {
        return []
      }
    }
  },

  methods: {

    nexStep() {
      //extract columns
      let columns = []
      this.selectedColumns.forEach(item => {
        columns.push(item.feature)
      })
      this.fileObject.featureSelectorColumns = columns
      this.confirmStep = true
      this.$emit('nextStep')

    },

  }
}
</script>
