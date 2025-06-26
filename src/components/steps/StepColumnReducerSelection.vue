<template>
  <div>
    <v-card
      outlined
      class="ma-3 pa-5"
      >
      <StepHeading
        :stepNumber="stepNumber"
        :stepTitle="stepTitle"
      />
      <div>
        <p>Click below to selected columns or paste a comma separated list of columns to be outputted. <br /> You can also <a @click="$refs.MiloFileUploadDialog.open()">import from a MILO results "report.csv" file</a>.</p>
        <v-layout class="ma-5">
          <v-row wrap>
            <v-col cols="12">
              <v-combobox clearable v-model="fileObject.columnReducerSelectedColumns" multiple chips class="ml-8" :items="fileObject.featureList"  outlined label="Selected Columns" @change="splitPasted()"></v-combobox>
              <div>
              </div>
              <div v-if="fileObject.columnReducerSelectedColumns.length > 0" class="body-1">
                <div>
                  <v-icon color="green" >mdi-check-circle</v-icon> {{fileObject.columnReducerSelectedColumns.length}} columns selected.
                </div>
              </div>
              <div v-if="this.fileObject.columnReducerErrorColumns != null">
                <div v-if="fileObject.columnReducerErrorColumns.length > 0">
                  <v-alert class="mt-3" text type="error" dismissible dense>
                    <span>The following column<span v-if="fileObject.columnReducerErrorColumns.length > 1">s</span> are invalid:</span>
                    <v-chip class="ml-2" small dark color="red lighten-3" v-for="(item,key) in fileObject.columnReducerErrorColumns" :key="key">{{item}}</v-chip>
                  </v-alert>
                </div>
              </div>
              <p>
              </p>
            </v-col>
          </v-row>
        </v-layout>
      </div>
      <div class="text-right" v-if="fileObject.columnReducerSelectedColumns.length > 0">
        <v-btn
          v-if="confirmStep == false"
          color="primary"
          rounded
          @click="nexStep()"
        >
          Confirm Column Selection
        </v-btn>
      </div>

    </v-card>

    <MiloFileUploadDialog
      ref="MiloFileUploadDialog"
      @setMiloColumns="setMiloColumns"
      />
  </div>



</template>

<script>
//packages
import underscore from 'underscore'

//support code

//components
import StepHeading from '@/components/StepHeading'
import MiloFileUploadDialog from '@/components/MiloFileUploadDialog'

export default {
  name: 'StepColumnReducerSelection',
  components: {
    StepHeading,
    MiloFileUploadDialog
  },
  props: [
    'stepNumber',
    'stepTitle',
    'fileObject'
  ],
  data() {
    return {
      confirmStep: false,

    }
  },
  created() {

  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
  },
  methods: {


    splitPasted() {
      //Split Pasted Text
      this.fileObject.columnReducerSelectedColumns.forEach((item, index) => {
        if (item.includes(',')) {
          console.log('comma detected', item, index)
          let result = item.split(',')
          result.map(s => s.trim());
          this.fileObject.columnReducerSelectedColumns.splice(index, 1, result)
        }
      })
      this.fileObject.columnReducerSelectedColumns = this.fileObject.columnReducerSelectedColumns.flat()

      //Validate Columns
      this.fileObject.columnReducerErrorColumns = []
      this.fileObject.columnReducerSelectedColumns.forEach(item => {
        if (!this.fileObject.featureList.includes(item)) {
          this.fileObject.columnReducerErrorColumns.push(item)

        }
      })
      this.fileObject.columnReducerErrorColumns.forEach(err => {
        let i = this.fileObject.columnReducerSelectedColumns.indexOf(err)
        this.fileObject.columnReducerSelectedColumns.splice(i, 1)
      })

      if (this.fileObject.columnReducerErrorColumns.length == 0) {
        this.fileObject.columnReducerErrorColumns = null
      }

      //Unique values only
      this.fileObject.columnReducerSelectedColumns = underscore.uniq(this.fileObject.columnReducerSelectedColumns)

       //reset next step when data changes
      this.$emit('changedStepData')
      this.confirmStep = false
    },
    setMiloColumns(value) {
      this.fileObject.columnReducerSelectedColumns = value
    },
    nexStep() {
      this.confirmStep = true
      this.$emit('nextStep')

    },

  }
}
</script>
