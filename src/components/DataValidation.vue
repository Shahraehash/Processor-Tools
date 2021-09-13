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
          <v-alert color="red" text>
            <v-icon color="red" >mdi-alert-circle</v-icon>
            {{fileData.nan_count}} rows are missing data in some columns.
          </v-alert>

        </div>
        <div v-if="!errors.missingData">
          <v-icon color="green" >mdi-check-circle</v-icon> All rows have complete data.
        </div>
      </div>

      <div>
        <div v-if="errors.textData">
          <v-alert color="red" text>
            <v-icon color="red" >mdi-alert-circle</v-icon>
            {{fileData.invalid_columns.length}} columns contain text. MILO requires numerical data.
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

      </div>





    </div>

  </v-card>

</template>
<script>
export default {
  name: 'DataValidation',
  props: ['fileData'],
  data() {
    return {
      errors: {
        missingData: false,
        textData: false,
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
