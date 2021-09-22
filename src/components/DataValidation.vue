<template>
  <v-card flat>
    <div class="text-center" v-if="fileData != null">
      <div>
        <v-icon large>mdi-table-column</v-icon>
        {{fileData.columns}} columns
        <v-icon large>mdi-table-row</v-icon>
        {{fileData.rows}} rows
      </div>
      <div>
        <div v-if="errors.missingData">
          <v-alert dense outlined color="warning" >
            <v-icon color="orange" >mdi-alert-circle</v-icon>
            {{fileData.nan_count}} rows are missing data.
          </v-alert>

        </div>
        <div v-if="!errors.missingData">
          <v-icon color="green" >mdi-check-circle</v-icon> All rows have complete data.
        </div>
      </div>

      <div>
        <div v-if="errors.textData">
          <v-alert dense outlined color="error" >
            <v-icon color="red" >mdi-alert-circle</v-icon>
            {{fileData.invalid_columns.length}} column has non-numerical data.
            <div>
              <v-chip dark small color="red lighten-3" v-for="(item, key) in fileData.invalid_columns" :key="key">{{item}}</v-chip>
            </div>

          </v-alert>
        </div>
        <div v-if="!errors.textData">
          <v-icon color="green" >mdi-check-circle</v-icon> All rows have numerical data.
        </div>
      </div>

      <div>
        <div v-if="errors.maxFeatures">
          <v-alert dense outlined color="error">
            Data set has {{fileData.columns}} columns. Max permitted is {{rules.maxFeatures}}.
          </v-alert>
        </div>
      </div>

      <div>
        <div v-if="errors.maxTrainingRows">
          <v-alert dense outlined color="error">
            Data set has {{fileData.row}} rows. Max permitted is {{rules.maxTrainingRows}}.
          </v-alert>
        </div>
      </div>

      <div>
        <div v-if="errors.maxTestingRows">
          <v-alert dense outlined color="error">
            Data set has {{fileData.row}} rows. Max permitted is {{rules.maxTestingRows}}.
          </v-alert>
        </div>
      </div>






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
          this.fileData.rows > this.rules.maxTrainingRows ? this.error.maxTrainingRows = true : this.error.maxTrainingRows = false
        }

        if (this.dataType == 'testing') {
          this.fileData.rows > this.rules.maxTestingRows ? this.error.maxTestingRows = true : this.error.maxTestingRows = false
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
