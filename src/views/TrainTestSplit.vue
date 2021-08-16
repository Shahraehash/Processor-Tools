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
      <v-file-input outlined label="Data File" @change="splitFileUpload"></v-file-input>
      <div class="">
        % of Data Used for Training
      </div>
      <v-row>
        <v-col cols="2">
          <v-select disabled outlined label :items='["10%","20%","30%"]'></v-select>
        </v-col>
      </v-row>

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
      prevalenceOption: 0

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
        console.log(result)
      })
    }


  }

}
</script>
