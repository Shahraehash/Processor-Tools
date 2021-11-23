<template>
  <v-card
    outlined
    class="ma-3 pa-5"
    >
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />

    <div class="mt-5 mb-3">
      Select your minimum correlation threshold.
    </div>
    <v-row>
      <v-col cols="2">
        <v-text-field
          dense
          outlined
          v-model="fileObject.correlationThreshold"
          type="number" max="1" min="-1"
        ></v-text-field>
      </v-col>
      <v-col cols="2">
        <v-btn icon large @click="fileObject.correlationThreshold += 0.01"><v-icon>mdi-plus-box</v-icon></v-btn>
        <v-btn class="ml-n3" icon large @click="fileObject.correlationThreshold -= 0.01"><v-icon>mdi-minus-box</v-icon></v-btn>
      </v-col>
    </v-row>
    <div class="mt-5 mb-3">
      Click on the features you wish to remove.
    </div>
    <v-data-table
      :headers="[{text: 'Feature Pair', value:'features'}, {text:'Value', value:'value'}]"
      :items="fileObject.correlationFilteredList()"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:item.features="{ item }">
        <v-chip

          v-for="feature in item.features"
          :key="feature"
          :color="determineCorrelationColors(feature,fileObject.correlationFeatureRemovalList)"
          @click="fileObject.toggleFeatureRemoval(feature)"
        >
          {{ feature }}
        </v-chip>
      </template>
    </v-data-table>

    <div class="mt-5 mb-3">
      Correlated selected for removal.
    </div>
    <div>
      <v-select
        chips
        outlined
        multiple
        :items="fileObject.featureList"
        v-model="fileObject.correlationFeatureRemovalList"
        >
      </v-select>
    </div>
    <!-- Grpah View -->
    <div>
      <!-- No Graph -->
      <div v-if="!fileObject.allowCorrelationGraph()">
        <v-alert type="warning" text>There are too many features in this dataset to display the correlation graph.</v-alert>

      </div>
      <!-- Graph -->
      <div v-if="fileObject.allowCorrelationGraph()">
        <div>
          <v-switch label="Show Graph" v-model="showGraph"></v-switch>
          <apexchart v-if="fileObject.correlation && showGraph" width="1000" type="heatmap" :options="options" :series="fileObject.correlation.graph"></apexchart>
        </div>
      </div>

    </div>

    <!-- Next Step -->
    <div class="text-right">
      <v-btn
        color="primary"
        rounded
        dark
        @click="nexStep()"
        >
        Confirm Features for Removal
      </v-btn>
    </div>




  </v-card>


</template>

<script>
//packages
import FileDownload from 'js-file-download'
//support code

//components
import StepHeading from '@/components/StepHeading'

export default {
  name: 'StepFindCorrelation',
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
      showGraph: false,
      options: {
        chart: {
          animations: {
            enabled:true
          }
        },
        dataLabels: {
          enabled: false
        },

        colors: ["#008FFB"],

      }

    }
  },
  methods: {
    determineCorrelationColors(item, correlationList) {
      let colors = [
        'deep-purple lighten-4',
        'teal lighten-4',
        'green lighten-4',
        'orange lighten-4',
        'pink lighten-4'
      ]
      let index = correlationList.indexOf(item)
      if (index == -1) {
        return ''
      }
      else if (index < colors.length - 1) {
        return colors[index]
      }
      else {
        return 'grey lighten-2'
      }

    },
    nexStep() {
      this.$emit('nextStep')

    },
    buildFiles() {
      this.$store.commit('FileProcessingDialogLoadingSet', true)
      this.$store.commit('FileProcessingDialogOpenSet', true)
      this.files[0].buildCorrelationFiles().then(files => {
        this.$store.commit('FileProcessingDialogLoadingSet', false)
        FileDownload(files.output, this.files[0].fileOutputName + '.csv')
        FileDownload(files.nan, this.files[0].fileOutputName + '_nan.csv')
      })
    },
  }
}
</script>
