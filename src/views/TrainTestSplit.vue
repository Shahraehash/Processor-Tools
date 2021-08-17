<template>
  <v-container>
    <v-card outlined class="ma-3 pa-3">
      <div >
        <v-row>
          <v-col cols="3">
            <v-btn icon @click="$router.push({name: 'Landing'})"><v-icon>mdi-arrow-left</v-icon></v-btn>
          </v-col>
          <v-col cols="6" class="text-center">
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

    <v-card outlined class="ma-3 pa-3">
      <div class="title">
        Step 1 - Select Data File
      </div>
      <v-file-input prepend-icon="mdi-file" chips truncate-length="100" outlined label="Data File" @change="splitFileUpload"></v-file-input>
      {{fileData}}
    </v-card>
    <v-card outlined class="ma-3 pa-3">
      <div class="title">
        Step 2 - Select Target Column
      </div>


      <v-row>

        <v-col cols="6">
          <v-select v-if="fileData" v-model="targetColumn" outlined label :items='fileData.column_names' @change="determinePrevalence"></v-select>
        </v-col>
      </v-row>\


      <v-progress-circular color="blue" class="ma-3" size="100" width="15" :value="(value / fileData.rows) * 100" v-for="(value, key) in prevalence" :key="key">{{key}}</v-progress-circular>

    </v-card>
    <v-card outlined class="ma-3 pa-3">
      <div class="">
        Prevelence in Validation Data Set
      </div>
      <v-radio-group disabled v-model="prevalenceOption">
        <v-radio label="Maintain Original Prevalence in Validation File (some data will be removed)"></v-radio>
        <v-radio label="Use All Remaining Data After Training Data Removed"></v-radio>
      </v-radio-group>

      <div class="">
        Build Files
      </div>
      <v-btn disabled color="blue">Build Files</v-btn>


    </v-card>

  </v-container>

</template>
<script>
import axios from 'axios'
export default {
  name: 'TrainTestSplit',
  data() {
    return {
      prevalenceOption: 0,
      fileData: null,
      targetColumn: null,
      prevalence: null,
    }
  },
  methods: {
    splitFileUpload(file) {
      var formData = new FormData();
      console.log(file)

      formData.append("file", file);
      axios.post('/train_test_split/upload', formData, {
          headers: {
          'Content-Type': 'multipart/form-data',
          'X-filename': file.name

        }
      }).then(result => {
        this.fileData = result.data
      })
    },
    determinePrevalence(field){
      console.log(field)
      let data = {
        target_column: this.targetColumn,
        storage_id: this.fileData.storage_id
      }
      return axios.post('train_test_split/prevalence', data, {
        headers: {
        'Content-Type': 'application/json',
        }
      }).then(result => {

        this.prevalence = JSON.parse(result.data)
      })
    }


  }

}
</script>
