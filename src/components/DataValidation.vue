<template>
  <v-card flat>
    <div class="text-left" v-if="fileData != null">
      <v-card class="py-2 px-3 mt-3 mr-5" flat outlined>
        <div class="overline">File Validation</div>

        <!-- Row Errors -->
        <div>
          <div v-if="dataType == 'training'">
            <div v-if="errors.maxTrainingRows">
              <v-icon color="red" >mdi-alert-circle</v-icon>
              {{fileData.rows}} rows
              <span class="grey--text">(Max is {{rules.maxTrainingRows}})</span>
            </div>
            <div v-if="!errors.maxTrainingRows">
              <v-icon color="green" >mdi-check-circle</v-icon>
              {{fileData.rows}} rows
              <span class="grey--text">(Max is {{rules.maxTrainingRows}})</span>
            </div>
          </div>
          <div v-if="dataType == 'testing'">
            <div v-if="errors.maxTestingRows">
              <v-icon color="red" >mdi-alert-circle</v-icon>
              {{fileData.rows}} rows
              <span class="grey--text">(Max is {{rules.maxTestingRows}})</span>
            </div>
            <div v-if="!errors.maxTestingRows">
              <v-icon color="green" >mdi-check-circle</v-icon>
              {{fileData.rows}} rows
              <span class="grey--text">(Max is {{rules.maxTestingRows}})</span>
            </div>
          </div>
        </div>
        <!-- Column Errors -->
        <div>
          <div v-if="errors.maxFeatures">
            <v-icon color="red" >mdi-alert-circle</v-icon>
            {{fileData.columns}} columns
            <span class="grey--text">(Max is {{rules.maxFeatures}})</span>
          </div>
          <div v-if="!errors.maxFeatures">
            <v-icon color="green" >mdi-check-circle</v-icon>
            {{fileData.columns}} columns
            <span class="grey--text">(Max is {{rules.maxFeatures}})</span>
          </div>
        </div>
        <!-- Missing Data Error -->
        <div>
          <div v-if="errors.missingData">
            <v-icon color="orange" >mdi-alert-circle</v-icon>
            {{fileData.nan_count}} rows are missing data. These rows cannot be used.
          </div>
          <div v-if="!errors.missingData">
            <v-icon color="green" >mdi-check-circle</v-icon> All rows have complete data.
          </div>
        </div>
        <!-- Text Data Error -->
        <div>
          <div v-if="errors.textData">
            <v-icon color="orange" >mdi-alert-circle</v-icon>
            {{fileData.invalid_columns.length}} column<span v-if="fileData.invalid_columns.length > 1">s</span> (
            <v-chip dark small color="orange lighten-3" v-for="(item, key) in fileData.invalid_columns" :key="key">{{item}}</v-chip>
            ) has non-numerical data. MILO can only use numerical data.


          </div>
          <div v-if="!errors.textData">
            <v-icon color="green" >mdi-check-circle</v-icon> All rows have numerical data.
          </div>
        </div>
      </v-card>







      <div>

      </div>





    </div>

  </v-card>

</template>
<script>
export default {
  name: 'DataValidation',
  props: ['fileData', 'dataType'],
  data() {
    return {
      rules: {
        maxFeatures: 2000,
        maxTrainingRows: 10000,
        maxTestingRows: 100000
      },
      errors: {
        missingData: false,
        textData: false,
        maxFeatures: false,
        maxTrainingRows: false,
        maxTestingRows: false,
      }

    }
  },
  watch: {
    fileData: function(newVal, oldVal) {
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.validateData()
    }
  },
  mounted() {
    this.validateData()
  },
  methods: {
    validateData() {
      if (this.fileData != null) {
        this.fileData.nan_count > 0 ? this.errors.missingData = true : this.errors.missingData = false
        this.fileData.invalid_columns.length > 0 ? this.errors.textData = true : this.errors.textData = false

        this.fileData.columns > this.rules.maxFeatures ? this.errors.maxFeatures = true : this.errors.maxFeatures = false

        if (this.dataType == 'training') {
          this.fileData.rows > this.rules.maxTrainingRows ? this.errors.maxTrainingRows = true : this.errors.maxTrainingRows = false
        }

        if (this.dataType == 'testing') {
          this.fileData.rows > this.rules.maxTestingRows ? this.errors.maxTestingRows = true : this.errors.maxTestingRows = false
        }


        let validData = true
        for (let i in this.errors) {
          if (this.errors[i] == true) {
            validData = false
          }

        }
        this.$emit('dataValid', {bool: validData, errors: this.errors})

      }


    }
  }
}
</script>
