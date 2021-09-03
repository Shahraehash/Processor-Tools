<template>
  <v-container>
    <v-card
      class="ma-3 pa-3"
      outlined
    >
      <div>
        <v-row>
          <v-col cols="3">
            <v-btn
              icon
              @click="$router.push({name: 'Landing'})"
            >
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
          </v-col>
          <v-col
            cols="6"
            class="text-center"
          >
            <v-icon x-large>mdi-call-split</v-icon>
            <span class="title">Train and Test Builder</span>
          </v-col>
          <v-col cols="3">
          </v-col>
        </v-row>
      </div>
      <v-card-text class="body-1">
        This tool allows you to build both a training and validation data set from a single data file.
      </v-card-text>
    </v-card>

    <v-card
      class="ma-3 px-4 py-2"
      outlined
    >
      <div class="overline mb-3">
        Step 1 - Select Data File
      </div>
      <v-row>
        <v-col
          cols="6"
          class="pb-0"
        >
          <v-file-input
            chips
            clearable
            label="Data File"
            outlined
            prepend-icon="mdi-file"
            truncate-length="100"
            v-model="file"
            @change="trainTestFileUpload"
          ></v-file-input>
        </v-col>
        <v-col
          cols="6"
          class="pb-0"
        >
          <v-card
            class="pt-3"
            flat
            v-if="fileData"
          >
            <v-icon large>mdi-table-column</v-icon>
            {{fileData.columns}} columns
            <v-icon large>mdi-table-row</v-icon>
            {{fileData.rows}} rows
          </v-card>
        </v-col>
        <v-col
          cols="12"
          class="mt-0 pt-0"
          v-if="fileData && fileData.nan_count > 0"
        >
          <v-alert
            dense
            text
            type="info"
          >
            {{fileData.nan_count}} rows have missing data. This will affect the output (see next step).
          </v-alert>
        </v-col>
      </v-row>
    </v-card>

    <v-card
      class="ma-3 px-4 py-2"
      outlined
      v-if="fileData != null"
    >
      <div class="overline mb-3">
        Step 2 - Select Target Column
      </div>
      <v-row>
        <v-col cols="6">
          <v-select
            outlined
            label="Target Column"
            prepend-icon="mdi-bullseye"
            v-if="fileData"
            v-model="targetColumn"
            :items='fileData.column_names'
            @change="determineClassMetadata"
          ></v-select>
        </v-col>
      </v-row>
      <div style="width:100%" >
        <div class="distrobution-box" v-bind:style="{ background: '#2196F3', width: class0percent + '%' }">Class 0: {{class0size}} ({{class0percent}}%)</div>
        <div class="distrobution-box" v-bind:style="{ background: '#009688', width: class1percent + '%' }">Class 1: {{class1size}} ({{class1percent}}%)</div>
        <div class="distrobution-box" v-bind:style="{ background: '#d3d3d3', width: placeholderSlot + '%' }">Data Distrobution Displayed After Selection</div>
      </div>

      <v-alert
        v-if="minSampleSizeError"
        color="red"
        type="error"
      >To use this tool, each class must have a an N greater than {{minSampleSize}}.</v-alert>

    </v-card>


    <v-card outlined class="ma-3 pa-3" v-if="!minSampleSizeError && targetColumn != null">
      <v-card-title class="">
        Step 3 - Select Split
      </v-card-title>
      <div >
        Select amount of training data. {{minSampleSize}} is the minimum supported sample size. We have automatically selected a value that you may adjust below.
      </div>
      <v-row>
        <v-col cols="5">
          <v-slider :min="minSampleSize" :max="maxSampleSize" v-model="trainingClassSampleSize" @change="calculatePercentage"></v-slider>
        </v-col>
        <v-col cols="1">
          {{trainingClassSampleSize}}
        </v-col>
      </v-row>
      <div >
        Select how you would like to use remain data in the global generalization testing set.
      </div>
      <v-radio-group v-model="prevalenceOption" @change="calculatePercentage">
        <v-radio label="Use All Remaining Data After Training Data Removed"></v-radio>
        <v-radio label="Maintain Original Prevalence in Validation File (some data will be removed)"></v-radio>
      </v-radio-group>

      <div class="">

      </div>


        <v-card class="mb-10">
          <div style="width:100%">
            <div class="title-box" v-bind:style="{ background: '#7E57C2', width: barSizes.train0 + barSizes.train1 + '%' }">
              Training Data

            </div>
            <div class="title-box" v-bind:style="{ background: '#5C6BC0', width: barSizes.test0 + barSizes.test1 + '%' }">
              Global Generalization Testing Data

            </div>

          </div>
          <div style="width:100%">
            <div class="distrobution-box" v-bind:style="{ background: '#64B5F6', width: barSizes.train0 + '%' }">
              <div>Train 0</div>
              <div>n={{trainingClassSampleSize}}</div>

            </div>
            <div class="distrobution-box" v-bind:style="{ background: '#4DB6AC', width: barSizes.train1 + '%' }">
              <div>Train 1</div>
              <div>n={{trainingClassSampleSize}}</div>
            </div>
            <div class="distrobution-box" v-bind:style="{ background: '#42A5F5', width: barSizes.test0 + '%' }">
              <div>Test 0</div>
              <div>n={{barData.test0global}}</div>
            </div>
            <div class="distrobution-box" v-bind:style="{ background: '#26A69A', width: barSizes.test1 + '%' }">
              <div>Test 1</div>
              <div>n={{barData.test1global}}</div>
            </div>
            <div class="distrobution-box" v-bind:style="{ background: '#F48FB1', width: barSizes.extra + '%' }">
              <div>Not Used</div>
              <div>n={{barData.extra}}</div>
            </div>
          </div>
        </v-card>
        <div class="text-right">
            <v-btn dark float="right" color="grey" rounded @click="processFiles">Build Files</v-btn>
        </div>






    </v-card>



  </v-container>

