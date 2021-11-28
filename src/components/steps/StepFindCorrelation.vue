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
          step="0.01"
        ></v-text-field>
      </v-col>

    </v-row>
    <div v-if="fileObject.correlationFilteredList().length == 0">
      <v-alert dense color="primary" text>No pairs meet the correlation threshold.</v-alert>

    </div>
    <div v-if="fileObject.correlationFilteredList().length >0">
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
    </div>


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
        @change="changedFeatureRemoval"
        clearable
        >
        <template #selection="{ item }">
          <v-chip :color="determineCorrelationColors(item,fileObject.correlationFeatureRemovalList)">{{item}}</v-chip>
        </template>
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
          <apexchart v-if="fileObject.correlation && showGraph" type="heatmap" :options="options" :series="fileObject.correlation.graph"></apexchart>
        </div>
      </div>

    </div>

    <!-- Next Step -->
    <div class="text-right">
      <v-btn
        v-if="fileObject.correlationFeatureRemovalList.length > 0"
        :disabled="confirmStep"
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
      confirmStep: false,
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

        // colors: ["#008FFB"],
        plotOptions: {
          heatmap: {
            colorScale: {
              ranges: [{
                  from: -1,
                  to: this.fileObject.correlationThreshold - 0.15,
                  color: '#00A100',
                  name: 'Low Correlation',
                },
                {
                  from: this.fileObject.correlationThreshold - 0.15,
                  to: this.fileObject.correlationThreshold,
                  color: '#128FD9',
                  name: 'Borderline',
                },
                {
                  from: this.fileObject.correlationThreshold,
                  to: 1,
                  color: '#FFB200',
                  name: 'At threshold',
                }
              ]
            }
          }
        }

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
    changedFeatureRemoval() {
      this.confirmStep = false
      this.$emit('changedFeatureRemoval')
    },
    nexStep() {
      this.confirmStep = true
      this.$emit('nextStep')

    },

  }
}
</script>
