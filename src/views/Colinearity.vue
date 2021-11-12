<template>
  <v-container>
    <MenuBar
      title="Colinearity Removal"
      icon="mdi-chart-bell-curve-cumulative"
      description="This tool allows you to detect covariance in datasets."
      @reset="resetStep1"
    />
    <!-- STEP 1 -->
    <v-card
      outlined
      class="ma-3 pa-5"
    >
      <StepHeading
        stepNumber="1"
        stepTitle="Select Data File"
      />
      <div>
        <!-- Training -->
        <v-card v-for="(fileObj, key) in files" :key="key" outlined class="ma-5 pa-3">
          <div class="overline">
            File {{key + 1}}
          </div>
          <v-layout class="ml-5">
            <v-row>
              <v-col cols="6" >
                <v-select
                  outlined
                  dense
                  label="Data Set Type"
                  v-model="fileObj.dataSet"
                  :items="$store.state.dataSet"
                  item-text="name"
                  item-value="value"
                ></v-select>
                <v-file-input
                  v-model="fileObj.file"
                  prepend-icon="mdi-file"
                  chips
                  truncate-length="100"
                  outlined
                  :disabled="fileObj.dataSet == null"
                  :label="fileObj.dataSet + ' file'"
                  @change="fileObj.uploadFile()"
                ></v-file-input>
              </v-col>
              <v-col cols="6" class="text-center">
                <v-progress-circular color="blue" size="50" width="10" v-if="fileObj.uploading" indeterminate></v-progress-circular>
                <DataValidation
                  class="mt-n3"
                  :fileData="fileObj.fileMetadata"
                  dataType="combined"
                />
              </v-col>
            </v-row>
          </v-layout>
        </v-card>
      </div>
    </v-card>


    <!-- STEP 2 -->
    <v-card
      v-if="files[0].fileMetadata"
      outlined
      class="ma-3 pa-5"
    >
      <StepHeading
        stepNumber="2"
        stepTitle="Select Target Column"
      />
      <div>

        <v-row>
            <v-col cols="6">
              <v-select
                clearable
                outlined
                label="Target Column"
                prepend-icon="mdi-bullseye"

                v-model="files[0].target"
                :items='files[0].fileMetadata.column_names'
                @change="files[0].validateTarget(files[0].target)"
              ></v-select>
            </v-col>
          </v-row>
        </div>
        <v-btn @click="files[0].generateCorrelation()">Cor</v-btn>
      </v-card>

    <apexchart v-if="files[0].correlation" width="1000" type="heatmap" :options="options" :series="files[0].correlation.graph"></apexchart>
  </v-container>



</template>
<script>
//packages

//support code
import CustObjs from '@/CustomObjects.js'

//components
import MenuBar from '@/components/MenuBar'
import DataValidation from '@/components/DataValidation'
import StepHeading from '@/components/StepHeading'


export default {
  name: 'Colinearity',
  components: {
    MenuBar,
    DataValidation,
    StepHeading,

  },
  data() {
    return {
      files: [],

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
  mounted() {
    //create new file object
    this.files.push(CustObjs.newFileObject())
  },
  methods: {

    //State Resetting
    resetStep1() {
      console.log('reset step 1')
    },


    fileValidationData(result){
      console.log(result)
      this.fileDataValid = result
    },
  }

}
</script>
