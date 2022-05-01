<template>
  <v-card outlined class="ma-5 pa-3">
    <div class="overline ml-5 mb-3">
      Cross-File Validation
    </div>
    <v-layout class="ml-5" >
      <v-row>
        <v-col cols="12" >
          <div v-if="dataColumnsMatch != null" class="body-1">
            <div>
              <div v-if="dataColumnsMatch.numberOfColumnsMatch">
                <v-icon color="green" >mdi-check-circle</v-icon> Number of Columns Match Between Files
              </div>
              <div v-if="!dataColumnsMatch.numberOfColumnsMatch">
                <v-icon color="red" >mdi-alert-circle</v-icon> Number of Columns Differ Between Files
              </div>
            </div>
            <div>
              <div v-if="dataColumnsMatch.columnNamesMatch">
                <v-icon color="green" >mdi-check-circle</v-icon> Column Names Match Between Files
              </div>
              <div v-if="!dataColumnsMatch.columnNamesMatch">
                <v-icon color="red" >mdi-alert-circle</v-icon> Column Names Differ Between Files

                <div class="pl-10 pb-5">
                  <div>
                    Columns in Test File Missing from Training:
                    <v-chip outlined v-for="(i, j) in dataColumnsMatch.inTestNotTrain" :key="j">{{i}}</v-chip>
                  </div>
                  <div>
                    Columns in Training File Missing from Training:
                    <v-chip outlined v-for="(i, j) in dataColumnsMatch.inTrainNotTest" :key="j">{{i}}</v-chip>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-layout>
  </v-card>


</template>

<script>
//packages
import underscore from 'underscore'

//support code


//components

export default {
  name: 'FilesCrossValidation',
  components: {

  },
  props: [
    'file0',
    'file1'
  ],
  data() {
    return {

    }
  },
  computed: {
    dataColumnsMatch() {
      if (this.file0.fileMetadata != null && this.file1.fileMetadata != null) {
        let numberOfColumnsMatch = this.file0.fileMetadata.columns == this.file1.fileMetadata.columns

        let inTrainNotTest = underscore.difference(this.file0.fileMetadata.column_names, this.file1.fileMetadata.column_names)
        let inTestNotTrain = underscore.difference(this.file0.fileMetadata.column_names, this.file1.fileMetadata.column_names)

        let columnNamesMatch = inTestNotTrain.length == 0 && inTrainNotTest.length == 0
        return {numberOfColumnsMatch, columnNamesMatch, inTrainNotTest, inTestNotTrain}
      }
      else {
        return null
      }
    },
  }
}
</script>