</template>
<script>
import axios from 'axios'
import FileDownload from 'js-file-download'

export default {
  name: 'TrainTestSplit',
  data() {
    return {
      file: null,
      fileData: null,

      prevalenceOption: 0,

      targetColumn: null,
      classMetadata: null,
      //class computed
      class0size: 0,
      class0percent: 0,
      class0nanSize: 0,
      class0nanPercent: 0,
      class1size: 0,
      class1percent: 0,
      class1nanSize: 0,
      class1nanPercent: 0,

      placeholderSlot: 100,

      minSampleSize:50,
      maxSampleSize:100, //changed programatically
      trainingClassSampleSize: 0,
      widthTest: 30,
      barSizes: {
        train0: 0,
        train1: 0,
        test0: 0,
        test1: 0,
        extra: 0
      },
      barData: {
        test0global: 0,
        test1global: 0,
        extra: 0
      }
    }
  },
  computed: {
    minSampleSizeError() {
      if (this.classMetadata != null) {
        if (this.classMetadata.class_counts[0] < this.minSampleSize || this.classMetadata.class_counts[1] < this.minSampleSize) {
          return true
        }

        else {
          return false
        }
      }
      return false
    }

  },
  methods: {
    trainTestFileUpload(file) {
      if (file != null) {
        //this method uploads form data
        var formData = new FormData();

        //file name data stored in X-file header of post request
        formData.append("file", file);
        axios.post('/train_test_split/upload', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            'X-filename': file.name

          }
        }).then(result => {
          //file data stored in data field of result
          this.fileData = result.data
        }).catch(() => {
          this.$store.commit('snackbarMessageSet', {
            color: 'red lighten-1',
            message: 'Error processing file.'
          })
          this.file = null
          this.fileData = null
        })
      }
      else {
        this.fileData = null
      }

    },
    determineClassMetadata(field){
      if (field != null) {
        let data = {
          target_column: this.targetColumn,
          storage_id: this.fileData.storage_id
        }
        return axios.post('train_test_split/metadata', data, {
          headers: {
          'Content-Type': 'application/json',
          }
        }).then(result => {
          this.classMetadata = result.data
          this.classMetadata.class_counts = JSON.parse(this.classMetadata.class_counts)

          if (this.classMetadata.nan_class_counts != null) {
            this.classMetadata.nan_class_counts = JSON.parse(this.classMetadata.nan_class_counts)
          }


          console.log(this.classMetadata)
          this.calculateMetadataMetrics()
          this.calculatePercentage()
          this.findTrainingClassSampleSize()
        })
      }
      else {
        this.classMetadata = null
      }

    },
    processFiles() {
      let data = {
        target_column: this.targetColumn,
        storage_id: this.fileData.storage_id,
        training_class_sample_size: this.trainingClassSampleSize, //Not matched to output
        prevalence_option: this.prevalenceOption, //0 = use all data, 1 = maintain initail prevalence
        majority_class: this.classMetadata.majority_class,
        extra: this.barData.extra // extra data used in maintaining inital prevalence

      }
      return axios.post('train_test_split/process', data, {
        headers: {
        'Content-Type': 'application/json',
        }
      }).then(response => {
        console.log(response)
        FileDownload(response.data.training, 'training.csv')
        FileDownload(response.data.testing, 'testing.csv')
        if ('extra' in response.data) {
          FileDownload(response.data.extra, 'extra.csv')
        }
      })

    },
    findTrainingClassSampleSize() {
      let minortyCount = this.classMetadata.class_counts[this.classMetadata.minority_class]
      let halfMinorityCount = Math.round(minortyCount / 2)
      this.maxSampleSize = minortyCount
      if (this.minSampleSize > halfMinorityCount) {
        this.trainingClassSampleSize = this.minSampleSize
      }
      else {
        this.trainingClassSampleSize = halfMinorityCount
      }
    },
    calculateMetadataMetrics() {
      this.class0size = this.classMetadata.class_counts[0]
      this.class1size = this.classMetadata.class_counts[1]
      this.class0percent = Math.round(1000 * (this.classMetadata.class_counts[0] / this.classMetadata.total_count)) / 10
      this.class1percent = Math.round(1000 * (this.classMetadata.class_counts[1] / this.classMetadata.total_count)) / 10
      this.placeholderSlot = 0
    },
    calculatePercentage() {
      if (this.prevalenceOption == 0) {
        this.barSizes.train0 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)
        this.barSizes.train1 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)
        this.barSizes.test0 = 100 * (this.classMetadata.class_counts[0] - this.trainingClassSampleSize) / this.classMetadata.total_count
        this.barSizes.test1 = 100 * (this.classMetadata.class_counts[1] - this.trainingClassSampleSize) / this.classMetadata.total_count
        this.barSizes.extra = 0

        this.barData.test0global = this.classMetadata.class_counts[0] - this.trainingClassSampleSize
        this.barData.test1global = this.classMetadata.class_counts[1] - this.trainingClassSampleSize
        this.barData.extra = 0
      }
      else if (this.prevalenceOption == 1) {
        console.log('swap')
        this.barSizes.train0 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)
        this.barSizes.train1 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)


        let percentMajority = this.classMetadata.class_counts[this.classMetadata.majority_class] / this.classMetadata.total_count
        let percentMinority = this.classMetadata.class_counts[this.classMetadata.minority_class] / this.classMetadata.total_count
        let minorityRemain = this.classMetadata.class_counts[this.classMetadata.minority_class] - this.trainingClassSampleSize
        let totalRemain = Math.round(minorityRemain / percentMinority)
        let majorityRemain = Math.round(percentMajority * totalRemain)
        let numberToDrop = this.classMetadata.class_counts[this.classMetadata.majority_class] - this.trainingClassSampleSize - majorityRemain


        console.log({
          percentMajority,
          percentMinority,
          minorityRemain,
          totalRemain,
          majorityRemain,
          numberToDrop
        })

        if (this.classMetadata.majority_class == 0) {
          this.barSizes.test0 = 100 * majorityRemain / this.classMetadata.total_count
          this.barSizes.test1 = 100 * minorityRemain / this.classMetadata.total_count
          this.barData.test0global = majorityRemain
          this.barData.test1global = minorityRemain

        }
        else if (this.classMetadata.majority_class == 1) {
          this.barSizes.test0 = 100 * minorityRemain / this.classMetadata.total_count
          this.barSizes.test1 = 100 * majorityRemain / this.classMetadata.total_count
          this.barData.test0global = minorityRemain
          this.barData.test1global = majorityRemain
        }
        this.barData.extra = numberToDrop
        this.barSizes.extra = 100 * numberToDrop / this.classMetadata.total_count

      }


    }


  }

}
</script>
<style>
.distrobution-box {
  padding-top:16px;
  height: 80px;
  transition: width 0.5s;
  display: inline-block;
  text-align: center;
  color: white;
  overflow: hidden;
}
.title-box {
  padding-top:5px;
  height: 30px;
  transition: width 0.5s;
  display: inline-block;
  text-align: center;
  color: white;
  overflow: hidden;
}


</style>
