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
      <div class="text-right">
        <v-btn
          button
          icon
          @click="exportDataCSV()"
          >
          <v-icon>mdi-download</v-icon>
        </v-btn>

      </div>
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
import Papa from 'papaparse'
import FileDownload from 'js-file-download'

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
        {'text': 'Random Forest Feature Importance', value: 'rf'}
      ],
      percentile: 25,
      percentileItems: [
        {'text': '25%', value: 25},
        {'text': '50%', value: 50},
        {'text': '75%', value: 75},
        {'text': '100%', value: 100},
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
        let reducedFeatures = this.fileObject.featureSelectorResults[this.method][this.percentile]
        console.log(reducedFeatures)
        let selectedTotalScore = reducedFeatures.reduce((s, f) => s + f.score, 0);
        let totalTotalScore = this.fileObject.featureSelectorResults[this.method][100].reduce((s, f) => s + f.score, 0);
        reducedFeatures.forEach(item => {
          item.selectedPercentage = Math.round((item.score / selectedTotalScore) * 10000)/100
          item.totalPercentage = Math.round((item.score / totalTotalScore) * 10000)/100
        })
        return reducedFeatures
      }
      else {
        return []
      }
    }
  },

  methods: {
    exportDataCSV() {
      let config = {
        delimiter: ",",
        header: true,
      }
      //tableCSV includes all columns and scores
      let tableCSV = Papa.unparse(this.fileObject.featureSelectorResults[this.method][this.percentile], config)
      let name = 'fs_table_export_' + this.method + '_' + this.percentile + '.csv'

      FileDownload(tableCSV, name)
    },
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
