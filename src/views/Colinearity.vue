<template>
  <v-container>
    <MenuBar
      title="Multicollinearity Assessment & Removal Tool"
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
                  @change="fileObj.dataFileUpload()"
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
          <v-expansion-panels
            class="pa-5"
            v-if="files[0].fileMetadata"
            >
            <v-expansion-panel
              dark
            >
              <v-expansion-panel-header>
                View Data Descriptions
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-data-table
                  :headers="[
                    {text: 'Column', value:'feature'},
                    {text: 'Count', value:'count'},
                    {text: 'Mean', value:'mean'},
                    {text: 'STDEV', value:'std'},
                    {text: 'Min', value:'min'},
                    {text: '25%', value:'25%'},
                    {text: '50%', value:'50%'},
                    {text: '75%', value:'75%'},
                    {text: 'Max', value:'max'},
                    {text: 'Skew', value:'skew'},
                    ]"
                  :items="files[0].fileMetadata.describe"
                  class="elevation-1"
                >
                </v-data-table>

              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
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
                :items='files[0].fileMetadata.column_names_reversed'
                @change="files[0].validateTarget(files[0].target)"
              ></v-select>
            </v-col>
          </v-row>
        </div>
        <div class="text-right">
          <v-btn
            color="primary"
            v-if="files[0].target"
            dark
            @click="files[0].generateCorrelation()"
            :disabled="files[0].correlation != null"
          >Calculate Correlations</v-btn>
        </div>

      </v-card>



      <!-- STEP 4 -->
      <v-card
        v-if="files[0].correlation"
        outlined
        class="ma-3 pa-5"
        >
        <StepHeading
          stepNumber="3"
          stepTitle="Select Columns to be Removed"
        />

        <div>
          Select your minimum correlation threshold.
        </div>
        <v-row>
          <v-col cols="2">
            <v-text-field
              dense
              outlined
              v-model="files[0].correlationThreshold"
              type="number" max="1" min="-1"
            ></v-text-field>
          </v-col>
          <v-col cols="2">
            <v-btn icon large @click="files[0].correlationThreshold += 0.01"><v-icon>mdi-plus-box</v-icon></v-btn>
            <v-btn icon large @click="files[0].correlationThreshold -= 0.01"><v-icon>mdi-minus-box</v-icon></v-btn>
          </v-col>
        </v-row>
        <div>
          Click on the features you wish to remove.
        </div>
        <v-data-table
          :headers="[{text: 'Feature Pair', value:'features'}, {text:'Value', value:'value'}]"
          :items="files[0].correlationObject.correlationFilteredList()"
          :items-per-page="5"
          class="elevation-1"
        >
          <template v-slot:item.features="{ item }">
            <v-chip
              dark
              v-for="feature in item.features"
              :key="feature"
              :color="determineCorrelationColors(feature,files[0].correlationFeatureRemovalList)"
              @click="files[0].toggleFeatureRemoval(feature)"
            >
              {{ feature }}
            </v-chip>
          </template>
        </v-data-table>

        <div>
          Correlated selected for removal.
        </div>
        <div>
          {{files[0].correlationFeatureRemovalList}}
        </div>
        <div>
          <v-switch label="Show Graph" v-model="showGraph"></v-switch>
          <apexchart v-if="files[0].correlation && showGraph" width="1000" type="heatmap" :options="options" :series="files[0].correlation.graph"></apexchart>
        </div>

        <v-btn @click="buildFiles()">Build Correlatoin File</v-btn>


      </v-card>
      <!-- <RecentFileList @loadFile="loadFile"/> -->


  </v-container>



</template>
<script>
//packages
import FileDownload from 'js-file-download'
//support code
import CustObjs from '@/CustomObjects.js'

//components
// import RecentFileList from '@/components/RecentFileList'
import MenuBar from '@/components/MenuBar'
import DataValidation from '@/components/DataValidation'
import StepHeading from '@/components/StepHeading'


export default {
  name: 'Colinearity',
  components: {
    // RecentFileList,
    MenuBar,
    DataValidation,
    StepHeading,

  },
  data() {
    return {
      files: [],
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
  created() {
    //create new file object
    this.files.push(CustObjs.newFileObject())
  },
  computed: {


  },
  methods: {
    buildFiles() {
      this.$store.commit('FileProcessingDialogLoadingSet', true)
      this.$store.commit('FileProcessingDialogOpenSet', true)
      this.files[0].buildCorrelationFiles().then(files => {
        this.$store.commit('FileProcessingDialogLoadingSet', false)
        FileDownload(files.output, this.files[0].fileOutputName + '.csv')
        FileDownload(files.nan, this.files[0].fileOutputName + '_nan.csv')
      })
    },
    // loadFile(file) {
    //   console.log(file)
    //   this.files[0].fileMetadata = file
    //   this.files[0].file = new File(["foo"], file.file_name)
    // },

    //State Resetting
    resetStep1() {
      console.log('reset step 1')
    },


    fileValidationData(result){
      console.log(result)
      this.fileDataValid = result
    },

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
        return 'blue'
      }
      else if (index < colors.length - 1) {
        return colors[index]
      }
      else {
        return 'grey lighten-2'
      }

    }
  }

}
</script>
